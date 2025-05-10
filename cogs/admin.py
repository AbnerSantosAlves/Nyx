import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord.ext import commands
from discord import app_commands

cor_atual = "0000FF"
cor_int = int(cor_atual, 16)


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


async def setup(bot):
    await bot.add_cog(admin(bot))