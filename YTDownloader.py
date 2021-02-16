import os
import asyncio
from pytube import YouTube

def download(url):
    link = YouTube(url)
    downloadLink = link.streams.filter(only_audio=True)
    downloadLink[0].download('audio/')
    #Converts StreamQuery to string splits it to a list and then gets the 
    #file type
    fileType = str(downloadLink).split()[2]
    fileType = '.' + fileType[-4:-1]
    linkName = link.title
    linkName = linkName.replace('.','')
    tempName = linkName.split()
    tempName = tempName[:2]
    newName = ''.join(tempName)
    os.replace('audio/' + linkName + fileType, 'audio/' + newName + fileType)
    return newName + fileType
