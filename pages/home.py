import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.Div(children='Cache Gather field data sheet'),
    html.Div(children='Uses Cache table structure to store field observations to cloud server'),
    html.Div(children='relies on local python script to:'),
    html.Div(children='- push observations to KC gData'),
    html.Div(children='- pull site list from KC gData'),
    html.Div(children='- pull site list from KC gData'),
    html.Div(children='- developed by: Ian H.'),
    dcc.Link(f"GitHub", href="https://github.com/Ian33")
])