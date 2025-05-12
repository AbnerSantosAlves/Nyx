import discord
from sqlalchemy.exc import SQLAlchemyError
from discord.ext.commands import CommandOnCooldown
from discord.ext import commands, tasks
from datetime import timedelta 
import asyncio
import random
from decimal import Decimal
from cogs.database import *


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    # Comando para ver o saldo
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

    # Comando do Daily
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

    #comando para apostar
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

    # comando para transferir
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


    #comando para adicionar ou remover
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

async def setup(bot):
    await bot.add_cog(Bank(bot))
