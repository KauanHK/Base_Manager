from base import Base

class Rect(Base):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class Circulo(Base):

    def __init__(self, raio):
        self.raio = raio
