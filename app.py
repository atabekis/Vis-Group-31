import dash
# import dash_loading_spinners
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import functions.config as config
from functions.mapboxplot import Mapboxplot
from functions.choropleth_mapbox import Choropleth
from functions.barchart import Barchart
import numpy as np
import pandas as pd
from textwrap import dedent
# import dash_loading_spinners
import time

app = dash.Dash(__name__)


def build_banner():
    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.H5('Somebody please end my suffering'),

            html.Button(
                id='whats-this-button',
                children="What's This?",
                n_clicks=0),
            html.Img(src='assets/TUE.png'),
            html.H3('Group 31')
        ]
    )


def build_explanation():
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
                            IM WRITING THIS TO LET YOU KNOW THAT BARTAN IS A LITTLE BITCH
                            AND I STAND WITH WHAT I SAY :)))
                            """)
                        )
                    )
                ]
            )
        ]
    )


def build_tabs():
    return html.Div(
        id='tabs',
        className='row container scalable',
        children=[
            dcc.Tabs(
                id='app-tabs',
                value='tab1',
                className='custom-tabs',
                children=[
                    dcc.Tab(
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
                    dcc.Tab(
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
                                        children=map_boxplot
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
                            )
                        ],
                        disabled=False)

                ]
            )
        ]
    )


def build_mapbox_info_display(clickData):
    name = ''
    price = ''
    service_fee = ''
    neighbourhood = ''
    room_type = ''
    min_nights = ''
    general_info = ''

    if clickData is not None:
        df_display = data[data['name'] == clickData['points'][0]['hovertext']]
        df_display = (df_display.reset_index()).iloc[0]
        name = df_display['name']
        price = f"${df_display['price']}"
        service_fee = df_display['service_fee']
        neighbourhood = df_display['neighbourhood']
        room_type = df_display['room_type']
        min_nights = df_display['minimum_nights']
        general_info = 'PENIS!!!'

    return html.Div(
        className="row",
        children=[
            html.Div(
                className="twelve columns banner",
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
                className="six columns banner",
                children=[
                    html.H6('General Info'),
                    html.H4(
                        id='mapbox-general-info',
                        children=[general_info]
                    )
                ]
            )
        ]
    ),


def build_mapbox_controls(neighbourhood_name):
    # Define the basic variables
    neighbourhood_group = config.get_neighbourhood_groups()
    neighbourhood = config.get_neighbourhood()
    min_price, max_price = config.get_price_min_max()
    instant_bookability = config.get_inst_bookable()
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
                                          # TODO: ADD CLASSNAME HERE AND IN CSS
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
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label("Instantly Bookable"),
                                      dcc.Dropdown(
                                          style={"border": "0px solid black"},
                                          id='instant-bookable',
                                          options=[{"label": i, "value": i} for i in instant_bookability],
                                          value=instant_bookability[0]
                                      )
                                  ]
                                  )
                     ]
                     )
        ]
    )


def build_choropleth_tabs():
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
                        id='loading-1',
                        type='graph',
                        children=[map_choropleth]
                    )
                    # map_choropleth
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
                        value='price', id='barchart-dropdown',
                        clearable=False, searchable=False
                    ),
                    dcc.Loading(
                        id='loading-2',
                        type='graph',
                        children=[map_barchart]

                    ),
                    # map_barchart
                ]
            )
        ]
    )


data = pd.read_csv("Data/airbnb_open_data_clean.csv", low_memory=False)

map_boxplot = Mapboxplot("boxplot1", data)
map_choropleth = Choropleth('choropleth', data)
map_barchart = Barchart("barchart1", data)

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


@app.callback(Output('markdown', 'style'),
              Input('whats-this-button', 'n_clicks'),
              Input('markdown-close', 'n_clicks'))
def update_markdown(open_click, close_click):
    callback = dash.callback_context
    if callback.triggered:
        prop_id = callback.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'whats-this-button':
            return {'display': 'block'}
    return {'display': 'none'}


@app.callback(
    Output(map_boxplot.html_id, "figure"), [
        Input("select-neighbourhood-group", "value"),
        Input("select-neighbourhood", "value"),
        Input('price-range-slider', "value"),
        Input('instant-bookable', "value"),
        Input('service-fee-range-slider', 'value')
    ])
def update_mapboxplot(neighbourhood_group, neighbourhood, price_range, inst_bookable, service_fee_range):
    return map_boxplot.update(neighbourhood_group, neighbourhood, price_range, inst_bookable, service_fee_range)


@app.callback(
    Output("tab1-content", "children"),
    Input("select-neighbourhood-group", "value")
)
def update_neighbourhoods(neighbourhood):
    return [build_mapbox_controls(neighbourhood)]


@app.callback(
    Output(map_choropleth.html_id, 'figure'),
    Input('choropleth-dropdown', 'value'),

)
def update_map_choropleth(value):
    return map_choropleth.update(value)


@app.callback(
    Output("data-display", "children"),
    Input(map_boxplot.html_id, 'clickData')
)
def update_data_display(clickData):
    return build_mapbox_info_display(clickData)


@app.callback(
    Output(map_barchart.html_id, 'figure'), [
        Input(map_choropleth.html_id, 'clickData'),
        Input('barchart-dropdown', 'value'),
        Input('app-tabs', 'value')]
)
def update_map_barchart(clickData, dropdown_choice, startup):

    if clickData is None:
        return map_barchart.update(None, None)

    else:
        name = clickData['points'][0]['location']
        return map_barchart.update(name, dropdown_choice)


app.run_server()

# asd
