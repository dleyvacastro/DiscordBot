import discord
import asyncio
from discord.ext import commands
from discord.utils import get

solicitud = {}

class Interacciones_Multiples(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases = ['sa'])
    async def solicitud_apodo(self, ctx, member: discord.Member, *, nick):
        reactions = ["🟢", "🔴"]
        ans = """
            Solicitud de {0}
            **CAMBIO DE APODO PARA** {1} -> {2}
            APRUEBA         :white_check_mark:   
            
            NO APRUEBA  :no_entry:
            """.format(ctx.message.author.name, member, nick)
        m = await ctx.send(ans)
        for name in reactions:
            emoji = get(ctx.guild.emojis, name=name)
            await m.add_reaction(emoji or name)
        
        solicitud[member] = (m, nick)
        # print(solicitud)

    @commands.command(pass_context=True, aliases = ['ca'])
    async def cierre_apodo(self, ctx, member: discord.Member):
        m = solicitud[member]
        msg = m[0]
        cache_msg = discord.utils.get(self.bot.cached_messages, id=msg.id) #or client.messages depending on your variable
        
        v1 = cache_msg.reactions[0].count
        v2 = cache_msg.reactions[1].count

        print(max(v1,v2))

        if v1 > v2:
            await ctx.send(f'A peticición popular el nombre de {member} sera {m[1]}.\nEl pueblo ha hablado')
            await member.edit(nick=m[1])
            await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo')
            await ctx.send(file = discord.File('./images/democracy.jpg'))
        elif v2 > v1:
            await ctx.send(f'Al parecer no era tan buena idea. {member} se salvo esta ocasión')
            await ctx.send(file = discord.File('./images/democracy.jpg'))
        else:
            await ctx.send(f'**TIBIOS HPTAS, por eso estamos como estamos**', file = discord.File('./images/fajardo.jpg'))

        await msg.edit(content = f'La acción para {member.mention} ya ha sido tomada')
    
    @commands.command()
    async def reactionGetter(self, ctx, ):
        msg = await ctx.send('Message to put reactions on')
        await msg.add_reaction("✅")
        await msg.add_reaction("🤍")
        await asyncio.sleep(4)
        cache_msg = discord.utils.get(self.bot.cached_messages, id=msg.id) #or client.messages depending on your variable
        print(cache_msg.reactions)
        print(cache_msg.reactions[0].count)

def setup(bot):
    bot.add_cog(Interacciones_Multiples(bot))