import discord
import asyncio
import random
from discord.ext import commands, tasks
from discord.utils import get
from replit import Database

db = Database('https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjM3NDc4MjksImlhdCI6MTYyMzYzNjIyOSwiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiI3OGI3YzQxMC0zNGM3LTQxNzAtYmRkNS03ZDcxMzNhODU5NTkifQ.EnZKvlY1FDuvLonmMdUFHvj8jPlfzNmTmX-WUdEs3cHpvpdpklPkytGrF8GaVQ0xfsx7HkiJGIPQQTsEflzUlA')


class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.give_tokens.start()
        self.miembros = []

        self.miembros_id = ['394982506417487872', '393592731420721154', '318611546383319041',
                            '396305256377614337', '704883078291521537', '528019938196324372']

    def get_user_money(self, user):
        v = int(db[f'{user.id}'])
        return v

    def cobro(self, author, precio):
        v = self.get_user_money(author)
        if v > precio:
            db[f'{author.id}'] = v - precio
            return True
        return False

    @tasks.loop(hours=24*7)
    async def give_tokens(self):
        self.star_giveaway = True
        for i in self.miembros_id:
            db[f"{i}"] = f'{int(db[f"{i}"]) + 70}'
            # print(db[f"{i}"])
        embed = discord.Embed(
            title='Give Away',
            description='10*`multiplicador` Diomede$.\n`multiplicador` es un numero aleatorio entre -5 y 10. Mucha suerte!',
            colour=discord.Colour.random()
        )
        await self.pruebas_c.send('Se han recargado los tokens de los miembros correspondientes.')
        ga = await self.pruebas_c.send(embed=embed)
        await ga.add_reaction('🥳')
        await asyncio.sleep(1)
        print('star givaway')
        await self.giveaway(ga)

    async def giveaway(self, message):
        cont = 0
        while self.star_giveaway:

            message = await self.pruebas_c.fetch_message(message.id)
            users = set()
            for reaction in message.reactions:
                async for user in reaction.users():
                    users.add(user)

            await asyncio.sleep(60*60)
            cont += 1
            if cont >= 3*24 or len(users) >= 6:
                participans = list(users)
                participans.remove(self.bot.user)
                if len(participans) == 0:
                    await self.pruebas_c('Nadie ha participado.')
                    break
                winner = random.choice(participans)
                value = 10*random.randint(-5, 10)
                db[f'{winner.id}'] = f'{self.get_user_money(winner)+value}'
                self.star_giveaway = False
        else:
            print('finished')
            await self.pruebas_c.send(f'Felicidades {winner.mention}. Se le han computado {value} Diomede$ en su cuenta.')
        return

    @ give_tokens.before_loop
    async def before_give_tokens(self):

        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(393593323463376899)
        self.pruebas_c = self.bot.get_channel(840258678334554122)
        for i in self.miembros_id:
            miembro = await guild.fetch_member(i)
            self.miembros.append(miembro)
        keys = db.keys()
        print(keys)

    @commands.command()
    async def Money(self, ctx):
        embed = discord.Embed(
            title='Cuentas de los miembros.',
            description='Diomede$ en el servidor.',
            colour=discord.Colour.random()
        )
        for i in self.miembros:
            embed.add_field(
                name=f'**{i.nick}**: {self.get_user_money(i)} Diomede$', value='** **', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Tasks(bot))
