import discord
from discord.ext import commands
import json
import clear
import music

cogs = [music, clear]

#Opening config 
with open('./config.json', 'r') as cjson:
    config = json.load(cjson)
     
token = config["token"]
prefix = config["prefix"]
    
client = commands.Bot(command_prefix = config["prefix"], 
intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(token)
