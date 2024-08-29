from base_manager import BaseManager


class Base:

    objects = None
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.objects = BaseManager(cls)

    def save(self):
        self.objects._save(self)

    def __str__(self):
        varss = vars(self)
        varss = [f'{var}={varss[var]}' for var in varss]
        str_vars = ', '.join(varss)
        return f'{self.__class__.__name__}({str_vars})'


class Rect(Base):
    

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def size(self):
        return self.width, self.height
    
    @property
    def area(self):
        return self.width * self.height
    
    

class Circle(Base):

    def __init__(self, radius):
        self.radius = radius

    @property
    def comprimento(self):
        return 2 * 3.14 * self.radius

    @property
    def area(self):
        return 3.14 * self.radius**2


for rect in Rect.objects.all():
    print(rect)