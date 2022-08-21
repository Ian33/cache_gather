from dash import Dash, callback, html, dcc, html, Input, Output, State
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

deployment = "web"

# Instantiate dash app
#web
#app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# local
#app = Dash(__name__)

if deployment == "web":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    server = app.server
    server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 
if deployment == "local":
    app = Dash(__name__)
# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
# web
#server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
# web
# server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

from get_site_list import query_site_list

df = query_site_list()

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Cache Gather" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown("""Cache Hydrology Field Sheet"""), html.Br()])
    
    body = html.Div([
        #dcc.Dropdown(options=[{'label': k, 'value': k} for k in all_options.keys()],
        dcc.Dropdown(options=df, value='', id='demo-dropdown'),
        html.Div(id='dd-output-container',
            style={'display': 'none'}), 
        ])

    datetime_input = html.Div([
        html.Div([
            html.Div(dcc.Input(id="date", type='text', placeholder="", value=datetime.datetime.now().strftime('%Y-%m-%d')), 
                style={'width': '30%', 'display': 'inline-block'}
            ),
            html.Div(dcc.Input(id="time_hour", type='number', placeholder="", value=datetime.datetime.now().strftime('%H'), min=0, max=24, step=1),
                style={'display': 'inline-block'}
            ),
            html.Div(dcc.Input(id="time_minute", type='number', placeholder="", value=datetime.datetime.now().strftime('%M'), min=0, max=60, step=1),
                style={'display': 'inline-block'}
            ),
        html.Div(id='datetime',
            style={'display': 'none'}), 
        ]),
    ])




    reference_input = html.Div([
        html.Div([
            html.Div(dcc.Input(id="reference_elevation", type='number', placeholder="", value="elevation"),
                style={'width': '30%', 'display': 'inline-block'}
            ),
            html.Div(dcc.Input(id="reference_inforation", type='text', placeholder="", value="information"),
                style={'width': '30%', 'display': 'inline-block'}
            ),
            html.Div(dcc.Input(id="observation", type='number', placeholder="", value=""),
                style={'width': '30%', 'display': 'inline-block'}
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
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
             children='Enter a value and press submit')
    ])

    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    app.layout = html.Div([header, body, datetime_input, reference_input, text_box, button, footer])

    # enable for web app
    if deployment == "web":
        return app
    if deployment == "local":
        pass

# Construct the dash layout
create_dash_layout(app)

from reference_information import get_reference_information
@app.callback(
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
@app.callback(
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
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('datetime', 'children'),
    Input("reference_elevation", 'value'),
    Input("reference_inforation", 'value'),
    Input("observation", 'value'),
    Input('demo-dropdown', 'value'),
    Input('text_box', 'value'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, datetime, reference_elevation, reference_information, observation, site, notes, value):
    df = upload_field_observation(n_clicks, datetime, reference_elevation, reference_information, observation, site, notes, value)
    string = 'The input value was "{}" and the button has been clicked {} times'.format(value, n_clicks)
    return string
#
if deployment == 'web':
   if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
if deployment == "local": 
    if __name__ == '__main__': app.run_server(debug=True)
# Run flask app
# web 
# if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
# local
# if __name__ == '__main__': app.run_server(debug=True)

