from dash import dcc, html
from uuid import uuid4

def get_layout():
    session_id = str(uuid4())

    return html.Div(
        id='app-layout',
        className='app-layout-div-class',
        children=[
            dcc.Store(id='session-id', data=session_id),
            dcc.Store(id='report-data'),
            
            html.Div(
                id='app-header-div-id',
                children=[
                    html.Button(
                        id='reset-button-id',
                        children='Reset'
                    )
                ]
            ),

            html.Div(
                id='revenue-by-product-div-id',
                children=dcc.Graph(id='revenue-by-product-graph-id')
            ),

            html.Div(
                id='revenue-by-region-div-id',
                children=dcc.Graph(id='revenue-by-region-graph-id')
            ),

            html.Div(
                id='revenue-by-month-div-id',
                children=dcc.Graph(id='revenue-by-month-graph-id')
            )
        ]
    )