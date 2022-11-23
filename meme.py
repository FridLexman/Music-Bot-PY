import discord
from discord import *                                                             
from discord.ext import commands

MB_DICT = ['MrBeast', 'Mr Beast', 'mr beast', 'MRBEAST']
DICT2 = ['based', 'BASED', 'Based', 'BaSeD']

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        @client.event
        async def on_message(message:Member):
            if message.author == client.user:
                return
            
            if any(word in message.content.lower() for word in MB_DICT):
                await message.reply('I LOVE MR. BEAST!!!')# if the message is 'Mr. Beast', the bot responds with 'I LOVE MR. BEAST!!!'

            if any(word in message.content.lower() for word in DICT2):
                await message.reply("based on WHAT???")# if the message is 'based', the bot responds with 'based on WHAT???'
                
            await client.process_commands(message)
            
def setup(client):
    client.add_cog(meme(client))