import numpy as np
import pandas as pd
import geopandas as gpd
import json
from math import pi

from bokeh.models import CustomJS, Button,TextInput,RadioGroup,CheckboxButtonGroup,CheckboxGroup,DatePicker,Slider
from bokeh.models import DateRangeSlider,Dropdown, MultiSelect,Paragraph,Panel, Tabs, Text,Scatter,Plot,Toggle
from bokeh.models import HBar, LinearAxis, Grid,Label, LabelSet, Range1d
from datetime import date

#Importing Libraries
from bokeh.palettes import Spectral11, inferno, viridis, Category20,Paired,Turbo,brewer, Blues8
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource,Div,RangeSlider,Spinner,CustomJS,Range1d,Select,HoverTool,BoxZoomTool,RangeTool 
from bokeh.models import ResetTool,PanTool, DatetimeTickFormatter, NumeralTickFormatter, CDSView, IndexFilter,TapTool
from bokeh.plotting import figure, output_notebook, show
from bokeh.layouts import layout, column, gridplot,row
from bokeh.io import push_notebook
from bokeh.transform import cumsum
from bokeh.models import Panel, Tabs

from pyproj import Proj, transform

from bokeh.tile_providers import get_provider, WIKIMEDIA, Vendors,CARTODBPOSITRON

from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, LogColorMapper

from bokeh.transform import factor_cmap

from itertools import cycle

from collections import Counter
from math import pi
from bokeh.transform import cumsum


from bokeh.io import curdoc, show


dfn = pd.read_csv('https://raw.githubusercontent.com/HelenIfedi/Bokeh_covid_artefact/main/covid_proj_data3.csv', index_col ='country')

#Load Geopandas File
gdf = gpd.read_file("https://raw.githubusercontent.com/HelenIfedi/Bokeh_covid_artefact/main/map_proj.geojson")

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
df_all['circle_sizes']= df_all['circle_sizes'].apply(lambda x : x if x > 0 else 2)

df_all.rename(columns={'variable':'dates', 'value':'cases'}, inplace=True)

df_all['dates']= pd.to_datetime(df_all['dates'])

#nslices = df_all.shape[1]-3


gdf_all = gdf.merge(dfn,left_on='NAME', right_on='country')
gdf_all.drop(['MercatorX', 'MercatorY'], axis=1, inplace=True)

gdf_all = gdf_all.sort_values('NAME',ascending=True, na_position='last')

#gdf_all['alpha-2'] = ['af', '', 'al', 'dz', '', 'ad', 'ao', 'ai', '', 'ag', 'ar', 'am', 'aw', '', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bm', 'bt', '', '', 'ba', 'bw', '', 'br', '', '', 'bg', 'bf', 'bi', 'cv', 'kh', 'cm', 'ca', 'ky', 'cf', 'td', 'cl', 'cn', '', '', 'co', 'km', 'cg', '', 'ck', 'cr', '', 'hr', 'cu', '', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'sz', 'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'gf', 'pf', '', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gd', 'gp', '', 'gt', 'gg', 'gn', 'gw', 'gy', 'ht', '', 'va', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ir', 'iq', 'ie', 'im', 'il', 'it', 'jm', 'jp', 'je', 'jo', 'kz', 'ke', 'ki', '', 'kr', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', '', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', '', '', 'mc', 'mn', 'me', 'ms', 'ma', 'mz', '', 'nan', '', 'np', 'nl', 'nc', 'nz', 'ni', 'ne', 'ng', '', '', 'mk', '', 'no', 'om', 'pk', 'pw', '', 'pa', 'pg', 'py', 'pe', 'ph', '', 'pl', 'pt', '', 'qa', '', 'ro', '', 'rw', '', '', 'kn', 'lc', '', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', '', 'sk', 'si', 'sb', 'so', 'za', '', 'ss', 'es', 'lk', 'sd', 'sr', '', 'se']

gdf_all['alpha-2'] = ['af', 'al', 'dz', 'ad', 'ao', 'ai', 'ag', 'ar', 'am', 'aw', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bm', 'bt', '', 'ba', 'bw', 'br', '', 'bg', 'bf', '', 'bi', 'cv', 'kh', 'cm', 'ca', 'ky', 'cf', 'td', 'cl', 'cn', 'co', 'km', 'cg', '', 'ck', 'cr', '', 'hr', 'cu', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'sz', 'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'gf', 'pf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gd', 'gp', 'gt', 'gg', 'gn', 'gw', 'gy', 'ht', 'va', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ir', 'iq', 'ie', 'im', 'il', 'it', 'jm', 'jp', 'je', 'jo', 'kz', 'ke', 'ki', '', 'kr', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', '', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', '', 'mc', 'mn', 'me', 'ms', 'ma', 'mz', 'nan', 'np', 'nl', 'nc', 'nz', 'ni', 'ne', 'ng', 'mk', 'no', 'om', 'pk', 'pw', 'pa', 'pg', 'py', 'pe', 'ph', 'pl', 'pt', 'qa', '', 'ro', 'ru', 'rw', '', 'kn', 'lc', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', 'sk', 'si', 'sb', 'so', 'za', 'ss', 'sd', 'es', 'lk', 'sr', 'se', 'ch', 'sy', 'tj', '', 'th', 'tl', 'tg', 'to', 'tt', 'tn', 'tr', 'tc', 'us', 'ug', 'ua', 'ae', 'gb', 'uy', 'uz', 'vu', '', 'vn', '', 'ye', 'zm', 'zw']

gdf_all = pd.melt(gdf_all, id_vars=['NAME','geometry','alpha-2'], value_vars=gdf_all.columns[3:-1])

#gdf_all['circle_sizes'] = (gdf_all['value'] / gdf_all['value'].max()) * 1000
gdf_all['circle_sizes'] = (gdf_all['value'] / gdf_all['value'].mean()) * 100
gdf_all['circle_sizes']= gdf_all['circle_sizes'].apply(lambda x : x if x > 0 else 2)

gdf_all.rename(columns={'NAME': 'country','variable':'dates', 'value':'cases'}, inplace=True)

gdf_all['dates']= pd.to_datetime(gdf_all['dates'])



#Selecting Dates
date_picked = DatePicker(title='Choose date', value="2022-01-03", min_date="2020-01-22", max_date="2022-07-03", 
                             max_width=200,)
date_picked2 = DatePicker(title='Choose date', value="2022-01-03", min_date="2020-01-22", max_date="2022-07-03", 
                             max_width=200,)

#country
country_select = "United Kingdom"

#get Div Data
cum_total = df_all['cases'].loc[df_all['dates']==date_picked.value].sum()
date=date_picked.value

#Definitions for Multiline plot
def nix(val, lst):
    return [x for x in lst if x!=val]
tickers1 = Select(value = 'US', options = nix("United Kingdom", DEFAULT_TICKERS))
tickers2 = Select(value = 'United Kingdom', options = nix("US", DEFAULT_TICKERS))


#Get All data
#Choropleth Data
#Get Data
def get_m_data2(date_picked):
    m_data = gdf_all[["country","geometry","cases","circle_sizes"]].loc[gdf_all['dates']==date_picked]
    #Read data to json.
    merged_json = json.loads(m_data.to_json())
    #Convert to String like object.
    json_data = json.dumps(merged_json)
    return json_data


def get_m_data(date_picked):
    m_data = gdf_all[["country","geometry","cases","circle_sizes"]].loc[gdf_all['dates']==date_picked]
    m_data['imgs'] = gdf_all['alpha-2'].map(lambda x:'https://cdn.jsdelivr.net/gh/lipis/flag-icon-css@master/flags/4x3/'+x+'.svg')
    #Read data to json.
    merged_json = json.loads(m_data.to_json())
    #Convert to String like object.
    json_data = json.dumps(merged_json)
    return json_data


palette = Blues8
#Reverse color order so that dark blue is highest Cases.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 1600)
#Define custom tick labels for color bar.
tick_labels = {'0': '0', '300': '300', '600':'600', '900':'900', '1200':'1200', '1500':'1500', '1800':'1800', 
               '2100':'>2100', '24000': '>2400'}

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=7,width = 600, height = 10,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', 
                     major_label_overrides = tick_labels)

#Hover has tuples with column name and column value
#hover = HoverTool(tooltips=[('Country','@country'), ('No. Cases','@cases')])
TOOLTIPS = """
    <div>
        <div>
            <img
                src="@imgs" height="42" alt="No Image" width="42"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 17px; font-weight: bold;">@cases{0,0}</span>
        </div>
        <div>
            <span>@country</span>
        </div>
        <div>
            <span style="font-size: 15px;">Location</span>
            <span style="font-size: 10px; color: #696;">($x, $y)</span>
        </div>
    </div>
"""
hover = HoverTool(tooltips=TOOLTIPS)

#Scatter Map get data function
def get_circle_data(date_picked):
    
    return {"x":df_all['MercatorX'].loc[df_all['dates'] == date_picked].to_list(),
            "y":df_all['MercatorY'].loc[df_all['dates'] == date_picked].to_list(),
            "circle_sizes" :df_all['circle_sizes'].loc[df_all['dates'] == date_picked].to_list(),
            "cases":df_all['cases'].loc[df_all['dates'] == date_picked].to_list(),
            "country":df_all['country'].loc[df_all['dates'] == date_picked].to_list()
        }

cartodb = get_provider(CARTODBPOSITRON)

#Bar Chart Data collection
def get_bar_data(date_picked):    
    ncountry = df_all[['country','cases']].loc[df_all['dates']==date_picked].sort_values('cases',ascending=True, 
                                                                                     na_position='first').tail(10)
    for item in ncountry['country']:
        if item in ["United Kingdom", "United Arab Emirates"]:
            ncountry['country'].replace({"United Kingdom": "UK", "United Arab Emirates" :"UAE"}, inplace=True)
        else:
            pass          

    return ({'country': ncountry['country'].to_list(), 'cases': ncountry['cases'].to_list()})


# Donut Data
#Donut Chart Data collection
def get_pie_data(date_picked):    
    ncountry = df_all[['country','cases']].loc[df_all['dates']==date_picked].sort_values('cases',ascending=True, 
                                                                                     na_position='first').tail(5)
    ncountry['angle'] = ncountry['cases']/ncountry['cases'].sum() * 2*pi
    ncountry['color'] = palette[:5]
        

    return ({'country': ncountry['country'].to_list(), 'cases': ncountry['cases'].to_list(),
            'angle': ncountry['angle'].to_list(), 'color': ncountry['color'].to_list()})

#Div Data
cum_total = df_all['cases'].loc[df_all['dates']==date_picked.value].sum()
template=("""
      <div class='content'>
       <div class='name' style='text-align:center;'> {date}</div>
       <div class='name' style='text-align:center;font-size:10px;'>Gobal Recorded Cases</div>
        <span class='percentage' style=' font-size:50px;  margin: 0px 0px;'> {cum_total}</span>
      </div>
      """)

text = template.format(date = date, cum_total=cum_total)

#Getting Line Data
#def get_initial_line_data():
    #df_bar = pd.read_csv('C:/Users/hp/Project Data Visualisation/uk_covid_cases_test.csv')
    #df_bar['dates']= pd.to_datetime(df_bar['dates'])
    #return df_bar[["dates", "cases", "country"]]
#Getting Line Data
def get_initial_line_data(country_select):
    if country_select in ["UK","UAE"]:
        if country_select == "UK":
            country_select = "United Kingdom"
        else: 
            country_select = "United Arab Emirates"
        
        return df_all[["dates", "cases", "country"]].loc[(df_all['country']==country_select )]
        
    else:
        return df_all[["dates", "cases", "country"]].loc[(df_all['country']==country_select )]


    #return df_all[["dates", "cases", "country"]].loc[(df_all['country']==country_select  )]

#Definitions for Multiline plot
def get_mult_line_data(t1,t2): 
    xs = []
    ys = []
    colors = []
    labels = []
    
    xs.append(df_all["dates"].loc[(df_all['country']==t1)])
    xs.append(df_all["dates"].loc[(df_all['country']==t2)])
    
    ys.append(df_all["cases"].loc[(df_all['country']==t1)])
    ys.append(df_all["cases"].loc[(df_all['country']==t2)])

    labels.append(t1)
    labels.append(t2)
    
    colors.append(palette[-1])
    colors.append('black')
    
    
    return ({'x': xs, 'y': ys, 'color': colors, 'label': labels})

#Get ColumnDataSources

#MultiLine Plot
        
source_mult=ColumnDataSource(data=get_mult_line_data(tickers1.value, tickers2.value))

#Choropleth Map
geo_source = GeoJSONDataSource(geojson = get_m_data(date_picked.value))

callback = CustomJS(code="alert('you Tapped a point')")
patches_tap = TapTool(callback = callback)

#Scatter Map
circle_source = ColumnDataSource(data = get_circle_data(date_picked.value))

#Bar Chart
#Source our data
data_b=get_bar_data(date_picked.value)
source_b=ColumnDataSource(data=data_b)

#Line Plot
source_line = ColumnDataSource(data= get_initial_line_data(country_select))

#Donut Plot
source_pie = ColumnDataSource(get_pie_data(date_picked.value))

#Create figures
#Choropleth Map
p = figure(title = 'Covid Cases on ' + date_picked.value, plot_height = 317 , plot_width = 500, 
           tools=[hover, 'tap, wheel_zoom, save, reset'], toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.axis.visible = False

#Add patch renderer to figure. 
p.patches('xs','ys', source = geo_source, fill_color = {'field' :'cases', 'transform' : color_mapper},
          line_color = 'lightblue', line_width = 0.25, fill_alpha = 1)

#Specify figure layout.
p.add_layout(color_bar, 'below')
p.toolbar.autohide = True
p.title.align = "center"


#Scatter Plot
p_circle = figure(plot_width=500, plot_height=317,
           x_range=(-17254521.072957404, 17254521.072957404), 
           y_range=(-8399737.889818357, 15538711.09630922),
           x_axis_type="mercator", y_axis_type="mercator", tools="tap,hover,save, wheel_zoom, reset",
           tooltips=[("country", "@country"), ("cases", "@cases{0,0}")],
           #tooltips=("@country", "@cases"),
           #tooltips=[("country", "@country"), ("cases", "@cases"), ('First Cases ever recorded' ,'@first_case'), ( "First Covid recorded" ,'@first_date'), ('Highest Case ever recorded' ,'@highest_case'), ("Day with the highest recorded cases",'@highest_date')],
           
           title="World Daily Covid Cases on the " + date_picked.value)

p_circle.add_tile(cartodb)

p_circle.circle(x="x", y="y", size= "circle_sizes", line_color = 'darkred', alpha = 0.6, source=circle_source)
p_circle.hover.point_policy = 'follow_mouse'
p_circle.axis.axis_label=None
p_circle.axis.visible=False
p_circle.grid.grid_line_color = None
p_circle.title.align = 'center'

#Bar
p_bar = figure(y_range=source_b.data['country'], height=450, width=250, toolbar_location='right', 
           title="Top infected Regions", width_policy ='fit',
          tools="hover, tap", tooltips=("@country: " "@cases{0,0}"))
p_bar.hbar(y='country', right='cases', left=0, height=0.8, source=source_b, line_color='white', color=palette[1],
          hover_color = '#2171b5', nonselection_alpha=0.4, selection_color=palette[5] )

labels = LabelSet(y='country', x =min(source_b.data['cases']), text='country', 
                  background_fill_alpha=0.8, background_fill_color='white', text_color='#084594',y_offset = -10,
                  source=source_b,text_font_size='12px' )

p_bar.add_layout(labels)
p_bar.toolbar.autohide = True
p_bar.ygrid.grid_line_color = None
p_bar.xaxis[0].formatter = NumeralTickFormatter(format="0,0")
p_bar.axis.visible = False
p_bar.x_range.start = 0
#p_bar.axis.axis_label=None
p_bar.grid.grid_line_color = None


#Donut Plot
p_pie = figure(plot_width=200, plot_height=200, title="Top 5 Affected countries Ratio", toolbar_location=None, 
           x_range=(-0.5,0.5), y_range=(-0.4,0.6),           
           tools="hover", tooltips=[("Country", "@country"),("Cases", "@cases{0,0.}")])

p_pie.annular_wedge(x=0, y=0.1, inner_radius=0.2, outer_radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', source=source_pie)

p_pie.axis.axis_label=None
p_pie.axis.visible=False
p_pie.grid.grid_line_color = None
p_pie.title.align = "center"

#Div Plot
div = Div(text=text, style={"color": "2px solid blue", "padding":"0px 10px"},
          width = 200, width_policy ='fit', background='#deebf7')


#Line Plot
p_line = figure(
    x_axis_label="Date", 
    plot_width=650, plot_height=250, x_axis_type="datetime", tools=["hover", "wheel_zoom", "xpan"])

p_line.line(x="dates", y="cases",
       source=source_line,
       legend_label=source_line.data['country'][0],
       width=4, color=palette[6]
       )

p_line.add_tools(HoverTool(tooltips=[( "Date",  "@dates{%F}" ),( "No.Cases", "@cases{0,0}" )],formatters={'@dates': 'datetime'}))
#p_line.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
p_line.toolbar.autohide = True
p_line.yaxis.major_label_text_font_size = '0pt'
p_line.legend.location = "top_left"
p_line.title.align = "center"



#MultiLine Plot

tools="pan, wheel_zoom, xbox_select, reset, box_select, box_zoom"
mult = figure(x_axis_type="datetime", plot_width=650, plot_height=250, tools=tools, 
              x_range=(source_line.data['dates'][0], source_line.data['dates'][-1]))

mult.multi_line('x', 'y', color = 'color', legend_field = 'label',source=source_mult, line_width=2, line_alpha=0.7 )

#Format multiplot
mult.add_tools(HoverTool(tooltips=[( "Date",  "$x{%F}"), ( "Cases", "$y{0,0}" )],formatters={'$x': 'datetime'}))
mult.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")
mult.yaxis.formatter=NumeralTickFormatter(format="0,0")
#legend
mult.legend.location = "top_left"
mult.legend.orientation = "horizontal"
mult.legend.label_text_font_size = "8pt"
# Increasing the glyph height
mult.legend.glyph_height = 2
# increasing the glyph width
mult.legend.glyph_width = 8
# Increasing the glyph's label height
mult.legend.label_height = 3 
# Increasing the glyph's label height
mult.legend.label_width = 4
#mult.xaxis.axis_label = "Dates"
#mult.yaxis.axis_label = "Number of Cases"
mult.toolbar.autohide = True
#mult.legend.click_policy="mute"
mult.yaxis.major_label_orientation = 1
#Ends Here

#Inspecting Lines
p_line2 = figure( title='Time series of Covid Cases in ' + country_select, y_axis_label="New Cases", plot_width=650, plot_height=200, 
                 x_axis_type="datetime", tools='', toolbar_location=None, 
                 x_range=(source_line.data['dates'][0], source_line.data['dates'][-1]),
                 #tooltips =( [("Date", "@dates"), ("No.Cases", "@cases{0,0}")],formatters = {'Date': 'datetime'})
                 )

p_line2.line(x="dates", y="cases",
       source=source_line,
       width=3,
       )
p_line2.add_tools(HoverTool(tooltips=[( "Date",  "@dates{%F}" ),( "No.Cases", "@cases{0,0}" )],formatters={'@dates': 'datetime'}))
p_line2.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
#p_line2.legend.location = "top_left"
p_line2.title.align = "center"
p_line2.yaxis.major_label_orientation = 1

#Drag x-range
select_range = figure( plot_height= 200, plot_width = 650,  y_range=p_line2.y_range,
                x_axis_type = "datetime", tools='',toolbar_location=None)

range_tool = RangeTool(x_range=p_line2.x_range)
range_tool.overlay.fill_color = "lightblue"
range_tool.overlay.fill_alpha=0.2

select_range.line('dates','cases', source=source_line)
select_range.ygrid.grid_line_color=None
select_range.add_tools(range_tool)
select_range.toolbar.active_multi = range_tool
select_range.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
#mult.legend.click_policy="mute"
select_range.yaxis.major_label_orientation = 1

#Call Backs

#Callbacks
def date_picked_change(attrname, old, new):
    update()
    
def date_picked_change2(attrname, old, new):
    update2()
    
def update5():
    new_date_picked= date_picked.value
    patch_idx = list(range(0,ncntry))
    patch_x = []
    patch_y = []
    
    for w in df_all['circle_sizes'].loc[df_all['dates'] == new_date_picked]:
        patch_x.append(w)
    for q in df_all['cases'].loc[df_all['dates'] == new_date_picked]:
        patch_y.append(q)
    patch = {"circle_sizes":list(zip(patch_idx, patch_x)),
            "cases":list(zip(patch_idx, patch_y))}
    
    circle_source.patch(patch)
    
def update_try():
    new_date_picked = date_picked.value
    new_cases = df_all['cases'].loc[df_all['dates'] == new_date_picked].to_list()
    p.renderers.fill_color.value = {'field' :new_cases, 'transform' : color_mapper}
    
def update():
    #Bar
    new_date_picked = date_picked.value
    new_df_b = get_bar_data(new_date_picked)
    source_b.data = new_df_b
    p_bar.y_range.factors= source_b.data['country']
    
    #Scatter
    patch_idx = list(range(0,ncntry))
    patch_x = []
    patch_y = []
    
    for w in df_all['circle_sizes'].loc[df_all['dates'] == new_date_picked]:
        patch_x.append(w)
    for q in df_all['cases'].loc[df_all['dates'] == new_date_picked]:
        patch_y.append(q)
    patch = {"circle_sizes":list(zip(patch_idx, patch_x)),
            "cases":list(zip(patch_idx, patch_y))}
    
    p_circle.title.text = " World Daily Covid Cases on the " + new_date_picked
    circle_source.patch(patch)
    
    #Div Update
    cum_total = df_all['cases'].loc[df_all['dates']==new_date_picked].sum()
    div.text = template.format(date = new_date_picked, cum_total=cum_total)
        
    #Choropleth
    #geo_source.geojson = get_m_data(new_date_picked)
    
    #Donut Chart
    new_df_pie = get_pie_data(new_date_picked)
    source_pie.data =  new_df_pie


def update2():
    #Bar
    new_date_picked2 = date_picked2.value
    new_df_b = get_bar_data(new_date_picked2)
    source_b.data = new_df_b
    p_bar.y_range.factors= source_b.data['country']

    
    #Div Update
    cum_total = df_all['cases'].loc[df_all['dates']==new_date_picked2].sum()
    div.text = template.format(date = new_date_picked2, cum_total=cum_total)
        
    #Choropleth
    p.title.text = " World Covid Cases on the " + new_date_picked2
    geo_source.geojson = get_m_data(new_date_picked2)
    
    #Donut Chart
    new_df_pie = get_pie_data(new_date_picked2)
    source_pie.data =  new_df_pie

    
    
    
#MultiCallBack
def tickers1_change(attrname, old, new):
    tickers2.options=nix(new, DEFAULT_TICKERS)
    update_mult()
    
def tickers2_change(attrname, old, new):
    tickers1.options=nix(new, DEFAULT_TICKERS)
    update_mult()

def update_mult():
    t1, t2= tickers1.value, tickers2.value
    df_mult_up = get_mult_line_data(t1, t2)
    source_mult.data = df_mult_up
    
    
#Callback
def hbar_select(attrname, old, new):
    new_inds = new
    calbk_data=source_b.data
    #source_b.data['country'][7]
    new_country= calbk_data['country'][new_inds[0]]
    #print(new_country)
    new_line_data = get_initial_line_data(new_country)
    p_line.legend.items[0].label.value = new_country
    p_line2.title.text = 'Time series of Covid Cases in ' + new_country
    source_line.data = new_line_data 

    

def geo_select(attrname, old, new):
    new_inds = new
    new_country =gdf_all['country'].iloc[new_inds[0]]
    new_line_data = get_initial_line_data(new_country)
    source_line.data = new_line_data 
    p_line2.title.text = 'Time series of Covid Cases in ' + new_country

#On CHange actions
date_picked.on_change("value", date_picked_change)
date_picked2.on_change("value", date_picked_change2)
tickers1.on_change("value", tickers1_change)
tickers2.on_change("value", tickers2_change)
    
source_b.selected.on_change('indices',hbar_select)
geo_source.selected.on_change('indices',geo_select)

#Layout2
#tickers =row(tickers1, tickers2)
mult_row = column(p_line2, select_range)
side_bar = column(div, p_bar)
left_row = column(date_picked2,p_pie)
map_row = row(p, left_row)
map_line = column(map_row, mult_row)
panel2_child = row(side_bar, map_line, background='white')
tab2 = Panel(child=panel2_child, title="Choropleth")

#Layout1
tickers =row(tickers1, tickers2)
mult_row1 = column(tickers, mult)
#side_bar1 = column(div, p_bar)
left_row1 = column(date_picked,p_pie)
map_row1 = row(p_circle, left_row1)
map_line1 = column(map_row1, mult_row1)
panel1_child = row(side_bar, map_line1, background='white')
tab1 = Panel(child=panel1_child, title="Scatter")

tabs = Tabs(tabs=[ tab1, tab2 ])


#Bokeh Server
#curdoc().theme = 'dark_minimal'
#curdoc().add_root(column(date_picked,row(p_bar, p_circle)))
curdoc().add_root(tabs)
curdoc().tittle = "Second Dashboard"