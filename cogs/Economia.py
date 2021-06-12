import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get


class Economia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.give_tokens.start()
        self.miembros = []

        self.miembros_id = ['394982506417487872', '393592731420721154', '318611546383319041',
                            '396305256377614337', '704883078291521537', '528019938196324372']

    @tasks.loop(seconds=10)
    async def give_tokens(self):
        tokens = open("cogs/Moneda.txt",  'r')
        usuarios = tokens.readlines()
        print(usuarios)
        tokens.close()
        tokens = open("cogs/Moneda.txt",  'w+')
        for i in range(len(usuarios)):
            usuario = usuarios[i].split(',')
            usuario[1] = f'{int(usuario[1][:-1])+1}'
            usuarios[i] = usuario

        for line in usuarios:
            nline = str(line).replace('[', '')
            nline = nline.replace(']', '')
            nline = nline.replace("'", '')

            tokens.write(nline + '\n')
            print(line)
        tokens.close()
        await self.pruebas_c.send('Se han recargado los tokens de los miembros correspondientes.')

    @give_tokens.before_loop
    async def before_give_tokens(self):

        tokens = open("cogs/Moneda.txt", 'w')
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(393593323463376899)
        self.pruebas_c = self.bot.get_channel(840258678334554122)
        for i in self.miembros_id:
            miembro = await guild.fetch_member(i)
            self.miembros.append(miembro)
        for i in self.miembros:
            tokens.write(f'{i.id}, 0\n')
        tokens.close()


def setup(bot):
    bot.add_cog(Economia(bot))
