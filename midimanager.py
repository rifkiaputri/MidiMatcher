import csv
import midiparser

class MidiManager:

    # Parse midi file to .csv format
    def parseMidi(self, inputPath, outputPath, fileName):
        inputName = inputPath + fileName
        outputName = outputPath + fileName[:-4] + '.csv'
        # print 'Writing ' + fileName[:-4] + ' to csv...'

        # Read midi file using midiparser library
        midi = midiparser.File(inputName)
               
        with open(outputName, 'wb') as csvfile:
            midiwriter = csv.writer(csvfile, delimiter=',')
            midiwriter.writerow(['time', 'semitone'])

            for track in midi.tracks:
                for event in track.events:
                    if event.type == midiparser.voice.NoteOn:
                        midiwriter.writerow([event.absolute, event.detail.note_no])
                        # Add Short pause model
                        # midiwriter.writerow([event.absolute+1, 999])
                       

    # Read midi note (semitone) from .csv format
    # Output: list of semitone
    def readMidi(self, path, fileName):
        tempsemitone = []
        tempcontour = []
        inputName = path + fileName
               
        with open(inputName) as csvfile:
            midireader = csv.DictReader(csvfile)

            for row in midireader:
                tempsemitone.append(int(row['semitone']))

        # For contour represetation
        for idx in range(len(tempsemitone)):
            if (idx+1 < len(tempsemitone)):
                tempcontour.append(tempsemitone[idx+1] - tempsemitone[idx])
            else:
                break

        # return tempcontour
        return tempsemitone

    # Read midi note (semitone) from .csv format, and segment it
    # Output: list of segmented semitone
    def segmentNote(self, path, fileName):
        temp = []
        notesdata = []
        segmented = []
        inputName = path + fileName
        outputName = path + fileName[:-4] + "_segmented.csv"

        with open(inputName) as csvfile:
            midireader = csv.DictReader(csvfile)
            for row in midireader:
                temp.append(int(row['semitone']))

        # TODO: hapus/edit note kalau panjangnya < 10 frame       
        frame = 0
        for index in range(len(temp)):
            frame += 1
            if (temp[index] != temp[index-1]):
                if (frame >= 10):    
                    notesdata.append([frame, temp[index-1]])
                frame = 0
        if (frame >= 10):
            notesdata.append([frame, temp[-1]])

        # Make output files for segmented notes
        for row in notesdata:
            for index in range(row[0]+1):
                segmented.append(row[1])

        with open(outputName, 'wb') as csvfile:
            segmentwriter = csv.writer(csvfile, delimiter=',')
            segmentwriter.writerow(['semitone'])
            for value in segmented:
                segmentwriter.writerow([value])

        return segmented
