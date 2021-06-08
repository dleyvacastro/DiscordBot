import discord
import asyncio
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        self.voice = get(self.bot.voice_clients, guild = ctx.guild)

        if self.voice and self.voice.is_connected():
            await self.voice.move_to(channel)
        else:
            self.voice = await channel.connect()
            self.voice.play(discord.FFmpegPCMAudio("./audios/tenebroso.mp3"), after = lambda e: print(f'has finished playing'))
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
            self.voice.source.volume = 0.6

        
        await ctx.send(f'El Señor Tenebroso esta en {channel}')
    
    @commands.command()
    async def leave(self, ctx): 
        channel = ctx.author.voice.channel
        self.voice = get(self.bot.voice_clients, guild = ctx.guild)

        if self.voice and self.voice.is_connected():
            await self.voice.disconnect()
            await ctx.send('El Señor Tenebroso se retira por ahora.')
        else:
            await ctx.send("¿Retirarme de donde?")
    
    @commands.command()
    async def play(self, ctx, url : str):
        channel = ctx.author.voice.channel
        self.voice = get(self.bot.voice_clients, guild = ctx.guild)

        if self.voice and self.voice.is_connected():
            await self.voice.move_to(channel)
        else:
            self.voice = await channel.connect()
        

        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
        except:
            print('failed to delete')

        self.voice = get(self.bot.voice_clients, guild = ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/beat',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("downloading audio")
            ydl.download({url})

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                os.rename(file, 'song.mp3')
        
        self.voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print(f'{name} has finished playing'))
        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(nname[0])
        print("playing")
def setup(bot):
    bot.add_cog(Music(bot))