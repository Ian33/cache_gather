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

deployment = "web"

# Instantiate dash app
#web
#app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# local
#app = Dash(__name__)

if deployment == "web":
    #app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], use_pages=True)
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
    server = app.server
    server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 
if deployment == "local":
    app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
# web
#server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
# web
# server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 



# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Cache Gather" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown("""Cache Hydrology Field Sheet"""), html.Br()])
    
    pages = html.Div([
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                ))
            for page in dash.page_registry.values()
        ])
    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    app.layout = html.Div([html.Div([header, pages, footer]),dash.page_container])
    

    # enable for web app
    if deployment == "web":
        return app
    if deployment == "local":
        pass

# Construct the dash layout
create_dash_layout(app)


    
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

