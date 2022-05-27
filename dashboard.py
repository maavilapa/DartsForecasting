import plotly.graph_objs as go
#import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.io as pio
import pandas as pd
#import plotly.express as px
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Test dashboard datup"

# CODE TO CREATE THE GRAPHS COMES HERE
from dash.dependencies import Input, Output

plotly_template = pio.templates["presentation"]

import os

#to get the current working directory
directory = os.getcwd()
print(directory)

Q0, Q1, Q2, Q3, Q4, Q5, Q6 = {}, {}, {}, {}, {}, {}, {}
models = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']
models[0] = 'ES'
models[1] = 'Prophet'
models[2] = 'RNN'
models[3] = 'TCN'
models[4] = 'Transformer'
models[5] = 'TFT'

forecast_horizon = {}
###################################
proyecto = "temperature"
forecast_horizon[proyecto] = 24
Q0[proyecto] = pd.read_csv(directory + '\data\raw\historical_data.csv', sep=",")
Q1[proyecto] = pd.read_csv(directory + '\data\forecasts\ES.csv', sep=",")
Q2[proyecto] = pd.read_csv(directory + '\data\forecasts\Prophet.csv', sep=",")
Q3[proyecto] = pd.read_csv(directory + '\data\forecasts\RNN.csv', sep=",")
Q4[proyecto] = pd.read_csv(directory + '\data\forecasts\TCN.csv', sep=",")
Q5[proyecto] = pd.read_csv(directory + '\data\forecasts\Transformer.csv', sep=",")
Q6[proyecto] = pd.read_csv(directory + '\data\forecasts\TFT.csv', sep=",")


##########################################################
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


#CALLBACK Historical data
@app.callback(Output('historical', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def historical_change(item, project, Location):
    if "location" in Q0[project].columns:
        figure = go.Figure([
            go.Scatter(
                name='historical data',
                x=Q0[project][(Q0[project].location == Location) & (Q0[project].item_id == item)]['Date'],
                y=Q0[project][(Q0[project].location == Location) & (Q0[project].item_id == item)]['value'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title='Historical data',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
        return figure
    else:
        figure = go.Figure([
            go.Scatter(
                name='historical data',
                x=Q0[project][Q0[project].item_id == item]['Date'],
                y=Q0[project][Q0[project].item_id == item]['value'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title='Historical data',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
        return figure


#M1_CALLBACK
@app.callback(Output('M1', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def M1_change(item, project, location):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''

    if Q1[project].empty:
        figure = go.Figure(
            layout={
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [{
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 30
                    }
                }]
            })
        figure.update_layout(template=plotly_template,
                             title=models[0] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
    else:
        figure = go.Figure([
            go.Scatter(
                name='P50',
                x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['p50']
                if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p50'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(name='P60',
                       x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                       y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['p60']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p60'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P40',
                       x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                       y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['p40']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p40'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P80',
                       x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                       y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['p80']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p80'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P20',
                       x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                       y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['p20']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p20'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(
                name='Target',
                x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date'].iloc[:]
                if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'].iloc[:],
                y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['target'].iloc[:]
                if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['target'].iloc[:],
                mode='lines',
                line=dict(color='firebrick'),
            ),
            go.Scatter(name='P95',
                       x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                       y=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['p95']
                       if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p95'],
                       marker=dict(color="#444"),
                       line=dict(width=1, dash='dot'),
                       showlegend=True),
            go.Scatter(
                name='P05',
                x=Q1[project][(Q1[project].Location == location) & (Q1[project].Item == item)]['Date']
                if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['Date'],
                y=Q1[project][(Q1[project].Location == location) &
                              (Q1[project].Item == item)]['p5'] if "Location" in Q1[project].columns else Q1[project][Q1[project].Item == item]['p5'],
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True)
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title=models[0] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))

    return figure


#M2_CALLBACK
@app.callback(Output('M2', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def M2_change(item, project, location):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''

    if Q2[project].empty:
        figure = go.Figure(
            layout={
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [{
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 30
                    }
                }]
            })
        figure.update_layout(template=plotly_template,
                             title=models[1] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
    else:
        figure = go.Figure([
            go.Scatter(
                name='P50',
                x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['p50']
                if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p50'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(name='P60',
                       x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                       y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['p60']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p60'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P40',
                       x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                       y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['p40']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p40'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P80',
                       x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                       y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['p80']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p80'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P20',
                       x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                       y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['p20']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p20'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(
                name='Target',
                x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date'].iloc[:]
                if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'].iloc[:],
                y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['target'].iloc[:]
                if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['target'].iloc[:],
                mode='lines',
                line=dict(color='firebrick'),
            ),
            go.Scatter(name='P95',
                       x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                       y=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['p95']
                       if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p95'],
                       marker=dict(color="#444"),
                       line=dict(width=1, dash='dot'),
                       showlegend=True),
            go.Scatter(
                name='P05',
                x=Q2[project][(Q2[project].Location == location) & (Q2[project].Item == item)]['Date']
                if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['Date'],
                y=Q2[project][(Q2[project].Location == location) &
                              (Q2[project].Item == item)]['p5'] if "Location" in Q2[project].columns else Q2[project][Q2[project].Item == item]['p5'],
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True)
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title=models[1] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))

    return figure


#M3_CALLBACK
@app.callback(Output('M3', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def M3_change(item, project, location):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''

    if Q3[project].empty:
        figure = go.Figure(
            layout={
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [{
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 30
                    }
                }]
            })
        figure.update_layout(template=plotly_template,
                             title=models[2] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
    else:
        figure = go.Figure([
            go.Scatter(
                name='P50',
                x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['p50']
                if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p50'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(name='P60',
                       x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                       y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['p60']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p60'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P40',
                       x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                       y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['p40']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p40'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P80',
                       x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                       y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['p80']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p80'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P20',
                       x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                       y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['p20']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p20'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(
                name='Target',
                x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date'].iloc[:]
                if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'].iloc[:],
                y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['target'].iloc[:]
                if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['target'].iloc[:],
                mode='lines',
                line=dict(color='firebrick'),
            ),
            go.Scatter(name='P95',
                       x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                       y=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['p95']
                       if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p95'],
                       marker=dict(color="#444"),
                       line=dict(width=1, dash='dot'),
                       showlegend=True),
            go.Scatter(
                name='P05',
                x=Q3[project][(Q3[project].Location == location) & (Q3[project].Item == item)]['Date']
                if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['Date'],
                y=Q3[project][(Q3[project].Location == location) &
                              (Q3[project].Item == item)]['p5'] if "Location" in Q3[project].columns else Q3[project][Q3[project].Item == item]['p5'],
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True)
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title=models[2] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))

    return figure


#M4_CALLBACK
@app.callback(Output('M4', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def M4_change(item, project, location):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''

    if Q4[project].empty:
        figure = go.Figure(
            layout={
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [{
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 30
                    }
                }]
            })
        figure.update_layout(template=plotly_template,
                             title=models[3] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
    else:
        figure = go.Figure([
            go.Scatter(
                name='P50',
                x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['p50']
                if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p50'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(name='P60',
                       x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                       y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['p60']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p60'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P40',
                       x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                       y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['p40']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p40'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P80',
                       x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                       y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['p80']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p80'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P20',
                       x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                       y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['p20']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p20'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(
                name='Target',
                x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date'].iloc[:]
                if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'].iloc[:],
                y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['target'].iloc[:]
                if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['target'].iloc[:],
                mode='lines',
                line=dict(color='firebrick'),
            ),
            go.Scatter(name='P95',
                       x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                       y=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['p95']
                       if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p95'],
                       marker=dict(color="#444"),
                       line=dict(width=1, dash='dot'),
                       showlegend=True),
            go.Scatter(
                name='P05',
                x=Q4[project][(Q4[project].Location == location) & (Q4[project].Item == item)]['Date']
                if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['Date'],
                y=Q4[project][(Q4[project].Location == location) &
                              (Q4[project].Item == item)]['p5'] if "Location" in Q4[project].columns else Q4[project][Q4[project].Item == item]['p5'],
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True)
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title=models[3] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))

    return figure


#M5_CALLBACK
@app.callback(Output('M5', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def M5_change(item, project, location):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''

    if Q5[project].empty:
        figure = go.Figure(
            layout={
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [{
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 30
                    }
                }]
            })
        figure.update_layout(template=plotly_template,
                             title=models[4] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
    else:
        figure = go.Figure([
            go.Scatter(
                name='P50',
                x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['p50']
                if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p50'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(name='P60',
                       x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                       y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['p60']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p60'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P40',
                       x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                       y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['p40']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p40'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P80',
                       x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                       y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['p80']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p80'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P20',
                       x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                       y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['p20']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p20'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(
                name='Target',
                x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date'].iloc[:]
                if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'].iloc[:],
                y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['target'].iloc[:]
                if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['target'].iloc[:],
                mode='lines',
                line=dict(color='firebrick'),
            ),
            go.Scatter(name='P95',
                       x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                       y=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['p95']
                       if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p95'],
                       marker=dict(color="#444"),
                       line=dict(width=1, dash='dot'),
                       showlegend=True),
            go.Scatter(
                name='P05',
                x=Q5[project][(Q5[project].Location == location) & (Q5[project].Item == item)]['Date']
                if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['Date'],
                y=Q5[project][(Q5[project].Location == location) &
                              (Q5[project].Item == item)]['p5'] if "Location" in Q5[project].columns else Q5[project][Q5[project].Item == item]['p5'],
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True)
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title=models[4] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))

    return figure


#M6_CALLBACK
@app.callback(Output('M6', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def M6_change(item, project, location):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''

    if Q6[project].empty:
        figure = go.Figure(
            layout={
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [{
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 30
                    }
                }]
            })
        figure.update_layout(template=plotly_template,
                             title=models[5] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))
    else:
        figure = go.Figure([
            go.Scatter(
                name='P50',
                x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['p50']
                if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p50'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(name='P60',
                       x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                       y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['p60']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p60'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P40',
                       x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                       y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['p40']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p40'],
                       mode='lines',
                       line=dict(color='rgb(238,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P80',
                       x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                       y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['p80']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p80'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(name='P20',
                       x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                       y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['p20']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p20'],
                       mode='lines',
                       line=dict(color='rgb(0,118,0)'),
                       visible='legendonly'),
            go.Scatter(
                name='Target',
                x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date'].iloc[:]
                if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'].iloc[:],
                y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['target'].iloc[:]
                if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['target'].iloc[:],
                mode='lines',
                line=dict(color='firebrick'),
            ),
            go.Scatter(name='P95',
                       x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                       y=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['p95']
                       if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p95'],
                       marker=dict(color="#444"),
                       line=dict(width=1, dash='dot'),
                       showlegend=True),
            go.Scatter(
                name='P05',
                x=Q6[project][(Q6[project].Location == location) & (Q6[project].Item == item)]['Date']
                if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['Date'],
                y=Q6[project][(Q6[project].Location == location) &
                              (Q6[project].Item == item)]['p5'] if "Location" in Q6[project].columns else Q6[project][Q6[project].Item == item]['p5'],
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True)
        ])
        figure.update_layout(template=plotly_template,
                             yaxis_title='Value',
                             title=models[5] + ' Forecast',
                             hovermode="x",
                             autosize=True,
                             margin=dict(l=150, r=150, b=50, t=50, pad=0))

    return figure


#MAPE ITEM CALLBACK
@app.callback(Output('Errors', 'figure'), [Input('item_id', 'value')], [Input('stockselector', 'value')], [Input('location', 'value')])
def mape_change(selected_dropdown_value, proyecto, location):
    figure = go.Figure()
    if "location" in Q0[proyecto].columns:
        if Q1[proyecto].empty == False:
            figure.add_trace(
                go.Bar(y=[Q1[proyecto][(Q1[proyecto].Item == selected_dropdown_value) & (Q1[proyecto].Location == location)]["mape"].median()],
                       x=[models[0]],
                       name=models[0]))
        if Q2[proyecto].empty == False:
            figure.add_trace(
                go.Bar(y=[Q2[proyecto][(Q2[proyecto].Item == selected_dropdown_value) & (Q2[proyecto].Location == location)]["mape"].median()],
                       x=[models[1]],
                       name=models[1]))
        if Q3[proyecto].empty == False:
            figure.add_trace(
                go.Bar(y=[Q3[proyecto][(Q3[proyecto].Item == selected_dropdown_value) & (Q3[proyecto].Location == location)]["mape"].median()],
                       x=[models[2]],
                       name=models[2]))
        if Q4[proyecto].empty == False:
            figure.add_trace(
                go.Bar(y=[Q4[proyecto][(Q4[proyecto].Item == selected_dropdown_value) & (Q4[proyecto].Location == location)]["mape"].median()],
                       x=[models[3]],
                       name=models[3]))
        if Q5[proyecto].empty == False:
            figure.add_trace(
                go.Bar(y=[Q5[proyecto][(Q5[proyecto].Item == selected_dropdown_value) & (Q5[proyecto].Location == location)]["mape"].median()],
                       x=[models[4]],
                       name=models[4]))
        if Q6[proyecto].empty == False:
            figure.add_trace(
                go.Bar(y=[Q6[proyecto][(Q6[proyecto].Item == selected_dropdown_value) & (Q6[proyecto].Location == location)]["mape"].median()],
                       x=[models[5]],
                       name=models[5]))

    else:
        if Q1[proyecto].empty == False:
            figure.add_trace(go.Bar(y=[Q1[proyecto][(Q1[proyecto].Item == selected_dropdown_value)]["mape"].median()], x=[models[0]], name=models[0]))
        if Q2[proyecto].empty == False:
            figure.add_trace(go.Bar(y=[Q2[proyecto][(Q2[proyecto].Item == selected_dropdown_value)]["mape"].median()], x=[models[1]], name=models[1]))
        if Q3[proyecto].empty == False:
            figure.add_trace(go.Bar(y=[Q3[proyecto][(Q3[proyecto].Item == selected_dropdown_value)]["mape"].median()], x=[models[2]], name=models[2]))
        if Q4[proyecto].empty == False:
            figure.add_trace(go.Bar(y=[Q4[proyecto][(Q4[proyecto].Item == selected_dropdown_value)]["mape"].median()], x=[models[3]], name=models[3]))
        if Q5[proyecto].empty == False:
            figure.add_trace(go.Bar(y=[Q5[proyecto][(Q5[proyecto].Item == selected_dropdown_value)]["mape"].median()], x=[models[4]], name=models[4]))
        if Q6[proyecto].empty == False:
            figure.add_trace(go.Bar(y=[Q6[proyecto][(Q6[proyecto].Item == selected_dropdown_value)]["mape"].median()], x=[models[5]], name=models[5]))

    figure.update_layout(template=plotly_template,
                         yaxis_title='Errors',
                         title='MAPE ' + str(selected_dropdown_value) + " " + str(location) if "location" in Q0[proyecto].columns else 'MAPE ' +
                         str(selected_dropdown_value),
                         hovermode="x",
                         autosize=True,
                         margin=dict(l=150, r=150, b=50, t=50, pad=0))
    return figure


#MAPE GENERAL
@app.callback(Output('Errors_general', 'figure'), [Input('stockselector', 'value')])
def mape_general_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    figure = go.Figure()
    if (Q1[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q1[selected_dropdown_value]["mape"], quartilemethod="linear", boxpoints=False, name=models[0]))
    if (Q2[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q2[selected_dropdown_value]["mape"], quartilemethod="linear", boxpoints=False, name=models[1]))
    if (Q3[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q3[selected_dropdown_value]["mape"], quartilemethod="linear", boxpoints=False, name=models[2]))
    if (Q4[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q4[selected_dropdown_value]["mape"], quartilemethod="linear", boxpoints=False, name=models[3]))
    if (Q5[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q5[selected_dropdown_value]["mape"], quartilemethod="linear", boxpoints=False, name=models[4]))
    if (Q6[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q6[selected_dropdown_value]["mape"], quartilemethod="linear", boxpoints=False, name=models[5]))
    figure.update_traces(jitter=1)
    figure.update_layout(template=plotly_template,
                         yaxis_title='Errors',
                         title='MAPE',
                         hovermode="x",
                         autosize=True,
                         margin=dict(l=150, r=150, b=50, t=50, pad=0))
    return figure


#MASE GENERAL
@app.callback(Output('MASE_general', 'figure'), [Input('stockselector', 'value')])
def mase_general_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    figure = go.Figure()
    if (Q1[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q1[selected_dropdown_value]["mase"], quartilemethod="linear", boxpoints=False, name=models[0]))
    if (Q2[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q2[selected_dropdown_value]["mase"], quartilemethod="linear", boxpoints=False, name=models[1]))
    if (Q3[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q3[selected_dropdown_value]["mase"], quartilemethod="linear", boxpoints=False, name=models[2]))
    if (Q4[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q4[selected_dropdown_value]["mase"], quartilemethod="linear", boxpoints=False, name=models[3]))
    if (Q5[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q5[selected_dropdown_value]["mase"], quartilemethod="linear", boxpoints=False, name=models[4]))
    if (Q6[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q6[selected_dropdown_value]["mase"], quartilemethod="linear", boxpoints=False, name=models[5]))
    figure.update_traces(jitter=0)
    figure.update_layout(template=plotly_template,
                         yaxis_title='Errors',
                         title='MASE',
                         hovermode="x",
                         autosize=True,
                         margin=dict(l=150, r=150, b=50, t=50, pad=0))
    return figure


#sMAPE GENERAL
@app.callback(Output('sMAPE_general', 'figure'), [Input('stockselector', 'value')])
def smape_general_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    figure = go.Figure()
    if (Q1[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q1[selected_dropdown_value]["smape"], quartilemethod="linear", boxpoints=False, name=models[0]))
    if (Q2[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q2[selected_dropdown_value]["smape"], quartilemethod="linear", boxpoints=False, name=models[1]))
    if (Q3[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q3[selected_dropdown_value]["smape"], quartilemethod="linear", boxpoints=False, name=models[2]))
    if (Q4[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q4[selected_dropdown_value]["smape"], quartilemethod="linear", boxpoints=False, name=models[3]))
    if (Q5[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q5[selected_dropdown_value]["smape"], quartilemethod="linear", boxpoints=False, name=models[4]))
    if (Q6[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q6[selected_dropdown_value]["smape"], quartilemethod="linear", boxpoints=False, name=models[5]))
    figure.update_traces(jitter=1)
    figure.update_layout(template=plotly_template,
                         yaxis_title='Errors',
                         title='sMAPE',
                         hovermode="x",
                         autosize=True,
                         margin=dict(l=150, r=150, b=50, t=50, pad=0))
    return figure


#RMSE GENERAL
@app.callback(Output('RMSE_general', 'figure'), [Input('stockselector', 'value')])
def rmse_general_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    figure = go.Figure()
    if (Q1[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q1[selected_dropdown_value]["rmsle"], quartilemethod="linear", boxpoints=False, name=models[0]))
    if (Q2[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q2[selected_dropdown_value]["rmsle"], quartilemethod="linear", boxpoints=False, name=models[1]))
    if (Q3[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q3[selected_dropdown_value]["rmsle"], quartilemethod="linear", boxpoints=False, name=models[2]))
    if (Q4[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q4[selected_dropdown_value]["rmsle"], quartilemethod="linear", boxpoints=False, name=models[3]))
    if (Q5[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q5[selected_dropdown_value]["rmsle"], quartilemethod="linear", boxpoints=False, name=models[4]))
    if (Q6[selected_dropdown_value].empty == False):
        figure.add_trace(go.Box(y=Q6[selected_dropdown_value]["rmsle"], quartilemethod="linear", boxpoints=False, name=models[5]))
    figure.update_traces(jitter=0)
    figure.update_layout(template=plotly_template,
                         yaxis_title='Errors',
                         title='RMSLE',
                         hovermode="x",
                         autosize=True,
                         margin=dict(l=150, r=150, b=50, t=50, pad=0))
    return figure


#Location dropdown CALLBACK
@app.callback(dash.dependencies.Output('location', 'options'), dash.dependencies.Output('location', 'disabled'),
              [dash.dependencies.Input('stockselector', 'value')])
def location(selected_project):
    if "location" in Q0[selected_project].columns:
        return get_options(Q0[selected_project].location.unique()), False
    else:
        return get_options([""]), True


#Item_id dropdown CALLBACK
@app.callback(dash.dependencies.Output('item_id', 'options'), [dash.dependencies.Input('stockselector', 'value')],
              [dash.dependencies.Input('location', 'value')])
def item_id(selected_project, Location):
    if "location" in Q0[selected_project]:
        return get_options(Q0[selected_project][Q0[selected_project].location == Location].item_id.unique())
    else:
        return get_options(Q0[selected_project].item_id.unique())


########### LAYOUT ########################
app.layout = html.Div(children=[html.H3(id = 'H3', children = 'Test dashboard Datup', style = {'textAlign': 'center',\
                                            'marginTop': 40,'marginBottom': 40}), html.Div(className='div-for-dropdown',
          children=[

               dcc.RadioItems(id='stockselector',
                           options=get_options(["temperature"]),
                           #multi=False,
                           #clearable=False,
                           value="temperature",
                           #style={'backgroundColor': 'white'},
                           className='stockselector',
                           labelStyle={'display': 'inline-block'}),

              dcc.Dropdown(id='location',
                           multi=False,
                           clearable=False,
                           value=Q0["temperature"].item_id.unique()[0],
                           #disabled=True,
                           style=dict(
                           width='40%',
                           verticalAlign="middle"
                                ),
                           className='location',
                           placeholder="Select location"),
              dcc.Dropdown(id='item_id',
                           multi=False,
                           clearable=False,
                           value=Q0["temperature"].item_id.unique()[0],
                           style=dict(
                           width='40%',
                           verticalAlign="middle"
                                ),
                           className='item_id',
                           placeholder="Select an item id"),
                    ],

          style={'color': '#1E1E1E'}),

    html.Div([
        dcc.Graph(
            id='historical',
            config={'displayModeBar': False}
        ),

    ]),
    html.Div([
        dcc.Graph(
            id='M1',
            config={'displayModeBar': False}
        ),
    ]),
        html.Div([
        dcc.Graph(
            id='M2',
            config={'displayModeBar': False}
        ),
    ]),

    html.Div([
    dcc.Graph(
            id='M3',
            config={'displayModeBar': False},
        ),
    ]),

    html.Div([
    dcc.Graph(
            id='M4',
            config={'displayModeBar': False},
        ),
    ]),

    html.Div([
    dcc.Graph(
            id='M5',
            config={'displayModeBar': False},
        ),
    ]),

    html.Div([
    dcc.Graph(
            id='M6',
            config={'displayModeBar': False},
        ),
    ]),


    html.Div([
        dcc.Graph(
            id='Errors',
            config={'displayModeBar': False}
        ),
    ]),
    html.Div([
        dcc.Graph(
            id='Errors_general',
            config={'displayModeBar': False}
        ),

    ]),
    html.Div([
        dcc.Graph(
            id='MASE_general',
            config={'displayModeBar': False}
        ),

    ]),
    html.Div([
        dcc.Graph(
            id='sMAPE_general',
            #figure=fig2,
            config={'displayModeBar': False}
        ),

    ]),
    html.Div([
        dcc.Graph(
            id='RMSE_general',
            #figure=fig2,
            config={'displayModeBar': False}
        ),

    ]),
                               ])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)