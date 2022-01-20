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
from bokeh.models import ColumnDataSource, Select, Range1d
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel
from bokeh.transform import dodge

#Initiate Sources
source1 = ColumnDataSource(data={
    "x" : df_poke["stats"],
    "y" : df_poke["Charizard"]
})
source2 = ColumnDataSource(data={
    "x" : df_poke["stats"],
    "y" : df_poke["Arceus"]
})

#Initiate tools for figure
select_tools = ['pan', 'wheel_zoom', 'save', 'reset']

#Initiate y_max for y_range
y_max = max(df_poke[["Charizard","Arceus"]].max())

#Initiate Figure
fig = figure(x_range = stats,
             plot_width = 650, 
             plot_height = 700, 
             title="Pokemon Stats Comparison", 
             tools = select_tools
            )

#Initate bar 1
fig.vbar(x = dodge("x", -0.15, range = fig.x_range), 
         top = "y", 
         width = 0.25,
         source = source1, 
         color = "salmon", 
         legend_label = "Pokemon 1",
         muted_alpha = 0.2
        )

#Initiate bar 2
fig.vbar(x = dodge('x', 0.15, range = fig.x_range), 
         top = "y", 
         width = 0.25,
         source = source2, 
         color = "royalblue", 
         legend_label = "Pokemon 2",
         muted_alpha=0.2
        )

#Set Legend
fig.legend.click_policy = "mute"
fig.legend.location = "top_left"

#Define update figure function
def update_fig(attr, old, new):
    selection1 = select1.value
    selection2 = select2.value
    
    new_data1 = {
        "x" : df_poke["stats"],
        "y" : df_poke[selection1]
    }
    new_data2 = {
        "x" : df_poke["stats"],
        "y" : df_poke[selection2]
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

#set layout
layout = row(column(select1, select2), fig)

curdoc().add_root(layout)
#test