import discord
import random
import os
from discord.ext import commands

class Interacciones_Unicas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong :sunglasses: {(self.bot.latency) * 1000} ms. {ctx.author.mention}')

    @commands.command()
    async def confesion(self, ctx, *, message):
        await ctx.channel.purge(limit = 1)  
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
        imgString = random.choice(image)  # Selects a random element from the list
        path = "./tombotruco/" + imgString
        await ctx.send(file=discord.File(path))
        

def setup(bot):
    bot.add_cog(Interacciones_Unicas(bot))