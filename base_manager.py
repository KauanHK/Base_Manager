import sqlite3
import inspect
import os
from typing import Any

class BaseManager:
    
    def __init__(self, obj):
        self.obj = obj
        self.DATABASE = 'db.sqlite3'
        self._create_table()

    def _create_table(self):
        if not os.path.exists(self.DATABASE):
            with open(self.DATABASE, 'w'):
                pass

        with sqlite3.connect(self.DATABASE) as conn:
            cursor = conn.cursor()
            table = self.obj.__name__
            parametros = inspect.signature(self.obj.__init__)
            colunas = [col for col in parametros.parameters if col != 'self']
            for i, col in enumerate(colunas):
                colunas[i] += ' INTEGER'
            colunas = ', '.join(colunas)
            comando = f"CREATE TABLE IF NOT EXISTS {table} ( id INTEGER PRIMARY KEY AUTOINCREMENT, {colunas} );"
            cursor.execute(comando)
            conn.commit()

    def create(self, **kwargs):
        try:
            self.obj(*kwargs.values())
        except:
            raise ValueError(f'kwargs inválidos para {self.obj.__name__}')
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            items = vars.items()
            colunas = [item[0] for item in items]
            values = [item[1] for item in items]
            colunas = ', '.join(colunas)
            values = [str(v) for v in values]
            values = ', '.join(values)
            comando = F"INSERT INTO {self.obj.__name__} ({colunas}) values ({values});"
            cursor.execute(comando)
            conn.commit()

    def all(self):
        with sqlite3.connect(self.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.obj.__name__};")
            db_data = cursor.fetchall()
            db_data = [data[1:] for data in db_data]
            objs = [self.obj(*data) for data in db_data]
            return objs

    def get(self, id: int, default: Any | None = 'raise'):
        if isinstance(id, int):
            try:
                with sqlite3.connect(self.DATABASE) as conn:
                    cursor = conn.cursor()
                    comando = f'SELECT * FROM {self.obj.__name__} WHERE id = {id};'
                    cursor.execute(comando)
                    db_data = cursor.fetchall()
                    return self.obj(*db_data[0][1:])
            except:
                if default == 'raise':
                    raise ValueError(f'{self.obj.__name__} com id {id} não foi encontrado.')
                else:
                    return default
                
                
    def delete(self, id: int):
        if not isinstance(id, int):
            raise ValueError(f'id precisa ser int')
        with sqlite3.connect(self.DATABASE) as conn:
            cursor = conn.cursor()
            comando = f"DELETE * FROM {self.DATABASE} WHERE id = {id};"
            print(comando)