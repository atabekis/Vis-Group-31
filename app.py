import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import numpy as np
import pandas as pd
from textwrap import dedent
# --------- Importing Base Functions ------------#
import functions.config as config
from functions.mapboxplot import Mapboxplot
from functions.choropleth_mapbox import Choropleth
from functions.histogram import Histogram
from functions.treemap import TreeMap

"""
JBI100 - Visualizations Final Project
Group No: 31
Bartan Ören, Luc Tortike, Ata Bekişoğlu, Sarp Akar
--------------------------------------------------------------------------------------------------------------
This app.py file is seperated into multiple building functions for the construction of the Dash web application.

->The html part of the code can be found in the builder functions such as 'build_banner()' and others. These are then 
  combined within each other and in the app.layout line. 
  
->The styling (CSS) part of the web application can be found in the 'assets' directory. The dash library automatically
  includes the styling given className as a parameter.
"""

# ------------------------------------------------------------------------------------------------------#
# ------------------------------- main todos go here please ------------------------------------------- #
# *: Not important, **: Important, ***: Very important
# TODO: ***check in a clean python env for requirements
# ------------------------------------------------------------------------------------------------------#


app = dash.Dash(__name__)
app.title = 'JBI100 Group 31'


def build_banner():
    """
    Builds the banner on the top of the application with app name, group number, TU/e logo and a button for explanation.
    :return: dash.html object
    """

    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.H5('JBI100 Visualisation'),

            html.Button(
                id='whats-this-button',
                children="Further Information",
                n_clicks=0),
            html.Img(src='assets/TUE.png'),
            html.H3('Group 31')
        ]
    )


def build_explanation():
    """
    Builds the markdown that pops up when the "Further Information" button is pressed.
    :return: dash.html object
    """
    return html.Div(
        id='markdown',
        className='modal',
        style={'display': 'none'},
        children=[
            html.Div(
                id='markdown-container',
                className='markdown-container',
                children=[
                    html.Div(
                        className='close-container',
                        children=[html.Button(
                            'Close',
                            id='markdown-close',
                            n_clicks=0,
                            className='closeButton'
                        )]
                    ),
                    html.Div(
                        className='markdown-text',
                        children=dcc.Markdown(
                            children=dedent("""
                            This visualisation tool is made for investors looking for a neighbourhood/borough to invest in, fitting with their requirements.
                            The tool allows the user to go through 2 tabs of visualisations.\n
                            In the first tab Airbnb data can be explored per neighbourhood and borough in order to make it easier for the user to choose a
                            starting location for their research.\n
                            In the second tab the user can view every available property in Airbnb dataset on the new york map and can look into all properties
                            of every listing.
                            An accompanying treemap figure also assists the user to quickly filter for the most common words withing the chosen area of interest.

                            """)
                        )
                    )
                ]
            )
        ]
    )


def build_tabs():
    """
    This is one of the main builder functions where two tabs are created for the two pages of the web application.
    within dcc.Tab() we run the builder functions as children.
    :return: dash.html object.
    """
    return html.Div(
        id='tabs',
        className='row container scalable',
        children=[
            dcc.Tabs(
                id='app-tabs',
                value='tab1',
                className='custom-tabs',
                children=[
                    dcc.Tab(                #Choropleth tab
                        id='tab1',
                        label='Choropleth',
                        value='tab1',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        disabled_style={
                            'backgroundColor': '#2d3038',
                            'color': '#95969A',
                            'borderColor': '#23262E',
                            'display': 'flex',
                            'flex-direction': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        },
                        disabled=False,
                        children=[
                            html.Br(),
                            build_choropleth_tabs()
                        ]
                    ),
                    dcc.Tab(            #Map box plot tab
                        id='tab2',
                        label='Mapbox',
                        value='tab2',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        disabled_style={
                            'backgroundColor': '#2d3038',
                            'color': '#95969A',
                            'borderColor': '#23262E',
                            'display': 'flex',
                            'flex-direction': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        },
                        children=[
                            html.Div(
                                build_mapbox_controls('All')
                            ),
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="eight columns",
                                        # children=map_boxplot
                                        children=[
                                            dcc.Loading(
                                                id='loading-boxplot',
                                                type='graph',
                                                children=[map_boxplot]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        id='data-display',
                                        className="four columns container",
                                        children=[
                                            html.Div(
                                                build_mapbox_info_display(None)
                                            )
                                        ]
                                    )
                                ]
                            ), html.Div(
                                className="row",
                                children=[
                                    html.Br(),
                                    html.Div(
                                        id='loading-treemap',
                                        className='twelve columns',
                                        children=tree_map
                                        # children=[
                                        #     dcc.Loading(
                                        #         id='loading-treemap',
                                        #         type='graph',
                                        #         children=[tree_map]
                                        #     )
                                        # ]
                                    )
                                ]
                            )
                        ],
                        disabled=False)

                ]
            )
        ]
    )


def build_mapbox_info_display(clickData):
    """
    This builds the right-hand side of the mapbox tab. Receiving data from the graph and processing the user click to
    display the desired data.

    :param clickData: Point data from mapbox scatter
    :return: dash.html object
    """

    # For the first loading of the tab we set all the cells to be empty.
    name = ''
    price = ''
    service_fee = ''
    neighbourhood = ''
    room_type = ''
    min_nights = ''
    rules = ''

    # If a user click is detected:
    if clickData is not None:
        df_display = data[data['name'] == clickData['points'][0]['hovertext']]
        df_display = (df_display.reset_index()).iloc[0]
        name = df_display['name']
        price = f"${df_display['price']}"
        service_fee = df_display['service_fee']
        neighbourhood = df_display['neighbourhood']
        room_type = df_display['room_type']
        min_nights = df_display['minimum_nights']
        rules = df_display['house_rules']

    return html.Div(
        className="row",
        children=[
            html.Div(
                className="twelve columns banner h2",
                children=[
                    html.H6('Name'),
                    html.H4(
                        id='mapbox-name',
                        children=[name]
                    )
                ]
            )
        ]
    ), html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns banner",
                children=[
                    html.H6('Price'),
                    html.H4(
                        id='mapbox-price',
                        children=[price]
                    )
                ]
            ),
            html.Div(
                className="six columns banner",
                children=[
                    html.H6('Service Fee'),
                    html.H4(
                        id='mapbox-service-fee',
                        children=[service_fee]
                    )
                ]
            )
        ]
    ), html.Div(
        className="row",
        children=[
            html.Div(
                className="twelve columns banner",
                children=[
                    html.H6('Neighbourhood'),
                    html.H4(
                        id='mapbox-neighbourhood',
                        children=[neighbourhood]
                    )
                ]
            )
        ]
    ), html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns banner",
                children=[
                    html.H6('Room Type'),
                    html.H4(
                        id='mapbox-room-type',
                        children=[room_type]
                    )
                ]
            ),
            html.Div(
                className="six columns banner",
                children=[
                    html.H6('Minimum Nights'),
                    html.H4(
                        id='mapbox-minimum-nights',
                        children=[min_nights]
                    )
                ]
            )
        ]
    ), html.Div(
        className="row",
        children=[
            html.Div(
                className="twelve columns banner",
                children=[
                    html.H6('Rules'),
                    html.H2(
                        id='mapbox-general-info',
                        children=[rules]
                    )
                ]
            )
        ]
    ),


def build_mapbox_controls(neighbourhood_name):
    """
    This section builds the top part of the mapbox tab with three dropdowns and two sliders
    :param neighbourhood_name: One of the neighbourhood names from the csv file
    :return: dash.html object
    """
    # Define the basic variables
    # Dropdown variables:
    neighbourhood_group = config.get_neighbourhood_groups()
    neighbourhood = config.get_neighbourhood()
    # instant_bookability = config.get_inst_bookable()

    # Slider variables
    min_price, max_price = config.get_price_min_max()
    min_service_fee, max_service_fee = config.get_service_fee()

    return html.Div(
        id='tab1-content',
        children=[
            html.Br(),
            html.Div(style={'display': 'flex', 'justify-content': 'space-between'},
                     children=[
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label('Select Neighbourhood Group'),
                                      dcc.Dropdown(
                                          style={"border": "0px solid black"},
                                          id="select-neighbourhood-group",
                                          options=[{"label": i, "value": i} for i in neighbourhood_group],
                                          value=neighbourhood_group[
                                              np.where(neighbourhood_group == neighbourhood_name)[0][0]],
                                          # value='All'
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  id='test',
                                  children=[
                                      html.Label('Select Neighbourhood'),
                                      dcc.Dropdown(
                                          style={"border": "0px solid black"},
                                          id="select-neighbourhood",
                                          options=[{"label": i, "value": i} for i in neighbourhood[neighbourhood_name]],
                                          value=neighbourhood[neighbourhood_name][0],
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label('Price Range', style={'margin-left': '20px'}),
                                      dcc.RangeSlider(
                                          min=min_price,
                                          max=max_price,
                                          value=[min_price, max_price],
                                          allowCross=False,
                                          id='price-range-slider',
                                          marks={
                                              min_price: {'label': str(min_price)},
                                              max_price: {'label': str(max_price)}
                                          },
                                          tooltip={"placement": "bottom", "always_visible": False}
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label('Service Fee', style={'margin-left': '20px'}),
                                      dcc.RangeSlider(
                                          min=min_service_fee,
                                          max=max_service_fee,
                                          value=[min_service_fee, max_service_fee],
                                          allowCross=False,
                                          id='service-fee-range-slider',
                                          marks={
                                              min_price: {'label': str(min_service_fee)},
                                              max_price: {'label': str(max_service_fee)}
                                          },
                                          tooltip={"placement": "bottom", "always_visible": False}
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '12%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      # html.Label("Reset Graphs"),
                                      html.Button(
                                          'Reset Graphs',
                                          id='reset-graphs-button',
                                          n_clicks=0,
                                          style={'width': '100%', 'margin': '20px'}
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '12%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      # html.Label("Reset Filters"),
                                      html.Button(
                                          'Reset Controls',
                                          id='reset-controls-button',
                                          n_clicks=0,
                                          style={'width': '100%', 'margin': '20px'}
                                      )
                                  ]
                                  )
                     ]
                     )
        ]
    )


def build_choropleth_tabs():
    """
    This section builds the page for choropleth, histogram and their controls.
    :return: dash.html object
    """
    return html.Div(
        id="choropleth-content",
        className="row",
        children=[
            html.Div(
                className="eight columns",
                children=[
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Neighbourhoods', 'value': 'neighbourhoods'},
                            {'label': 'Boroughs', 'value': 'boroughs'},
                        ],
                        value='neighbourhoods', id='choropleth-dropdown',
                        clearable=False, searchable=False
                    ),
                    dcc.Loading(
                        id='loading-choropleth',
                        type='graph',
                        children=[map_choropleth]
                    )
                ]
            ),

            html.Div(
                className="four columns",
                children=[
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Price', 'value': 'price'},
                            {'label': 'Number of reviews per month', 'value': 'reviews_per_month'},
                            {'label': 'Service fee', 'value': 'service_fee'}
                        ],
                        value='price', id='histogram-dropdown',
                        clearable=False, searchable=False
                    ),
                    dcc.Loading(
                        id='loading-histogram',
                        type='graph',
                        children=[map_histogram]

                    ),
                ]
            )
        ]
    )


# ------------------------------------------------------------------------------------------------------#
# ---------------------- Creating the global variables and importing data ----------------------------- #
# ------------------------------------------------------------------------------------------------------#
data = pd.read_csv("Data/airbnb_open_data_clean.csv", low_memory=False)

map_boxplot = Mapboxplot("boxplot1", data)
map_choropleth = Choropleth('choropleth', data)
map_histogram = Histogram("histogram1", data)
tree_map = TreeMap("treemap", data)

# ------------------------------------------------------------------------------------------------------#
# ------------------------------ Building the main app layout ----------------------------------------- #
# ------------------------------------------------------------------------------------------------------#
app.layout = html.Div(
    children=[
        build_banner(),
        build_tabs(),
        html.Div(
            id='app-content',
            className='container scalable'
        ),
        build_explanation()
    ]
)


# ------------------------------------------------------------------------------------------------------#
# ----------------------- Setting the callback functions for interactions ----------------------------- #
# ------------------------------------------------------------------------------------------------------#

#further information button
@app.callback(
    Output('markdown', 'style'),
    Input('whats-this-button', 'n_clicks'),
    Input('markdown-close', 'n_clicks'))
def update_markdown(open_click, close_click):
    callback = dash.callback_context
    if callback.triggered:
        prop_id = callback.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'whats-this-button':
            return {'display': 'block'}
    return {'display': 'none'}

#update treemap and mapboxplot figures
@app.callback([
    Output(map_boxplot.html_id, "figure"),
    Output(tree_map.html_id, "figure")
]
    , [
        Input("select-neighbourhood-group", "value"),
        Input("select-neighbourhood", "value"),
        Input('price-range-slider', "value"),
        Input('service-fee-range-slider', 'value'),
        Input(map_boxplot.html_id, 'selectedData'),
        Input(tree_map.html_id, 'clickData'),
        Input(map_boxplot.html_id, "figure"),
        Input('reset-graphs-button', "n_clicks"),
        Input("tab1-content", "children")

    ])
def update_mapboxplot_treemap(neighbourhood_group, neighbourhood, price_range, service_fee_range, map_box_selected_data,
                              tree_map_selected_data, current_data, click, children):
    # process data
    df = data.copy()

    callback = dash.callback_context
    if callback.triggered:
        prop_id = callback.triggered[0]['prop_id'].split('.')[0]

    if (tree_map_selected_data is not None) and prop_id != 'reset-graphs-button':
        filter_string = tree_map_selected_data['points'][0]['label']

        df = df[df['processed'].str.contains(filter_string, case=False).fillna(False)]

        long_lat_list = []
        for i in range(len(current_data['data'][0]['lat'])):
            long_lat_list.append(
                (
                    current_data['data'][0]['lon'][i],
                    current_data['data'][0]['lat'][i]
                )
            )

        df = df[df[['long', 'lat']].apply(tuple, axis=1).isin(long_lat_list)]

    # filter data on chosen groups
    if neighbourhood_group != 'All':
        df = df.loc[df['neighbourhood_group'] == neighbourhood_group]

    if neighbourhood != 'All':
        df = df.loc[df['neighbourhood'] == neighbourhood]

    # filter data according to the given price range
    min_price_mask = df["price"] >= price_range[0]
    max_price_mask = df["price"] <= price_range[1]
    df = df[min_price_mask & max_price_mask]
    
    # filter data according to the given service fee range
    min_service_mask = df["service_fee"] >= service_fee_range[0]
    max_service_mask = df["service_fee"] <= service_fee_range[1]
    df = df[min_service_mask & max_service_mask]

    if map_box_selected_data is not None:
        selection_list = map_box_selected_data['points']
        long_lat_list = []
        for point in selection_list:
            lon = point['lon']
            lat = point['lat']
            long_lat_list.append((lon, lat))

        df = df[df[['long', 'lat']].apply(tuple, axis=1).isin(long_lat_list)]

    return map_boxplot.update(df), tree_map.update(df)

#resetting figure filters
@app.callback(
    Output("tab1-content", "children"),
    Input('reset-controls-button', 'n_clicks')
)
def update_neighbourhoods( click):
    return build_mapbox_controls('All')

#updating choropleth figure
@app.callback(
    Output(map_choropleth.html_id, 'figure'),
    Input('choropleth-dropdown', 'value')
)
def update_map_choropleth(value):
    return map_choropleth.update(value)

#display further information depending on the mapboxplot click
@app.callback(
    Output("data-display", "children"),
    Input(map_boxplot.html_id, 'clickData')
)
def update_data_display(clickData):
    return build_mapbox_info_display(clickData)

#Update histogram figure with the choropleth information
@app.callback(
    Output(map_histogram.html_id, 'figure'), [
        Input(map_choropleth.html_id, 'clickData'),
        Input('histogram-dropdown', 'value'),
        Input('app-tabs', 'value'),
        Input('choropleth-dropdown', 'value')])
def update_map_histogram(clickData, dropdown_choice, startup, map_dropdown):
    if clickData is None:
        return map_histogram.update(None, None, None)

    else:
        name = clickData['points'][0]['location']
        return map_histogram.update(name, dropdown_choice, map_dropdown)

app.run_server(debug=False, port='3131')