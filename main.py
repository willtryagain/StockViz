from re import X
import dash
from dash import dependencies
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=external_stylesheets,
)
df = pd.read_csv("data/indexData.csv", parse_dates=["Date"])

available_indexes = df['Index'].unique()
years = [str(year) for year in df['Date'].dt.year.unique()]
years = years[0::5]
app.title = "Stock Viz"
app.layout = html.Div([
    html.Div([ 
        html.Img(src=app.get_asset_url("22926706.jpg"), style={'width': '10%', 'height': '10%'}),
        html.Div(["Stock Viz"], style={'display': 'block', 'font-size': '100px', 'margin-top': '50px'})],
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),


    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-index',
                options=[{'label': i, 'value': i} for i in available_indexes],
                value='IXIC'
            )
        ],
        style={'padding':'12px 16px'}),
    ],



    style={'padding': '10px 5px'}),

    html.Div(dcc.RangeSlider(
        id='crossfilter-year--slider',
        min=df['Date'].dt.year.min(),
        max=df['Date'].dt.year.max(),
        value=[2010, 2015],
        marks={yr : yr for yr in years},
        step=1
    ), style={'padding': '0px 20px 20px 20px'}),

    html.Table([
        html.Tr([ 
            html.Td(id='region'),
            html.Td(id='exchange'),
            html.Td(id='currency'),
        ],style={'display': 'flex', 'justify-content': 'space-between'}),
    ], style={'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Div([    
        html.Div([
            dcc.Graph(
                id='crossfilter-open',
                hoverData={'points': [{'customdata': 'xyz'}]}
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id='crossfilter-volume',
                hoverData={'points': [{'customdata': 'xyz'}]}
            )
        ], style={'width': '30%', 'display': 'inline-block'}),


        html.Div([
            dcc.Graph(
                id='crossfilter-high',
                hoverData={'points': [{'customdata': 'xyz'}]}
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div(
        [
         html.Div([
        dcc.Graph(
            id='crossfilter-low',
            hoverData={'points': [{'customdata': 'xyz'}]}
        )
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-close',
            hoverData={'points': [{'customdata': 'xyz'}]}
        )
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-adjclose',
            hoverData={'points': [{'customdata': 'xyz'}]}
        )
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 20'}),
  
    ],style={'display': 'flex', 'justify-content': 'space-between'}),



    
   
])


@app.callback(
    dash.dependencies.Output('region', 'children'),
    [dash.dependencies.Input('crossfilter-index', 'value')])
def update_row(xaxis_column_name):
    dff = pd.read_csv("data/indexInfo.csv")
    dff = dff[dff['Index'] == xaxis_column_name]
    return dff['Region']

@app.callback(
    dash.dependencies.Output('exchange', 'children'),
    [dash.dependencies.Input('crossfilter-index', 'value')])
def update_row(xaxis_column_name):
    dff = pd.read_csv("data/indexInfo.csv")
    dff = dff[dff['Index'] == xaxis_column_name]
    return dff['Exchange']

@app.callback(
    dash.dependencies.Output('currency', 'children'),
    [dash.dependencies.Input('crossfilter-index', 'value')])
def update_row(xaxis_column_name):
    dff = pd.read_csv("data/indexInfo.csv")
    dff = dff[dff['Index'] == xaxis_column_name]
    return dff['Currency']


@app.callback(
    dash.dependencies.Output('crossfilter-open', 'figure'),
    [dash.dependencies.Input('crossfilter-index', 'value'),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, year_value):
    dff = df[df['Index'] == xaxis_column_name]
    dff = dff[(year_value[0] <= dff['Date'].dt.year) & (dff['Date'].dt.year <= year_value[1])]
    fig = px.scatter(dff, x='Date', y="Open")
    fig.update_layout(height=300,margin={'l': 40, 'b': 20, 't': 10, 'r': 0}, hovermode='closest')
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-high', 'figure'),
    [dash.dependencies.Input('crossfilter-index', 'value'),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, year_value):
    dff = df[df['Index'] == xaxis_column_name]
    dff = dff[(year_value[0] <= dff['Date'].dt.year) & (dff['Date'].dt.year <= year_value[1])]
    fig = px.scatter(dff, x='Date', y="High")
    fig.update_layout(height=300, margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-low', 'figure'),
    [dash.dependencies.Input('crossfilter-index', 'value'),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, year_value):
    dff = df[df['Index'] == xaxis_column_name]
    dff = dff[(year_value[0] <= dff['Date'].dt.year) & (dff['Date'].dt.year <= year_value[1])]
    fig = px.scatter(dff, x='Date', y="Low")
    fig.update_layout(height=300,margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-close', 'figure'),
    [dash.dependencies.Input('crossfilter-index', 'value'),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, year_value):
    dff = df[df['Index'] == xaxis_column_name]
    dff = dff[(year_value[0] <= dff['Date'].dt.year) & (dff['Date'].dt.year <= year_value[1])]
    fig = px.scatter(dff, x='Date', y="Close")
    fig.update_layout(height=300,margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


@app.callback(
    dash.dependencies.Output('crossfilter-adjclose', 'figure'),
    [dash.dependencies.Input('crossfilter-index', 'value'),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, year_value):
    dff = df[df['Index'] == xaxis_column_name]
    dff = dff[(year_value[0] <= dff['Date'].dt.year) & (dff['Date'].dt.year <= year_value[1])]
    fig = px.scatter(dff, x='Date', y="Adj Close")
    fig.update_layout(height=300,margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-volume', 'figure'),
    [dash.dependencies.Input('crossfilter-index', 'value'),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, year_value):
    dff = df[df['Index'] == xaxis_column_name]
    dff = dff[(year_value[0] <= dff['Date'].dt.year) & (dff['Date'].dt.year <= year_value[1])]
    fig = px.scatter(dff, x='Date', y="Volume")
    fig.update_layout(height=300,margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)