import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def query_site_list():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("select site_number from sites")
    #df = pd.DataFrame(cur.fetchall())
    df = pd.DataFrame(cur.fetchall(),columns=['site_number'])
    df = df["site_number"].to_list()
    return(df)