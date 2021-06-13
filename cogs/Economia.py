import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
from replit import Database

db = Database('https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjM2Mzg3NDcsImlhdCI6MTYyMzUyNzE0NywiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiI3OGI3YzQxMC0zNGM3LTQxNzAtYmRkNS03ZDcxMzNhODU5NTkifQ.h4ToqqoRxDAhDd8SeQ5_OPuLJzXkTlKDQWEP23HfxfJuoIFFqc0XWKALQmTeIQjya1HV2TTFYibngDJM0k1tAg')


class Economia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.give_tokens.start()
        self.miembros = []

        self.miembros_id = ['394982506417487872', '393592731420721154', '318611546383319041',
                            '396305256377614337', '704883078291521537', '528019938196324372']
        # precios

        self.chnick_p = 20
        self.censura_p = 10
        self.tts_p = 5
        self.golpe_de_estado_p = 6402

    def get_user_money(self, user):
        v = int(db[f'{user.id}'])
        return v

    def cobro(self, author, precio):
        v = self.get_user_money(author)
        if v > precio:
            db[f'{author.id}'] = v - precio
            return True
        return False

    @tasks.loop(hours=24)
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

    @commands.command()
    async def money(self, ctx, member: commands.MemberConverter = None):
        if member == None:
            member = ctx.author
        await ctx.reply(f'Maldito asalariado usted tiene: {self.get_user_money(member)} Dorian Coins.')

    @commands.command()
    @commands.has_role(849454598296830023)
    async def add_money(self, ctx, member: commands.MemberConverter = None, amount=1):
        if member == None:
            member = ctx.author
        id = str(member.id)
        db[id] = f'{int(db[id])+amount}'
        await ctx.reply(f'Maldito asalariado, se le ha depositado {amount}$ en su cuenta, ahora usted tiene: {self.get_user_money(ctx.author)} Dorian Coins.')

    @commands.command()
    @commands.has_role(849454598296830023)
    async def rest_money(self, ctx, member: commands.MemberConverter = None, amount=1):
        if member == None:
            member = ctx.author
        id = str(member.id)
        db[id] = f'{int(db[id])-amount}'
        await ctx.reply(f'Maldito asalariado, se le ha retirado {amount}$ de su cuenta, ahora usted tiene: {self.get_user_money(member)} Dorian Coins.')

    @commands.command()
    async def send(self, ctx, member: commands.MemberConverter, amount: int = 1):
        id = str(member.id)
        a_id = str(ctx.author.id)
        if int(db[a_id]) < amount:
            await ctx.reply('Hoy no se fia, mañana si.')
            return
        db[a_id] = f'{int(db[a_id])-amount}'
        db[id] = f'{int(db[id])+amount}'
        await ctx.reply(f'Transfrencia exitosa. Se han enviado {amount}$ a {member.mention}.')

    # Comandos compras.
    @commands.command(pass_context=True)
    async def chnick(self, ctx, member: commands.MemberConverter, *, nick):
        if self.cobro(ctx.author, self.chnick_p):
            await member.edit(nick=nick)
            await ctx.send(f'{ctx.author.mention} ha redimido un cambio de apodo para {member.nick} por {self.chnick_p}, ahora tienes {db[str(ctx.author.id)]}.')
            await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo.')
        else:
            await ctx.send(f'Trabaje vago pobre')

    @commands.command(aliases=['RCN', 'Caracol', 'censura'])
    async def clear(self, ctx, amount=2):
        """
        Alias: RCN, Caracol, Censura
        """
        if self.cobro(ctx.author, self.censura_p):
            await ctx.channel.purge(limit=amount)
            if amount > 10:
                await ctx.send(f'Premio Juan Pablo Bieri al Censurador del año, ¿Usted mató a Jaime Garzon o q? {ctx.author.mention}')
            # await ctx.author.edit(nick="Dr. MinTIC")
        else:
            await ctx.send('Trabaje vago mamamerto.')

    @commands.command()
    async def tts(self, ctx, *, message):
        if self.cobro(ctx.author, self.tts_p):
            await ctx.send(ctx.author.mention)
            await ctx.send(message, tts=1)
            await ctx.message.delete()
        else:
            await ctx.send('Trabaje vago mamerto')

    @commands.command()
    async def golpe_de_estado(self, ctx):
        miembros = []
        admin_role = get(ctx.guild.roles, id=685973595423375388)
        firmes_role = get(ctx.guild.roles, id=685974684134801457)
        anuncio = self.bot.get_channel(839554918561611837)
        await ctx.send(f'{ctx.author.mention} quiere tomar el poder por la fuerza')
        if self.cobro(ctx.author, self.golpe_de_estado_p):
            await ctx.send('Y tiene el capital para lograrlo. Felicidades nuevo admin.')
            await anuncio.send(f'El nuevo admin es (golpe de estado): {ctx.author.mention}')
            await anuncio.send(file=discord.File('./images/admin.jpg'))
            for i in db.keys():
                miembro = await ctx.guild.fetch_member(i)
                miembros.append(miembro)
            for i in miembros:
                if i.id == ctx.author.id:
                    await i.add_roles(admin_role)
                    await i.remove_roles(firmes_role)
                else:
                    await i.add_roles(firmes_role)
                    await i.remove_roles(admin_role)
        else:
            await ctx.send('Pero no tiene los recursos suficientes, buen intento.')


def setup(bot):
    bot.add_cog(Economia(bot))
