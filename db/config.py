import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DB:
    con = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port="5432"
    )

    cur = con.cursor()

    def select(self, **where):
        fields = ','.join(self.fields) if self.fields else '*'
        table_name = self.__class__.__name__.lower()
        query = f"""select {fields} from {table_name}"""
        self.cur.execute(query)
        return self.cur

    def insert_into(self, **params):
        fields = ','.join(params.keys())
        values = tuple(params.values())
        table_name = self.__class__.__name__.lower()
        query = f"""insert into {table_name}({fields}) values ({','.join(['%s'] * len(params))})"""

        self.cur.execute(query, values)
        self.con.commit()

    def delete(self, **kwargs):
        t = list(kwargs.keys())
        t.append(' ')
        table_name = self.__class__.__name__.lower()
        table_field = " = %s,".join(t).strip(', ')
        params = tuple(kwargs.values())
        query = f"""delete from {table_name} where {table_field}"""
        self.cur.execute(query, params)
        self.con.commit()

    def update(self, user_id: str, **kwargs):
        table_name = self.__class__.__name__.lower()
        f = list(kwargs.keys())
        f.append(' ')
        set_fields = " = %s,".join(f).strip(', ')
        params = list(kwargs.values())
        params.append(user_id)
        query = f"""update {table_name} set {set_fields} where user_id=%s"""
        self.cur.execute(query, params)
        self.con.commit()