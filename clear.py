import discord
from discord.ext import commands

class clear(commands.Cog):
        def __init__(self, client):
            self.client = client
            
            @client.command()
            @commands.has_permissions(manage_messages=True)
            async def clear(ctx, amount=10):
                if commands.has_permissions(manage_messages=True): 
                    await ctx.channel.purge(limit=amount)                                     
                    await ctx.send(f'{amount} Messages Deleted!')                        
                return
            
def setup(client):
    client.add_cog(clear(client))