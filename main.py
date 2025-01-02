"""
Small Enemy Spider - Discord Music Player

Step 1: Enter the bot token in "apikeys.py".
Step 2: Create the "Audio" and "Storage" folders. They can stay empty at first.
Step 3: Run main.py.

If it doesn't work because of FFMpeg, download and place FFMpeg into the same directory as main.py.

Commands:
: play [YOUTUBE LINK] - Play a song from youtube.
: play_storage [PATH TO WAV FILE] - Play a song from the storage folder. The path starts from within the storage folder.
: stop - Stop the current song.
: leave - Leave the current call.
: join - Join the call.
"""

from __future__ import unicode_literals

import nextcord
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from pathlib import Path
import os
import subprocess

from pytube import YouTube
import yt_dlp

from apikeys import *
import time

haltLoop = False

intents = nextcord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = ': ', intents=nextcord.Intents.all())

@client.event
async def on_ready():
    print("OH WAIT A MINUTE THAT'S A")
    print("SMALL")
    print("ENEMY")
    print("SPIDER.")
    print("----------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("No.")

@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You ain't in a voice channel.")

    await ctx.message.delete()

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Make me.")

    await ctx.message.delete()

@client.command(pass_context = True)
async def play(ctx, arg, loopStart=0, loopEnd=0):
    global haltLoop
    
    targetSong = arg
    joined = True

    startTarget = int(loopStart)
    endTarget = int(loopEnd)
    
    await ctx.message.delete()

    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You ain't in a voice channel.")
            joined = False

    if joined:
        if ctx.voice_client.is_playing():
            haltLoop = True
            ctx.voice_client.stop()
        
        folderPath = os.join(Path(__file__).parent(), "audio")
        folderPathBack = Path(__file__).parent()

        outputName = folderPathBack + "output.mp4"

        videoName = ""
        videoID = ""
        videoLength = 0.0

        targetFile = ""

        hasDownloaded = False

        while not hasDownloaded:
            hasDownloaded = True
            try:
                ydl_opts = {
                    'outtmpl': 'output_temp'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([arg])

                    infoDict = ydl.extract_info(arg, download=False)
                    videoName = infoDict.get('title', None)
                    videoLength = infoDict['duration']
                    videoID = infoDict.get('id', None)

                    targetFile = infoDict.get('filename', None)
            except:
                print("Download failed, may I try again?")
                input("> ")
                hasDownloaded = False
        
        fileExtension = ""

        for file in os.listdir(folderPathBack):
            try:
                if file[:file.index(".")] == "output_temp":
                    fileExtension = file[file.index("."):]
            except ValueError:
                pass
        
        convSource = os.path.join(folderPathBack, "output_temp" + fileExtension)
        convDestination = os.path.join(folderPathBack, "output.mp4")

        if fileExtension != ".mp4":
            command = r"ffmpeg -i " + convSource + r" -ab 160k -ac 2 -ar 44100 -vn " + convDestination
            subprocess.call(command, shell=True)
        else:
            os.rename(convSource, convDestination)

        print("Download complete. Conversion time.")

        if os.path.exists(os.path.join(folderPath, "song.wav")):
            os.remove(os.path.join(folderPath, "song.wav"))

        if os.path.exists(os.path.join(folderPath, "song.mp4")):
            os.remove(os.path.join(folderPath, "song.mp4"))
        
        if os.path.exists(os.path.join(folderPathBack, "output_temp" + fileExtension)):
            os.remove(os.path.join(folderPathBack, "output_temp" + fileExtension))

        print("Okay done deleting.")

        titleName = ""

        for char in videoName:
            if not char in [":", "'", "/", "\\", "<", ">", "?", "|", "\""]:
                titleName += char

        print("Loading song: " + titleName)

        if endTarget == 0:
            endTarget = videoLength

        if endTarget < 0 or startTarget > endTarget or startTarget > videoLength or startTarget == endTarget:
            await ctx.send("Can't work with those loop boundaries.")

        else:
            cExtension = 0
            extensions = ["webm", "mkv", "m4v", "mp4", "avi", "m4a", "mov", "ivf"]
            requiredExtension = ""
            
            while requiredExtension == "":
                try:
                    requiredExtension = extensions[cExtension]
                    downloadedSong = os.path.join(folderPathBack, "output." + requiredExtension)

                    os.rename(downloadedSong, os.path.join(folderPath, "song_temp.mp4"))
                except FileNotFoundError:
                    cExtension += 1
                    requiredExtension = ""

            if not (startTarget == 0 and endTarget == videoLength):
                ffmpeg_extract_subclip(os.path.join(folderPath, "song_temp.mp4"), startTarget, endTarget, targetname=os.path.join(folderPath, "song.mp4"))
                os.remove(os.path.join(folderPath, "song_temp.mp4"))
            else:
                os.rename(os.path.join(folderPath, "song_temp.mp4"), os.path.join(folderPath, "song.mp4"))

            songPath = os.path.join(folderPath, "song.mp4")
            finalPath = os.path.join(folderPath, "song.wav")

            command = r"ffmpeg -i " + songPath + r" -ab 160k -ac 2 -ar 44100 -vn " + finalPath
            
            subprocess.call(command, shell=True)

            def repeat(guild, voice, audio):
                global haltLoop
                
                if haltLoop:
                    haltLoop = False
                else:
                    source = FFmpegPCMAudio(os.path.join(folderPath, "song.wav"))
                    voice.play(audio, after=lambda e:repeat(guild, voice, source))
                    voice.is_playing()

            if not ctx.voice_client:
                channel = ctx.message.author.voice.channel
                await channel.connect()
            
            print("\n" + titleName + " is brought to you by " + str(ctx.message.author) + ".\n")
            
            source = FFmpegPCMAudio(os.path.join(folderPath, "song.wav"))
            player = ctx.voice_client.play(source, after=lambda e: repeat(ctx.guild, ctx.voice_client, source))

@client.command(pass_context = True)
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
    else:
        await ctx.send("Already paused.")

    await ctx.message.delete()

@client.command(pass_context = True)
async def resume(ctx):
    if not ctx.voice_client:
        await ctx.send("Not playing anything.")
    elif ctx.voice_client.is_paused():
        ctx.voice_client.resume()
    else:
        await ctx.send("Not playing anything.")

    await ctx.message.delete()

@client.command(pass_context = True)
async def stop(ctx):
    global haltLoop
    
    ctx.voice_client.stop()
    haltLoop = True
    
    await ctx.message.delete()

@client.command(pass_context = True)
async def play_storage(ctx, arg):
    global haltLoop
    
    targetSong = arg
    joined = True
    
    await ctx.message.delete()

    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You ain't in a voice channel.")
            joined = False

    if joined:
        if ctx.voice_client.is_playing():
            haltLoop = True
            ctx.voice_client.stop()
        
        folderPath = r"C:\Users\conta\Desktop\Code_Projects\Python\Discord_Bots\Small_Enemy_Spider\Storage"
        folderPathBack = r"C:\Users\conta\Desktop\Code_Projects\Python\Discord_Bots\Small_Enemy_Spider"

        outputName = folderPathBack + "output.mp4"

        videoName = ""
        videoID = ""
        videoLength = 0.0

        targetFile = ""

        if not ctx.voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()

        print("\n" + targetSong + " is brought to you by " + str(ctx.message.author) + ".\n")

        def repeat(guild, voice, audio):
            global haltLoop
            
            if haltLoop:
                haltLoop = False
            else:
                source = FFmpegPCMAudio(os.path.join(folderPath, targetSong + ".wav"))
                voice.play(audio, after=lambda e:repeat(guild, voice, source))
                voice.is_playing()

        if not ctx.voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()

        source = FFmpegPCMAudio(os.path.join(folderPath, targetSong + ".wav"))
        player = ctx.voice_client.play(source, after=lambda e: repeat(ctx.guild, ctx.voice_client, source))

@client.command()
async def restart(ctx):
    client.exit(1)

client.run(botToken)