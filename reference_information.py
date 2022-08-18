import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def get_reference_information(value):
    def query(value):
    
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f"select datum from sites")
        #df = pd.DataFrame(cur.fetchall())
        df = pd.DataFrame(cur.fetchall(),columns=['datum'])
        df = df["datum"].to_list()
        
    if value == "":
        return {""}
    else:
        data = query(value)
        return data
