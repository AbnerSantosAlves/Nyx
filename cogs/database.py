from sqlalchemy import create_engine, Column, Integer, DECIMAL, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from discord.ext import commands


class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

db = create_engine("sqlite:///database.db")
Seesion = sessionmaker(bind=db)
session = Seesion()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    discordId = Column("discordId", Integer)
    moedas = Column("moedas", DECIMAL(10, 2))

    def __init__(self, discordId, moedas): #Essa função deve ser carregada sempre ao usar uma classe no python. Através dela, você deve passar os parâmetros que terá na classe.
        self.discordId = discordId
        self.moedas = moedas


def add_usuario(discordId):
    usuario = session.query(Usuario).filter_by(discordId=discordId).first()
    if not usuario:  # Usuário não existe
        usuario = Usuario(discordId=discordId, moedas=100)
        session.add(usuario)
        session.commit()
    return usuario

def ver_saldo(discordId):
    add_usuario(discordId)
    usuario = session.query(Usuario).filter_by(discordId=discordId).first()
    if usuario:
        return usuario.moedas

def add_saldo(discordId, quantidade):
    usuario = session.query(Usuario).filter_by(discordId=discordId).first()
    if usuario:
        usuario.moedas += quantidade
        session.commit()
    else:
        add_usuario(discordId) 
        add_saldo(discordId, quantidade)


def formatar_moeda(valor):
    valor_formatado = f"{float(valor):,.2f}"
    return valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")

def obter_posicao_usuario(discordId):
    ranking = (
        session.query(Usuario)
        .order_by(desc(Usuario.moedas))
        .all()
    )


    for posicao, user in enumerate(ranking, start=1):
        if user.discordId == discordId:
            return posicao

    return None 

Base.metadata.create_all(db)

async def setup(bot):
    await bot.add_cog(DatabaseCog(bot))
