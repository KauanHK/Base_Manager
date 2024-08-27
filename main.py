from typing import Callable

class By:
    WIDTH = 1
    HEIGHT = 2
    AREA = 3

class Objs:

    def __init__(self):
        self._rects = []

    def _add(self, rect: "Rect"):
        self._rects.append(rect)

    def _get_rect_by_id(self, id: int):
        for rect in self._rects:
            if rect.id == id:
                return rect

    def remove(self, rect: "Rect" = None, id: int | None = None):
        if isinstance(rect, Rect):
            for rec in self._rects:
                if rec.id == rect.id:
                    self._rects.remove(rec)
        elif isinstance(id, int):
            rect = self._get_rect_by_id(id)
            if rect is None:
                raise ValueError(f'Nenhum Rect com id {id} foi encontrado.')
                

    def all(self):
        return self._rects
    
    def get(self, id: int | None = None, by: int | None = None, key: Callable | None = None):
        if isinstance(id, int):
            rect = self._get_rect_by_id(id)
            if rect is None:
                raise ValueError(f'Nenhum Rect com id {id} foi encontrado.')
        elif callable(key):
            funcs = {
                By.WIDTH: lambda rect: rect.width,
                By.HEIGHT: lambda rect: rect.height,
                By.AREA: lambda rect: rect.area,
            }
            try:
                key = funcs[by]
            except ou
            return key(self._rects, key=funcs[by])
        
    def filter(self, by: int, key: Callable | None = max):
        if by == By.AREA:
            return key(self._rects, key=lambda rect: rect.area)


class Rect:
    
    objects = Objs()
    _id_counter = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.id = self._id_counter
        Rect._id_counter += 1
        self.objects._add(self)

    def display(self):
        print('-'*self.width)
        for i in range(self.height):
            print('|', ' '*(self.width-4), '|')
        print('-'*self.width)

    @property
    def size(self):
        return self.width, self.height
    
    @property
    def area(self):
        return self.width * self.height
    
    def __str__(self):
        return f'Rect(ID = {self.id})'
    

r1 = Rect(5, 4)
r2 = Rect(10, 8)
r3 = Rect(1,8)
r4 = Rect(7,2)

Rect.objects.remove(id = 2)
menor_width = Rect.objects.get(by=By.AREA, key=max)
maior_area = Rect.objects.filter(By.AREA)

print('\n', *Rect.objects.all())
print(f'Menor largura: {menor_width}')
print(f'Maior área: {maior_area}', '\n')