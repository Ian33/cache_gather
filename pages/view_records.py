from dash import Dash, Input, Output, callback, dash_table, html, dcc, State
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import os
from sqlalchemy import create_engine
import psycopg2

dash.register_page(__name__)

# info on updating
# https://dash.plotly.com/live-updates

# set up database connection
from sql import get_observations, update_observations, create_connection

layout = html.Div([
#     html.Div([
        html.Button('load field observations', id='load_val', n_clicks=0),
        html.Div(id='load_text',
             children='load'),
        html.Button('submit changes', id='submit_changes_button', n_clicks=0),
        html.Div(id='submit_changes_text',
             children='submit changes'),
        html.Div(dash_table.DataTable(id='tbl', sort_action='native', editable=True, row_deletable=True, 
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'}
        )),
    ])

@callback(
    Output('tbl', 'data'),
    Output('tbl', 'columns'),
    Output('load_text', 'children'),
    Input('load_val', 'n_clicks'),
)
def get_data(load_val):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #today = pd.to_datetime("today")
    if 'load_val' in changed_id:

        db_obs = get_observations()
        return  db_obs.to_dict('records'), [{"name": i, "id": i} for i in db_obs.columns], "refreshed"


    else:
        db_obs = get_observations()
        return  db_obs.to_dict('records'), [{"name": i, "id": i} for i in db_obs.columns], ""
    
@callback(
    Output('submit_changes_text', 'children'),
    Input('submit_changes_button', 'n_clicks'),
    Input('tbl', 'data'),
    Input('tbl', 'columns'),
)
def update_output(n_clicks, data, columns):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #today = pd.to_datetime("today")

    if 'submit_changes_button' in changed_id:

        df = pd.DataFrame(data)
        #if df.empty:
            #return "no data"
       # else:
        update_observations(df)
        engine = create_connection()        
        df.to_sql('observations', engine, if_exists='replace',index=False)
        return "edits submitted"
    else:

        #return dash.no_update
        return ""

