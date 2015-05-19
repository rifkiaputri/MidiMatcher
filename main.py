import csv
import os
import searchmanager
import sys
import time


def main():
    # Set input and output path
    rawDBPath = 'D:/Data Kiki/Tugas/Tingkat 4/Tugas Akhir/MidiMatcher/files/'
    dbPath = 'D:/Data Kiki/Tugas/Tingkat 4/Tugas Akhir/MidiMatcher/transcriptions/'
    recordPath = 'D:/Data Kiki/Tugas/Tingkat 4/Tugas Akhir/MidiMatcher/records/'

    # Init database
    print 'Initializing database...'
    controller = searchmanager.SearchManager()
    controller.init(rawDBPath, dbPath)
    print 'Database successfully initialized.'

    print '\n*************************************************************'
    print '************************ MIDIMATCHER ************************'
    print '*************************************************************\n'
    
    command = ''

    while command.strip() != 'exit':
        command = raw_input('Type \'h\' to begin humming, \'exit\' to close the application\n')
        recordName = 'query'

        if command.strip() == 'h':
            # Call sox program to record humming file
            try:
                print 'Press ctrl+c to stop recording'
                os.system('sox -t waveaudio 0 \"' + recordPath + recordName + '.wav\"')
            except KeyboardInterrupt:
                print 'Stop recording.'

            if os.path.isfile(recordPath + recordName + '.wav'):
                # Call praat script for humming transcription
                os.system('praatcon.exe pitch_listing.praat 10 yes 0 70 2000 \"' + recordName + '\"')
                
                # Begin searching module
                result = controller.getDistance(recordPath, recordName, dbPath)
                controller.sortByDist(result, 10, recordPath, recordName)
                print '\n'

            else:
                print 'No such file.'

        if command.strip() == 'exit':
            sys.exit(1)

if __name__ == '__main__':
    main()