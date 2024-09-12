from base_manager import BaseManager

class Base:

    objects = BaseManager()

    def save(self):
        self.objects.save(self)
    
    def delete(self):
        self.objects.delete(obj=self)

    def __str__(self):
        str_vars = [f'{var} = {value}' for var, value in vars(self).items()]
        str_vars = ', '.join(str_vars)
        return f'{self.__class__.__name__}({str_vars})'