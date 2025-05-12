import discord
from discord.ext import commands
import requests

cor_atual = "0000FF"
cor_int = int(cor_atual, 16)

class OSINT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def tracker_domain(self, ctx, domain: str):
        url = "https://whois-api6.p.rapidapi.com/whois/api/v1/getData"

        payload = {"query": domain}
        headers = {
            "x-rapidapi-key": "14c3111bdfmshe6c9afb56444e20p1f11adjsnbd84b7acba6a",
            "x-rapidapi-host": "whois-api6.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        mensagem = await ctx.send(f"<a:HD_Loading:1370931991733600256> Estou consultando os dados.")

        try:
            response = requests.post(url, json=payload, headers=headers)
            result = response.json().get("result", {})

            domain_name = result.get("domain_name", "Desconhecido")
            registrar = result.get("registrar", "Não informado")
            creation_date = result.get("creation_date", ["Não disponível"])[0]
            expiration_date = result.get("expiration_date", ["Não disponível"])[0]
            country = result.get("country", "Não informado")
            org = result.get("org", "Não informado")
            
            file = discord.File(r"imagens\icc2.gif", filename="icc2.gif")
            embed = discord.Embed(title=f"<a:z6check:1370930658355974224> Resultado obtido - {domain_name}", color=0x00ff00)
            embed.add_field(name="<:MD_bBluePoint:1370931323111215244> ``Registrador:``", value=f"*{registrar}*", inline=False)
            embed.add_field(name="<:MD_bBluePoint:1370931323111215244> ``Organização:``", value=f"*{org}*", inline=False)
            embed.add_field(name="<:MD_bBluePoint:1370931323111215244> ``Criado em:``", value=f"*{creation_date}*", inline=False)
            embed.add_field(name="<:MD_bBluePoint:1370931323111215244> ``Expira em:``", value=f"*{expiration_date}*", inline=False)
            embed.add_field(name="<:MD_bBluePoint:1370931323111215244> ``País:``", value=f"*{country}*", inline=False)

            await mensagem.edit(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao consultar o domínio: `{e}`")

    @commands.command()
    async def tracker_ip(self, ctx, ip: str):
        url = "https://bin-ip-checker.p.rapidapi.com/ip-lookup"

        querystring = {"ip":f"{ip}"}

        headers = {
	        "x-rapidapi-key": "14c3111bdfmshe6c9afb56444e20p1f11adjsnbd84b7acba6a",
            "x-rapidapi-host": "bin-ip-checker.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("success"):
                ip_info = data.get("IP", {})
                embed = discord.Embed(title=f"Informações do IP: {ip}", color=0x00ff00)

                # Adicionando as informações no embed
                embed.add_field(name="🌍 País", value=ip_info.get("country", "Não disponível"), inline=False)
                embed.add_field(name="🏙️ Cidade", value=ip_info.get("city", "Não disponível"), inline=False)
                embed.add_field(name="💻 ISP", value=ip_info.get("isp", "Não disponível"), inline=False)
                embed.add_field(name="🌐 Região", value=ip_info.get("region", "Não disponível"), inline=False)
                embed.add_field(name="🌎 Localização", value=f"{ip_info.get('latitude')}, {ip_info.get('longitude')}", inline=False)
                embed.add_field(name="🕒 Hora Atual", value=ip_info.get("current_time", "Não disponível"), inline=False)
                embed.add_field(name="🗺️ Código Postal", value=ip_info.get("zip_code", "Não disponível"), inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Não foi possível encontrar informações para o IP '{ip}'.")
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao consultar o IP: {e}")

 
    @commands.command(name="scanlink", help="Verifica se um link é malicioso, phishing ou coletor de IP.")
    async def scan_link(self, ctx, url: str):
        """Comando para verificar links maliciosos"""
        await ctx.send("🔎 Verificando o link, aguarde um momento...")

        api_url = "https://malicious-scanner.p.rapidapi.com/rapid/url"
        querystring = {"url": url}
        headers = {
            "x-rapidapi-key": "14c3111bdfmshe6c9afb56444e20p1f11adjsnbd84b7acba6a",
            "x-rapidapi-host": "malicious-scanner.p.rapidapi.com"
        }

        try:
            response = requests.get(api_url, headers=headers, params=querystring)
            data = response.json()

            if not data.get("success") or "data" not in data:
                await ctx.send("❌ Não foi possível analisar o link ou ele é inválido.")
                return

            info = data["data"]
            embed = discord.Embed(
                title="🔍 Análise de Link",
                description=f"Resultado da varredura do link informado:",
                color=discord.Color.orange()
            )

            embed.add_field(name="🔗 URL Analisada", value=info.get("original_url", url), inline=False)
            embed.add_field(name="📦 Tipo", value=info.get("type", "Desconhecido"), inline=True)
            embed.add_field(name="🌍 Domínio", value=info.get("domain", "N/A"), inline=True)
            embed.add_field(name="📅 Domínio criado em", value=info.get("domain_age", "Desconhecido")[:10], inline=True)
            embed.add_field(name="📍 Redirecionamento", value=info.get("redirect_url", "Nenhum"), inline=False)

            embed.add_field(name="🛡️ Status", value=info.get("status", "Desconhecido"), inline=True)
            embed.add_field(name="⚠️ Categoria", value=info.get("category", "N/A"), inline=True)

            # Avaliação de riscos
            riscos = []
            if info.get("status", "").lower() == "suspicious":
                riscos.append("🚨 Link classificado como *suspeito* por múltiplos motores.")
            if info.get("category", "").lower() in ["phishing", "malware", "tracking"]:
                riscos.append(f"⚠️ Categoria detectada: **{info.get('category')}**.")
            if info.get("is_new_domain"):
                riscos.append("🆕 Domínio recente (alerta para uso malicioso temporário).")
            if info.get("type") == "redirect":
                riscos.append("🔁 Link contém redirecionamento.")
            if info.get("is_anti_bot"):
                riscos.append("🤖 Comportamento anti-bot detectado (pode tentar bloquear rastreamento).")

            if riscos:
                embed.add_field(
                    name="💀 Potenciais Riscos",
                    value="\n".join(riscos),
                    inline=False
                )
            else:
                embed.add_field(name="✅ Nenhum risco aparente", value="O link parece seguro.", inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao verificar o link.\nErro: `{str(e)}`")






async def setup(bot):
    await bot.add_cog(OSINT(bot))
