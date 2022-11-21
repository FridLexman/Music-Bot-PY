import discord
from discord.ext import commands
import youtube_dl
import discord.utils
import urllib.parse, urllib.request, re
import asyncio

queue = []

class music(commands.Cog):
        def __init__(self, client):
            self.client = client 

        @commands.command()
        async def join(self, ctx):
            if ctx.author.voice is None:
                await ctx.send("You're Not Connected")
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

        @commands.command()
        async def play(self, ctx):
            vc = ctx.voice_client
            if len(queue) <= 0 and vc.is_playing() == False:
                await ctx.send("There are no songs in the queue. Add a song using the '.queue(song_name)' ")
                return
            elif vc.is_playing() == False:
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                source = await discord.FFmpegOpusAudio.from_probe(queue[0], **FFMPEG_OPTIONS)
                vc.play(source)
                queue.pop(0)
                
            await asyncio.sleep(5)
            await self.play(ctx)

        @commands.command()                       
        async def queue(self, ctx, *, search):

            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}


            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})',
                                    htm_content.read().decode())
            await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(search_results[0], download=False)
                url2 = info['formats'][0]['url']
                queue.insert(len(queue), url2) 
                
        @commands.command()
        async def q_lenght(self, ctx):
            await ctx.send(len(queue))
            
        @commands.command()
        async def clear_q(self, ctx):
            queue.clear()    

        @commands.command()
        async def stop(self, ctx):
            await ctx.voice_client.stop()            

        @commands.command()
        async def disconnect(self, ctx):
            await ctx.voice_client.disconnect()

        @commands.command()
        async def pause(self, ctx):
            await ctx.voice_client.pause()

        @commands.command()
        async def resume(self, ctx):
            await ctx.voice_client.resume()


def setup(client):
    client.add_cog(music(client))
