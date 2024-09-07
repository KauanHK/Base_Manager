import sqlite3
import inspect
import os

def _colunas(obj):
    colunas = get_colunas(obj)
    for i, col in enumerate(colunas):
        colunas[i] = f'{col} INTEGER'
    return ', '.join(colunas)

def get_colunas(obj):
    parametros = inspect.signature(obj.__init__)
    colunas = [col for col in parametros.parameters if col != 'self']
    return colunas

def _create_table(database: str, obj):
    '''Cria a tabela do objeto se ela não existir.
    Cria o banco de dados também se não existir.'''

    # Verificar se o banco de dados existe
    if not os.path.exists(database):
        with open(database, 'w'):
            pass
    
    colunas = _colunas(obj)
    table = obj.__name__
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        comando = f"CREATE TABLE IF NOT EXISTS {table} ( id INTEGER PRIMARY KEY AUTOINCREMENT, {colunas});"
        cursor.execute(comando)
        conn.commit()

def _save(database: str, obj, vars: dict):
    vars = {key: f"'{value}'" for key, value in vars.items()}
    colunas = ', '.join(vars.keys())
    valores = ', '.join(vars.values())
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        comando = F'INSERT INTO {obj.__name__} ({colunas}) values ({valores});'
        cursor.execute(comando)
        conn.commit()

def _condicoes(kwargs: dict):
    condicoes = [f"{key} = '{value}'" for key, value in kwargs.items()]
    return ' AND '.join(condicoes)

def _filter(database: str, obj, condicoes: dict):
    comando = f"SELECT * FROM {obj.__name__} WHERE {condicoes}"
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(comando)
        objs = []
        for linha in cursor.fetchall():
            objs.append(obj(*linha[1:]))
        return objs