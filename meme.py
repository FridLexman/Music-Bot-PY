import discord
from discord import *                                                             
from discord.ext import commands
import random
import os

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
            
        @client.event
        async def on_voice_state_update(member:Member, before, after:VoiceState):
            if after.channel == None and before.channel.guild.name == "Jakoby's Safe Haven":
                mediaFiles = os.listdir("media/.")
                fileIndex = random.randint(0, len(mediaFiles)-1)
                channel:TextChannel = client.get_channel(949810707535376415)
                await channel.send(f"Get some GOOD SLEEP! {member.mention}", file=discord.File(f"media/{mediaFiles[fileIndex]}"), delete_after=20)

def setup(client):
    client.add_cog(meme(client))