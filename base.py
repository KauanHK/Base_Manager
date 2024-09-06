from base_manager import BaseManager


class Base:

    objects = None

    def __init_subclass__(cls):
        cls.objects = BaseManager(cls)

    def save(self):
        varss = vars(self)
        self.objects._save(varss)
    
    def delete(self):
        self.objects.delete(obj=self)

    def __str__(self):
        str_vars = [f'{var} = {value}' for var, value in vars(self).items()]
        str_vars = ', '.join(str_vars)
        return f'{self.__class__.__name__}({str_vars})'