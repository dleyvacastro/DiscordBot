import discord
from discord.ext import commands

class Moderacion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['RCN', 'Caracol', 'Censura', 'censura'])
    @commands.has_any_role(685973595423375388, 849454598296830023)
    async def clear(self, ctx, amount = 2):
        """
        Alias: RCN, Caracol, Censura
        """
        await ctx.channel.purge(limit = amount)
        if amount > 10:
            await ctx.send(f'Premio Juan Pablo Bieri al Censurador del año, ¿Usted mató a Jaime Garzon o q? {ctx.author.metion}')
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
    

def setup(bot):
    bot.add_cog(Moderacion(bot))