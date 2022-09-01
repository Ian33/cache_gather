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
    try:
        math = float(reference_elevation)-float(observation)
    except:
        math=""
    df = {'site': [site], 'datetime': [datetime], 'observation': [math], 'notes': [notes]}
    df = pd.DataFrame(data=df)
    #df.to_sql('field_observations', cur, if_exists='append')
    df.to_sql('observations', engine, if_exists='append',index=False)

    df = "submitted"
    return df