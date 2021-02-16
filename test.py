import os

audio = {}

def audioFiles():
  files = os.listdir('audio')
  audioDict = {}
  for file in files:
    audioDict[file[:-4]] = file
  return audioDict

audio = audioFiles()

print(audio['MarkScream'])