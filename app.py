import pandas as pd
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input,Output,State
import plotly.express as px
from flask_caching import Cache
from import_data import import_main_dataset
from create_graphs import *


colors={
    'background':"#161928",
    # 'background':'#b0ddfd',
    'marker':'#f3d34e',
    'navbar':"#f3d34e"
}




app = dash.Dash(name=__name__,external_stylesheets=[dbc.themes.CYBORG])
server=app.server

cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
})


def serve_layout():
    return dbc.Container([
        html.Div(id='empty_div',style={'display':'none'}),
############################################### NAVBAR  ############################################################################
        dbc.NavbarSimple(
            brand='Done by Alisher Karabaev',
            children=[
                dbc.Col([
                    dbc.Row([
                        dbc.Button(
                        "About",
                        id='about_button',
                        color="primary"
                        )
                    ],
                    justify="center"),
                    dbc.Row([
                        dbc.Collapse(
                        dbc.Card(dbc.CardBody(
                            'This is overview of houses for sell located in Madrid. \
                                All graphs are interactive, just click and you will see it :)  \
                                    To clear selection press button "Clear selection" located below. \
                                        This dashboard can also generate reports. For example, go to report generator, \
                                            choose "Districts" as object of report, "All metrics" as a metric and \
                                                "Average" as aggregation type and you will see all the averages of each metric for \
                                                    each district. Reports can be EXPORTED to EXCEL just by clicking "Export" and can \
                                                        be filtered if you put something in the row below header (you will see \
                                                            "filter data" there) '
                        ),
                        color="primary",
                        inverse=True),
                        id='about_collapse'
                        )
                    ],
                    justify='center')
                    
                    
                ]),
                dbc.Button(
                    "Go to Linkedin profile of creator",
                    href="https://www.linkedin.com/in/alisher-karabaev/",
                    color="primary"
                )
            ],
        color=colors['navbar']
        ),
        #################################### TABS #####################################################################
        dbc.Tabs([
            dbc.Tab(
                label='Analysis by districts',
                children=[
                    dbc.Row([
                        dcc.Graph(id='bubble_avg_price_by_district')
                    ],
                    justify='center'
                    )
                ]
            ),
            dbc.Tab(
                label='Analysis by house type and number of rooms',
                children=[
                    dbc.Row([
                        dcc.Graph(id='bar_avg_price_by_house_type'),
                        dcc.Graph(id='bar_avg_price_by_room_quantity')
                    ],
                    justify="center"
                    )
                    
                ]
            ),
            dbc.Tab(
                label='Report generator',
                children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                html.Div([
                                    dcc.Dropdown(
                                        id='report_object',
                                        options=[
                                            {'label':'District','value':'Neighborhood'},
                                            {'label':'House type','value':'House type'},
                                            {'label':'Number of rooms','value':'Number of rooms'}
                                        ],
                                        placeholder='Choose object of the report'
                                    )
                                ],
                                style={
                                    'width':'80%'
                                })
                                
                            ],
                            justify='start'
                            ),
                            dbc.Row([
                                html.Div([
                                    dcc.Dropdown(
                                        id='report_metric',
                                        options=[
                                            {'label':'All metrics','value':'All metrics'},
                                            {'label':'Total area (m2)','value':'Total area (m2)'},
                                            {'label':'Price (euro)','value':'Price (euro)'},
                                            {'label':'Number of rooms','value':'Number of rooms'},
                                            {'label':'Number of bathrooms','value':'Number of bathrooms'},
                                            {'label':'Price for m2 (euro)','value':'Price for m2 (euro)'}
                                        ],
                                        placeholder='Choose metric of the report'
                                    )
                                ],
                                style={
                                    'width':'80%'
                                })
                                
                            ]),

                            dbc.Row([
                                html.Div([
                                    dcc.Dropdown(
                                        id='report_aggregation',
                                        options=[
                                            {'label':'Sum','value':'Sum'},
                                            {'label':'Average','value':'Average'}
                                        ],
                                        placeholder='Choose aggregation of the report'
                                    )
                                ],
                                style={
                                    'width':'80%'
                                })
                                
                            ])
                        ],
                        width=2
                        ),
                        dbc.Col([
                            dash_table.DataTable(
                                id='table',
                                export_format='xlsx',
                                export_headers='display',
                                filter_action='native',
                                sort_action='native',
                                sort_mode='multi',
                                style_header={'backgroundColor': 'rgb(255, 255, 255)'},
                                style_cell={
                                    'backgroundColor': 'rgb(255, 255, 255)',
                                    'color': 'black',
                                    'textAlign':'left'
                                },
                                style_as_list_view=True,
                                page_size=20
                            )
                        ])
                    ],
                    justify='start'
                    )
                ]
            )
        ]),

        ######################################### LEDS  #################################################################
        dbc.Row([
            html.H1(
                id='led_labels',
                style={
                    'color':colors['marker'],
                    'font-size':'50px'
                }
            )
        ],
        justify='center'
        ),
        dbc.Row([
                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "Average area (m2)",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_average_area',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ]),

                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "Average price (euro)",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_average_price',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ]),

                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "Average number of rooms",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_average_number_of_rooms',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ]),

                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "Number of houses",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_number_of_houses',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ])

                

                       

            ],
            justify='center'
            ),

            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "Renewal needed (%)",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_renewal_needed',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ]),

                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "Average number of bathrooms",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_average_number_of_bathrooms',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ]),
                

                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "With lift (%)",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_lift',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ]),

                dbc.Col([
                    dbc.Row([
                        html.H1(
                            "With parking (%)",
                            style={
                                'color':colors['marker'],
                                'font-size':'35px'
                            }
                        )
                    ],
                    justify='center'
                    ),
                    dbc.Row([
                        daq.LEDDisplay(
                            id='led_parking',
                            backgroundColor=colors['background']
                        )
                    ],
                    justify='center'
                    )
                ])
            ],
            justify='center'
            ),
            dbc.Row([
                dbc.Button(
                    "Clear selection",
                    id='clear_selection_button',
                    color='primary'
                )
            ],
            justify='center')

    ],
    fluid=True)



@app.callback(
    Output('about_collapse','is_open'),
    [Input('about_button','n_clicks'),
    State('about_collapse','is_open')]
)
@cache.memoize(timeout=0)
def open_close_about_collapse(button_clicks,is_open):
    if button_clicks:
        return not is_open
    return is_open

@app.callback(
    Output('bar_avg_price_by_house_type','figure'),
    [Input('empty_div','children')]
)
@cache.memoize(timeout=0)
def callback_generate_bar_avg_price_by_house_type(empty_input):
    df=import_main_dataset()
    df=df[['House type','Price for m2 (euro)']].groupby('House type',as_index=False).mean().sort_values(by='Price for m2 (euro)')
    figure=generate_bar_chart(df,colors,'Average price for square meter by house type')
    return figure

@app.callback(
    Output('bar_avg_price_by_room_quantity','figure'),
    [Input('empty_div','children')]
)
@cache.memoize(timeout=0)
def callback_generate_bar_avg_price_by_room_quantity(empty_input):
    df=import_main_dataset()
    df=df[['Number of rooms','Price for m2 (euro)']].groupby('Number of rooms',as_index=False).mean().sort_values(by='Price for m2 (euro)')
    figure=generate_bar_chart(df,colors,"Average price for square meter by number of rooms")
    return figure
    
@app.callback(
    [Output('led_labels','children'),
    Output('led_average_area','value'),
    Output('led_average_price','value'),
    Output('led_average_number_of_rooms','value'),
    Output('led_average_number_of_bathrooms','value'),
    Output('led_renewal_needed','value'),
    Output('led_number_of_houses','value'),
    Output('led_lift','value'),
    Output('led_parking','value')],
    [Input('bar_avg_price_by_house_type','clickData'),
    Input('bar_avg_price_by_room_quantity','clickData'),
    Input('bubble_avg_price_by_district','clickData'),
    Input('clear_selection_button','n_clicks')]
)
@cache.memoize(timeout=0)
def callback_update_leds(clickData1,clickData2,clickData3,clear_button):
    df=import_main_dataset()
    changed_id=[p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'bar_avg_price_by_house_type' in changed_id:
        clicked_item=clickData1['points'][0]['x']
        df=df[df['House type']==clicked_item]
        label="Overview of " + clicked_item + " houses"
    elif 'bar_avg_price_by_room_quantity' in changed_id:
        clicked_item=clickData2['points'][0]['x']
        df=df[df['Number of rooms']==clicked_item]
        label="Overview of "+ str(clicked_item)+ "-room houses"
    elif 'bubble_avg_price_by_district' in changed_id:
        clicked_item=clickData3['points'][0]['x']
        df=df[df['Neighborhood']==clicked_item]
        label="Overview of houses from "+ clicked_item
    else:
        label="Overview of all houses"

    average_area=round(df['Total area (m2)'].mean(),0)
    average_price=round(df['Price (euro)'].mean(),0)
    average_number_of_rooms=round(df['Number of rooms'].mean(),2)
    average_number_of_bathrooms=round(df['Number of bathrooms'].mean(),2)
    renewal_needed=round(df['Is renewal needed'].mean()*100,0)
    number_of_houses=len(df)
    lift=round(df['Has lift'].mean()*100,0)
    parking=round(df['Has parking'].mean()*100,0)
    return label,average_area,average_price,average_number_of_rooms,\
    average_number_of_bathrooms,renewal_needed,number_of_houses,lift,parking


@app.callback(
    Output('bubble_avg_price_by_district','figure'),
    [Input('empty_div','children')]
)
@cache.memoize(timeout=0)
def callback_generate_bubble_avg_price_by_district(empty_div):
    df=import_main_dataset()
    df=df[['Neighborhood','Price for m2 (euro)']].groupby('Neighborhood').agg(['mean','count']).reset_index()
    df.columns=['District','Average price for m2 (euro)','Number of houses']
    df=df.sort_values(by='Average price for m2 (euro)')
    figure=generate_bubble_chart(df,colors,"Average price and number of houses by district")
    return figure

@app.callback(
    [
        Output('table','data'),
        Output('table','columns')
    ],
    [
        Input('report_object','value'),
        Input('report_metric','value'),
        Input('report_aggregation','value'),
        State('table','data'),
        State('table','columns')
    ]
)
@cache.memoize(timeout=0)
def callback_generate_table(object,metric,aggregation,initial_data,initial_columns):
    if all([object,metric,aggregation]):
        df=import_main_dataset()
        if metric=='All metrics':
            df=df[[object,'Total area (m2)','Price (euro)','Number of rooms','Number of bathrooms','Price for m2 (euro)']]
        else:
            df=df[[object,metric]]
        if aggregation=='Sum':
            df=df.groupby(object,as_index=False).sum()
        else:
            df=df.groupby(object,as_index=False).mean()
        return df.to_dict('records'), [{'name':i,"id":i} for i in df.columns]
    else:
        return initial_data,initial_columns


app.layout=serve_layout
if __name__ == '__main__':
    app.run_server(debug=False)





