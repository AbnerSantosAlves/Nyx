import discord
from sqlalchemy.exc import SQLAlchemyError
from discord.ext import commands, tasks
from discord import Color
from discord import app_commands
from discord.ext.commands import CommandOnCooldown
from datetime import timedelta 
import asyncio
import random
from decimal import Decimal
import requests
import aiohttp
import time, os
from cogs.database import *



cor_atual = "000000"
cor_int = int(cor_atual, 16)

class geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def comandos(self, ctx:commands.Context):
        emoji = "<a:CH_IconLoadingBlurple:1313891027320438835>"
        file = discord.File(r"C:\Users\Abner\Desktop\Private - Abner\Programação\Nyx\imagens\icc2.gif", filename="icc2.gif")

        help = discord.Embed(title="<:dev_azul:1313910637310513214> Todos os comandos", description="*all Nyx commands*", color=Color(cor_int))
        help.add_field(name=f"⠀\n{emoji} *__Uso geral:__*", value="> - `N'roll (número)`\n > - `N'coinflip`\n > - `N'server`\n > - `N'choose (frase, frase, frase)`\n", inline=False)
        help.add_field(name=f"⠀\n{emoji} *__Admin:__*", value="> - `N'criar_enquete`\n > - `N'clear {número de mensagens}`\n > - `N'ban (membro) (motivo)`\n  > - `N'kick (membro)`\n", inline=False)
        help.set_thumbnail(url="attachment://icc2.gif")
        help.set_footer(text="Desenvolvido unicamente por Rodion")
        await ctx.send(embed=help, file=file)

    #comando de número aleatório
    @commands.command()
    async def roll(self, ctx:commands.Context, dados:str):
        if "d" in dados:
            nr_dados, nr_rolagem = dados.split("d")
            nr_dados = int(nr_dados)
            nr_rolagem = int(nr_rolagem)
        else:
            nr_dados = 1
            nr_rolagem = int(dados)
             
        resultados = [random.randint(1, nr_rolagem) for _ in range(nr_dados)]
        resultado_formatado = " + ".join(str(r) for r in resultados)
        total = sum(resultados)

        if len(resultado_formatado) > 2000:
           await ctx.send(f"<:game_die:1313971447873404968> | Rolando {nr_dados}d{nr_rolagem}... Você tirou: {total}\n`Muitos dados -> {total}`")
           return
        
        if nr_dados == 1:
            await ctx.send(f"<:game_die:1313971447873404968> | Rolando {nr_dados}d{nr_rolagem}... Você tirou: {total}")
        else:
            await ctx.send(f"<:game_die:1313971447873404968> | Rolando {nr_dados}d{nr_rolagem}... Você tirou: {total}\n`{resultado_formatado} -> {total}`")

        
    #Comando de cara ou coroa
    @commands.command()
    async def coinflip(self, ctx:commands.Context):
        coinflip = ['Cara', 'Coroa']
        resultado = random.choice(coinflip)
        await ctx.send(resultado)
    
    #Comandos do discord com /

    @app_commands.command(name="saldo", description="Veja o seu saldo no bot.")
    async def saldo(self, interaction: discord.Integration):
        moedas = await ver_saldo(interaction.user)
        await interaction.response.send_messagem(f"Você tem {moedas} moedas")

    @app_commands.command()
    @app_commands.choices(cor=[
     app_commands.Choice(name='Vermelho', value='BA2D0B'),
     app_commands.Choice(name='Azul', value='22577A'),
     app_commands.Choice(name='Amarelo', value='FFC145')
])
    async def cor(self, interact:discord.Integration, cor:app_commands.Choice[str]):
        await interact.response.send_message(f'O código hexadecimal da cor {cor.name} é {cor.value}')



    #informações gerais do servidor
    @commands.command()
    async def server(self, ctx:commands.context):
        server = ctx.guild 
        nome = server.name
        dono = server.owner 
        data = server.created_at
        total_text_channels = len(ctx.guild.text_channels)
        total_voice_channels = len(ctx.guild.voice_channels)
        total_channels = len(ctx.guild.channels)
        max_membros = server.member_count
        boosts = ctx.guild.premium_subscription_count
        embed = discord.Embed(
        title=f"{nome}", 
        description="*<:z_mod_DiscordShield:1338558678751772815> Acompanha todas as informações gerais do servidor.*\n",
                    #  "**`ID:`**ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ**`Dono:`**\n"
                    #  f"{ctx.guild.id}ㅤㅤㅤ{server.owner.display_name}\n\n"
                    #  "**`Criação:`**ㅤㅤㅤㅤㅤㅤㅤㅤ**`Membros:`**\n"
                    #  f"{server.created_at.strftime("%d/%m/%Y")}ㅤㅤㅤㅤㅤㅤㅤ{max_membros}\n"
                    #  f"{server.created_at.strftime("%H:%M:%S")}\n\n"
                    #  "**`Boosts:`**ㅤㅤㅤㅤㅤㅤㅤㅤㅤ**`Guias:`**\n"
                    #  f"{boosts} ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤChats de texto:{total_text_channels}\n"
                    #  f"ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤChats de voz:{total_voice_channels}\n"
                    #  f"ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤChats de voz:{total_channels}\n", 
        color=discord.Color.blue())

    
        # Adicionando campos no embed
        embed.add_field(name="⠀\n``Id:``", value=f"{ctx.guild.id}ㅤㅤㅤ", inline=True)
        embed.add_field(name="``Dono:``", value=f"{server.owner.display_name}ㅤㅤㅤ", inline=True)
        data_criacao = server.created_at.strftime('%d/%m/%Y\n%H:%M:%S')
        embed.add_field(name="``Data de criação``", value=data_criacao, inline=True)
        embed.add_field(name="``Número de membros``", value=f"{max_membros}", inline=True)
        embed.add_field(name="``Boosts:``", value=f"{boosts} impulsos", inline=True)
        embed.add_field(name="``Guias:``", value=f"Chats de texto: {total_text_channels}\nChats de voz: {total_voice_channels}\nTotal: {total_channels}\n")
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_image(url=ctx.guild.banner.url if ctx.guild.banner else None)
        await ctx.send(ctx.author.mention, embed=embed)

    #Comando de escolhas.
    @commands.command()
    async def choose(self, ctx:commands.context, *, textos):
        lista_textos = textos.split(',')
        escolha = random.choice(lista_textos)
        await ctx.send(escolha)

    @commands.command(aliases=['bal'])
    async def saldo(self, ctx: commands.Context, membro: discord.Member = None):
        membro = membro or ctx.author  # Padrão: o usuário que executou o comando
        id_user = membro.id
        emoji = "<:wizard_money:1325526117536239677>"

        try:
            if membro == ctx.author:
                qt_moedas = ver_saldo(id_user)
                moedas = formatar_moeda(qt_moedas)
                posicao = obter_posicao_usuario(id_user)
                await ctx.reply(f"{emoji} | Você possui **{moedas} Nyxies** e ocupa o **{posicao}ª lugar** no Ranking! Continue com essa garra e vamos dominar esse pódio juntos!")
            if membro != ctx.author:
                qt_moedas = ver_saldo(id_user)
                moedas = formatar_moeda(qt_moedas)
                posicao = obter_posicao_usuario(id_user)
                await ctx.reply(f"{emoji} | {membro.mention} tem **{moedas} Nxies** e está em {posicao}º no Ranking.")
        except SQLAlchemyError as e:
            await ctx.send("Ocorreu um erro ao acessar o banco de dados.")
            print(f"Erro no banco: {e}")  # Para fins de depuração

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx:commands.Context):
            qt_aleatoria = random.randint(1000, 10000)
            id_user = ctx.author.id
            add_saldo(id_user, qt_aleatoria)
            moedas = ver_saldo(id_user)
            daily = formatar_moeda(qt_aleatoria)
            posicao = obter_posicao_usuario(id_user)
            emoji = "<:emoji_105:1325547101291020449>"

            moedas_formatadas = formatar_moeda(moedas)
            await ctx.reply(f"{emoji} | Parábens, você acabou de ganhar **{daily} Nyxies**, seu saldo agora é **{moedas_formatadas} Nyxies** e você se encontra em **{posicao}º no Ranking.**")

    @daily.error
    async def daily_error(self, ctx: commands.Context, error: Exception):
        """Tratamento de erros do comando daily"""
        if isinstance(error, CommandOnCooldown):
            # Calcula o tempo restante para o cooldown
            remaining_time = round(error.retry_after)
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60

            # Envia uma mensagem informando o tempo restante
            await ctx.send(
                f"{ctx.author.mention}, você precisa esperar **{hours}h {minutes}m {seconds}s** "
                f"para usar o comando novamente. ⏳"
            )

    @commands.command()
    async def apostar(self, ctx: commands.Context, membro: discord.Member, quantidade):
        id_membro = membro.id
        id_author = ctx.author.id
        quantidade = Decimal(quantidade)
        qt_format = formatar_moeda(quantidade)
    
        moedas_membro = ver_saldo(id_membro)
        moedas_author = ver_saldo(id_author)

        if membro.mention == ctx.author:
            await ctx.send("<:anime_xiao_rage:1326596304280883364> | Você não pode apostar consigo mesmo, seu bobão!")

        if moedas_membro < quantidade:
            await ctx.send("O concorrente não tem a quantidade de Nyxies requeridas.")
            return
        if moedas_author < quantidade:
            await ctx.send("Ué, você não tem todas essas Nyxies!")
            return
    
        # Mensagem para confirmar a aposta
        confirm_message = await ctx.send(
            f"<a:CH_IconLoadingGreen:1326595842311720961> | {membro.mention}, você acaba de ser desafiado para uma aposta no valor de {qt_format}.\n"
            "-# Reaja com ✅ para aceitar ou ❌ para recusar."
        )
    
        # Adicionando as reações
        await confirm_message.add_reaction("✅")
        await confirm_message.add_reaction("❌")
        
        reactions = {"user": False, "author": False}

        def check(reaction, user):  
            if user == membro and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id ==            confirm_message.id:
                reactions["user"] = True
            if user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirm_message.id:
                reactions["author"] = True
            return reactions["user"] and reactions["author"]

        try:
            # Espera pelas reações
            await self.bot.wait_for('reaction_add', timeout=120.0, check=check)

        # Verifica as reações finais para determinar o próximo passo
            if reactions["user"] and reactions["author"]:
                # Determinar vencedor
                competidores = [id_membro, id_author]
                ganhador = random.choice(competidores)

            if ganhador == id_membro:
                add_saldo(id_membro, quantidade)
                perda = quantidade * -1
                add_saldo(id_author, perda)
                qt = formatar_moeda(quantidade)
                await ctx.send(f"<a:kurama_money_animated:1326594977035456543> | O vencedor da aposta foi o {membro.mention} e ele acaba de levar para casa **{qt} Nyxies**!")
        
            elif ganhador == id_author:
                add_saldo(id_author, quantidade)
                perda = quantidade * -1
                add_saldo(id_membro, perda)
                qt = formatar_moeda(quantidade)
                await ctx.send(f"<a:kurama_money_animated:1326594977035456543> | O vencedor da aposta foi o {ctx.author.mention} e ele acaba de levar para casa **{qt} Nyxies**!")
            else:
                await ctx.send(f"A aposta foi recusada por {membro.mention} ou {ctx.author.mention}!")
        except asyncio.TimeoutError:
            await ctx.send(f"{membro.mention}, o tempo para responder à aposta expirou.", ephemeral=True)

    @commands.command(aliases=['transferir', 'pagar'])
    async def pay(self, ctx: commands.Context, membro: discord.Member, quantidade):
        id_membro = membro.id
        id_author = ctx.author.id
        quantidade = Decimal(quantidade)
    
        # Verificando o saldo de ambos os jogadores
        moedas_author = ver_saldo(id_author)
        if moedas_author < quantidade:
            await ctx.send("Você não tem Nyxies suficientes para realizar essa transferência.")
            return

    # Mensagem para confirmação da transferência
        confirm_message = await ctx.send(
        f"{membro.mention}, {ctx.author.mention} quer te transferir {quantidade} Nyxies.\n"
        "Reaja com ✅ para aceitar ou ❌ para recusar."
        )

        # Adicionando as reações
        await confirm_message.add_reaction("✅")
        await confirm_message.add_reaction("❌")

        # Função de verificação das reações
        def check(reaction, user):
            return str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirm_message.id and \
               (user == membro or user == ctx.author)

        try:
            accepted_reactions = 0

            while accepted_reactions < 2:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction.emoji) == "✅":
                    accepted_reactions += 1
                elif str(reaction.emoji) == "❌":
                    await ctx.send(f"A transferência foi recusada por {user.mention}.")
                    return

            # Se ambos reagiram com ✅
            add_saldo(id_author, -quantidade)
            add_saldo(id_membro, quantidade)
            qt = formatar_moeda(quantidade)
            await ctx.send(f"A transferência foi realizada! {ctx.author.mention} transferiu {qt} para {membro.mention}.")
        except asyncio.TimeoutError:
            await ctx.send(f"O tempo para responder à transferência expirou. Transferência cancelada.")




    @commands.command()
    async def rankingcosmo(self, ctx: commands.Context):    
        embed = discord.Embed(
            title="",
            description=(
                f"## Ranking\n"
                "O sistema de ranking do servidor é uma maneira de recompensar a participação ativa dos membros com benefícios exclusivos.\n\n"
                f"-# `Viajante (0 XP):` <@&1308617881038356510>\n"
                "<:cdw_b_dot01:1323737091586392065> Acesso básico ao servidor;\n"
                "<:cdw_b_dot01:1323737091586392065> Participação em eventos gerais;\n"
                "<:cdw_b_dot01:1323737091586392065> Emoji exclusivos do servidor;\n"
                "<:cdw_b_dot01:1323737091586392065> Capacidade de usar stickers personalizados.\n\n"
            
                f"-# `Explorador (5.000 XP):` <@&1333281196657872908>\n"
                "<:cdw_b_dot01:1323737091586392065> Tag personalizada (para até 3 pessoas);\n"
                "<:cdw_b_dot01:1323737091586392065> Pode enviar anexos em todos os canais.\n"
                "<:cdw_b_dot01:1323737091586392065> Pode escolher 1 emoji para o servidor;\n"
                "<:cdw_b_dot01:1323737091586392065> Imunidade nos sorteios.\n\n"

            
                f"-# `Astronauta (10.000 XP):` <@&1333281198319079534>\n"
                "<:cdw_b_dot01:1323737091586392065> Tag personalizada (para até 5 pessoas);\n"
                "<:cdw_b_dot01:1323737091586392065> Uma cor destacada das demais;\n"
                "<:cdw_b_dot01:1323737091586392065> Pode enviar anexos em todos os canais;\n"
                "<:cdw_b_dot01:1323737091586392065> Pode escolher 3 emojis para o servidor;\n"
                "<:cdw_b_dot01:1323737091586392065> Pode adicionar 3 figurinhas ao servidor;\n"
                "<:cdw_b_dot01:1323737091586392065> Pode criar tópicos privados/públicos;\n"
                "<:cdw_b_dot01:1323737091586392065> Voz prioritária nas call's.\n"
                "<:cdw_b_dot01:1323737091586392065> Imunidade nos sorteios.\n\n"
        ),
            color=cor_int
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def regrascosmos(self, ctx:commands.Context):
        file = discord.File(r"C:\Users\Abner\Desktop\Private - Abner\Programação\Nyx\imagens\banner - regras.png", filename="regras.png")
        embed = discord.Embed(
            title="",
            description=(
                "### <:Sv_RulesBook:1345456488558362634> Diretrizes da comunidade\n\n"

                "**``Respeito mútuo``**\n"
                "Este servidor preza por um ambiente saudável e respeitoso. Ofensas, discriminação, discursos de ódio ou qualquer forma de desrespeito não serão tolerados.\n\n"

                "**``Proibido Spam``**\n"
                "Para manter o ambiente organizado, evite mensagens repetitivas, links irrelevantes ou qualquer tentativa de flood.\n\n"

                "**``Conteúdo apropriado``**\n"
                "Não será permitido o compartilhamento de conteúdo adulto (NSFW), materiais ilegais ou qualquer tipo de pirataria.\n\n"

                "**``Manter os tópicos``**\n"
                "Cada canal possui um propósito específico. Certifique-se de usar o local correto para discussões, perguntas ou compartilhamentos.\n\n"

                "**``Divulgação com permissão``**\n"
                "Divulgações de outros servidores ou projetos externos devem ser previamente autorizadas pela equipe de administração.\n\n"

                "**``Privacidade``**\n"
                "A privacidade dos membros é fundamental. Nunca compartilhe informações pessoais de terceiros, como números de telefone, endereços ou dados sensíveis, sem consentimento.\n\n"

                "**``Regras do Discord``**\n"
                "Este servidor segue as diretrizes gerais do Discord, que garantem um ambiente seguro e funcional para todos. [Saiba mais](https://discord.com/guidelines)\n\n"

                "Se você presenciar uma situação como essa, não hesite em contar com a nossa equipe de moderadores, que está sempre à disposição para ajudar. Todas as punições serão aplicadas conforme a gravidade e as circunstâncias do ato."

            ),
                color=cor_int
            )
        
        embed.set_footer(text=f"Cosmos Amistoso - Mantendo a comunidade segura")
        embed.set_image(url="attachment://regras.png")
        
        
        await ctx.send(embed=embed, file=file)

    @commands.command()
    async def add_money(self, ctx:commands.Context, member:discord.Member, quantidade):
        id_membro = member.id
        dono = 390495283034718230
        quantidade = Decimal(quantidade)


        if ctx.author.id == dono:
            add_saldo(id_membro, quantidade)
            qt = formatar_moeda(quantidade)
            await ctx.send(f"Foram adicionadas **{qt} Nyxie** em {member.mention}")
        else:
            await ctx.send(f"Você não tem permissão para usar esse comando!")

    @commands.command()
    async def game(self, ctx): 
        API_KEY = "8daababb5a354161966ef14b37c1af1c"
        BASE_URL = "https://api.rawg.io/api/games"
        async with ctx.channel.typing():
            try:
                # Fazer uma requisição à API RAWG para buscar jogos populares
                response = requests.get(BASE_URL, params={"key": API_KEY, "page_size": 20})
                if response.status_code != 200:
                    await ctx.send("Desculpe, não consegui acessar a API no momento. Tente novamente mais tarde!")
                    return

                # Pegar um jogo aleatório da resposta
                games = response.json()["results"]
                random_game = random.choice(games)

                # Fazer uma segunda requisição para obter detalhes do jogo
                game_id = random_game["id"]
                details_response = requests.get(f"{BASE_URL}/{game_id}", params={"key": API_KEY})
                if details_response.status_code != 200:
                    await ctx.send("Não consegui acessar os detalhes do jogo. Tente novamente mais tarde!")
                    return

                game_details = details_response.json()

                # Extrair informações do jogo
                game_name = game_details["name"]
                game_description = (
                    game_details.get("description_raw") or 
                    game_details.get("description") or 
                    "Descrição indisponível."
                )[:1000]  # Limitar caracteres
                game_slug = game_details.get("slug")  # Slug para construir o URL
                game_url = f"https://rawg.io/games/{game_slug}" if game_slug else "https://rawg.io"  # URL do jogo ou link padrão

                game_description = GoogleTranslator(source='auto', target='pt').translate(game_description)
                game_image = game_details.get("background_image", "https://via.placeholder.com/300")  # Imagem padrão se não houver

                # Criar embed para enviar no Discord
                embed = discord.Embed(
                    title=f"Sugestão: {game_name}",
                    description=f"{game_description}.. [Saiba mais]({game_url})",
                
                    color=discord.Color.blue()
                )
                embed.set_image(url=game_image)
                embed.set_footer(text="Sugestão de jogo pela RAWG.")

                await ctx.send(embed=embed)

            except Exception as e:
                print(f"Erro: {e}")
                await ctx.send("Ocorreu um erro ao buscar informações. Tente novamente mais tarde.")

    @commands.command()
    async def fatos(self, ctx):
        url = 'https://uselessfacts.jsph.pl/random.json'

        response = requests.get(url)
        async with ctx.channel.typing():
            if response.status_code == 200:
                dados = response.json()
                fato = dados['text']
                fato = GoogleTranslator(source='auto', target='pt').translate(fato)
                await ctx.send(f"<a:emoji_110:1327518188681957377> | **Fato aleatório:** {fato}")
            else:
                await ctx.send(f"<:a_remsad:1327518743324131349> | Hm.. parece que nenhum fato aleatório foi encontrado!")


    @commands.command()
    async def avatar(self, ctx:commands.Context, membro: discord.Member = None):
        if membro == None:
            membro = ctx.author

        icon_url = membro.avatar.url
        embed = discord.Embed(title="", description=f"**{membro.display_name}**\n Clique no icon para baixá-lo! Ou clique [aqui]({membro.avatar.url})", color=cor_int)
        embed.set_image(url=f'{icon_url}')
        await ctx.send(embed=embed)

    @commands.command()
    async def contagem(self, ctx:commands.Context, valor:int):
        menssagem = await ctx.send(f"`{valor}`")
        for i in range(valor):
            time.sleep(1)
            valor = valor - 1
            if valor == 0:
                await menssagem.edit(content="`!!!`")
            else:
                await menssagem.edit(content=f"`{valor}`")

        
    @commands.command()
    async def eventoCidade(self, ctx:commands.Context):
        file = discord.File(r"C:\Users\Abner\Desktop\Private - Abner\Programação\Nyx\imagens\Evento - Cidade dorme.png", filename="Evento.png")
        if ctx.author.id != 390495283034718230:
            await ctx.send("Você não pode usar esse comando.")
            return
        canal = self.bot.get_channel(1283970701778354317)
        embed = discord.Embed(
            title="",
            description=
            "**CIDADE SOB AMEAÇA – PÂNICO!**\n\n"
            "A cidade está em perigo! Um assassino misterioso está eliminando cidadãos durante a noite, e cabe a vocês descobrir quem ele é antes que seja tarde demais.\n\n"
            "``Personagens do jogo:``\n\n"
            "**Assassino** – Escolhe uma vítima a cada rodada e tenta não ser descoberto.\n"
            "**Detetive** – Investiga um jogador por noite para tentar encontrar o assassino.\n"
            "**Anjo** – Protege um jogador por rodada, impedindo que ele seja eliminado.\n"
            "**Cidadãos** – Precisam sobreviver e ajudar a identificar o assassino.\n\n"
            "``Como jogar:``\n\n"
            "<:MD_pPinkPoint:1346145063692140654>O apresentador distribui os papéis e anuncia que a cidade dorme. Durante a noite, ele chama cada um dos personagens (assassino, anjo e detetive) para que façam suas escolhas. Em seguida, acorda a cidade e anuncia os acontecimentos, dando aos cidadãos tempo para discutirem sobre quem pode ser o assassino. O jogador mais votado será eliminado da partida. O ciclo se repete, alternando entre noites e dias.\n\n"

            "> O assassino eliminado (vitória dos cidadãos).\n"
            "> Os cidadãos eliminados (vitória do assassino).\n\n"

            "Créditos: <@1127052448763232318>\n"
            "Inicio do evento: 04/03/2025"

            
            ,
            color=cor_int
        )
        embed.set_image(url="attachment://Evento.png")
        embed.set_footer(text="Reage no emoji abaixo para participar!")
        mensagem = await canal.send("<@&1308612316815949874>", embed=embed, file=file)
        emojis = ["☑️"]
        for emoji in emojis:
            await mensagem.add_reaction(emoji)
        embed.set_footer(text="Reage no emoji para marcar a sua participação!")
       # await ctx.send("Informações do evento enviadas para o canal de avisos.")
    
    @commands.command()
    async def votaçãoCidade(self, ctx:commands.Context):
        embed = discord.Embed(
            title="",
            description=
            "### Votação\n\n"
            "Selecione o assassino:\n"
            "`x`: 1️⃣ㅤㅤㅤㅤ`E`: 6️⃣\n"
            "`a`: 2️⃣ㅤㅤㅤㅤ`F`: 7️⃣\n"
            "`b`: 3️⃣ㅤㅤㅤㅤ`G`: 8️⃣\n"
            "`c`: 4️⃣ㅤㅤㅤㅤ`H`: 9️⃣\n"
            "`d`: 5️⃣ㅤㅤㅤㅤ`I`: 🔟\n"

            ,
            color=cor_int
        )
        mensagem = await ctx.send(embed=embed)
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "🔟"]
        for emoji in emojis:
            await mensagem.add_reaction(emoji)


    @commands.command()
    async def ranking(self, ctx):
        embed = discord.Embed(title="", 
                              description="### <:avisos_prd:1354443238395613346> Cargos por XP\n\n"
                                          "ㅤ\n> **Os Cargos de Interação são conquistados à medida que você participa das conversas no servidor. Quanto mais você interage, mais XP você ganha e mais alto sobe na hierarquia. Cada cargo representa o seu progresso e dedicação à comunidade. Suba de nível e se torne uma figura de destaque no Cosmos!**\n\n"
                                          "``Viajante Cósmico - Nível 1``\n"
                                          "Acesso básico ao servidor.\n\n"

                                        "<:B_estrela:1354445805309661324> ``Quasar - Nível 15``\n"
                                        "Permissão de usar emojis externos.\n"
                                        "Paleta de cores exclusivas.\n\n"

                                        "<:b_nuvemcoroa:1354445414312706049> ``Nebulon - Nível 30``\n"
                                        "Permissão para enviar mídias no (chat geral).\n"
                                        "Pode solicitar 2 emojis para o servidor.\n\n"

                                        "<:black_dragao:1354445466724597801> ``Eclipse - Nível 45``\n"
                                        "Passará a ganhar o dobro de XP.\n"
                                        "Pode solicitar até 4 emojis para o servidor.\n"
                                        "Poderá solicitar até 1 Tag personalizada.\n\n"


                                        "<:EstrelaShuriken:1354445513218592949> ``Pulsar - Nível 60``\n"
                                        "Acesso a sorteios exclusivos\n"
                                        "Permissão para enviar mídias em qualquer chat\n"
                                        "Poderá solicitar até 2 Tags personalizadas\n\n"

                                        "<:black_infinity:1354445553492033577> ``Titanus - Nível 75``\n"
                                        "Pode solicitar até 4 Tags personalizadas\n"
                                        "Terá voz prioritária nas Calls\n"
                                        "Imunidade aos sorteios\n\n"

                                        "<:a_black_cartas_hw:1354445601219149877> ``Singularity - Nível 90``\n"
                                        "Pode solicitar 1 figurinha para o servidor\n"
                                        "Poderá selecionar uma nova cor de Nick\n"
                                        "Passará a ganhar o triplo de XP\n\n"

                                        "<:Yellow_wings:1354445640054345800> ``Ómega - Nível 120``\n"
                                        "Acesso antecipado a eventos e atualizações.\n"
                                        "Terá participação em algumas decisões STAFF.\n"
                                        "Sugestãos serão tratadas como pioridade.\nㅤ\n"
                                        





                              , color=cor_int)
        embed.set_image(url="https://www.mundoinverso.com.br/wp-content/uploads/2019/04/Interestelar-gif-buraco-negro.gif")
        embed.set_footer(text="Os XP são contabilizados pela Loritta.")
        await ctx.send(embed=embed)
    

    @commands.command()
    async def msg(self, ctx):
        canal = self.bot.get_channel(1283964806436487272)

        msg = "### <:lp_avisobranco:1354446782293082363> Acontecimento recente. \n\nComo alguns de vocês podem ter percebido, recentemente nosso servidor foi alvo de um ataque (raid) que causou alguns danos à estrutura e organização. Esse ataque foi feito por um dos fundadores antigos, e infelizmente o servidor ficou desordenado por um tempo. No entanto, conseguimos retomar o controle e colocar tudo de volta nos trilhos de maneira rápida e eficaz!\n\nQueremos garantir que o servidor está seguro agora, mas, devido aos acontecimentos, algumas mudanças ocorreram:\n\n> **Reset dos XPs:** Todos os pontos de experiência (XP) foram resetados. Sabemos que isso pode ser frustrante, mas foi uma medida necessária para garantir que a progressão do servidor seja justa para todos. Confira: <#1323741813584039970> \n\n> **Mudança nos Cargos e Chats:** Alguns cargos foram ajustados e reorganizados. Agora, temos uma estrutura mais dinâmica e flexível, permitindo que todos possam progredir de maneira mais eficiente.\n\nPedimos a compreensão de todos e estamos à disposição para esclarecer qualquer dúvida. Continuamos comprometidos em fazer deste servidor um lugar divertido e acolhedor para todos. <@&1354451194881511465>"

        await canal.send(msg)


async def setup(bot):
    await bot.add_cog(geral(bot))