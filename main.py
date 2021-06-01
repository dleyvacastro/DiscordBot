import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='$')




@bot.event
async def on_ready():
    print('Loggining on {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    public = 'welcome, {0.mention}:'.format(member)
    await member.guild.system_channel.send(public)


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong :sunglasses: {(bot.latency) * 1000} ms')


@bot.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Ahora seras conocido como: {member.mention} mamahuevo')

@bot.command(pass_context=True)
async def apodo(ctx, member: discord.Member, nick):
    reactions = ["🟢", "🔴"]
    ans = """
        Solicitud de {0}
        **CAMBIO DE APODO PARA** {1} -> {2}
        APRUEBA         :white_check_mark:   
        
        NO APRUEBA  :no_entry:
        """.format(ctx.message.author.name, member, nick)
    m = await ctx.send(ans)
    for name in reactions:
        emoji = get(ctx.guild.emojis, name=name)
        await m.add_reaction(emoji or name)
    await asyncio.sleep(10)
    most_voted = max(m.reactions, key=lambda r: r.count)
    await m.channel.send(f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")
    
@bot.command(pass_context=True)
async def test(ctx):
    m = await ctx.send("test")
    await asyncio.sleep(10)
    print (m.reactions)

@bot.command()
async def cricko(ctx):
    await ctx.send('Es igual pero mas crico')


keep_alive()
bot.run(os.environ['TOKEN'])
