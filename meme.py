import discord
from discord.ext import commands

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            if "based" in message.content:
                await message.reply("based on WHAT?")
            await client.process_commands(message)

def setup(client):
    client.add_cog(meme(client))
            
