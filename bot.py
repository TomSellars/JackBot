import os
import discord
import asyncio
import YTDownloader
import random
import re
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.mp4 import MP4

load_dotenv(find_dotenv('tokens.env',raise_error_if_not_found=True))
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
TESTSERVER = os.getenv('DISCORD_TESTSERVER')
bot = commands.Bot(command_prefix='!')
audio = {}
quotes = []

#Imports the audio files from audio folder
def audioFiles():
  global audio
  audio.clear()
  files = os.listdir('audio')
  audioDict = {}
  for file in files:
    audioDict[file[:-4]] = 'audio/' + file
  audio = audioDict

#loads the quotes into the bot
def loadQuotes():
  global quotes
  with open('quotes.txt', 'r') as file:
    quotes = file.readlines()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    audioFiles()
    loadQuotes()

#Gets botcommands text channel
async def botCommandsText():
    guild = discord.utils.get(bot.guilds, name=SERVER)
    # guild = discord.utils.get(bot.guilds, name=TESTSERVER)
    text = discord.utils.get(guild.channels, name='botcommands')
    return text

#Gets last message in botcommands channel
async def lastMessage():
    text = await botCommandsText()
    messageID = text.last_message_id
    message = await text.fetch_message(messageID)
    messageText = message.content
    return str(messageText).split()[1:]

#Returns the audio length of the file
async def audioLength(file):
  if(file[-1] == '3'):
    audio = MP3(file)
  elif(file[-1] == 'v'):
    audio = WAVE(file)
  elif(file[-1] == '4'):
    audio = MP4(file)
  return audio.info.length

#Test Command
@bot.command(name="Test")
async def Test(ctx):
    await ctx.send("nothing to test :smile:")

#Pong
@bot.command(name="ping")
async def Pong(ctx):
    await ctx.send("pong")
    channelName = ctx.message.author.voice.channel
    channelName = str(channelName)
    voicechannel = discord.utils.get(ctx.guild.channels, name=channelName)
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio(executable='D:\Programs\FFmpeg\\ffmpeg.exe', source="audio/pong.mp3"))
    await asyncio.sleep(1)
    await Leave(ctx)

#Joins a voice channel and plays the specified audio file or downloads and plays a youtube audio clip
@bot.command(name="Join")
async def Join(ctx):
    message = await lastMessage()
    channelName = ''
    soundSource = ''
    if len(message) >= 2:
        for word in message[:-1]:
          channelName += word + ' '
        channelName = channelName[:-1]
        if message[-1] not in audio.keys():
          soundSource = 'audio/' + YTDownloader.download(message[-1])
          await asyncio.sleep(2)
        else:
          soundSource = audio[message[-1]]
        bug = random.randint(0,10)
        if bug == 10:
          soundSource = 'stickbug.mp4'
        voicechannel = discord.utils.get(ctx.guild.channels, name=channelName)
        sleepTime = await audioLength(soundSource)
        vc = await voicechannel.connect()
        vc.play(discord.FFmpegPCMAudio(executable='D:\Programs\FFmpeg\\ffmpeg.exe', source=soundSource))
        audioFiles()
        await asyncio.sleep(sleepTime)
        await Leave(ctx)
    else:
        await ctx.send("Specify a server then a sound clip to play")
        await ctx.send(list(audio.keys()))

#Refreshes the audio dictionary
@bot.command(name="RefreshAudio")
async def RefreshAudio(ctx):
  audioFiles()

#Re-Gets all of the quotes from the channels
@bot.command(name="updateQuotes")
async def updateQuotes(ctx):
  global quotes
  guild = discord.utils.get(bot.guilds, name=SERVER)
  quotes1 = discord.utils.get(guild.channels, name='quotes-2018-and-2019')
  quotes2 = discord.utils.get(guild.channels, name='quotes-2020')
  quotes3 = discord.utils.get(guild.channels, name='quotes-2021')
  os.remove('quotes.txt')
  with open('quotes.txt', 'a') as file:
    file.write('` \n')
    async for message in quotes1.history(limit=173, oldest_first=True):
      file.write(message.content + '\n')
      file.write('` \n')
    async for message in quotes2.history(limit=111, oldest_first=True):
      file.write(message.content + '\n')
      file.write('` \n')
    count = 0
    async for i in quotes3.history(limit=None):
      count +=1
    async for message in quotes3.history(limit=count, oldest_first=True):
      file.write(message.content + '\n')
      file.write('` \n')

@bot.command(name='RandomQuote')
async def RandomQuote(ctx):
  global quotes
  randomInt = random.randint(1, len(quotes) - 1)
  isDate = re.findall("\d*/\d*/\d*", quotes[randomInt])
  if (quotes[randomInt] == '` \n'):
    await ctx.send(quotes[randomInt + 1])
    if(quotes[randomInt + 2] != '` \n'):
      await ctx.send(quotes[randomInt + 2])
  elif(isDate != []):
    await ctx.send(isDate)
    await ctx.send(quotes[randomInt + 1])
    if(quotes[randomInt + 2] != '` \n'):
      await ctx.send(quotes[randomInt + 2])
  else:
    if (quotes[randomInt-1] != '` \n'):
      await ctx.send(quotes[randomInt-1])
    await ctx.send(quotes[randomInt])
    if (quotes[randomInt+1] != '` \n'):
      await ctx.send(quotes[randomInt +1])

#Leaves any connected voice channels
@ bot.command(name="Leave")
async def Leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
