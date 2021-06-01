import os
import discord
import random
import frases
from discord.ext import commands
# from replit import db
# import request
# import json

client = discord.Client()
commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('Loggining on {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith('$Hoy denuevo te voy a veer'):
        await message.channel.send('Monda pa tu jopo mkon')
    
    if msg.startswith('$frase'):
        await message.channel.send(frases.index[random.randint(0,len(frases.index)-1)])
    
    if msg.startswith('$apodo'):
        data = msg.split(" ")
        if len(data) != 3:
            await message.channel.send('Parametros incompletos')
            return
        
        if len(data[1]) == 0:
            await message.channel.send('Parametros incorrectos')
            return

        ans = """
        
        Solicitud de {0}
        **CAMBIO DE APODO PARA** {1} -> {2}
        1. APRUEBA
        2. NO APRUEBA
        """.format(message.author.mention, data[1], data[2])
        await message.channel.send(ans)
        member = message.author
        await member.edit(nick=data[2])

@client.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

client.run(os.environ['TOKEN'])
