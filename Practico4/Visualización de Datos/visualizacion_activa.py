from os.path import dirname, join

import numpy as np
import pandas as pd
import datetime
import json

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc

tweets = pd.read_json('tweets.json')
tweets['user'] = tweets.apply(lambda row: row.user['screen_name'],axis=1)
tweets['dia_semana'] = tweets.apply(lambda row: row.created_at.date().isoweekday(),axis=1)
tweets['hora'] = tweets.apply(lambda row: row.created_at.hour,axis=1)
tweets['mes'] = tweets.apply(lambda row: row.created_at.month,axis=1)
tweets['created_at'] = tweets.apply(lambda row: row.created_at.date().strftime('%d/%m/%y'),axis=1)

tweets['color'] = np.where(tweets['retweeted'] == True, 'green','blue')
tweets["alpha"] = np.where(tweets['retweeted'] == True, 0.9, 0.25)


tweets.fillna(0, inplace=True)  # just replace missing values with zero

axis_map = {
    "Meses": "mes",
    "Dias de la Semana": "dia_semana",
    "Horario": "hora"
}

# Create Input controls
favoritos = Slider(title="Numero de Favoritos", value=10, start=0, end=300, step=10)
retweets = Slider(title="Numero de ReTweets", start=0, end=1000, value=0, step=10)
palabras = TextInput(title="Buscador palabras")

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Dias de la Semana")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Horario")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[],
user=[], created_at=[],
favorite_count=[], retweet_count=[],
 color=[], dia_semana=[], mes=[], hora=[], alpha=[]))

TOOLTIPS=[
    ("Usuario", "@user"),
    ("Fecha", "@created_at"),
    ("Favoritos", "@favorite_count"),
    ("Retweets", "@retweet_count")
]

p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tooltips=TOOLTIPS)
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None, fill_alpha="alpha")


def select_tweets():
    palabras_val = palabras.value.strip()
    selected = tweets[
        (tweets.favorite_count >= favoritos.value) &
        (tweets.retweet_count >= retweets.value)
    ]
    if (palabras_val != ""):
        selected = selected[selected.text.str.contains(palabras_val)==True]
    return selected

def update():
    df = select_tweets()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d tweets seleccionados" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        dia_semana=df['dia_semana'], 
        mes=df['mes'], 
        hora=df['hora'],
        alpha=df["alpha"],
        user=df['user'],
        created_at=df['created_at'],
        favorite_count=df['favorite_count'], 
        retweet_count=df['retweet_count'],
    )

controls = [favoritos, retweets, palabras, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Tweets"