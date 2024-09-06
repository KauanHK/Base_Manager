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

    def _save(self, vars: dict):
        vars = {key: f"'{value}'" for key, value in vars.items()}
        colunas = ', '.join(vars.keys())
        valores = ', '.join(vars.values())
        with sqlite3.connect(self.DATABASE) as conn:
            cursor = conn.cursor()
            comando = F'INSERT INTO {self.obj.__name__} ({colunas}) values ({valores});'
            cursor.execute(comando)
            conn.commit()

    def create(self, **kwargs):
        kwargs = {key: f"'{value}'" for key, value in kwargs.items()}
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            colunas = ', '.join(kwargs.keys())
            values = ', '.join(kwargs.values())
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

    def get(self, id: int | None = None, raise_: bool = True, **kwargs):
        if isinstance(id, int):
            comando = f'SELECT * FROM {self.obj.__name__} WHERE id = {id};'

        else:
            condicoes = [f"{key} = '{value}'" for key, value in kwargs.items()]
            condicoes = ' AND '.join(condicoes)
            comando = f"SELECT * FROM {self.obj.__name__} WHERE {condicoes}"

        try:
            with sqlite3.connect(self.DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(comando)
                db_data = cursor.fetchall()
                return self.obj(*db_data[0][1:])
        except:
            if raise_ == 'raise':
                raise ValueError(f'{self.obj.__name__} com id {id} não foi encontrado.')
            else:
                return raise_
                
                
    def delete(self, id: int | None = None, obj = None, **kwargs):
        if isinstance(id, int):
            comando = f"DELETE FROM {self.obj.__name__} WHERE id = {id};"
        elif obj is not None:
            items = vars(obj).items()
            condicoes = [f"{key} = '{value}'" for key, value in items]
            condicoes = ' AND '.join(condicoes)
            comando = f"DELETE FROM {self.obj.__name__} WHERE {condicoes};"
        else:
            condicoes = [f"{key} = '{value}'" for key, value in kwargs.items()]
            condicoes = ' AND '.join(condicoes)
            comando = f"DELETE FROM {self.obj.__name__} WHERE {condicoes}"

        with sqlite3.connect(self.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(comando)
            conn.commit()