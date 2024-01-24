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
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                options = [ {'label':'All Sites','value':'ALL'},
                                            {'label': 'CCAFSLC-40','value':'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                            {'label': 'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A','value':'KSC LC-39A'},
                                            ],
                                value='ALL',
                                placeholder="Select a Launch Site",
                                searchable=True
                                            ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload,max_payload],
                                    marks={
                                        0:{'label':'0 Kg'},
                                        2500:{'label':'2500 Kg'},
                                        5000:{'lable':'5000 Kg'},
                                        7500:{'label':'7500 Kg'},
                                        10000:{'label':'10000 Kg'}
                                    }
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scarter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
)
def get_pie(value):
    aux_df=spacex_df
    if value=='ALL':
        fig=px.pie(aux_df,values='class',names='Launch Site',title='Total Success Launches By Site')
        return fig
    else:
        aux_df = spacex_df[spacex_df['Launch Site']==value].groupby(['Launch Site','class']).size().reset_index(name='class count')
        title=f"Total Succes Launches for site {value}"
        fig=px.pie(aux_df,values='class count',names='class',title=title)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scarter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload):            
                                        low, high =selected_payload
                                        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
                                        filtered_df1 = spacex_df[mask]
                                        if  selected_site =='ALL':
                                            fig = px.scatter(filtered_df1, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                            title='Correlation of Payload and Successful Missions for All Sites')
                                            return fig
                                        else:
                                            filtered_df2= filtered_df1[filtered_df1['Launch Site'] ==  selected_site]
                                            fig = px.scatter(filtered_df2, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                            title=f'Correlation of Payload and Successful Missions for site {selected_site}')
                                            return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
