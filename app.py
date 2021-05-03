import os
import pandas as pd
import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

#----------------------------------------------------------
# Layout

app.layout = html.Div([
    
    html.H1("Where in Europe to work as a Data Scientist?", style={'text-align': 'center'}),
    html.H2("Salary comparison & job satisfaction comparison for European countries 2017-2020", style={'text-align': 'center'}),
    
    html.H4("Choose comparison", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="slct_comparison",
            options=[
                {"label": "Salary", "value": "Salary"},
                {"label": "Job satisfaction", "value": "Job Satisfaction"},
                {"label": "Combined", "value": "Combined"}
                ],
            multi=False,
            value="Salary",
            style={"width": "100%", "height" : "40px", "display": "flex", "align-items": "center", "justify-content": "center"}
            ),
        
    html.Div(id='output_container2', children=[], style={"display": "flex", "align-items": "center", "justify-content": "center", "font-size" : "18px"}),
    
    html.Div(id='output_container3', children=[], style={"display": "flex", "align-items": "center", "justify-content": "center", "font-size" : "18px"}),
    
    html.H4("Choose year", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
            options=[
                  {"label": "2020", "value": 2020},
                  {"label": "2019", "value": 2019},
                  {"label": "2018", "value": 2018},
                  {"label": "2017", "value": 2017}],
            multi=False,
            value=2020,
               style={'width': "100%",  "display": "flex", "align-items": "center", "justify-content": "center"}
               ),
        
    html.Div(id='output_container1', children=[], style={"display": "flex", "align-items": "center", "justify-content": "center", "font-size" : "18px"}),
    
    dcc.Graph(
    id="my_comp_map",
    figure={
        "layout": {
            "title": "My Dash Graph",
            "height": 1400,  # px
        },
    },
)
    
    
])

#----------------------------------------------------------
# Callback

df = pd.read_csv('processed_data.csv')

@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='output_container2', component_property='children'),
     Output(component_id='output_container3', component_property='children'),
     Output(component_id='my_comp_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id='slct_comparison', component_property='value')]
)

def update_graph(year_slctd, comparison_slctd):
    print('Showing: ', comparison_slctd, year_slctd)

    container1 = "The year chosen by user is: {}".format(year_slctd)
    container2 = "The comparison chosen by user is: {}".format(comparison_slctd)
    
    data = df.copy()
    data = data[data["Year"] == year_slctd]

    if comparison_slctd == "Salary":
        
        container3 =  "The values shown are the median salaries in US dollars."
        
        fig = px.choropleth(
            data_frame=data,
            locationmode='ISO-3',
            locations='Codes',
            scope="europe",
            color='Salary',
            range_color=[20000, 100000],
            hover_data=['Country', 'Salary'],
            height=1200,
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        
    elif comparison_slctd == "Combined":
        
        container3 = "The values shown are salary and job satisfaction rates combined, where 0 is the lowest and 10 the highest possible rate. Both properties are equally weighted."
        
        fig = px.choropleth(
            data_frame=data,
            locationmode='ISO-3',
            locations='Codes',
            scope="europe",
            color='Combined',
            range_color=[2, 8],
            hover_data=['Country', 'Combined'],
            height=1200,
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        
    else:     
        
        container3 = "The value shown are the average job satisfaction rates. 0 is the lowest and 10 the highest possible rate."

        fig = px.choropleth(
            data_frame=data,
            locationmode='ISO-3',
            locations='Codes',
            scope="europe",
            color='Job Satisfaction',
            range_color=[2, 8],
            hover_data=['Country', 'Job Satisfaction'],
            height=1200,
            color_continuous_scale=px.colors.sequential.Plasma,
        )

    
    return container1, container2, container3, fig


#----------------------------------------------------------
# Launch 

if __name__ == '__main__':
    app.run_server(debug=True)
