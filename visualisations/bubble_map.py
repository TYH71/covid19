import pandas as pd
import plotly.express as px
# Live COVID-19 Data by John Hopkins University, Center for Systems Science and Engineering
covid_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
covid_df = covid_df.rename(columns={
    'Country_Region': 'Country',
    'Long_': 'Long'
})
sidebar = 'Confirmed'
bubble_map = px.scatter_geo(covid_df[['Lat', 'Long', 'Country', sidebar]].dropna(),
    lat='Lat',
    lon='Long',
    hover_name='Country', 
    size=sidebar, 
    projection='robinson',
    color=sidebar,
    size_max=50,
    color_continuous_scale = ['deepskyblue','red']
)
bubble_map.update_geos(
    resolution=110,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue"
)
bubble_map.update_layout(
    height=350, 
    margin={"r":15,"t":15,"l":15,"b":15}, 
    paper_bgcolor='white'
)
bubble_map.show()