import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput

cor_atual = "0000FF"
cor_int = int(cor_atual, 16)


class MyModal(Modal):
    def __init__(self):
        super().__init__(title="Seja staff do Cosmos")

        self.nome = TextInput(label="Seu nome", placeholder="Digite seu nome aqui")
        self.add_item(self.nome)

        self.idade = TextInput(label="Sua idade", placeholder="Digite sua idade aqui", style=discord.TextStyle.short)
        self.add_item(self.idade)

        self.frequencia = TextInput(label="Frequência no discord", placeholder="Escreva aqui a sua frequência", style=discord.TextStyle.short)
        self.add_item(self.frequencia)

        self.motivo = TextInput(label="Porque deseja entrar", placeholder="Escreva o motivo aqui", style=discord.TextStyle.paragraph)
        self.add_item(self.motivo)

        self.adicional = TextInput(label="Adicional", placeholder="Escreva o adicional aqui", style=discord.TextStyle.paragraph, required=None)
        self.add_item(self.adicional)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            dono = await interaction.client.fetch_user(390495283034718230)
            dm_channel = await dono.create_dm()
            await dm_channel.send(
                f"**Novo Formulário Recebido:**\n\n"
                f"**Nome:** {self.nome.value}\n"
                f"**Idade:** {self.idade.value}\n"
                f"**Frequência:** {self.frequencia.value}\n"
                f"**Motivo:** {self.motivo.value}\n"
                f"**Adicional:** {self.adicional.value}"
            )
            await interaction.response.send_message("Formulário enviado com sucesso!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Não consegui enviar o formulário ao administrador. Verifique se ele aceita DMs.", ephemeral=True)

class FormularioView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # View persistente

    @discord.ui.button(label="Quero fazer parte!", style=discord.ButtonStyle.primary, custom_id="formulario_staff")
    async def botao_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(MyModal())
        except Exception as e:
            await interaction.response.send_message("Você já respondeu ou houve um erro.", ephemeral=True)
            print(f"Erro ao abrir modal: {e}")

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    # Comando para banir membros
    @commands.command(aliases=['banir'])
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx:commands.Context, membro:discord.Member=None, reason=None):
        file = discord.File(r"C:\Users\Abner\Desktop\Private - Abner\Programação\Nyx\imagens\digital-person.gif", filename="person.gif")
        if membro == None or membro == ctx.message.author:
            await ctx.send("Você não pode se banir, bobinho.")
            return
        if reason == None:
            reason = "Não especificado."
        
        await membro.ban()
        await ctx.send(f"{membro.display_name} foi banido!")
        embed = discord.Embed(title="", 
        description="**<:f_mod_DiscordShield:1338558678751772815> Um membro acaba de ser banido**\n\n"
                    f"``Autor do banimento:`` {membro.mention} (ID {membro.id})\n"
                    f"``Usuário punido:`` {ctx.author.mention} (ID {ctx.author.id})\n"
                    f"``Motivo:`` {reason}\n", 
        color=cor_int
        
        )

        canal = self.bot.get_channel(1326660250715295765)
        embed.set_thumbnail(url="attachment://person.gif")
        await canal.send(embed=embed, file=file)

  
    #Comando para expulsar membros
    @commands.command(aliases=['expulsar'])
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx:commands.Context, member:discord.Member, reason=None):
        file = discord.File(r"C:\Users\Abner\Desktop\Private - Abner\Programação\Nyx\imagens\cubo - animation.gif", filename="icon.gif")
        if member == ctx.author:
             await ctx.send("Você não pode se expulsar!")
        if reason == None:
             reason = "Motivo não especificado"

        await member.kick()
        await ctx.send(f"{member.display_name} foi expulso.")
        embed = discord.Embed(
            title="",
            description=f"<:f_mod_DiscordShield:1338558678751772815> **{member.name} acaba de ser expulso**\n\n"
                    f"``Autor da expulsão:`` {member.mention} (ID {member.id})\n"
                    f"``Usuário punido:`` {ctx.author.mention} (ID {ctx.author.id})\n"
                    f"``Motivo:`` {reason}\n", 
            color=cor_int
        )
        canal = self.bot.get_channel(1326660250715295765)
        embed.set_thumbnail(url="attachment://icon.gif")
        await canal.send(embed=embed, file=file)
          
     # Comando para limpar mensagens    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx:commands.Context, nr:int):
         canal = ctx.channel
         msg = f'{nr} mensagens deletadas'
         await canal.purge(limit=nr)
         await ctx.send(msg)


    #Comando para bloquear todos os chats
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def lockdown(self, ctx, *, reason="Sem razão específica"):
         if ctx.author.id != ctx.guild.owner.id:
             return
         for channel in ctx.guild.text_channels:
             await channel.set_permissions(ctx.guild.default_role, send_messages=False)
         await ctx.send(f"Todos os canais de texto foram bloqueados. Motivo: {reason}")

    #comando para desbloquear todos os chats
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unlockdown(self, ctx, *, reason="Sem razão específica"):
        if ctx.author.id != ctx.guild.owner.id:
            return
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"Todos os canais de texto foram liberados. Motivo: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def formulario_staff(self, ctx: commands.Context):
        file = discord.File(r"imagens\Banner - Seja staff.jpg", filename="staff.jpg")
        embed = discord.Embed(
            title="",
            description="## Faça parte da nossa equipe!\n\n"
            "Estamos em busca de pessoas dedicadas e responsáveis para fazer parte da nossa equipe! Se você gosta de interagir com a comunidade, manter a ordem e ajudar no crescimento do servidor, essa pode ser a sua chance.\n\n"
            "`O que buscamos?`\n"
            "<:pnc_2yellowarrow:1371974300038594600>Maturidade e responsabilidade\n"
            "<:pnc_2yellowarrow:1371974300038594600>Atividade no servidor\n"
            "<:pnc_2yellowarrow:1371974300038594600>Boa comunicação\n"
            "<:pnc_2yellowarrow:1371974300038594600>Saber trabalhar em equipe\n"
            "<:pnc_2yellowarrow:1371974300038594600>Conhecimento básico de moderação (opcional, mas um diferencial).\n\n"
            "Se você preenche todos os requisitos e acredita que pode contribuir para tornar o nosso servidor um lugar ainda melhor, queremos conhecer você! Preencha o formulário abaixo com atenção, fornecendo todas as informações solicitadas."
        )
        embed.set_image(url="attachment://staff.jpg")
        await ctx.send(embed=embed, file=file, view=FormularioView())

async def setup(bot):
    await bot.add_cog(admin(bot))