import discord
from discord.ext import commands
from discord.utils import get
import os
import random
import asyncio
# from keep_alive import keep_alive
from Anexos import *

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Y quien monda es Dorian?'))
    print('Loggining on {0.user}'.format(bot))


@bot.event
async def on_member_join(member):
    public = 'welcome, {0.mention}:'.format(member)
    await member.guild.system_channel.send(public)


@bot.listen('on_message')
async def whatever_you_want_to_call_it(message):
    # do stuff here
    # do not process commands here
    if message.author == bot.user:
        return

    firmes = bot.get_channel(722869247675596911)
    if message.channel.id == 849770114991783966:
        # print(message.content)
        if message.content.startswith('tts'):
            # print("1")
            await firmes.send(random.choice(resp(message.author, message.content.replace('tts', ''))), tts=True)
        else:
            await firmes.send(random.choice(resp(message.author, message.content)))

        await message.delete()
        await bot.process_commands(message)

"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Escriba bien el comando maldito impedido')
    if isinstance(error, commands.CommandNotFound):
        # await ctx.send('¿De que me hablas viejo?')
        await ctx.send(file=discord.File('./images/de_que_me_hablas.jpg'))
"""

@bot.command()
@commands.has_role(849454598296830023)
async def force_load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    await ctx.send('✅Las extenciones han sido recargadas✅')


@bot.command()
@commands.has_role(849454598296830023)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.has_role(849454598296830023)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
@commands.has_role(849454598296830023)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'✅ Modulo {extension} Recargado')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#keep_alive()
bot.run(os.environ['TOKEN'])
