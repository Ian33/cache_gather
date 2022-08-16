from dash import Dash, callback, html, dcc, html, Input, Output
from sqlalchemy import create_engine
import sqlalchemy
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku

# Instantiate dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Your app title" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Hi. I'm your Dash app."""), html.Br()])
    
    # Body 
    # body = html.Div([dcc.Markdown(""" ## I'm ready to serve static files on Heroku. Just look at this! """), html.Br(), html.Img(src='charlie.png')])
    
    
    all_options = {
        'America': ['New York City', 'San Francisco', 'Cincinnati'],
        'Canada': [u'Montréal', 'Toronto', 'Ottawa']
    }
    
    username = "fefwnlolmwdfap"
    password = "1ecfbf257fe1dfab544971996e815feab76ea41b7833def47fdbbeaa32b61a26"
    host_name = "ec2-18-204-142-254.compute-1.amazonaws.com"
    db_name = "dejak6ljiumpji"
    engine = create_engine(f"postgresql://{username}:{password}@{host_name}/{db_name}")
 
    #sites.to_sql('sites', engine)
    #sites.to_sql('sites', engine, if_exists='replace')

    #sites.to_sql("sites", con = engine, if_exists='append')

    sql = "select * from sites"
    df = pd.read_sql(sql,con=engine)
 
    site_list = df["site_number"].to_list()

    
    body = html.Div([
        #dcc.Dropdown(options=[{'label': k, 'value': k} for k in all_options.keys()],
        dcc.Dropdown(options=[{'label': k, 'value': k} for k in all_options],
        value='NYC',
        id='demo-dropdown'),
        html.Div(id='dd-output-container')
        ])

        
    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown("""test""")])
    
    # Assemble dash layout 
    app.layout = html.Div([header, body, footer])

    return app

# Construct the dash layout
create_dash_layout(app)

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'

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
