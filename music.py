import discord
from discord.ext import commands
import yt_dlp
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
            queue.insert(len(queue), searchResult["source"])
        
        # Add to queue if song is requested while still playing
        elif vc.is_playing() and search is not None: 
            searchResult = self.getYoutubeLink(search)
            await ctx.send(f'Added "{searchResult["title"]}" to the queue! \nhttp://www.youtube.com/watch?v={searchResult["search_result"]}')
            queue.insert(len(queue), searchResult["source"])
        
        if len(queue) > 0 and not vc.is_playing():
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            source = await discord.FFmpegOpusAudio.from_probe(queue[0], **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(ctx), self.client.loop))
            queue.pop(0)

    async def play_next_song(self, ctx):
        vc = ctx.voice_client
        if len(queue) > 0:
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            source = await discord.FFmpegOpusAudio.from_probe(queue[0], **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(ctx), ctx.bot.loop))
            queue.pop(0)

    def getYoutubeLink(self, searchQuery):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'extract_flat': 'in_playlist', 'default_search': 'auto'}
        data = dict()
        query_string = urllib.parse.urlencode({'search_query': searchQuery})
        htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})',
                                htm_content.read().decode())
        data["search_result"] = search_results[0]

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(search_results[0], download=False)
            data["source"] = info['url'] 
            data["title"] = info["title"]
            return data

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you want me to play? Try doing ".play {song name}"')

    @commands.command()
    async def clear_q(self, ctx):
        queue = []  

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not connected! Try playing a song using ".play {song name}"')
        ctx.voice_client.stop()   
        queue = []
        await ctx.voice_client.disconnect()    

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not connected! Try playing a song using ".play {song name}"')
        ctx.voice_client.stop()        

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not connected! Try playing a song using ".play {song name}"')
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not connected! Try playing a song using ".play {song name}"')
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not connected! Try playing a song using ".play {song name}"')
        await ctx.voice_client.resume() 
        queue = []


def setup(client):
    client.add_cog(music(client))
