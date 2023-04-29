from dash import Dash, callback_context, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
from uuid import uuid4

from layout import get_layout

# Create a Dash object
app=Dash(__name__)

# Create layout of Dash application
app.layout=get_layout()

# Define the callback for cross filtering
@app.callback(
    Output('revenue-by-product-graph-id', 'figure'),
    Output('revenue-by-region-graph-id', 'figure'),
    Output('revenue-by-month-graph-id', 'figure'),
    Output('report-data', 'data'),

    Input('session-id', 'data'),
    Input('revenue-by-product-graph-id','clickData'),
    Input('revenue-by-region-graph-id','clickData'),
    Input('revenue-by-month-graph-id','clickData'),

    State('report-data', 'data')    
)
def display_visualizations(session_id, product_click_data, region_click_data, month_click_data, report_data):
    ctx = callback_context

    # Check if this callback is getting called for the first time or the session id is recreated
    # session id is configured to be re-created whenever 'Reset' button is clicked. 
    # Hence a click on "Reset" button also satisfies this if condition and makes the app to load data from source. 
    if report_data is None or ctx.triggered_id == 'session-id':
        #Read the data from source
        print('Reading data from source')
        data_df = pd.read_csv('assets/sales_data.csv')
    
    # If the above condition is not satisfied, the it means the callback is triggered by interaction on one of the charts
    # In this case, read the data from report data store
    # 'data-store' contains data filtered via earlier interactions
    else :
        # Read the data from store - report_data
        print('Reading data from dcc.Store')
        data_df = pd.read_json(report_data)

    # Filter the data based on user interaction. Look at bottom of file for example of click data.   
    if ctx.triggered_id == 'revenue-by-product-graph-id':
        clicked_product = product_click_data['points'][0]['x']
        data_df = data_df[data_df['Product Name'] == clicked_product]

    elif ctx.triggered_id == 'revenue-by-region-graph-id':
        clicked_region = region_click_data['points'][0]['x']
        data_df = data_df[data_df['Region Name'] == clicked_region]

    elif ctx.triggered_id == 'revenue-by-month-graph-id':
        clicked_month = month_click_data['points'][0]['x']
        data_df = data_df[data_df['Month Name'] == clicked_month]

    
    # Create charts based on filtered data

    # Revenue by product graph
    revenue_by_product_df = data_df[['Product Name', 'Revenue']].groupby(by=['Product Name']).sum().reset_index()
    revenue_by_product_chart = px.bar(
        data_frame=revenue_by_product_df,
        x='Product Name',
        y='Revenue',
        text='Revenue', 
        )
    revenue_by_product_chart.update_xaxes(title=None)
    revenue_by_product_chart.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    
    # Revenue by region graph
    revenue_by_region_df = data_df[['Region Name', 'Revenue']].groupby(by=['Region Name']).sum().reset_index()
    revenue_by_region_chart = px.bar(
        data_frame=revenue_by_region_df,
        x='Region Name',
        y='Revenue',
        text='Revenue'
        )
    revenue_by_region_chart.update_xaxes(title=None)
    revenue_by_region_chart.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    
    # Revenue by month graph
    revenue_by_month_df = data_df[['Month Name', 'Revenue']].groupby(by=['Month Name']).sum().reset_index()
    revenue_by_month_chart = px.bar(
        data_frame=revenue_by_month_df,
        x='Month Name',
        y='Revenue',
        text='Revenue'
        )
    revenue_by_month_chart.update_xaxes(title=None)
    revenue_by_month_chart.update_layout(margin=dict(l=10, r=10, t=10, b=10))

    # Return the created charts and filtered data frame converted to json
    # This filtered data frame is saved in dcc.Store object with id 'report-data'
    # The same filtered data is available to the callback for further filtering until "Reset" button is cliecked 
    
    return revenue_by_product_chart, revenue_by_region_chart, revenue_by_month_chart, data_df.to_json()


# Callback to reset the dashboard to original state when "Reset" button is clicked
# This callback recreates the session id and assigns the outcome to dcc.Store object with id 'session-id'
# Any change in 'data' property of dcc.Store object with id 'session-id' triggers the above callback
@app.callback(
    Output('session-id','data'),
    Input('reset-button-id','n_clicks'),
    prevent_initial_call = True
)
def reset_dashboard(n_clicks):
    return str(uuid4())


if __name__ == '__main__':
    app.run(port=8050,debug=True, dev_tools_hot_reload=True)


# Example of click data object:
# {
#     'points': [
#         {
#             'curveNumber': 0, 
#             'pointNumber': 4, 
#             'pointIndex': 4, 
#             'x': 'Product 5', 
#             'y': 677597,
#             'label': 'Product 5', 
#             'value': 677597, 
#             'text': 677597, 
#             'bbox': {
#                 'x0': 619.49, 
#                 'x1': 726.51, 
#                 'y0': 67.25, 
#                 'y1': 67.25
#                 }
#         }
#     ]
# }