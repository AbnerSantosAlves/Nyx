import discord
from discord.ext import commands
import random

class CipherGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_challenges = {}
        self.phrases = [
            "O segredo está nas estrelas",
            "Python é a melhor linguagem",
            "Decifre este código misterioso",
            "A resposta está em 42",
            "Nunca subestime a força do café"
        ]

        # Métodos de criptografia
        self.metodos_criptografia = {
            "Cifra de César (+3)": self.caesar_cipher,
            "Texto Reverso": self.reverse_text,
            "Código das Vogais": self.vowel_code,
            "Código Morse": self.morse_code
        }

    # Métodos de criptografia
    def caesar_cipher(self, text, shift=3):
        result = ""
        for char in text:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - start + shift) % 26 + start)
            else:
                result += char
        return result

    def reverse_text(self, text):
        return text[::-1]

    def vowel_code(self, text):
        replacements = {'A': '4', 'E': '3', 'I': '1', 'O': '0', 'U': '7'}
        return ''.join(replacements.get(c.upper(), c) for c in text)

    def morse_code(self, text):
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..', ' ': '/'
        }
        return ' '.join(morse_dict.get(c.upper(), '') for c in text)

    @commands.command(name="decifrar")
    async def cipher_challenge(self, ctx):
        """Inicia um desafio de decifração"""
        phrase = random.choice(self.phrases)  #
        metodo, encoder = random.choice(list(self.metodos_criptografia.items())) 
        encoded = encoder(phrase)

        self.active_challenges[ctx.author.id] = phrase.lower()

        embed = discord.Embed(
            title="🔐 Desafio Criptográfico",
            description=f"**Método usado:** {metodo}\n**Mensagem codificada:**\n```{encoded}```",
            color=0x00ff00
        )
        embed.set_footer(text="Você tem 3 tentativas! Responda com !resposta [sua tentativa]")

        await ctx.send(embed=embed)

    @commands.command(name="resposta")
    async def check_answer(self, ctx, *, answer: str):
        """Verifica sua resposta para o desafio"""
        user_id = ctx.author.id
        answer = answer.lower().strip()

        if user_id not in self.active_challenges:
            await ctx.send("Você não tem um desafio ativo! Use !decifrar para começar.")
            return

        correct_answer = self.active_challenges[user_id]

        if answer == correct_answer:
            await ctx.send(f"**Correto!** {ctx.author.mention} decifrou o código!")
            del self.active_challenges[user_id]
        else:
            await ctx.send("❌ Resposta incorreta! Tente novamente.")

async def setup(bot):
    await bot.add_cog(CipherGame(bot))
