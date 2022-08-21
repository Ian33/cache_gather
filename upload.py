import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def upload_field_observation(n_clicks, datetime, reference_elevation, reference_information, observation, site, notes):
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
    #engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host_name}/{db_name}")






    #cur.execute(f"select reference_information from sites where site_number = '{value}'")
    #df = pd.DataFrame(cur.fetchall(),columns=['reference_information'])
    #reference_information = df["reference_information"].tolist()
    #reference_information = str(reference_information[0])
    try:
        math = float(reference_elevation)-float(observation)
    except:
        math=""
    df = {'site': [site], 'datetime': [datetime], 'observation': [math], 'notes': [notes]}
    df = pd.DataFrame(data=df)
    #df.to_sql('field_observations', cur, if_exists='append')
    df.to_sql('field_observations', engine, if_exists='append',index=False)

    #sites = pd.read_csv(r"C:\Users\ianrh\Documents\cache_gather\static\site_list.csv")
    #sites = sites.set_index('site_sql_id')
    #sites.to_sql('sites', engine)
    '''
    
    cur.execute("select * from field_observations")
    df = pd.DataFrame(cur.fetchall())
    return df
    '''
    '''
    conn = engine.raw_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM field_observations;")
    df2 = pd.DataFrame(cur.fetchall())
    print("data")
    print(df2)

    cur.close()
    conn.close()
    '''
    df = "submitted"
    return df