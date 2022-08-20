import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def query_site_list():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        username = "cwtcmzqujpmszj"
        password = "d9717d1ad9420277ea4b7a2332885a6e7cbc39073d29a0cfd9f733d2df6835b6"
        host_name = "ec2-44-206-197-71.compute-1.amazonaws.com"
        db_name = "d3fpg63d3qj0lt"
        conn = psycopg2.connect(f"postgresql://{username}:{password}@{host_name}/{db_name}")
    cur = conn.cursor()
    cur.execute("select site_number from sites")
    #df = pd.DataFrame(cur.fetchall())
    df = pd.DataFrame(cur.fetchall(),columns=['site_number'])
    df = df["site_number"].to_list()
    
    return(df)