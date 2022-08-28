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
from get_field_observations import get_db_obs, get_engine

# db_obs.to_dict('records'),[{"name": i, "id": i} for i in db_obs.columns]
#db_obs = get_db_obs() 
layout = html.Div([
   
   
#     html.Div([
        html.Button('load field observations', id='load_val', n_clicks=0),
        html.Div(id='load_text',
             children='load'),
        html.Button('upload', id='upload_val', n_clicks=0),
        html.Div(id='upload_text',
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
    Output('tbl', 'data'),
    Output('tbl', 'columns'),
    Output('load_text', 'children'),
    Input('load_val', 'n_clicks'),
)
def get_data(load_val):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #today = pd.to_datetime("today")
    if 'load-val' in changed_id:
        db_obs = get_db_obs()
        return  db_obs.to_dict('records'), [{"name": i, "id": i} for i in db_obs.columns], "query"
    else:
        db_obs = get_db_obs()
        return  db_obs.to_dict('records'), [{"name": i, "id": i} for i in db_obs.columns], "query"
    #else:
    #    return  [{}], [], "query"
    #db_obs = get_db_obs()
    #return db_obs.to_dict('records'), [{"name": i, "id": i} for i in db_obs.columns]

@callback(
    Output('upload_text', 'children'),
    Input('upload_val', 'n_clicks'),
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
            engine = get_engine()
            #df.to_sql('field_observations', cur, if_exists='append')
            #df.to_sql('field_observations', engine, if_exists='append',index=False)
            df.to_sql('field_observations', engine, if_exists='replace',index=False)
            return "edits submitted"
    else:
        return dash.no_update