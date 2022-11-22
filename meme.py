import discord
from discord.ext import commands

MB_DICT = ['MrBeast', 'Mr Beast', 'mr beast', 'MRBEAST']
class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        @client.event
        async def on_message(message):
            if any(word in message.content.lower() for word in MB_DICT):
                await message.channel.send('I LOVE MR. BEAST!!!')# if the message is 'Mr. Beast', the bot responds with 'I LOVE MR. BEAST!!!'
                return
            else:
                await client.process_commands(message)
                
def setup(client):
    client.add_cog(meme(client))