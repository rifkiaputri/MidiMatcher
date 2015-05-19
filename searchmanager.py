from operator import itemgetter
import csv
import midimanager
import mlpy
import os

class SearchManager:

    # Database initialization
    # Convert all .mid files to .csv format
    def init(self, inputPath, outputPath):
        db = midimanager.MidiManager()

        for fileName in os.listdir(inputPath):
            if fileName.endswith('.mid'):
                db.parseMidi(inputPath, outputPath, fileName)
    
    # Match record to database
    def getDistance(self, songPath, songName, dbPath):
        temp = []
        manager = midimanager.MidiManager()
        record = manager.segmentNote(songPath, songName + '_result.csv')

        print 'Searching ' + songName + ' in database...'
        for fileName in os.listdir(dbPath):
            if fileName.endswith('.csv'):
                reference = manager.readMidi(dbPath, fileName)
                dist, cost, path = mlpy.dtw_subsequence(record, reference)
                temp.append([int(dist), fileName[:-10]])
        return temp

    # Sort list of song by DTW distance
    # Output: Printed top-N list of song on console
    def sortByDist(self, list, N, path, fileName):
        temp = sorted(list, key=itemgetter(0))

        idx = 0
        print '\nTop-' + str(N) + ' result:'
        with open(path + 'searchresult.csv', 'a') as csvfile:
            resultwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            for result in temp:
                idx += 1
                print str(idx) + '. ' + result[1]
                resultwriter.writerow([str(idx) + '. ' + result[1], str(result[0])])
                if idx == N:
                    break
    