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
    header = html.Div([
                html.Br(),
                html.Div([
                    dcc.Markdown(""" ### Cache Gather: Hydrology Field Sheet &nbsp;"""),],
                    style={'display': 'inline-block'},
                ),
                html.Div([
                    html.Img(src=r'static/chipmunk/chipmunk_large.png', alt='image'),],
                 style={'display': 'inline-block'},
                ),
                html.Br()
            ])
    
    pages = html.Div([
            #html.Div(
                #dcc.Link(
                #    f"{page['name']} - {page['path']}", href=page["relative_path"]
                #)
            # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
            html.Div(
                    dbc.Button(f"{page['name']}",
                        outline=True,
                        color="primary",
                        size="sm",
                        href=page["relative_path"],),
                        style={
                            'display': 'inline-block',
                            'margin-right': '5px',
                            "border-radius": "10px",
                            'height':'37px', 
                            'verticalAlign': 'top',
                            }
            )
            # 'width': '5%', 
            for page in dash.page_registry.values()
        ])
    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" by: Ian Higgins """)])
    
    # Assemble dash layout 
    app.layout = html.Div([ html.Div([header, pages]),dash.page_container, html.Div([footer])])
    

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

