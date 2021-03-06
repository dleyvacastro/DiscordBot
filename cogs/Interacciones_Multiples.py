import discord
import asyncio
from discord.ext import commands
from discord.utils import get

solicitud = {}


class Interacciones_Multiples(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cierre_apodo_control = {}

    @commands.command(pass_context=True, aliases=['va', 'votacion_apodo'])
    async def solicitud_apodo(self, ctx, member: commands.MemberConverter, *, nick):

        embed = discord.Embed(
            title=f'Cambio de apodo.',
            description=f'El usuario {ctx.author.mention} solicita un cambio de nombre para:\n{member.mention} -> `{nick}`',
            colour=discord.Colour.random()
        )
        embed.set_footer(text='Se agradece la brevedad en su voto')
        embed.set_image(url='https://media.discordapp.net/attachments/394983545015238676/849679916751650925/Democracia-COVID-19-coronavirus-AmeCC81rica-Latina-Caribe-voto-votacioCC81n-derechos-civiles-min-102.png?width=647&height=442')
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/394983545015238676/849687628017041458/mickey.png?width=442&height=442')
        embed.set_author(name=str(ctx.author).split(
            '#')[0], icon_url=ctx.author.avatar_url)
        embed.add_field(name='Empieza la votación.',
                        value='Por favor, vote una sola vez.', inline=False)
        embed.add_field(
            name='APRUEBA', value=':white_check_mark:', inline=True)
        embed.add_field(name='NO APRUEBA', value=':no_entry:', inline=True)

        reactions = ["🟢", "🔴"]
        m = await ctx.send(embed=embed)
        for name in reactions:
            emoji = get(ctx.guild.emojis, name=name)
            await m.add_reaction(emoji or name)

        solicitud[member] = (m, nick)
        self.cierre_apodo_control[member] = True

        cache_msg = discord.utils.get(self.bot.cached_messages, id=m.id)
        await asyncio.sleep(2)
        v1 = cache_msg.reactions[0].count - 1
        v2 = cache_msg.reactions[1].count - 1

        v = await ctx.send(f'{member.mention}')
        while self.cierre_apodo_control[member] and v1+v2 < 5:
            v1 = cache_msg.reactions[0].count - 1
            v2 = cache_msg.reactions[1].count - 1

            r_embed = discord.Embed(
                title=f'Resultado para {member.name}',
                description=f'Estado actual: ',
                colour=discord.Color.random()
            )
            r_embed.add_field(name=f'{member.name}',
                              value=f'@{nick}', inline=True)
            r_embed.add_field(name='Aprobado', value=f'{v1} votos', inline=True)
            r_embed.add_field(name='No Aprueba', value=f'{v2} votos', inline = True)
            r_embed.set_footer(text=f'{v1+v2}/5 miembros han votado.')
            embed.set_image(url='https://media.discordapp.net/attachments/394983545015238676/849679916751650925/Democracia-COVID-19-coronavirus-AmeCC81rica-Latina-Caribe-voto-votacioCC81n-derechos-civiles-min-102.png?width=647&height=442')
            embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/394983545015238676/849687628017041458/mickey.png?width=442&height=442')
            embed.set_author(name=str(ctx.author).split(
            '#')[0], icon_url=ctx.author.avatar_url)
            await v.edit(embed=r_embed)
        
        if v1 > v2:
            await ctx.send(f'A peticición popular el nombre de {member} sera {nick}.\nEl pueblo ha hablado')
            await member.edit(nick=nick)
            await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo')
            await ctx.send(file=discord.File('./images/democracy.jpg'))
        elif v2 > v1:
            await ctx.send(f'Al parecer no era tan buena idea. {member} se salvo esta ocasión')
            await ctx.send(file=discord.File('./images/democracy.jpg'))
        else:
            await ctx.send(f'**TIBIOS HPTAS, por eso estamos como estamos**', file=discord.File('./images/fajardo.jpg'))

        await m.delete()
        await v.delete()

    @commands.command(pass_context=True, aliases=['da', 'desicion_apodo'])
    async def cierre_apodo(self, ctx, member: commands.MemberConverter = None):
        self.cierre_apodo[member] = False
        if member == None:
            m = solicitud[list(solicitud.keys())[len(solicitud)-1]]
        else:
            m = solicitud[member]
        msg = m[0]
        # or client.messages depending on your variable
        cache_msg = discord.utils.get(self.bot.cached_messages, id=msg.id)

        v1 = cache_msg.reactions[0].count
        v2 = cache_msg.reactions[1].count

        print(max(v1, v2))

        if v1 > v2:
            await ctx.send(f'A peticición popular el nombre de {member} sera {m[1]}.\nEl pueblo ha hablado')
            await member.edit(nick=m[1])
            await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo')
            await ctx.send(file=discord.File('./images/democracy.jpg'))
        elif v2 > v1:
            await ctx.send(f'Al parecer no era tan buena idea. {member} se salvo esta ocasión')
            await ctx.send(file=discord.File('./images/democracy.jpg'))
        else:
            await ctx.send(f'**TIBIOS HPTAS, por eso estamos como estamos**', file=discord.File('./images/fajardo.jpg'))

        await msg.delete()

    @commands.command()
    async def reactionGetter(self, ctx, ):
        msg = await ctx.send('Message to put reactions on')
        await msg.add_reaction("✅")
        await msg.add_reaction("🤍")
        await asyncio.sleep(4)
        # or client.messages depending on your variable
        cache_msg = discord.utils.get(self.bot.cached_messages, id=msg.id)
        print(cache_msg.reactions)
        print(cache_msg.reactions[0].count)


def setup(bot):
    bot.add_cog(Interacciones_Multiples(bot))