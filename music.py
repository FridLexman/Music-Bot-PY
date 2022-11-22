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

        async def join(self, ctx):
            if ctx.author.voice is None:
                await ctx.send("You must connect to a channel first!")
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

        @commands.command(name="play")
        async def play(self, ctx, *, search):
            # Join if it has not already
            if ctx.voice_client is None:
                await self.join(ctx)
            vc = ctx.voice_client

            # Add to queue if there is nothing in the queue
            if len(queue) <= 0 and not vc.is_playing() and search is not None:
                searchResult = self.getYoutubeLink(search)
                await ctx.send(f'Now playing "{searchResult["title"]}" \nhttp://www.youtube.com/watch?v={searchResult["search_result"]}')
                queue.insert(len(queue), searchResult["url"])

            # Play a song if there is songs in the queue
            if len(queue) > 0 and not vc.is_playing():
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                source = await discord.FFmpegOpusAudio.from_probe(queue[0], **FFMPEG_OPTIONS)
                vc.play(source)
                queue.pop(0)
                if(len(queue) <= 0): # After playing the song and popping the queue, if there are no more songs, stop checking
                    return

            # Add to queue if song is requested while still playing
            elif vc.is_playing() and search is not None: 
                searchResult = self.getYoutubeLink(search)
                await ctx.send(f'Added "{searchResult["title"]}" to the queue! \nhttp://www.youtube.com/watch?v={searchResult["search_result"]}')
                queue.insert(len(queue), searchResult["url"]) 
                
            await asyncio.sleep(5)
            await self.play(ctx, None)

        @play.error
        async def play_error(self, ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send('What do you want me to play? Try doing "!play {song name}"')

        def getYoutubeLink(self, searchQuery):
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            data = dict()
            query_string = urllib.parse.urlencode({'search_query': searchQuery})
            htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})',
                                    htm_content.read().decode())
            data["search_result"] = search_results[0]

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(search_results[0], download=False)
                data["url"] = info['formats'][0]['url'] 
                data["title"] = info["title"]
                return data  

        @commands.command()
        async def q_lenght(self, ctx):
            await ctx.send(len(queue))
            
        @commands.command()
        async def clear_q(self, ctx):
            queue = []  

        @commands.command()
        async def stop(self, ctx):
            if ctx.voice_client is None:
                await ctx.send('I am not connected! Try using "!join" or play a song using "!play {song name}"')
            ctx.voice_client.stop()   
            queue = []
            await ctx.voice_client.disconnect()    

        @commands.command()
        async def skip(self, ctx):
            if ctx.voice_client is None:
                await ctx.send('I am not connected! Try using "!join" or play a song using "!play {song name}"')
            ctx.voice_client.stop()        

        @commands.command()
        async def disconnect(self, ctx):
            if ctx.voice_client is None:
                ctx.send('I am not connected! Try using "!join" or play a song using "!play {song name}"')
            await ctx.voice_client.disconnect()

        @commands.command()
        async def pause(self, ctx):
            if ctx.voice_client is None:
                await ctx.send('I am not connected! Try using "!join" or play a song using "!play {song name}"')
            await ctx.voice_client.pause()

        @commands.command()
        async def resume(self, ctx):
            if ctx.voice_client is None:
                await ctx.send('I am not connected! Try using "!join" or play a song using "!play {song name}"')
            await ctx.voice_client.resume()



def setup(client):
    client.add_cog(music(client))
