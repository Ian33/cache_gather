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

from sql import get_site_list, upload_observation
df = get_site_list() 

dropdown = html.Div([
        dcc.Dropdown(options=df, value='', id='site_list_dropdown'),
        html.Div(id='dd-output-container',
        style={'display': 'none'}), 
    ])

parameter = html.Div([
        # list of available parameters based on site selected
        # tbl parameter column parameter (cfs, wl_feet, deg c)
        dcc.Dropdown(value='', id='parameter_dropdown'),
        html.Div(id='parameter_container',
        style={'display': 'none'}), 
        # list of measureing locations for a parameter at a site
        # tbl parameter column reference_information
        dcc.RadioItems(value = '', id = 'parameter_references',
        options=[""],
        inline=True,
        style={'display': 'none'}, 
        ),
        # list of actual datum for survey info ie 270 ft for a survey location of top of tube
        # tbl parameter column reference point
        # html children to store number for reference (ie stores 200 feet for a top of tube)
        html.Div(id='reference_point',
             children='reference_point',
             style={'display': 'none'}, )
    ])

date_time = html.Div([
        html.Div([
            html.Div(dcc.Input(id="date", type='text', placeholder="", value=""), 
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '15px',
                    "border-radius": "10px"}
            ),
            html.Div(dcc.Input(id="time_hour", type='number', placeholder="", value="", min=0, max=24, step=1),
                #style={'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
            html.Div(dcc.Input(id="time_minute", type='number', placeholder="", value="", min=0, max=60, step=1),
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
            # text box that displays elevation of selected reference point
            html.Div(dcc.Input(id="reference_elevation", type='number', placeholder="", value="elevation"),
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"}
            ),
            # text input for field observation
            html.Div(dcc.Input(id="observation", type='number', placeholder="", value=""),
                #style={'width': '30%', 'display': 'inline-block'}
                style={'display': 'inline-block',
                    'margin-right': '5px',
                    "border-radius": "10px"},
                
            ),
           
        ]),
    ])

text_box = html.Div([
    dcc.Textarea(
        id='notes_text_box',
        value='',
        style={'width': '100%', 'height': 50},
    ),
    html.Div(id='notes_text_box_output', 
        style={'whiteSpace': 'pre-line'})
    ])
    
button = html.Div([
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='button_text',
             children='Enter a value and press submit')
    ])

layout = html.Div([dropdown, parameter, date_time, reference_input, text_box, button])

from reference_information import get_reference_information, get_parameters, get_parameter_references
#from sql import get_parameters

# reference elevation ability
@callback(
    Output('reference_elevation', "disabled"),
    Input('parameter_dropdown', 'value'),
)
def reference_elevation_ability(parameter_dropdown_value):
    if parameter_dropdown_value == 'water_level':
        disabled = False
    else:
        disabled = True
    return disabled

#""" get site from dropdown and returns reference elevation """
@callback(
    
    Output('dd-output-container', 'children'),
    Output('date', 'value'),
    Output('time_hour', 'value'),
    Output('time_minute', 'value'),
    # list of available parameters based on site selected
    # tbl parameter column parameter (cfs, wl_feet, deg c)
    Output('parameter_dropdown', 'options'),
    # list of measureing locations for a parameter at a site
    # tbl parameter column reference_information
    Output('parameter_references', 'options'),
    # automatically select first reference
    Output('parameter_references', 'value'),
    # list of actual datum for survey info ie 270 ft for a survey location of top of tube
    # tbl parameter column reference point
    # html children to store number for reference (ie stores 200 feet for a top of tube)
    Output('reference_point', 'children'),
    # text box that displays elevation of selected reference point
    Output("reference_elevation", 'value'),
    # text input for field observation
    Output("observation", 'value'),

    Input("site_list_dropdown", 'value'),
    Input('parameter_dropdown', 'value'),
)

def update_output(site_list_value, parameter_dropdown_value):
    #observation, output = get_reference_information(site_list_value)
    #
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time_hour = datetime.datetime.now().strftime('%H')
    time_minute = datetime.datetime.now().strftime('%M')

    parameter_options = get_parameters(site_list_value)
    parameter_references_options, reference_point, parameter_references_value = get_parameter_references(site_list_value, parameter_options, parameter_dropdown_value)

    dd_output_container = ""
    date = date
    time_hour = time_hour
    time_minute = time_minute
    # list of available parameters based on site selected
    # tbl parameter column parameter (cfs, wl_feet, deg c)
    parameter_dropdown = parameter_options
    # list of measureing locations for a parameter at a site
    # tbl parameter column reference_information
    parameter_references_options = parameter_references_options
    # automatically select first reference
    parameter_references_value = parameter_references_value
    # list of actual datum for survey info ie 270 ft for a survey location of top of tube
    # tbl parameter column reference point
    # html children to store number for reference (ie stores 200 feet for a top of tube)
    reference_point = reference_point
    reference_elevation = reference_point[0]
    # text input for field observation
    #observation = parameter_references_value
    observation = ""

    return dd_output_container, date, time_hour, time_minute, parameter_dropdown,parameter_references_options, parameter_references_value, reference_point, reference_elevation, observation
    #return  date, time_hour, time_minute, parameter_options, reference_information, parameter_reference_value, reference_point

# update text box
@callback(
    Output('notes_text_box', 'value'),
    Output('datetime', 'children'),
    # reference elevation is pulling from parameter_reference
    #Input('parameter_references', 'value'),
    Input("reference_elevation", 'value'),
    Input("observation", 'value'),
    Input("date", "value"),
    Input("time_hour", "value"),
    Input("time_minute", "value"),
    Input("parameter_references", "value"),
    Input('parameter_dropdown', 'value'),

)

def update_output(reference_elevation, observation, date, time_hour, time_minute, parameter_reference, parameter_dropdown_value):
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
    if parameter_dropdown_value == 'water_level':
        return f"measure location: {parameter_reference} reference elevation: {reference_elevation} observation: {observation} level: {math} at {time}", time
    else:
        return f"measure location: {parameter_reference} observation: {observation} parameter: {parameter_dropdown_value} at {time}", time
#"""load info"""
@callback(
    Output('button_text', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('datetime', 'children'),
    # reference elevation is pulling from parameter_reference
    #Input('parameter_references', 'value'),
    Input("reference_elevation", 'value'),
    Input("parameter_references", 'value'),
    Input("observation", 'value'),
    Input('site_list_dropdown', 'value'),
    Input('notes_text_box', 'value'),
    Input('parameter_dropdown', 'value'),
)
def update_output(n_clicks, datetime, reference_elevation, parameter_reference, observation, site, notes, parameter):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #today = pd.to_datetime("today")
    if 'submit-val' in changed_id:
        df = upload_observation(datetime, parameter, reference_elevation, observation, site, notes)

        return df
    else:
        return dash.no_update
    
    
    
    