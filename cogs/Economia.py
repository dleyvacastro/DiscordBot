import discord
import asyncio
import random
from discord.ext import commands, tasks
from discord.utils import get
import sqlite3
from sqlite3 import Error
from sql import *

"""
db = Database('https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjM3NDc4MjksImlhdCI6MTYyMzYzNjIyOSwiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiI3OGI3YzQxMC0zNGM3LTQxNzAtYmRkNS03ZDcxMzNhODU5NTkifQ.EnZKvlY1FDuvLonmMdUFHvj8jPlfzNmTmX-WUdEs3cHpvpdpklPkytGrF8GaVQ0xfsx7HkiJGIPQQTsEflzUlA')
"""

class db:
    def __init__(self):
        self.con = sqlite3.connect('dorian2.db')
        self.cursor = self.con.cursor()

        self.rtypes = {'mute': 150, 'general':100}

    def insert_member(self, user):
        self.cursor.execute(sql_insert_user(user.id))
        self.con.commit()

    def close(self):
        self.con.close()

    def get_user_money(self, user):
        self.cursor.execute(sql_user_money(user.id))
        rows = self.cursor.fetchall()
        #print(rows[0][0])
        return rows[0][0]
    
    def get_members_money(self):
        self.cursor.execute(sql_members_money())
        rows = self.cursor.fetchall()
        return rows

    def set_money(self, user, value):
        #print(user.id)
        self.cursor.execute(sql_set_money(user.id, value))
        self.con.commit()

    def compute_money(self, user, amount : int):
        value = self.get_user_money(user) + int(amount)
        self.set_money(user, value)

    def reset_economy(self):
        self.cursor.execute(sql_reset_economy())
        self.con.commit()

    def cobro(self, user, precio):
        v = self.get_user_money(user)
        if v > precio:
            self.compute_money(user, -precio)
            self.con.commit()
            return True
        return False

    def get_multa(self, user, rtype):
        self.cursor.execute(sql_get_multa(user.id, rtype))
        rows = self.cursor.fetchall()
        #print(rows)
        return rows[0][0]

    def get_multas(self, user):
        self.cursor.execute(sql_get_multas(user.id))
        rows= self.cursor.fetchall()
        #print(rows)
        return rows[0][2], rows[0][3]

    def get_reports(self, user, rtype):
        self.cursor.execute(sql_get_reports(user, rtype))
        rows = self.cursor.fetchall()
        return int(rows[0][0])

    def generate_report(self, user, rtype):
        if rtype not in self.rtypes:
            print('unknown type')
            return
        self.cursor.execute(sql_generate_report(user.id, rtype))
        self.cursor.execute(sql_get_last_report_id(user.id))
        rid = self.cursor.fetchall()[0][0]
        print(f"su reporte se identifica #{rid}")
        self.con.commit()
        return rid
    
    def remove_report(self, user, rid):
        self.cursor.execute(sql_remove_report(rid))
        self.con.commit()

    def pay(self, user, rtype):
        if rtype not in self.rtypes:
            print('unknown type')
            return
        elif self.get_multa(user, rtype) == 0:
            print('no hay multas de ese tipo')
        elif self.cobro(user, self.rtypes[rtype]):
            self.cursor.execute(sql_pay_multa(user.id, rtype))
            self.con.commit()
            print('multa pagada')
            return True
        return False
        

class Economia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = db()
        self.miembros = []

        self.miembros_id = ['394982506417487872', '393592731420721154', '318611546383319041',
                            '396305256377614337', '704883078291521537', '528019938196324372']
        # precios

        self.precios = {'chnick_p': 100, 'censura_p': 10, 'tts_p': 5, 'golpe_de_estado_p': 6402, 'mute_p': 20}
        """
        self.chnick_p = 100
        self.censura_p = 10  # por mensaje
        self.tts_p = 5
        self.golpe_de_estado_p = 6402
        self.mute_p = 20
        """

    @ commands.Cog.listener('on_ready')
    async def get_member(self):
        guild = self.bot.get_guild(393593323463376899)
        for i in self.miembros_id:
            miembro = await guild.fetch_member(i)
            self.miembros.append(miembro)

    @commands.command()
    async def money(self, ctx):
        await ctx.reply(f'Maldito asalariado, usted tiene {self.db.get_user_money(ctx.author)} Diomede$')

    @commands.command()
    async def Money(self, ctx):
        embed = discord.Embed(
            title = 'Diomede$ en el server',
            description = 'la economia actualmente se encuentra: ',
            colour = discord.Colour.green()
        )

        money = self.db.get_members_money()

        for i in money:
            try:
                user = await ctx.guild.fetch_member(i[0])
                print(user)
            except:
                pass
            embed.add_field(name = f'{user.nick}: {i[1]} Diomede$', value = '** **', inline = 0)     

        await ctx.send(embed = embed)

    @commands.command()
    async def compute_money(self, ctx, member: commands.MemberConverter, amount):
        self.db.compute_money(member, amount)
        await ctx.send(f'{member.mention} se le ha computado {amount} Diomede$ a su cuenta.')
    
    @commands.command()
    async def set_money(self, ctx, member: commands.MemberConverter, amount):
        self.db.set_money(member, amount)
        await ctx.send(f'{member.mention} ahora ud tiene {amount} Diomede$.')

    @commands.Cog.listener('on_voice_state_update')
    async def voice_generation(self, member, before, after):
        cont = 0
        afk = member.guild.afk_channel
        
        while before.channel is None and after.channel is not None:
            if member.voice.channel == afk:
                return
            await asyncio.sleep(60)
            cont += 1
        else:
            self.db.compute_money(member, cont)

    @commands.command()
    async def report(self, ctx, member : commands.MemberConverter, rtype):
        rid = self.db.generate_report(member, rtype)
        nrep = self.db.get_reports(member, rtype)%3
        print(nrep)

        await ctx.send(f"{member.mention} se le ha movido al canal AFK dado que no se ha muteado al irse. su reporte se identifica #{rid}. Advertencia: {nrep+1}/3")
        afk = ctx.guild.afk_channel
        await member.move_to(afk)
        
        #if nrep != 0:
            #return
        
        while 1:
            user = await self.bot.wait_for('voice_state_update')
            if user[0] == member:
                break

        await ctx.send(f'{member.mention} ha despertado de su bulloso letargo.')

        if nrep != 2:
            print('end')
            return
        
        print('multa')
        soy_bulloso_role = get(ctx.guild.roles, id=820088027388706867)
        time_cont = 0
        await member.add_roles(soy_bulloso_role)
                
        await ctx.send(f'MALPARIDO BULLOSO. \n{soy_bulloso_role.mention} por 10 minutos {member.mention}. Puede quitar la sancion pagando.')
        while time_cont < 60*10:
            time_cont += 1
            try:
                user2 = await self.bot.wait_for('paid_mute', timeout = 1)
                print(user)
            except:
                pass
                user2 = False
            if user2:
                break
        await member.remove_roles(soy_bulloso_role)
        await ctx.send('multa pagada')
    
    @commands.command()
    async def pay(self, ctx, rtype):
        if self.db.pay(ctx.author, rtype):
            if rtype == 'mute':
                self.bot.dispatch("paid_mute", ctx.author)

    @commands.command()
    async def multas(self, ctx, rtype = ''):
        embed = discord.Embed(
            title = 'Criminal buscado',
            description = f'Se le acusa al señor {ctx.author.mention} de:',
            colour = discord.Colour.dark_blue()
        )
        if rtype == '':
            mute, general = self.db.get_multas(ctx.author)
            embed.add_field(name = f'**Mute: {mute} multas**', value = f'** **', inline = False)
            embed.add_field(name = f'**General: {general} multas**', value = f'** **', inline = False)
        else:
            embed.add_field(name = f'{rtype}: {self.db.get_multa(ctx.author, rtype)}', value = '** **')
        
        await ctx.send(embed = embed)

    @commands.command(pass_context=True)
    async def chnick(self, ctx, member: commands.MemberConverter, *, nick):
        if self.db.cobro(ctx.author, self.precios['chnick_p']):
            await member.edit(nick=nick)
            await ctx.send(f'{ctx.author.mention} ha redimido un cambio de apodo para {member.nick}, ahora tienes {self.db.get_user_money(ctx.author)} Diomede$.')
            await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo.')
        else:
            await ctx.send(f'Trabaje vago pobre')

    async def clear(self, ctx, amount=1):
        #Alias: RCN, Caracol, Censura
        if self.db.cobro(ctx.author, self.precios['censura_p']*(amount)):
            await ctx.channel.purge(limit=amount+1)
            if amount > 10:
                await ctx.send(f'Premio Juan Pablo Bieri al Censurador del año, ¿Usted mató a Jaime Garzon o q? {ctx.author.mention}')
            await ctx.send(f'alguien ha censurado usando {self.censura_p *(amount)} Diomede$. Ahora te quedan {self.db.get_user_money(ctx.author)}.')
            # await ctx.author.edit(nick="Dr. MinTIC")
        else:
            await ctx.send('Trabaje vago mamamerto.')
        
    @ commands.command()
    async def tts(self, ctx, *, message):
        if self.db.cobro(ctx.author, self.precios['tts_p']):
            await ctx.send(ctx.author.mention)
            await ctx.send(message, tts=1)
        else:
            await ctx.send('Ni pa un hpta tts tiene mucho pobre.')

    @ commands.command()
    async def chito(self, ctx, member: commands.MemberConverter, minutes=0):
        if minutes == 0 and self.db.cobro(ctx.author, self.precios['mute_p']):
            await ctx.send(f'{member.mention} CALLESE MALPARIDO')
            await member.edit(mute=True)
            await asyncio.sleep(5)
            await member.edit(mute=False)
            return
        if self.db.cobro(ctx.author, self.precios['mute_p'] + 50*minutes):
            costo = self.precios['mute_p'] + 50*minutes
            await ctx.send(f'Parce {member.mention} ud tiene que ser muy fastidioso para que {ctx.author.mention} gastara {costo} diomede$ para callarlo')
            await ctx.send(f'{member.mention} CALLESE MALPARIDO. Cierre la jeta por {minutes} minutos.')
            await member.edit(mute=True)
            await asyncio.sleep(minutes*60)
            await member.edit(mute=False)
        else:
            await ctx.send('Trabaje vago mamerto')


    # Precios
    @ commands.command()
    async def precio(self, ctx):
        embed = discord.Embed(
            title='Guia económica',
            description='Aca encontrara todas las acciones disponibles hasta el momento con su respectivo valor en Diomede$',
            colour=discord.Colour.random()
        )
        embed.add_field(
            name=f'tts. Costo: {self.precios["tts_p"]} Diomede$', value='Envia un mensaje tts', inline=False)
        embed.add_field(name=f'chnick. Costo: {self.precios["chnick_p"]} Diomede$',
                        value='Comando para forzar el cambio de apodo de un miembro especifico.', inline=False)
        embed.add_field(name=f'cesura. Costo: {self.precios["censura_p"]} Diomede$ por cada mensaje.',
                        value='Borra los n mensajes anteriores, si no se especifica n solo borra 1.', inline=False)
        embed.add_field(
            name=f'golpe_de_estado. Costro: {self.precios["golpe_de_estado_p"]} Diomede$.', value='Tomas el poder por la fuerza.', inline=False)
        embed.add_field(name=f'chito. Costo: {self.precios["mute_p"]} Diomede$ + 50 por minuto.',
                        value=f'Mutea a alguien durante n minutos, si n no se especifica, el efecto durara 5 segs', inline=False)
        await ctx.send(embed=embed)


"""
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
        #Alias: RCN, Caracol, Censura
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
"""

def setup(bot):
    bot.add_cog(Economia(bot))
