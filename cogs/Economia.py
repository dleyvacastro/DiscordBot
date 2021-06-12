import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
from replit import db



class Economia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.give_tokens.start()
        self.miembros = []

        self.miembros_id = ['394982506417487872', '393592731420721154', '318611546383319041',
                            '396305256377614337', '704883078291521537', '528019938196324372']
        #precios

        self.chnick_p = 20

    @tasks.loop(hours = 24)
    async def give_tokens(self):
        for i in self.miembros_id:
            db[f"{i}"] = f'{int(db[f"{i}"]) + 1}'
            print(db[f"{i}"])
        await self.pruebas_c.send('Se han recargado los tokens de los miembros correspondientes.')
        

    @give_tokens.before_loop
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
    @commands.has_role(849454598296830023)
    async def reset_economy(self, ctx, message):
        if message == 'CONFIRMAR':
            for i in self.miembros_id:
                db[f"{i}"] = 0
            await ctx.send('Las cuentas de todos los miembros ahora son 0')
        else:
            await ctx.send('Por favor confime la orden.')

    def get_money(self, author):
        v = db[str(author)]
        return v

    @commands.command()
    async def money(self, ctx, member: commands.MemberConverter = None):
        if member == None:
            member = ctx.author
        await ctx.reply(f'Maldito asalariado usted tiene: {self.get_money(member.id)} Dorian Coins.')

    @commands.command()
    @commands.has_role(849454598296830023)
    async def add_money(self, ctx, member: commands.MemberConverter = None, amount = 1):
        if member == None:
            member = ctx.author
        id = str(member.id)
        db[id] = f'{int(db[id])+amount}'
        await ctx.reply(f'Maldito asalariado, se le ha depositado {amount}$ en su cuenta, ahora usted tiene: {self.get_money(ctx.author.id)} Dorian Coins.')

    @commands.command()
    @commands.has_role(849454598296830023)
    async def rest_money(self, ctx, member: commands.MemberConverter = None, amount = 1):
        if member == None:
            member = ctx.author
        id = str(member.id)
        db[id] = f'{int(db[id])-amount}'
        await ctx.reply(f'Maldito asalariado, se le ha retirado {amount}$ de su cuenta, ahora usted tiene: {self.get_money(ctx.author.id)} Dorian Coins.')

    @commands.command()
    async def send(self, ctx, member: commands.MemberConverter, amount = 1):
        id = str(member.id)
        a_id = str(ctx.author.id)
        db[a_id] = f'{int(db[a_id])-amount}'
        db[id] = f'{int(db[id])+amount}'
        await ctx.reply(f'Transfrencia exitosa. Se han enviado {amount}$ a {member.mention}.')

    @commands.command()
    async def compra(self, ctx, parameter, member: commands.MemberConverter, nick):
        v = db[f'{ctx.author.id}']
        if parameter == 'chnick'  and v >= self.chnick_p:
            db[f'{ctx.author.id}'] = int(db[f'{ctx.author.id}'])
            await member.edit(nick = nick)
            await ctx.send(f'{member.name} Ahora seras conocido como {member.mention} mamahuevo.')            
        

def setup(bot):
    bot.add_cog(Economia(bot))
