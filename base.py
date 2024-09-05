from base_manager import BaseManager


class Base:

    objects = None

    def __init_subclass__(cls):
        cls.objects = BaseManager(cls)

    def save(self):
        self.objects._save(vars(self))

    def __str__(self):
        varss = vars(self)
        str_vars = [f'{var} = {varss[var]}' for i, var in enumerate(varss)]
        str_vars = ', '.join(str_vars)
        return f'{self.__class__.__name__}({str_vars})'