from bokeh import models, plotting, io
import pandas as pd
from time import sleep
from itertools import cycle
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource

import pandas as pd
from bokeh.models import CustomJS, Button,TextInput,RadioGroup,CheckboxButtonGroup,CheckboxGroup,DatePicker
from bokeh.models import DateRangeSlider,Dropdown, MultiSelect,Paragraph,Panel, Tabs, Text,Scatter,Plot
from bokeh.models import HBar, LinearAxis, Grid
from datetime import date

#Importing Libraries
from bokeh.palettes import Spectral11, inferno, viridis, Category20,Paired,Turbo,brewer
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource,Div,RangeSlider,Spinner, CustomJS, Range1d, Select, HoverTool,BoxZoomTool 
from bokeh.models import ResetTool,PanTool, DatetimeTickFormatter, NumeralTickFormatter, CDSView, IndexFilter,TapTool
from bokeh.plotting import figure, output_notebook, show
from bokeh.layouts import layout, column, gridplot,row

import numpy as np

from pyproj import Proj, transform

from bokeh.plotting import figure
from bokeh.tile_providers import get_provider,CARTODBPOSITRON
from bokeh.io import  show

import warnings


dfn = pd.read_csv('https://raw.githubusercontent.com/HelenIfedi/Bokeh_covid_artefact/main/covid_proj_data3.csv', index_col ='country')

dfn.dropna(subset = ['Lat', 'Long'], inplace=True)
inProj = Proj(init='epsg:3857')
outProj = Proj(init='epsg:4326')

a=[]
b=[]
for lon, lat in list(zip(dfn["Long"], dfn["Lat"])):
    x, y = transform(outProj,inProj,lon,lat)
    a.append(x)
    b.append(y)
    
dfn['MercatorX'] = a
dfn['MercatorY'] = b

dfn.drop(['Lat', 'Long'], axis=1, inplace=True)
ncntry= dfn.shape[0]
nslices = dfn.shape[1]
DEFAULT_TICKERS = dfn.index

dfn.reset_index(inplace =True)

df_all = pd.melt(dfn, id_vars=['country', 'MercatorX', 'MercatorY'], value_vars=dfn.columns[1:-1])

df_all['circle_sizes'] = df_all['value'] / df_all['value'].max() * 100
df_all['circle_sizes']= df_all['circle_sizes'].apply(lambda x : x if x > 0 else 1)

df_all.rename(columns={'variable':'dates', 'value':'cases'}, inplace=True)

df_all['dates']= pd.to_datetime(df_all['dates'])

#Line Data
state ='United Kingdom'

state_data = df_all[['dates', 'cases']].loc[df_all['country']==state]
state_data.rename(columns= {'United Kingdom':'cases'}, inplace=True)


source = ColumnDataSource(state_data)

#Scatter Plot Data
data_scr= ColumnDataSource(data=df_all.iloc[:ncntry])

cartodb = get_provider(CARTODBPOSITRON)

p = figure(plot_width=720, plot_height=400,
           x_range=(-17254521.072957404, 17254521.072957404), 
           y_range=(-8399737.889818357, 15538711.09630922),
           x_axis_type="mercator", y_axis_type="mercator",
           tooltips=[("country", "@country"), ("Cases", "@cases")],
           #tooltips=("@country", "@cases"),
           title="Time Series of daily Covid cases around the world")

p.add_tile(cartodb)


p.circle(x="MercatorX", y="MercatorY",
         size='circle_sizes',
         fill_color="dodgerblue", line_color="dodgerblue",
         fill_alpha=0.3,
         source=data_scr)
p.title.align = "center"


#Line Plot
#plot
p_line = figure(
    x_axis_label="Date", y_axis_label="New Cases", title="Stream Of Covid Daily Cases Through time",
    plot_width=700, plot_height=200, x_axis_type="datetime", tools=["hover", "wheel_zoom"])

p_line.line(x="dates", y="cases",
       source=source,
       legend_label=state,
       width=4,
       )
p_line.legend.location = "top_left"
p_line.title.align = "center"
p_line.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
p_line.yaxis.major_label_orientation = 1

io.curdoc().add_root(column(p, p_line, background="white"))

#Circle Streaming
index_generator_circle = cycle(range(nslices))
def stream_circle():    
    
    #global index  
    index_c = next(index_generator_circle)
    start_c = (index_c+1)* ncntry
    end_c = (index_c +2) * ncntry
    
    """Add `num_points` circles to figure `fig`."""
    patch_id = list(range(0,ncntry))
    patch_id = [int(iy) for iy in patch_id]
    patch_circle_size = list(df_all['circle_sizes'].iloc[start_c:end_c])
    patch_cases = list(df_all['cases'].iloc[start_c:end_c])    
    patch = {"circle_sizes":list(zip(patch_id, patch_circle_size)),
            "cases":list(zip(patch_id, patch_cases))}
    
    data_scr.patch(patch)

#Line Streaming    
index_generator = cycle(range(len(state_data.index)))
def stream():
    index = next(index_generator)
    if index + 1 == len(state_data.index):
        sleep(2)    
        
    source.data = state_data.iloc[:index]

    
io.curdoc().add_periodic_callback(stream_circle, 5)
io.curdoc().add_periodic_callback(stream, 10)
