import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def get_reference_information(value):
    if value == "":
        return "", "", "", "select site"

    else:
        from sql import get_engine
        engine = get_engine()
        conn = engine.raw_connection()

        cur = conn.cursor()
        cur.execute(f"select reference_information from sites where site_number = '{value}'")
        df = pd.DataFrame(cur.fetchall(),columns=['reference_information'])
        reference_information = df["reference_information"].tolist()
        reference_information = str(reference_information[0])

# reference_elevation
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

