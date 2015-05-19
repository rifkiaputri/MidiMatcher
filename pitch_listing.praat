# Output Sound and LongSound Pitch listings into separate Table objects
# Modification: Convert pitch to semitone, save output as csv file
# Written by Jose J. Atria (28 January 2012)
# Modified by Rifki Afina Putri (31 January 2015)
# Last revision: 31 January 2015
# Tested to work with Praat v 5.4.03
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# A copy of the GNU General Public License is available at
# <http://www.gnu.org/licenses/>.

form Dump pitch values
  comment Directory of sound files
  positive Window_length_(ms) 10
  comment Set the window to be longer than your longest voiced interval or
  boolean skip_VUV_check yes
  integer Time_step 0 (=auto)
  positive Minimum_pitch_(Hz) 70
  positive Maximum_pitch_(Hz) 2000
  text filename dummy
endform

windowLength  = window_length
pitchTimestep = time_step
pitchFloor  = minimum_pitch
pitchCeiling  = maximum_pitch
sound_directory$ = "D:\Data Kiki\Tugas\Tingkat 4\Tugas Akhir\MidiMatcher\records\"

# If the VUV detection check is skipped, there is the possibility that the
# boundary between the parts of the LongSound falls within a voiced interval,
# which might cause problems with f0 measurements.
# You can, however, skip it if you prefer.
noCheck = skip_VUV_check

filename$ = filename$ + ".wav"
Read from file: sound_directory$ + "\" + filename$

type$ = extractWord$(selected$(), "")
name$ = selected$(type$)

if type$ = "Sound"
  # printline >'type$'<
  pitch = To Pitch... pitchTimestep pitchFloor pitchCeiling
  table = Create Table with column names... 'name$'_f0 0 time semitone f0
  for j to Object_'pitch'.nx
    call AnalyzeFrame
  endfor
  call getTimeStamp
  time$ = getTimeStamp.string$
  select table
  Save as comma-separated file: sound_directory$ + name$ + "_result.csv"
  Remove
  select pitch
  Remove
elsif type$ = "LongSound"
  # printline >'type$'<
  long = selected ()
  length = Get total duration
  parts = ceiling(length / windowLength)
  table = Create Table with column names... 'name$'_f0 0 time semitone f0
  start = 0
  # printline 'parts' parts...
  for p to parts
    select long 
    if p < parts
      end = start + windowLength
    else
      end = Object_'long'.xmax
    endif
    # printline Processing part 'p' of 'parts' : 'start'..'end'
    part = Extract part... start end yes
    pitch = To Pitch... pitchTimestep pitchFloor pitchCeiling
    select part
    textgrid = To TextGrid (silences)... pitchFloor 0 -25 0.1 0.1 silent sounding
    intervals = Get number of intervals... 1
    label$ = Get label of interval... 1 intervals
    if !noCheck and label$ = "sounding"
      if intervals>1
        # printline Moving boundary to previous silence...
        a = Get start point... 1 intervals-1
        b = Get end point... 1 intervals-1
        end = a+((b-a)/2)
        select pitch
        lastframe = Get frame number from time... end
      else
        pause Voiced interval longer than window size. Continue or retry with a longer window length.
        lastframe = Object_'pitch'.nx
      endif
    else
      lastframe = Object_'pitch'.nx
    endif
    for j to lastframe
      call AnalyzeFrame
    endfor
    call getTimeStamp
    time$ = getTimeStamp.string$
    select table
    Save as comma-separated file: sound_directory$ + name$ + "_result.csv"
    Remove
    select part
    plus pitch
    plus textgrid
    Remove
    start = end
  endfor
endif
# printline Done

procedure AnalyzeFrame
  select pitch
  time = Get time from frame number... j
  f0 = Get value in frame... j Hertz
  if f0 != undefined
    semitone = 12*log2(f0/440)+69
    select table
    Append row
    Set numeric value... Object_'table'.nrow time 'time:3'
    Set numeric value... Object_'table'.nrow semitone 'semitone:0'
    Set numeric value... Object_'table'.nrow f0 'f0:3'
  # else
    # semitone = 999
    # select table
    # Append row
    # Set numeric value... Object_'table'.nrow time 'time:3'
    # Set numeric value... Object_'table'.nrow semitone 'semitone:0'
  endif
endproc

# Get a time stamp in normalized format
procedure getTimeStamp
  .currentDateTime$ = date$()
  .string$ = replace_regex$(.currentDateTime$, "[A-Z][a-z]+\s+([A-Z][a-z]+)\s+(\d+)\s+(\d+)\W(\d+)\W(\d+)\s+(\d+)$", "\6_\1_\2_\3_\4_\5", 0)
endproc