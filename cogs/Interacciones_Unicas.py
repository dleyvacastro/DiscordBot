import discord
import random
import os
import asyncio
from discord.ext import commands
from statistics import mode


class Interacciones_Unicas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong :sunglasses: {(self.bot.latency) * 1000} ms. {ctx.author.mention}')

    @commands.command()
    async def confesion(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        respuestas = [
            f'Se dice por ahi que:\n**{message}**',
            f'Algún careverga de por ahí les manda a decir que:\n**{message}**',
            f'Los lideres de oposición comentan que:\n**{message}**',
            f'El que se comió un payaso tiene un comentario:\n**{message}**',
            f'Su cucha le manda a decir que:\n**{message}**',
            f'Diomedes le manda desde la tumba:\n**{message}**',
            f'Oye! Te hablo desde la prisión Wilson Manyoma:\n**{message}**',
            f'El Señor Tenebroso ha enviado un comunicado. Atentos todos:\n**{message}**',
            f'Zoocucha manifiesta que:\n**{message}**',
            f'Extra! Se ha encontrado un fragmento perdido del manifiesto comunista que dice:\n**{message}**',
            message,
            f'Se escucha por las calles del centro que:\n**{message}**',
            f'La nueva cancion de Jbalvin dice:\n**{message}**',
            f'La Pulla subió un video diciendo que:\n**{message}**',
            f'Oigan a mi tia. Disque:\n**{message}**',
            f'He de decir que:\n**{message}**',
            f'Me dijo un pajarito que: \n**{message}**',
            f'Yo lo quiero mucho, pero: \n**{message}**',
            f'Uy la liendra publico en twitter que: \n**{message}**',
            f'No me incumbe pero: \n**{message}**',
            f'Mucha perra, disque: \n**{message}**',
            f'El foro de Sao Paulo ha pronunciado que: \n**{message}**',
            f'La primera linea comenta que: \n**{message}**',
            f'En el congreso me dijeron que: \n**{message}**',
            f'Semana publicó: \n**{message}**',
            f'Jhay cortez me contó que: \n**{message}**',
            f'La fiscalía confirmó que: \n**{message}**',
            f'Un grafiti en la septima dice que: \n**{message}**',
            f'Maria Fernanda Cabal me contó que <@396305256377614337> dijo: \n**{message}**',
            f'Wikileaks ha filtrado un mensaje:\n**{message}**\n Y por culpa de Petro su autor ha quedado al descubierto, {ctx.author.mention}'
        ]
        # print(len(respuestas))
        await ctx.send(random.choice(respuestas))

    @commands.command()
    async def tombotruco(self, ctx):
        image = os.listdir('./tombotruco/')
        # Selects a random element from the list
        imgString = random.choice(image)
        path = "./tombotruco/" + imgString
        await ctx.send(file=discord.File(path))

    @commands.command()
    async def choose(self, ctx, *, options):
        options = options.split(',')
        await ctx.send(random.choice(options))

    @commands.command()
    async def poll(self, ctx, question, *, options):
        reacted = {}
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣',
                     '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        options = options.split(',')
        embed = discord.Embed(
            title=f'Urna virtual',
            description=question,
            colour=discord.Colour.random()
        )
        embed.set_thumbnail(
            url='https://www.mdirector.com/wp-content/uploads/2020/09/Encuesta-mensaje.png')
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        for i in range(len(options)):
            embed.add_field(
                name=f'{reactions[i]} {options[i]}', value="** **", inline=False)

        m = await ctx.send(embed=embed)

        for i in range(len(options)):
            await m.add_reaction(reactions[i])

        m2 = await ctx.send(f'La opcion ganadora es: ...')

        while len(reacted) < 5:
            reaction, user = await self.bot.wait_for('reaction_add')
            reacted[user] = reaction

            await m2.edit(content=f'La opcion ganadora por el momento es: {mode(reacted.values())}')

        await m2.edit(content=f'La opcion ganadora es: {mode(reacted.values())}')

    @commands.command()
    async def testEmbed(self, ctx):
        # author = self.bot.get_user(393592731420721154)
        embed = discord.Embed(
            title='Menu de Ayuda',
            description='Pre-fix: `$`',
            colour=discord.Colour.dark_red()
        )
        embed.set_footer(text=f'Creado para {ctx.guild.name}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name='Daniel Leyva', icon_url=ctx.author.avatar_url)
        embed.add_field(name='**Interacciones Unicas**',
                        value='Comandos de una sola interacción.', inline=False)
        embed.add_field(
            name='confesion', value='   Enviara el mensaje de forma anonima', inline=True)
        embed.add_field(name='Alias', value='`cf`, `confesion`', inline=True)
        embed.add_field(
            name='ping', value='    Devuelve la latencia entre el cliente y el bot', inline=False)
        embed.add_field(name='tombotruco',
                        value='   Enviara la imagen de un tombo.', inline=False)
        embed.add_field(name='**Interacciones Multiples**',
                        value='Comandos los cuales involucran mas de una acción o miembro.', inline=False)

        embed.add_field(name='solicitud_apodo',
                        value='Se creara una votación para cambiar el apodo de de un miembro.', inline=True)
        embed.add_field(
            name='Alias', value='`va`,`votacion_apodo`', inline=True)

        embed.add_field(name='🔽Termina en 🔽', value='🔽🔽🔽🔽🔽🔽', inline=False)

        embed.add_field(name='cierre_apodo', value='Cerrará la votación para el cambio de nombre para el miembro especificado y dependiendo de esto tomara la accion correspondiente.', inline=True)

        embed.add_field(
            name='Alias', value='`da`,`desicion_apodo`', inline=True)

        m = await ctx.send(embed=embed)

        await asyncio.sleep(5)
        embed2 = discord.Embed(
            title='test',
            description='test desc',
            colour=discord.Colour.random()
        )
        await m.edit(embed=embed2)


def setup(bot):
    bot.add_cog(Interacciones_Unicas(bot))
