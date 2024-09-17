from fastapi import FastAPI
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

class DataBase(BaseModel):
    db_id : UUID = Field(default_factory = uuid4)
    db_name : str

class Query(DataBase):
    q : str

# create database file name 
def mk_name(db_name, db_id):
    return db_name + '-' + str(db_id) + '.db'

def execute_query(query):
    try:
        database_name = mk_name(query.db_name, query.db_id)
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cur.execute(query.q)
        conn.commit()
        conn.close()

        return {'msg': 'query executed'}

    except Exception as e:
        return {'msg': str(e)}

@app.get('/')
def index():
    return {'msg': 'Hello, world'}

@app.put('/create_db')
def create_db(db : DataBase):
    try:
        database_name = mk_name(db.db_name, db.db_id)
        conn = sqlite3.connect(database_name)
        conn.close()

        return {
            'msg': f'conncted to {database_name}',
            'db_name': database_name
        }
    
    except Exception as e:
        return {'msg': str(e)}

@app.put('/create_table')
def create_table(query : Query):
    return execute_query(query)

@app.put('/execute_query')
def execute_query_endpoint(query : Query):
    return execute_query(query)
