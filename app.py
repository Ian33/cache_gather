from dash import Dash, callback, html, dcc, html, Input, Output

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku
import os 
from sqlalchemy import create_engine
import psycopg2
# Instantiate dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 
'''
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute("select site_number from sites")
#df = pd.DataFrame(cur.fetchall())
df = pd.DataFrame(cur.fetchall(),columns=['site_number'])
df = df["site_number"].to_list()

'''
from get_site_list import query_site_list

df = query_site_list()

#engine = create_engine(DATABASE_URL)
# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Your app title" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Hi. I'm your Dash app."""), html.Br()])
    
    # Body 
    # body = html.Div([dcc.Markdown(""" ## I'm ready to serve static files on Heroku. Just look at this! """), html.Br(), html.Img(src='charlie.png')])

    body = html.Div([
        #dcc.Dropdown(options=[{'label': k, 'value': k} for k in all_options.keys()],
        dcc.Dropdown(options=df,
            value='',
            id='demo-dropdown'),
        html.Div(id='dd-output-container'),
        ])

    reference_dropdown = html.Div([
        dcc.RadioItems(
            value='MTL', id="reference_informationn_radio_button"),
        ])
    show_reference_elevation = html.Div([html.Div(id='refernce_elevation')])

        
    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    app.layout = html.Div([header, body, reference_dropdown, show_reference_elevation, footer])

    return app

# Construct the dash layout
create_dash_layout(app)

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'

# get reference information
from reference_information import get_reference_information, get_reference_elevation
@app.callback(
    Output('reference_informationn_radio_button', "options"),
    Input('demo-dropdown', 'value'))


def reference_informationn_get_options(value):
    reference_information = get_reference_information(value)
    return reference_information, reference_elevation
@app.callback(
    Output('refernce_elevation', 'children'),
    Input('demo-dropdown', 'value'))

def reference_elevation(value):
    reference_elevation = get_reference_elevation(value)
    return reference_elevation    
    
    
#


# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)

###
# from dash import Dash, dcc, html, Input, Output
'''
app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
    html.Div(id='dd-output-container')
])
'''
'''
@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
    '''
