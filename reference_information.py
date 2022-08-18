import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def get_reference_information(value):
    if value == "":
        return [{'label': "", 'value': ""}]
    else:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f"select reverence_information from sites where site_number = '{value}'")
        df = pd.DataFrame(cur.fetchall(),columns=['reverence_information'])
        df = df["reverence_information"].tolist()
        return [{'label': i, 'value': i} for i in df]
        #return df
