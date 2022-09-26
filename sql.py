import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd


def create_connection():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        #conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        engine = create_engine(DATABASE_URL)
    except:
        username = "cwtcmzqujpmszj"
        password = "d9717d1ad9420277ea4b7a2332885a6e7cbc39073d29a0cfd9f733d2df6835b6"
        host_name = "ec2-44-206-197-71.compute-1.amazonaws.com"
        db_name = "d3fpg63d3qj0lt"
        #conn = psycopg2.connect(f"postgresql://{username}:{password}@{host_name}/{db_name}")
        engine = create_engine(f"postgresql://{username}:{password}@{host_name}/{db_name}")

    return engine 

def get_site_list():
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
    conn.close()
    return df

def upload_observation(datetime, parameter, reference_elevation, observation, site, notes):
    engine = create_connection()    
    try:
        math = float(reference_elevation)-float(observation)
    except:
        math=""
    df = {'site': [site], 'datetime': [datetime], 'parameter': [parameter],'observation': [math], 'notes': [notes]}
    df = pd.DataFrame(data=df)
    #df.to_sql('field_observations', cur, if_exists='append')
    df.to_sql('observations', engine, if_exists='append',index=False)

    df = "submitted"
    return df

def get_observations():
    engine = create_connection()
    conn = engine.raw_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM observations;")
    db_obs = pd.DataFrame(cur.fetchall(), columns=['site', 'datetime', 'parameter', 'observation', 'notes'])
    return db_obs

def update_observations(df):
    engine = create_connection()        
    df.to_sql('observations', engine, if_exists='replace',index=False)
    statement = "updated"
    return statement

