import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def get_reference_information(value):
    if value == "":
        return "", "", "", "select site"
    else:
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
        cur.execute(f"select reference_information from sites where site_number = '{value}'")
        df = pd.DataFrame(cur.fetchall(),columns=['reference_information'])
        reference_information = df["reference_information"].tolist()
        reference_information = str(reference_information[0])

    cur.execute(f"select reference_elevation from sites where site_number = '{value}'")
    df = pd.DataFrame(cur.fetchall(),columns=['reference_elevation'])
    reference_elevation = df["reference_elevation"].tolist()
    reference_elevation = str(reference_elevation[0])

# reference_inforation
    cur.execute(f"select reference_information from sites where site_number = '{value}'")
    df = pd.DataFrame(cur.fetchall(),columns=['reference_information'])
    reference_information = df["reference_information"].tolist()
    reference_information = str(reference_information[0])

# observation
    observation = ""

# output
    output = f"site: {value}, elevation: {reference_elevation}, elevation of: {reference_information}, observation: {observation}"
    conn.close()
    return reference_elevation, reference_information, observation, output

