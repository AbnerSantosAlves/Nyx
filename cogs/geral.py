import discord
from discord.ext import commands, tasks
from discord import Color
from discord import app_commands
from deep_translator import GoogleTranslator
import asyncio
import random
import requests
import aiohttp
import time, os
from cogs.database import *

async def cores():
    ecolor = ['FF0000', '00FF00', '0000FF', 'FFFF00', 'FF00FF', '00FFFF', 
              'FFFFFF', '000000', '808080', '800000', '008000', '000080', 
              '808000', '800080', '008080', 'C0C0C0', 'FFA500', 'A52A2A', 
              'ADD8E6', 'FFC0CB']
    
    cor = random.choice(ecolor)
    hexadecimal = int(cor, 16)  # Converter a string para inteiro no formato hexadecimal
    return hexadecimal


# COMANDOS QUE ESTÃO NESTE CÓDIGO:
# N'COMANDOS - EXIBE TODOS OS COMANDOS DO BOT           #MANUTENÇÃO
# N'ROLL - PARA ROLAR UM NÚMERO SELECIONADO
# N'COINFLIP - PARA GIRAR A MOEDA (RETURN: CARA OU COROA)
# N'CHOOSE - PARA ESCOLHER ENTRE TERMOS SELECIONADOS
# N'SERVER - INFORMAÇÕES GERAIS DOS SERVIDORES          #MANUTENÇÃO
# N'GAME - RECOMENDA UM JOGO ALEATÓRIO                  #MANUTENÇÃO
# N'FATOS - GERA UM FATO ALEATÓRIO
# N'DOG - GERA UMA FOTO DE UM DOG ALEATÓRIO
# N'CAT - GERA UMA FOTO DE UM GATO ALEATÓRIO

class geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()


    @commands.command()
    async def roll(self, ctx:commands.Context, rolagem : str):
        embed_color = await cores()
        if 'd' in rolagem.upper():
            numero_dados, numero_roll = rolagem.split('d') #Separando os número através do "d" -> 2d20
            numero_dados = int(numero_dados)
            numero_roll = int(numero_roll)
        else:
            numero_dados = 1
            numero_roll = int(rolagem)
        
        #sorteando o número
        resultados = [random.randint(1, numero_roll) for _ in range(numero_dados)]
        resultado_formatado = " + ".join(str(r) for r in resultados)
        total = sum(resultados)

        #criando a Embed    
        embed = discord.Embed(title=f"<a:loading:1370837297355817163> Rolando {numero_dados}d{numero_roll}", description="Gerando...", color=embed_color)
        mensagem = await ctx.send(embed=embed)
        await asyncio.sleep(3)

        #trabalhando os formatos de mensagem. Tratativa de erros em limites de caracteres e a exibição do calculo.
        if len(resultado_formatado) > 2000:
           embed.description=f"Você tirou: {total}\n`Muitos dados -> {total}`"
           return        
        if numero_dados == 1:
            embed.description=f"Você tirou: {total}"
        else:
            embed.description(f"Você tirou: {total}\n`{resultado_formatado} -> {total}`")
        

        #resultado final
        embed.title=f"<:correto:1370838889174143108> Resultado obtido de {numero_dados}d{numero_roll}"
        await mensagem.edit(embed=embed)

    #comando para girar a moeda (cara ou coroa)
    @commands.command()
    async def coinflip(self, ctx:commands.Context):
        moeda = ['Cara', 'Coroa']
        escolha = random.choice(moeda)
        await ctx.send(escolha)
    
    #Comando de escolhas.
    @commands.command()
    async def choose(self, ctx:commands.context, *, textos):
        lista_textos = textos.split(',')
        escolha = random.choice(lista_textos)
        await ctx.send(escolha)


    @commands.command()
    async def server(self, ctx:commands.Context):
        embed_color = await cores()
        server_name = ctx.guild.name
        server_owner = ctx.guild.owner
        server_member = ctx.guild.member_count
        server_region = ctx.guild.region
        server_id = ctx.guild.id
        server_boost = ctx.guild.premium_tier

        informacoes = {
            "Nome" : f"{server_name}",
            "ID" : f"{server_id}",
            "Dono" : f"{server_owner}",
            "membros" : f"{server_member}",
            "Região" : f"{server_region}",
            "Nível Boost" : f"{server_boost}"
        }

        embed = discord.Embed(title="", description=f"## Informações de {informacoes['Nome']}", color=embed_color)

        for nome, valor in informacoes.items():
            embed.add_field(name=nome, value=valor, inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    async def fatos(self, ctx):
        url = 'https://uselessfacts.jsph.pl/random.json'

        response = requests.get(url)
        async with ctx.channel.typing():
            if response.status_code == 200:
                dados = response.json()
                fato = dados['text']
                fato = GoogleTranslator(source='auto', target='pt').translate(fato)
                await ctx.send(f"<:CEU_Maikima_bang:1370850425972199495> | **Fato aleatório:** {fato}")
            else:
                await ctx.send(f"<:a_remsad:1327518743324131349> | Hm.. parece que nenhum fato aleatório foi encontrado!")

    @commands.command()
    async def dog(self, ctx):
        embed_color = await cores()
        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json() 
            img = dados['message']
            embed = discord.Embed(title="", description="**Novo dog desbloqueado!**", color=embed_color)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        embed_color = await cores()
        url = "https://api.thecatapi.com/v1/images/search?limit=1&api_key=live_Sb6GQBPV6EWFIW50aXH4pbWDYtau9t3C8RVY9l5nD7nM9BQRwtZnsbRrhmL5ZOJg"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json() 
            img = dados[0]['url']
            embed = discord.Embed(title="", description="**Novo cat desbloqueado**", color=embed_color)
            embed.set_image(url=img)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Infelizmente, nenhum gato foi encontrado..")


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def embed_boost(self, ctx):
        file = discord.File(r"imagens\Banner - Seja Boost.jpg", filename='boost.jpg')
        embed = discord.Embed(
            title="", 
            description="## Impulsione o servidor\n"
            "\nAo impulsionar o servidor, você estará contribuindo para manter todos os benefícios que tornam a nossa comunidade mais dinâmica.\n\n"
            "**<:boost_red:1371877067473289317> Benefícios**\n"
            "Acesso a cores exclusivas somente para Boosters\n"
            "Permissão para enviar mídias em todos os chats\n"
            "Você ficará em destaque na lista de membros\n"
            "Passará a receber o dobro de XP na Loritta\n"
            "Pode solicitar até 2 Tags personalizadas\n",
            color=0xFFA500)
        embed.set_image(url="attachment://boost.jpg")
        embed.set_footer(text="Cosmos amistoso")

        await ctx.send(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(geral(bot))