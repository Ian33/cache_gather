from dash import Dash, Input, Output, callback, dash_table, html, dcc
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import os
from sqlalchemy import create_engine
import psycopg2

dash.register_page(__name__)

#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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
#df = {'site': ["test two"], 'datetime': ["03/20/2022 11:56"], 'observation': ["4"], 'notes': ["a test note"]}
#df = pd.DataFrame(data=df)

# Query the database and obtain data as Python objects
conn = engine.raw_connection()
cur = conn.cursor()
cur.execute("SELECT * FROM field_observations;")
df = pd.DataFrame(cur.fetchall(), columns=['site', 'datetime', 'observation', 'notes'])


layout = html.Div([dbc.Container([
    dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], 
        id='tbl', sort_action='native', editable=True, row_deletable=True, style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },),
]),
#     html.Div([
        html.Button('upload', id='upload-val', n_clicks=0),
        html.Div(id='upload_text',
             children='submit changes')
    ])
#])
"""
@callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
 Output('datatable-upload-container', 'data'),
    Output('datatable-upload-container', 'columns'),
return df_csv.to_dict('records'), [{"name": i, "id": i} for i in df_csv.columns]
        if contents is None:  # nothing to upload
            return [{}], []
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"
"""
@callback(
    Output('upload_text', 'children'),
    Input('upload-val', 'n_clicks'),
    Input('tbl', 'data'),
    Input('tbl', 'columns'),
)
def update_output(n_clicks, data, columns):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #today = pd.to_datetime("today")
    if 'upload-val' in changed_id:
        df = pd.DataFrame(data)
        if df.empty:
            return "no data"
        else:
            #df.to_sql('field_observations', cur, if_exists='append')
            df.to_sql('field_observations', engine, if_exists='append',index=False)
            return "edits submitted"
    else:
        return dash.no_update
    
    
    
