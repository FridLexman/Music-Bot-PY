from discord import *
import discord
from discord.ext import commands
import random
import os

class meme(commands.Cog):
    def __init__(self, client:Client):
        self.client = client

        @client.event
        async def on_message(message:Message):
            if message.author == client.user or message.author.id == 969010164625735780:
                return
            if "based" in message.content.lower():
                await message.reply("based on WHAT?")

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
            
