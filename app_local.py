from dash import Dash, callback, html, dcc, html, Input, Output

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
#import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku
import os 
from sqlalchemy import create_engine
import psycopg2
# Instantiate dash app
#app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app = Dash(__name__)

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
#server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
#server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

from get_site_list import query_site_list

df = query_site_list()

# can delete this
#engine = create_engine(DATABASE_URL)

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Hydrology Field Sheet" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown("""Hydrology Field Sheet"""), html.Br()])
    
    body = html.Div([
        #dcc.Dropdown(options=[{'label': k, 'value': k} for k in all_options.keys()],
        dcc.Dropdown(options=df,
            value='',
            id='demo-dropdown'),
        html.Div(id='dd-output-container', style={'display': 'none'}), 
        ])

    reference_input = html.Div([
        html.Div([
            html.Div(dcc.Input(id="reference_elevation", type='number', placeholder="", value="elevation"), style={'width': '30%', 'display': 'inline-block'}
            ),
            html.Div(dcc.Input(id="reference_inforation", type='text', placeholder="", value="information"), style={'width': '30%', 'display': 'inline-block'}
            ),
            html.Div(dcc.Input(id="observation", type='number', placeholder="", value=""), style={'width': '30%', 'display': 'inline-block'}
            ),
        ]),
    ])

    text_box = html.Div([
    dcc.Textarea(
        id='text_box',
        value='',
        style={'width': '100%', 'height': 300},
    ),
    html.Div(id='text_box_output', style={'whiteSpace': 'pre-line'})
    ])
        
    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    app.layout = html.Div([header, body, reference_input, text_box, footer])

    # enable for web app
    #return app

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
    Input("reference_elevation", 'value'),
    Input("reference_inforation", 'value'),
    Input("observation", 'value'),
)

def update_output(reference_elevation, reference_information, observation):
    try:
        math = float(reference_elevation)-float(observation)
    except:
        math = "nothing"
    return f"measure location: {reference_information} reference elevation: {reference_elevation} observation: {observation} level: {math} "
    
#


# Run flask app
#if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
if __name__ == '__main__':
    app.run_server(debug=True)

