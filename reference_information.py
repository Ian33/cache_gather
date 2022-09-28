import os 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

def get_reference_information(site_list_value):
  
    if site_list_value == "":
        return [""], "", ""
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

        cur.execute(f"select reference_elevation from sites where site_number = '{site_list_value}'")
        df = pd.DataFrame(cur.fetchall(),columns=['reference_elevation'])
        reference_elevation = df["reference_elevation"].tolist()
        reference_elevation = str(reference_elevation[0])
        reference_elevation = ""
        # observation
        observation = ""

        # output
        output = f"site: {site_list_value}, elevation: {reference_elevation}, elevation of: "", observation: {observation}"
        conn.close()
        return reference_elevation, observation, output

def get_parameters(site_list_value):
    if site_list_value == "":
        return [""]
    
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
        cur.execute(f"SELECT parameter FROM parameter WHERE site = '{site_list_value}';")
        
        dfp = pd.DataFrame(cur.fetchall())
        parameter_options = dfp[0].to_list()
        
        #print(parameter_options)
        conn.close()
        #parameter_options = ["water_level", "water_temperature"]
        return parameter_options

def get_parameter_references(site_list_value, parameter_options, parameter_dropdown_value):
    # list of measureing locations for a parameter at a site
    # tbl parameter column reference_information
    # parameter_references_options

    # list of actual datum for survey info ie 270 ft for a survey location of top of tube
    # tbl parameter column reference point
    # reference_point

    # list of measureing locations for a parameter at a site
    # tbl parameter column reference_information
    # parameter_references_options
    # automatically select first reference from parameter_references_options
    # parameter_references_value
    #parameter_references_options, reference_point, parameter_references_value
    
    if parameter_dropdown_value == "":
        return [""], [""], ""
    
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
        cur.execute(f"SELECT reference_point, reference_information FROM parameter WHERE (site = '{site_list_value}' AND parameter = '{parameter_dropdown_value}');")
        dfp = pd.DataFrame(cur.fetchall())

       
        # list of measureing locations for a parameter at a site
        # tbl parameter column reference_information
        # parameter_references_options
        parameter_references_options = dfp[1].to_list()

        # list of actual datum for survey info ie 270 ft for a survey location of top of tube
        # tbl parameter column reference point
        # reference_point
        reference_point = dfp[0].to_list()

        # list of measureing locations for a parameter at a site
        # tbl parameter column reference_information
        # parameter_references_options
        # automatically select first reference from parameter_references_options
        # parameter_references_value
        parameter_references_value = parameter_references_options[0]
       
        conn.close()
        # list of measureing locations for a parameter at a site
        # tbl parameter column reference_information
        # parameter_references_options

        # list of actual datum for survey info ie 270 ft for a survey location of top of tube
        # tbl parameter column reference point
        # reference_point

        # list of measureing locations for a parameter at a site
        # tbl parameter column reference_information
        # parameter_references_options
        # automatically select first reference from parameter_references_options
        # parameter_references_value
        #parameter_references_options, reference_point, parameter_references_value
        return parameter_references_options, reference_point, parameter_references_value
