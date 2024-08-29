import sqlite3
import os
from typing import Callable, Literal, Union


class BaseManager:

    def __init__(self, obj_type, db_name: str = 'db.sqlite3'):
        self.obj_type = obj_type
        self.obj_name = self.obj_type.__name__
        self.db_name = db_name.lower()
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.obj_name} (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           width INTEGER,
                           height INTEGER
                           )
        """)
            conn.commit()

    def _save(self, obj):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            varss = vars(obj)
            colunas = ', '.join(varss.keys())
            formated = ', '.join([str(var) for var in varss.values()])
            comando = f"INSERT INTO {self.obj_name} ({colunas}) values ({formated})"
            print(comando)
            cursor.execute(comando)
            conn.commit()
            


    def _get_rect_by_id(self, id: int):
        for rect in self.objects:
            if rect.id == id:
                return rect

    def remove(self, obj: Union["Rect", None] | None = None, id: int | None = None):
        if isinstance(id, int):
            obj = self._get_obj_by_id(id)
            if obj is None:
                raise ValueError(f'Nenhum Rect com id {id} foi encontrado.')
        elif isinstance(self.obj_type, obj.__class__.__name__):
            for rec in self.objects:
                if rec.id == obj.id:
                    self.objects.remove(rec)
        
                

    def all(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            comando = f"SELECT * FROM {self.obj_name}"
            cursor.execute(comando)
            db_objs = cursor.fetchall()

            # Remover ID
            db_objs = [list(db_obj)[1:] for db_obj in db_objs]
            objs = [self.obj_type(*obj) for obj in db_objs]
            return objs
    
    def get(self, id: int | None = None, by: Literal['width', 'height', 'area'] | None = None, key: Callable | None = max):
        if isinstance(id, int):
            rect = self._get_rect_by_id(id)
            if rect is None:
                raise ValueError(f'Nenhum Rect com id {id} foi encontrado.')
        elif callable(key):
            funcs = {
                'width': lambda rect: rect.width,
                'height': lambda rect: rect.height,
                'area': lambda rect: rect.area,
            }

            if by not in funcs:
                raise ValueError(f'Valor inválido para by: {by}')
            func = funcs[by]
            try:
                rect = key(self.objects, key=func)
            except Exception as e:
                raise Exception(f'Erro: {e}')
            return rect
        
    def filter(self, by: int, key: Callable | None = max):
        if by == By.AREA:
            return key(self.objects, key=lambda rect: rect.area)