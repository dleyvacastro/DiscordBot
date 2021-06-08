import discord
from discord.ext import commands
from discord.utils import get

class Senado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Senadores_id = ['394982506417487872','393592731420721154','318611546383319041','396305256377614337','704883078291521537','528019938196324372']
        self.propuestas_dict = {}
        self.Senadores = []
        self.cerrar_votacion = False

    @commands.command()
    async def senado(self, ctx):
        firmes_role = get(ctx.guild.roles, id = 685974684134801457)
        senador_role = get(ctx.guild.roles, id = 850899217161388073)

        for i in self.Senadores_id:
            senador = await ctx.guild.fetch_member(i)
            self.Senadores.append(senador)

        for senador in self.Senadores:
            await senador.add_roles(senador_role)
        
        channel = self.bot.get_channel(850901257320923147)
        propuestas = self.bot.get_channel(850915389638836245)

        await channel.send(f'Entonces es así, {ctx.author.mention} ha convocado al honorable Senado Galáctico.')
        await channel.send('¿Qué será ahora?, ¿Golpe de estado?')
        await channel.send(f'Les deseo mucha suerte {senador_role.mention}, que gane el mejor mentiroso.')
        await channel.send('En caso de elección. \nAspirantes a candidatos por favor escriban `$candidato`.')
        await channel.send(f'Querido candidato, use el canal {propuestas.mention} para escribir sus propuestas, una vez haya terminado utilice en este canal el comando `$propuestas` para que sean publicadas. Tenga en cuenta que si desea revisarlas antes puede enviar un mensaje privado a {self.bot.user.mention} con el mismo comando')
        await channel.send(f'Comando `$votacion` para realizar las elecciones. Al ganador se le dara el rango corresponiente, mientras que a los demas se les designara el rol {firmes_role.mention}.')
    @commands.command()
    async def candidato(self, ctx, member : commands.MemberConverter = None):
        if member == None:
            member = ctx.author
        if member in self.propuestas_dict.keys():
            await ctx.send('Se va apostular 2 veces o que?')
            return
        self.propuestas_dict[member] = []
        await ctx.send(f'{member.mention} se ha postulado.')

    @commands.Cog.listener('on_message')
    async def propuestas_listener(self, ctx):
        propuestas = self.bot.get_channel(850915389638836245)
        # print(ctx.author not in self.propuestas_dict.keys())
        if ctx.author == self.bot.user:
            return
        
        if ctx.channel != propuestas:
            return

        if ctx.author not in self.propuestas_dict.keys():
            await ctx.reply('Si esta tan creativo, postulese.')
            return
        self.propuestas_dict[ctx.author].append(ctx.content)
        # print(self.propuestas_dict)

        await ctx.delete()

    @commands.command()
    async def propuestas(self, ctx):
        p = self.propuestas_dict[ctx.author]
        embed = discord.Embed(
            title = f'Propuestas de {ctx.author.name}',
           description = f'El candidato {ctx.author.mention} se compromete, bajo gravedad de juramento a cumplir los siguientes postulados:',
           colour = discord.Colour.random()
        )
        embed.set_image(url = 'https://previews.123rf.com/images/tuk69tuk/tuk69tuk1704/tuk69tuk170400032/75104100-minimalist-style-vector-business-finance-concept-businessman-choosing-worker-from-group-of-businessp.jpg')
        embed.set_thumbnail(url = ctx.author.avatar_url)
        embed.set_author(name = str(ctx.author).split('#')[0], icon_url = ctx.author.avatar_url)
        for i in range(len(p)):
            embed.add_field(name = f'Propuesta #{i+1}', value = p[i], inline = False)
        
        await ctx.send(embed = embed)

    @commands.command()
    async def votacion(self, ctx):
        senador_role = get(ctx.guild.roles, id = 850899217161388073)
        admin_role = get(ctx.guild.roles, id = 685973595423375388)
        firmes_role = get(ctx.guild.roles, id = 685974684134801457)
        anuncio = self.bot.get_channel(839554918561611837)
        p = list(self.propuestas_dict.keys())
        reacted = {}
        r = {}
        result ={}
        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']

        embed = discord.Embed(
            title = f'Votación para nuevo admin',
            description = 'A las puertas de tener un nuevo titere los candidatos son:',
            colour = discord.Colour.random()
        )

        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_image(url = 'https://bogota.gov.co/sites/default/files/styles/1050px/public/2021-04/votacion-cuarentena-.png')
        
        for i in range(len(p)):
            r[reactions[i]] = p[i]
            embed.add_field(name = f'{reactions[i]} {p[i].name}',value = "** **",inline = False)
        
        v = await ctx.send(embed = embed)

        for i in range(len(p)):
            await v.add_reaction(reactions[i])

        while not self.cerrar_votacion:
            reaction, user = await self.bot.wait_for('reaction_add')
            # print(reaction.count)
            if user not in reacted.keys():
                reacted[user] = reaction
            result[r[reaction.emoji]] = reaction.count
            # a = list(reacted.values())
            # print(a[0].emoji == reactions[0])
            if len(reacted) > 4:
                print('desicion')
                break
        else:
            print('forced')
        winner = max(result, key = result.get)
        # print(type(winner))

        await anuncio.send(f'El nuevo admin es: {winner.mention}')
        await anuncio.send(file = discord.File('./images/admin.jpg'))
        await winner.add_roles(admin_role)

        for i in self.Senadores_id:
            senador = await ctx.guild.fetch_member(i)
            self.Senadores.append(senador)

        # print(self.Senadores)
        self.Senadores.remove(winner)
        for i in self.Senadores:
            await i.remove_roles(admin_role)
            await i.remove_roles(senador_role)
            await i.add_roles(firmes_role)
        

    @commands.command()
    async def cerrar_votacion(self,ctx):
        self.cerrar_votacion = True
    
    #@commands.command()
    #async def k(self, ctx):
    #    a = await ctx.guild.fetch_member('393592731420721154')
    #    gargola = get(ctx.guild.roles, id = 685973595423375388)
    #    await a.add_roles(gargola)

def setup(bot):
    bot.add_cog(Senado(bot))