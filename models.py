from utils.base import Base

class Rect(Base):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class Circulo(Base):

    def __init__(self, raio):
        self.raio = raio

class Usuario(Base):

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


class Jogador(Base):
    def __init__(self, nome, time, gols):
        self.nome = nome
        self.time = time
        self.gols = gols
        