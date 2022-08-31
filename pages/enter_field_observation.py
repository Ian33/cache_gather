from dash import Dash, callback, html, dcc, html, Input, Output
import dash
#import dash_datetimepicker
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import datetime
#import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku
import os 
from sqlalchemy import create_engine
import psycopg2

dash.register_page(__name__)
from sql import get_site_list

df = get_site_list()    
dropdown = html.Div([
        dcc.Dropdown(options=df, value='', id='demo-dropdown'),
        html.Div(id='dd-output-container',
        style={'display': 'none'}), 
    ])
date_time = html.Div([
        html.Div([
            html.Div(dcc.Input(id="date", type='text', placeholder="", value=datetime.datetime.now().strftime('%Y-%m-%d')), 
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '15px',
                    "border-radius": "10px"}
            ),
            html.Div(dcc.Input(id="time_hour", type='number', placeholder="", value=datetime.datetime.now().strftime('%H'), min=0, max=24, step=1),
                #style={'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
            html.Div(dcc.Input(id="time_minute", type='number', placeholder="", value=datetime.datetime.now().strftime('%M'), min=0, max=60, step=1),
                #style={'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
        html.Div(id='datetime',
            style={'display': 'none'}), 
        ]),
    ])

reference_input = html.Div([
        html.Div([
            html.Div(dcc.Input(id="reference_elevation", type='number', placeholder="", value="elevation"),
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
            html.Div(dcc.Input(id="reference_inforation", type='text', placeholder="", value="information"),
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
            html.Div(dcc.Input(id="observation", type='number', placeholder="", value=""),
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
        ]),
    ])

text_box = html.Div([
    dcc.Textarea(
        id='text_box',
        value='',
        style={'width': '100%', 'height': 50},
    ),
    html.Div(id='text_box_output', 
        style={'whiteSpace': 'pre-line'})
    ])
    
button = html.Div([
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='button_text',
             children='Enter a value and press submit')
    ])

layout = html.Div([dropdown, date_time, reference_input, text_box, button])

from reference_information import get_reference_information
@callback(
    Output("reference_elevation", 'value'),
    Output("reference_inforation", 'value'),
    Output("observation", 'value'),
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value'),
)

def update_output(value):
    reference_elevation, reference_information, observation, output = get_reference_information(value)
    return reference_elevation, reference_information, observation, output

# update text box
@callback(
    Output('text_box', 'value'),
    Output('datetime', 'children'),
    Input("reference_elevation", 'value'),
    Input("reference_inforation", 'value'),
    Input("observation", 'value'),
    Input("date", "value"),
    Input("time_hour", "value"),
    Input("time_minute", "value")

)

def update_output(reference_elevation, reference_information, observation, date, time_hour, time_minute):
    try:
        math = float(reference_elevation)-float(observation)
        #time = datetime(date, time_hour, time_minute, 0)
    except:
        math = "nothing"
        time = 'no time'
    try:
        time = f"{date} {time_hour}:{time_minute}"
    except:
        time = ""
    return f"measure location: {reference_information} reference elevation: {reference_elevation} observation: {observation} level: {math} at {time}", time
from upload import upload_field_observation
@callback(
    Output('button_text', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('datetime', 'children'),
    Input("reference_elevation", 'value'),
    Input("reference_inforation", 'value'),
    Input("observation", 'value'),
    Input('demo-dropdown', 'value'),
    Input('text_box', 'value'),
)
def update_output(n_clicks, datetime, reference_elevation, reference_information, observation, site, notes):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #today = pd.to_datetime("today")
    if 'submit-val' in changed_id:
        df = upload_field_observation(n_clicks, datetime, reference_elevation, reference_information, observation, site, notes)
        return df
    else:
        return dash.no_update
    
    
    
    