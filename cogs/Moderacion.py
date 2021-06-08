import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from statistics import mode

class Moderacion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.zawarudo = False

    @commands.command(aliases = ['RCN', 'Caracol', 'Censura', 'censura'])
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def clear(self, ctx, amount = 2):
        """
        Alias: RCN, Caracol, Censura
        """
        await ctx.channel.purge(limit = amount)
        if amount > 10:
            await ctx.send(f'Premio Juan Pablo Bieri al Censurador del año, ¿Usted mató a Jaime Garzon o q? {ctx.author.mention}')
            # await ctx.author.edit(nick="Dr. MinTIC")
    
    @commands.command()
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def kick(self, ctx, member : commands.MemberConverter, *, reason = None):
        await member.kick(reason = reason)
        await ctx.send(f'Se comenta que a alias {member.mention} lo enterraron por sapo.')

    @commands.command()
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def ban(self, ctx, member : commands.MemberConverter, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f'No debiste incordiar al Señor Tenebroso {member.mention}.')

    @commands.command()
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for i in banned_users:
            user = i.user
            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(f'Bienvenido de nuevo hermanito bolivariano {user.mention}.')
                return
    
    @commands.command(pass_context=True)
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def chnick(self, ctx, member: commands.MemberConverter, *, nick):
        await member.edit(nick=nick)
        await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo')
    
    @commands.command()
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def zawarudo(self, ctx):
        tts = True
        dio_time = ['Ni', 'San', 'Yon', 'Go', 'Roku', 'Nana', 'Hachi', 'Kyuu', 'Jyuu']
        embed = discord.Embed(
            title = 'Yare Yare Daze',
            description = 'Estan como muy aletosos.',
            colour = discord.Colour.random()
        )
        embed.set_image(url='https://media1.tenor.com/images/3546df32c4974a720904643ecf5956ef/tenor.gif?itemid=17040017')
        await ctx.send(embed = embed)
        self.zawarudo = True
        self.channel_stoped = ctx.channel

        try:
            channel = ctx.author.voice.channel
            self.voice = get(self.bot.voice_clients, guild = ctx.guild)
            tts = False
            if self.voice and self.voice.is_connected():
                await self.voice.move_to(channel)
            else:
                self.voice = await channel.connect()

            self.voice.play(discord.FFmpegPCMAudio("./audios/zawarudo.mp3"), after = lambda e: print(f'has finished playing'))
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
            self.voice.source.volume = 0.5
            await ctx.send('Zawardo!, Tomare Toki wo', tts = tts)
            await asyncio.sleep(5)
        except:
            await ctx.send('Zawardo!, Tomare Toki wo', tts = tts)       
            await asyncio.sleep(1)     
        

        m = await ctx.send('Ichi byou keika')
        for i in dio_time:
            await asyncio.sleep(2)
            await m.edit(content = i+' byou keika')
        await asyncio.sleep(1.5)
        m2 = await ctx.send('Toki ua ugoki des', tts = tts)
        await asyncio.sleep(1.5)
        await m2.edit(content = 'Toki wa ugoki dasu')
        self.zawarudo = False

    @commands.Cog.listener('on_message')
    async def time_stop(self, ctx):
        if ctx.author == self.bot.user:
            return
        if self.zawarudo and ctx.channel == self.channel_stoped:
            await ctx.channel.purge(limit = 1)

    



def setup(bot):
    bot.add_cog(Moderacion(bot))