import sqlite3
import pandas as pd
import process
from typing import Any

class BaseManager:
    
    '''Classe para gerenciamento de banco de dados SQL'''

    def __init__(
            self,
            obj,
            database: str = 'db.sqlite3'
    ):
        '''
        Classe para gerenciamento de banco de dados SQL.
        
        Parâmetros
        ------------
            obj: A classe que contém os dados que serão armazenados
            
            database (str): Nome do arquivo sqlite3

        '''
        self.obj = obj
        self.database = database
        process._create_table(self.database, self.obj)



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
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.obj.__name__};")
            db_data = cursor.fetchall()
            db_data = [data[1:] for data in db_data]
            objs = [self.obj(*data) for data in db_data]
            return objs

    def get(self, **kwargs):
        '''Retorna o primeiro elemento da tabela cuja condição é verdadeira.
        '''
        condicoes = process._condicoes(kwargs)
        comando = f"SELECT * FROM {self.obj.__name__} WHERE {condicoes}"
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()
                cursor.execute(comando)
                db_data = cursor.fetchall()
                return self.obj(*db_data[0][1:])
        except:
            raise ValueError(f'{self.obj.__name__} com {condicoes} não foi encontrado.')
    
    def filter(self, **kwargs):
        condicoes = process._condicoes(kwargs)
        return process._filter(self.database, self.obj, condicoes)
        
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

        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(comando)
            conn.commit()

    def to_dataframe(self, **kwargs):
        if len(kwargs.items()):
            condicoes = process._condicoes(kwargs)
            comando = f"SELECT * FROM {self.obj.__name__} WHERE {condicoes};"
        else:
            comando = f"SELECT * FROM {self.obj.__name__};"
        with sqlite3.connect(self.database) as conn:
            return pd.read_sql_query(comando, conn)
