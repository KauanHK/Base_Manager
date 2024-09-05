from base import Base

class Rect(Base):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

print('\n')

Rect.objects.create(
    width = 12,
    height = 7
)

Rect.objects.delete(id=7)

for rect in Rect.objects.all():
    print(rect)

print('\n')