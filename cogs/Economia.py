import discord
import asyncio
import random
from discord.ext import commands, tasks
from discord.utils import get
from replit import Database

db = Database('https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjM3NDc4MjksImlhdCI6MTYyMzYzNjIyOSwiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiI3OGI3YzQxMC0zNGM3LTQxNzAtYmRkNS03ZDcxMzNhODU5NTkifQ.EnZKvlY1FDuvLonmMdUFHvj8jPlfzNmTmX-WUdEs3cHpvpdpklPkytGrF8GaVQ0xfsx7HkiJGIPQQTsEflzUlA')


class Economia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.miembros = []

        self.miembros_id = ['394982506417487872', '393592731420721154', '318611546383319041',
                            '396305256377614337', '704883078291521537', '528019938196324372']
        # precios

        self.chnick_p = 100
        self.censura_p = 10  # por mensaje
        self.tts_p = 5
        self.golpe_de_estado_p = 6402
        self.mute_p = 20

    @ commands.Cog.listener('on_ready')
    async def get_member(self):
        guild = self.bot.get_guild(393593323463376899)
        for i in self.miembros_id:
            miembro = await guild.fetch_member(i)
            self.miembros.append(miembro)

    def get_user_money(self, user):
        v = int(db[f'{user.id}'])
        return v

    def cobro(self, author, precio):
        v = self.get_user_money(author)
        if v > precio:
            db[f'{author.id}'] = v - precio
            return True
        return False

    def chm(self, member, amount):
        v = db[f'{member.id}']
        if v < amount:
            return False
        db[f'{member.id}'] = f'{int(db[f"{member.id}"])+amount}'
        return True

    @ commands.command()
    @ commands.has_role(849454598296830023)
    async def reset_economy(self, ctx, message):
        if message == 'CONFIRMAR':
            for i in self.miembros_id:
                db[f"{i}"] = 0
            await ctx.send('Las cuentas de todos los miembros ahora son 0')
        else:
            await ctx.send('Por favor confime la orden.')

    @ commands.command()
    async def money(self, ctx, member: commands.MemberConverter = None):
        if member == None:
            member = ctx.author
        await ctx.reply(f'Maldito asalariado usted tiene: {self.get_user_money(member)} Dorian Coins.')

    @ commands.command()
    @ commands.has_role(849454598296830023)
    async def add_money(self, ctx, member: commands.MemberConverter = None, amount=1):
        if member == None:
            member = ctx.author
        id = str(member.id)
        db[id] = f'{int(db[id])+amount}'
        await ctx.reply(f'Maldito asalariado, se le ha depositado {amount}$ en su cuenta, ahora usted tiene: {self.get_user_money(ctx.author)} Dorian Coins.')

    @ commands.command()
    @ commands.has_role(849454598296830023)
    async def rest_money(self, ctx, member: commands.MemberConverter = None, amount=1):
        if member == None:
            member = ctx.author
        id = str(member.id)
        db[id] = f'{int(db[id])-amount}'
        await ctx.reply(f'Maldito asalariado, se le ha retirado {amount}$ de su cuenta, ahora usted tiene: {self.get_user_money(member)} Dorian Coins.')

    @ commands.command()
    async def send(self, ctx, member: commands.MemberConverter, amount: int = 1):
        id = str(member.id)
        a_id = str(ctx.author.id)
        if int(db[a_id]) < amount:
            await ctx.reply('Hoy no se fia, mañana si.')
            return
        db[a_id] = f'{int(db[a_id])-amount}'
        db[id] = f'{int(db[id])+amount}'
        await ctx.reply(f'Transfrencia exitosa. Se han enviado {amount}$ a {member.mention}.')

    # Precios
    @ commands.command()
    async def precios(self, ctx):
        embed = discord.Embed(
            title='Guia económica',
            description='Aca encontrara todas las acciones disponibles hasta el momento con su respectivo valor en Diomede$',
            colour=discord.Colour.random()
        )
        embed.add_field(
            name=f'tts. Costo: {self.tts_p} Diomede$', value='Envia un mensaje tts', inline=False)
        embed.add_field(name=f'chnick. Costo: {self.chnick_p} Diomede$',
                        value='Comando para forzar el cambio de apodo de un miembro especifico.', inline=False)
        embed.add_field(name=f'cesura. Costo: {self.censura_p} Diomede$ por cada mensaje.',
                        value='Borra los n mensajes anteriores, si no se especifica n solo borra 1.', inline=False)
        embed.add_field(
            name=f'golpe_de_estado. Costro: {self.golpe_de_estado_p} Diomede$.', value='Tomas el poder por la fuerza.', inline=False)
        embed.add_field(name=f'chito. Costo: {self.mute_p} Diomede$ + 50 por minuto.',
                        value=f'Mutea a alguien durante n minutos, si n no se especifica, el efecto durara 5 segs', inline=False)
        await ctx.send(embed=embed)

    # Generacion de Diomede$

    @ commands.Cog.listener('on_voice_state_update')
    async def voice_generation(self, member, before, after):
        pruebas_c = self.bot.get_channel(840258678334554122)
        cont = 0
        while before.channel is None and after.channel is not None:
            await asyncio.sleep(60)
            cont += 1
        else:
            db[f'{member.id}'] = int(db[f'{member.id}']) + cont

    @commands.command()
    async def report(self, ctx, rtype, member: commands.MemberConverter):
        soy_bulloso_role = get(ctx.guild.roles, id=820088027388706867)
        if f'rm{member.id}' not in db.keys():
            db[f'rm{member.id}'] = str(0)
        if rtype == 'mute':
            afk = ctx.guild.afk_channel
            await member.move_to(afk)
            db[f'rm{member.id}'] = f'{int(db[f"rm{member.id}"])+1}'
            nrep = db[f'rm{member.id}']
            await ctx.send(f'{member.mention} reportado por bulloso. {nrep}/3')

            if int(nrep) >= 3:
                time_cont = 0
                await member.add_roles(soy_bulloso_role)
                db[f'rm{member.id}'] = str(0)
                await ctx.send(f'MALPARIDO BULLOSO. \n{soy_bulloso_role.mention} hasta que pague {member.mention}.')
                while time_cont < 300:
                    time_cont += 1
                    await asyncio.sleep(1)
                await member.remove_roles(soy_bulloso_role)

    # Comandos compras

    @ commands.command(pass_context=True)
    async def chnick(self, ctx, member: commands.MemberConverter, *, nick):
        if self.cobro(ctx.author, self.chnick_p):
            await member.edit(nick=nick)
            await ctx.send(f'{ctx.author.mention} ha redimido un cambio de apodo para {member.nick} por {self.chnick_p}, ahora tienes {db[str(ctx.author.id)]}.')
            await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo.')
        else:
            await ctx.send(f'Trabaje vago pobre')

    @ commands.command(aliases=['RCN', 'Caracol', 'censura'])
    async def clear(self, ctx, amount=1):
        """
        Alias: RCN, Caracol, Censura
        """
        if self.cobro(ctx.author, self.censura_p*(amount)):
            await ctx.channel.purge(limit=amount+1)
            if amount > 10:
                await ctx.send(f'Premio Juan Pablo Bieri al Censurador del año, ¿Usted mató a Jaime Garzon o q? {ctx.author.mention}')
            await ctx.send(f'alguien ha censurado usando {self.censura_p *(amount)} Diomede$. Ahora te quedan {self.get_user_money(ctx.author)}.')
            # await ctx.author.edit(nick="Dr. MinTIC")
        else:
            await ctx.send('Trabaje vago mamamerto.')

    @ commands.command()
    async def tts(self, ctx, *, message):
        if self.cobro(ctx.author, self.tts_p):
            await ctx.send(ctx.author.mention)
            await ctx.send(message, tts=1)
            await ctx.message.delete()
        else:
            await ctx.send('Trabaje vago mamerto')

    @ commands.command()
    async def chito(self, ctx, member: commands.MemberConverter, minutes=0):
        if minutes == 0 and self.cobro(ctx.author, self.mute_p):
            await member.edit(mute=True)
            await asyncio.sleep(5)
            await member.edit(mute=False)
            return
        if self.cobro(ctx.author, self.mute_p + 50*minutes):
            await member.edit(mute=True)
            await asyncio.sleep(minutes*60)
            await member.edit(mute=False)
        else:
            await ctx.send('Trabaje vago mamerto')

    @ commands.command()
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
