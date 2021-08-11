"""
This is a part of my final work in IBM Data Science course.
Its purpose is to create a Dashboard with Plotly Dash.
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[{'label': 'ALL', 'value': 'all'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                                value='all',
                                                placeholder='Select a Launch Site here',
                                                searchable=True),
                                html.Br(),

                                # Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[min_payload, max_payload]),

                                # Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))

def get_graph(site):
    if site == 'all':
        data = spacex_df[spacex_df['class'] == 1].groupby(['Launch Site'], as_index=False).count()
        pie_fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launch by all Sites')
    else:
        data = spacex_df[spacex_df['Launch Site'] == site].groupby(['class'], as_index=False).count()
        pie_fig = px.pie(data, values='Launch Site', names='class', title='Total Success Launch by ' + site)
        
    return pie_fig
    
    
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value'))
                
def get_second_graph(site, year):
    data = spacex_df[(spacex_df['Payload Mass (kg)'] < year[1]) & (spacex_df['Payload Mass (kg)'] > year[0])]
    if site == 'all':
        scatter_fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload (kg) and Landing Outcomes for all Sites ')
    else:
        data = data[data['Launch Site'] == site]
        scatter_fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload (kg) and Landing Outcomes for ' + site)
    
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
