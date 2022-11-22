import discord
from discord.ext import commands

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        @client.event
        async def on_message(message):
            if message.content.startswith('Mr Beast'):
                await message.channel.send('I LOVE MR. BEAST!!!')# if the message is 'Mr. Beast', the bot responds with 'I LOVE MR. BEAST!!!'
                return
            
def setup(client):
    client.add_cog(meme(client))