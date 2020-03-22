import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from config import MAPBOX_ACCESS_TOKEN
from importer import import_json_ms_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

df = import_json_ms_data()

df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d,%H:%M:%S')
df.lat = df.lat.astype('float')
df.lon = df.lon.astype('float')

fig = px.line_mapbox(df,
                     lat="lat",
                     lon="lon",
                     color="id"
                     )
fig.update_layout(mapbox_zoom=4,
                  mapbox_center_lat=41,
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})

timestamps = df['timestamp'].map(lambda x: dt.datetime(x.year, x.month, 1)).unique()
timestamps.sort()
values = [str(x.year) + '-' + str(x.month) for x in pd.DatetimeIndex(timestamps)][0::6]
labels = [int(x.timestamp()) for x in pd.DatetimeIndex(timestamps)][0::6]
zipped = zip(labels, values)
marks = dict(zipped)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='COTRA Simulator'),

    html.Div(children='''
        Dash: Tracked data of microsoft data.
    '''),

    dcc.Graph(
        id='main_graph',
        figure=fig
    ),
    dcc.RangeSlider(
        id='slider',
        updatemode='mouseup',
        min=int(df['timestamp'].min().timestamp()),
        max=int(df['timestamp'].max().timestamp()),
        value=[df['timestamp'].min().timestamp(), df['timestamp'].mean().timestamp()],
        className="dcc_control",
        marks=marks,
        allowCross=False
    ),
])


def filter_dataframe(df, year_slider):
    dff = df[(df['timestamp'] > dt.datetime.fromtimestamp(year_slider[0]))
             & (df['timestamp'] < dt.datetime.fromtimestamp(year_slider[1]))]
    return dff


# Slider -> count graph
@app.callback(Output('main_graph', 'figure'),
              [Input('slider', 'value')])
def update_year_slider(slider):
    dff = filter_dataframe(df, slider)

    fig = px.line_mapbox(dff, lat="lat",
                         lon="lon",
                         color="id"
                         )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
