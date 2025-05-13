import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import timedelta
import os
import random
import json
import datetime
from dotenv import load_dotenv
import os
from keep_alive import keep_alive


cumprimentos = [
    "E aí, como vocês estão?", "Bom dia, pessoal! Prontos para mais um dia?", 
    "Olá a todos! Espero que estejam bem!", "Oi, galera! Como está indo?", 
    "Salve, salve! Tudo tranquilo por aqui?", "Oi, pessoal! Vamos fazer algo divertido hoje?", 
    "Olá! Quem está por aí hoje?", "E aí, pessoal! Como estão as coisas?", 
    "Oi, gente! Espero que estejam tendo um ótimo dia!", "Olá! Animados para o que vem pela frente?", 
    "Saudações, aventureiros! Como está a missão de hoje?", "Hey, turma! Bora colocar a conversa em dia?", 
    "Olá, terráqueos! Como estão os humanos hoje?", "Fala, pessoal! Que tal compartilharmos umas histórias?", 
    "Bom dia, boa tarde ou boa noite! Alguém por aí?", "Ei, amigos! Contem-me uma novidade!", 
    "Olá, nação! Como estão dominando o universo?", "Oi, seres incríveis! Estão prontos para dominar o dia?", 
    "Salve, salve! Prontos para mais um dia épico?", "Olá! Que tal começar o dia com energia positiva?"
]

gifs_hug = ["https://media1.tenor.com/m/nd_M3VFwVD0AAAAd/anime-hug.gif", "https://media1.tenor.com/m/FgLRE4gi5VoAAAAd/hugs-cute.gif", "https://media1.tenor.com/m/-GGSvsfmkeQAAAAd/hug.gif", "https://media1.tenor.com/m/J7eGDvGeP9IAAAAd/enage-kiss-anime-hug.gif", "https://media1.tenor.com/m/m_bbfF_KS-UAAAAd/engage-kiss-anime-hug.gif"]


permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix="N'", intents=permissoes)
cor_atual = "0xFF0000"
cor_int = int(cor_atual, 16)



async def carregar_cogs():
     for arquivo in os.listdir('cogs'):
          if arquivo.endswith('.py'):
            await bot.load_extension(f'cogs.{arquivo[:-3]}')

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


@bot.event
async def on_ready():
    await carregar_cogs()
    print('Estou pronto')
    owner = 390495283034718230
    user = 1299629174008315956
    ## user = await bot.fetch_user(owner)
    ms = await bot.fetch_user(user)
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f'NXV Studios'))
    await loop_messagem.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para usar esse comando.")


@tasks.loop(hours=10)
async def loop_messagem():
    msg_loop = random.choice(cumprimentos)
    canal = bot.get_channel(1283964033807941652)
    # await canal.send(msg_loop)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.type == discord.MessageType.premium_guild_subscription:
        perfil_autor = message.author.avatar.url  
        embed = discord.Embed(
            title=f"{message.author.display_name} Deu boost no servidor",
            description="Muito obrigado por impulsionar o nosso servidor! Isso ajuda bastante a manter a nossa comunidade ativa e dinâmica."
        )
        embed.set_author(name=message.author.name, icon_url=perfil_autor)  
        embed.set_thumbnail(url=perfil_autor)
        embed.add_field(name="Total de Boost(server):", value=message.guild.premium_subscription_count, inline=True)
        embed.add_field(name="Nível:", value=message.guild.premium_tier, inline=True)
        await message.channel.send(embed=embed)

    
    if "salada" in message.content.lower():
        await message.reply("Eu só de canto, observando essa salada.")
        await message.channel.send("Nada aceso, quarto escuro")
        await message.channel.send("Vai tomando, vida rasa, rasa")
    if "neymar" in message.content.lower():
        await message.reply("ô neimar")
        await message.channel.send("ô neimarr")
    
    
    await bot.process_commands(message)


class HugView(discord.ui.View):
    def __init__(self, autor: discord.Member, membro: discord.Member):
        super().__init__()
        self.autor = autor  # Quem enviou o comando
        self.membro = membro  # Quem recebeu o comando

    @discord.ui.button(label="Retribuir abraço", style=discord.ButtonStyle.primary)
    async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Garantir que apenas o destinatário do abraço pode retribuir
        if interaction.user.id != self.membro.id:
            await interaction.response.send_message(
                "Apenas quem recebeu o abraço pode retribuir!",
                ephemeral=True
            )
            return

        # Mensagem de retribuição
        embed = discord.Embed(
            title="Que adorável!",
            description=f"{interaction.user.mention} retribuiu o abraço de {self.autor.mention}!",
            color=cor_int
        )
        
        gif_hug = random.choice(gifs_hug)
        embed.set_image(url=gif_hug)
        view = HugView(self.membro, self.autor)
        await interaction.response.send_message(embed=embed, view=view)

# Comando para enviar a mensagem com o botão
@bot.command(aliases=['hug', 'abraco'])
async def abraço(ctx, membro: discord.Member):

    if membro.id == ctx.author.id:
        bot = ctx.bot.user.mention  
        embed = discord.Embed(
        title="Ah.. Está se sentindo sozinho? Tome!",
        description=f"{bot} deu um abraço em {ctx.author.mention}!",
        color=cor_int
    )
        gif_hug = random.choice(gifs_hug)
        embed.set_image(url=gif_hug)
        view = HugView(ctx.author, membro)
        await ctx.send(embed=embed, view=view)
        return

    view = HugView(ctx.author, membro)
    embed = discord.Embed(
        title="Aww... que fofo!",
        description=f"{ctx.author.mention} deu um abraço em {membro.mention}!",
        color=cor_int
    )
    gif_hug = random.choice(gifs_hug)
    embed.set_image(url=gif_hug)
    await ctx.send(embed=embed, view=view)


keep_alive()
bot.run(DISCORD_BOT_TOKEN)
