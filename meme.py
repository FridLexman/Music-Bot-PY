import discord
from discord import *                                                             
from discord.ext import commands
import random
import os
import openai
import json
import requests
import re

MB_DICT = ['MrBeast', 'Mr Beast', 'mr beast', 'MRBEAST']
DICT2 = ['based', 'BASED', 'Based', 'BaSeD']

with open('./config.json', 'r') as cjson:
    config = json.load(cjson)

openai.api_key= config["openai_apikey"]
class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        @client.event
        async def on_message(message:Member):
            if message.author.bot:
                return
            if any(word in message.content.lower() for word in MB_DICT):
                await message.reply('I LOVE MR. BEAST!!!')# if the message is 'Mr. Beast', the bot responds with 'I LOVE MR. BEAST!!!'
            await client.process_commands(message)
            
        @client.event
        async def on_voice_state_update(member:Member, before, after:VoiceState):
            if after.channel == None and before.channel.guild.name == "Jakoby's Safe Haven":
                mediaFiles = os.listdir("media/.")
                fileIndex = random.randint(0, len(mediaFiles)-1)
                channel:TextChannel = client.get_channel(949810707535376415)
                await channel.send(f"Get some GOOD SLEEP! {member.mention}", file=discord.File(f"media/{mediaFiles[fileIndex]}"), delete_after=20)
                
    @commands.command()        
    async def joke(self, ctx):
        # Make a GET request to the icanhazdadjoke API
        response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        # Get the joke from the response
        joke = response.json()['joke']
        # Send the joke to the channel
        await ctx.send(joke)
        

                   
    @commands.command()
    async def openai(self, ctx, *, search):
        
        response = openai.Image.create(
        prompt= search,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']
        
        await ctx.message.reply(image_url)

    @openai.error
    async def open_ai_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.message.reply(error.original.user_message)
            
def setup(client):
    client.add_cog(meme(client))