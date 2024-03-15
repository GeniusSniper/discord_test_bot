# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
ROLEID = int(os.getenv('DISCORD_ROLE_ID'))
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))

# client = discord.Client(intents=discord.Intents.default())

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # print(client.guilds)
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):

    role = get(member.guild.roles, id=ROLEID)
    await member.add_roles(role)

    # await member.create_dm()
    # await member.dm_channel.send(
    #     f'Hi {member.name}, welcome to my Discord server!'
    # )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    if 'sniper' in message.content:
        response = '别问，问就是不会'
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

client.run(TOKEN)