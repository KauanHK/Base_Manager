import sqlite3
import pandas as pd
import inspect
import os
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
        self._create_table()

    def _colunas(self):
        colunas = self.get_colunas()
        for i, col in enumerate(colunas):
            colunas[i] = f'{col} INTEGER'
        return ', '.join(colunas)

    def _create_table(self):
        '''Cria a tabela do objeto se ela não existir.
        Cria o banco de dados também se não existir.'''

        # Verificar se o banco de dados existe
        if not os.path.exists(self.database):
            with open(self.database, 'w'):
                pass

        
        colunas = self._colunas()
        table = self.obj.__name__
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            comando = f"CREATE TABLE IF NOT EXISTS {table} ( id INTEGER PRIMARY KEY AUTOINCREMENT, {colunas});"
            cursor.execute(comando)
            conn.commit()

    def _save(self, vars: dict):
        vars = {key: f"'{value}'" for key, value in vars.items()}
        colunas = ', '.join(vars.keys())
        valores = ', '.join(vars.values())
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            comando = F'INSERT INTO {self.obj.__name__} ({colunas}) values ({valores});'
            cursor.execute(comando)
            conn.commit()

    def _condicoes(self, kwargs: dict):
        condicoes = [f"{key} = '{value}'" for key, value in kwargs.items()]
        return ' AND '.join(condicoes)
    
    def get_colunas(self):
        parametros = inspect.signature(self.obj.__init__)
        colunas = [col for col in parametros.parameters if col != 'self']
        return colunas

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
        condicoes = self._condicoes(kwargs)
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
        condicoes = self._condicoes(kwargs)
        return self._filter(condicoes)
        
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

    def _filter(self, condicoes):
        comando = f"SELECT * FROM {self.obj.__name__} WHERE {condicoes}"
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(comando)
            objs = []
            for linha in cursor.fetchall():
                objs.append(self.obj(*linha[1:]))
            return objs

    def to_dataframe(self, **kwargs):
        if len(kwargs.items()):
            condicoes = self._condicoes(kwargs)
            comando = f"SELECT * FROM {self.obj.__name__} WHERE {condicoes};"
        else:
            comando = f"SELECT * FROM {self.obj.__name__};"
        with sqlite3.connect(self.database) as conn:
            return pd.read_sql_query(comando, conn)
