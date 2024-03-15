# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.utils import get

from discord.ext import commands,tasks

from discord import FFmpegPCMAudio
from mpplayerfile import give_link,download_vid,find_music_name,remove_all_files, delete_selected_file
from discord import FFmpegAudio
from discord import FFmpegOpusAudio
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
ROLEID = int(os.getenv('DISCORD_ROLE_ID'))
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))

# client = discord.Client(intents=discord.Intents.default())

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!',intents=intents)

def guild_check(user): # only for devlopement purpose
    return user.guild.id != GUILDID

@bot.event
async def on_ready():
    # print(bot.guilds)
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    if(guild_check(member)):
        return

    role = get(member.guild.roles, id=ROLEID)
    await member.add_roles(role)

    # await member.create_dm()
    # await member.dm_channel.send(
    #     f'Hi {member.name}, welcome to my Discord server!'
    # )

@bot.event
async def on_message(message):
    if guild_check(message.author):
        return
    if message.author == bot.user:
        return
    
    
    if 'sniper' in message.content:
        response = '别问，问就是不会'
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

    await bot.process_commands(message)

# @bot.command()
# async def test(ctx, *, arg):
#     print('here')
#     await ctx.send(arg)

@bot.command()
async def pause(ctx):
    if guild_check(ctx.message):
        return
    if ctx.voice_client and ctx.voice_client.is_playing(): # if the music is already playing 
        ctx.voice_client.pause() #pausing the music 
        await ctx.send("Playback paused.") #sending confirmation on  channel
    else:
        await ctx.send('[-] An error occured: You have to be in voice channel to use this commmand') #if you are not in vc

@bot.command()
async def resume(ctx):
    if guild_check(ctx.message):
        return
    if ctx.voice_client and ctx.voice_client.is_paused(): # If the music is already paused
        ctx.voice_client.resume() #resuming the music
        await ctx.send("Playback resumed.")#sending confirmation on  channel
    else:
        await ctx.send('[-] An error occured: You have to be in voice channel to use this commmand') #if you are not in vc

@bot.command()
async def leave(ctx): 
    if guild_check(ctx.message):
        return
    if ctx.voice_client: #if you are in vc 
        await ctx.guild.voice_client.disconnect() #disconnecting from the vc
        await ctx.send("Lefted the voice channel") #sending confirmation on channel
        await asyncio.sleep(1)
        remove_all_files("music") #deleting the all the files in the folder that  we downloaded to not waste space on your pc

    else:
        await ctx.send("[-] An Error occured: You have to be in a voice channel to run this command") #if you are not in vc

@bot.command()
async def join(ctx):
    if guild_check(ctx.message):
        return
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        try:

             await channel.connect() #connecting to channel
        except:
            await ctx.send("[-] An error occured: Couldn't connect to the channel") #if there is an error

    else:
        await ctx.send("[-] An Error occured: You have to be in a voice channel to run this command") #if you are not in vc



@bot.command(name="play")
async def play(ctx,*,title):
    if guild_check(ctx.message):
        return
    download_vid(title) # Downloading the mp4 of the desired vid
    voice_channel = ctx.author.voice.channel

   
    if not ctx.voice_client: #if you are not in  vc 
        voice_channel = await voice_channel.connect() #connecting to vc

    try:
        async with ctx.typing():
            player = discord.FFmpegPCMAudio(source=f"music/{find_music_name()}") #executable part is where we downloaded ffmpeg. We are writing our find_mmusic name func because , we want to bot to play our desired song fro the folder
            player = discord.PCMVolumeTransformer(player, volume=0.3)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'Now playing: {find_music_name()}') #sening confirmmation

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        delete_selected_file(find_music_name()) # deleting the file after it played

    except Exception as e:
        await ctx.send(f'Error: {e}') #sending error


bot.run(TOKEN)
# client.run(TOKEN)