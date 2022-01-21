# Data handling
import pandas as pd
import numpy as np

#Import dataset
df_poke = pd.read_csv("./data/pokedex.csv")

##Data Exploration

#Pick name and stats column
stats = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
df_poke = df_poke[["name", "hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]]

#Set name as index
df_poke.set_index("name", inplace=True)

#Set data type to int
df_poke = df_poke.astype(int)

#Transpose
df_poke = df_poke.transpose()

#Set index into stats column
df_poke = df_poke.reset_index().rename(columns={"index" : "stats"})

#Remove "name" from index
df_poke.columns.name = None

# Bokeh libraries
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel, RadioButtonGroup
from bokeh.transform import dodge

#Initiate Color Map
color_map = ["salmon", "royalblue", "palegreen", "gold"]

#Initiate Sources
source1 = ColumnDataSource(data={
    "x" : df_poke["stats"],
    "y" : df_poke["Charizard"],
    "color": [color_map[0] for i in range(6)]
})
source2 = ColumnDataSource(data={
    "x" : df_poke["stats"],
    "y" : df_poke["Arceus"],
    "color": [color_map[1] for i in range(6)]
})

#Mengatur Tooltips untuk Hover (Jika menggerakan mouse ke gambar, menampilkan data)

tooltips = [
            ("Stat","@x"),
            ("Value","@y"),
           ]

#Figure Size Variable
fig_width = 800
fig_height = 650

#Initiate tools for figure
select_tools = ['pan', 'wheel_zoom', 'save', 'reset']

#Initiate Vertical Bar Figure
fig_ver = figure(x_range = stats,
             plot_width = fig_width, 
             plot_height = fig_height,
             x_axis_label = "Stats", 
             y_axis_label = "Value",
             title="Pokemon Stats Comparison",
             tools = select_tools
            )
fig_ver.y_range.start = 0

#Initate vertical bar 1
fig_ver.vbar(x = dodge("x", -0.15, range = fig_ver.x_range), 
         top = "y", 
         width = 0.25, 
         color = "color",
         source = source1,
         legend_label = "Pokemon 1",
         muted_alpha = 0.2
        )

#Initiate vertical bar 2
fig_ver.vbar(x = dodge('x', 0.15, range = fig_ver.x_range), 
         top = "y", 
         width = 0.25, 
         color = "color",
         source = source2,
         legend_label = "Pokemon 2",
         muted_alpha=0.2
        )

#Menambahkan Hover
fig_ver.add_tools(HoverTool(tooltips=tooltips))

#Set Legend
fig_ver.legend.click_policy = "mute"
fig_ver.legend.location = "top_left"

#Initiate Horizontal Bar Figure
fig_hor = figure(y_range = stats,
             plot_width = fig_width, 
             plot_height = fig_height,
             x_axis_label = "Value", 
             y_axis_label = "Stats",
             title="Pokemon Stats Comparison", 
             tools = select_tools
            )
fig_hor.x_range.start = 0

#Initate horizontal bar 1
fig_hor.hbar(y = dodge("x", -0.15, range = fig_hor.y_range), 
         right = "y", 
         height = 0.25,
         color = "color",
         source = source1,
         hover_color = "red",
         legend_label = "Pokemon 1",
         muted_alpha = 0.2
        )

#Initiate horizontal bar 2
fig_hor.hbar(y = dodge('x', 0.15, range = fig_hor.y_range), 
         right = "y", 
         height = 0.25,
         color = "color",
         source = source2, 
         legend_label = "Pokemon 2",
         muted_alpha=0.2
        )

#Menambahkan Hover
fig_hor.add_tools(HoverTool(tooltips=tooltips))

#Set Legend
fig_hor.legend.click_policy = "mute"
fig_hor.legend.location = "top_right"

#Define update figure function
def update_fig(attr, old, new):
    selection1 = select1.value
    selection2 = select2.value
    
    new_data1 = {
        "x" : df_poke["stats"],
        "y" : df_poke[selection1],
        "color" : [color_map[RBG1.active] for i in range(6)]
    }
    new_data2 = {
        "x" : df_poke["stats"],
        "y" : df_poke[selection2],
        "color" : [color_map[RBG2.active] for i in range(6)]
    } 
    
    source1.data = new_data1
    source2.data = new_data2

#Initiate options for select (all name excluding "stats")
options = df_poke.columns.to_list()
del options[0]

#Initiate Select dropdown 1
select1 = Select(
    options = options,
    title = "Choose Pokemon 1 (red)",
    value = "Charizard"
)

#Initiate Select dropdown 2
select2 = Select(
    options = options,
    title = "Choose Pokemon 2 (blue)",
    value = "Arceus"
)

#Detect value changes in select dropdowns
select1.on_change('value', update_fig)
select2.on_change('value', update_fig)

#set color labels
color_labels = ["red","blue","yellow","green"]

#Initiate Radio Button Group 1
RBG1 = RadioButtonGroup(
    labels = color_labels,
    active = 0
)

#Initiate Radio Button Group 2
RBG2 = RadioButtonGroup(
    labels = color_labels,
    active = 1
)

RBG1.on_change('active', update_fig)
RBG2.on_change('active', update_fig)

#set layout
layout_ver = row(column(select1, RBG1, select2, RBG2), fig_ver)
layout_hor = row(column(select1, RBG1, select2, RBG2), fig_hor)

#set panel
panel_ver = Panel(child=layout_ver, title='Vertical Bar')
panel_hor = Panel(child=layout_hor, title='Horizontal Bar')

#set tabs
tabs = Tabs(tabs=[panel_ver, panel_hor])

curdoc().add_root(tabs)

color1 = "green"