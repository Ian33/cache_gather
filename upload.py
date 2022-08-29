import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def upload_field_observation(n_clicks, datetime, reference_elevation, reference_information, observation, site, notes):
    from sql import get_engine
    engine = get_engine()

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