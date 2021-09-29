"""
# COVID-19 Dashboard
## User Guide
    Console:
    pip install streamlit
    streamlit run app.py
"""

# Import Libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import requests as req
from streamlit.proto.DataFrame_pb2 import DataFrame

# Import Data
covid_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
covid_df = covid_df.rename(columns={
    'Country_Region': 'Country',
    'Long_': 'Long'
})
covid_df = covid_df.drop(columns=['People_Tested', 'People_Hospitalized'])
title = {
    "Confirmed": 'Confirmed COVID-19 Cases', 
    "Deaths": 'Death Count caused by COVID-19', 
    "Recovered": 'Recovered Cases', 
    "Active": 'Current Active COVID-19 Cases'
}
description = {
    "Confirmed": 'Counts include confirmed and probable (where reported).', 
    "Deaths": 'Counts include confirmed and probable (where reported).', 
    "Recovered": 'Recovered cases are estimates based on local media reports, and state and local reporting when available, and therefore may be substantially lower than the true number.', 
    "Active": 'Active cases = total cases - total recovered - total deaths.'
}


# side bar
st.sidebar.title('COVID-19 Dashboard')
sidebar = st.sidebar.selectbox(
    "Feature Selection",
    ("Confirmed", "Deaths")
)
st.sidebar.header('About')
st.sidebar.info('''
This web application is authored and maintained by TYH71, with aims to create visualisations for COVID-19 Data.
''')
st.sidebar.header('Contribute')
st.sidebar.info('''
GitHub Page can be found here.
https://github.com/TYH71/covid19
''')


# Header on Streamlit
with st.container():

    st.markdown('''
    # COVID-19 Dashboard
    ''')
    st.info('''
        This web application aims to deliver interative dashboard with relevant visualisations based on real time COVID-19 Pandemic Data.
        It was first identified in December 2019 in Wuhan, China. 
        The World Health Organization declared the outbreak a Public Health Emergency of International Concern in January 2020 and a pandemic in March 2020.
        Data is sourced from John Hopkins University CSSE.
    ''')
    st.markdown('''
        > - Author :\tTYH71
        > - Data :\tCOVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
        > - Source: https://github.com/CSSEGISandData/COVID-19/
        > - Time-series API: https://covid19api.com
    ''')
    dependency = st.expander('Dependencies')
    dependency.code('''
    import pandas as pd
    import plotly.express as px
    import streamlit as st
    import requests as req
    ''')

st.write('---')


# Displaying Data
with st.container():
    st.markdown('''
    ### COVID-19 Data
    ''')
    st.code('''
    covid_df = pd.read_csv(source)
    print(covid_df)
    ''')
    st.dataframe(covid_df.style)

st.write('---')


# Bubble Map - Total COVID-19 Cases across the world
with st.container():
    st.write(f"### {title[sidebar]}")
    st.code(f'''
    # Bubble Map to show the {title[sidebar]} around the world.
    # Description: {description[sidebar]}
    # Multivariate : Latitude, Longitude, Country, {sidebar}
    ''')
    # bubble_map = px.scatter_geo(covid_df[['Lat', 'Long', 'Country', sidebar]].dropna(),
    #     lat='Lat',
    #     lon='Long',
    #     hover_name='Country', 
    #     size=sidebar, 
    #     projection='robinson',
    #     color=sidebar,
    #     size_max=50,
    #     color_continuous_scale = ['deepskyblue','red']
    # )
    # bubble_map.update_geos(
    #     resolution=110,
    #     showcoastlines=True, coastlinecolor="RebeccaPurple",
    #     showland=True, landcolor="LightGreen",
    #     showocean=True, oceancolor="LightBlue",
    #     showlakes=True, lakecolor="Blue",
    #     showrivers=True, rivercolor="Blue"
    # )
    # bubble_map.update_layout(
    #     height=350, 
    #     margin={"r":15,"t":15,"l":15,"b":15}, 
    #     paper_bgcolor='white'
    # )

    ## Updated on 29th Sep
    bubble_map = px.scatter_mapbox(
        data_frame=covid_df[['Lat', 'Long', 'Country', sidebar]].dropna(),
        lat='Lat',
        lon='Long',
        hover_name='Country',
        color=sidebar,
        mapbox_style="carto-positron",
        size=sidebar,
        size_max=50,
        color_continuous_scale = ['deepskyblue','red'],
        zoom=.5
    )

    st.plotly_chart(bubble_map)

st.write('---')


# Time-Series Graph
with st.container():
    st.write('### Time Series Graph')
    st.code(f'''
    # Time Series Graph presents the COVID-19 Data Points at each time intervals.
    # Description: {description[sidebar]}
    # Trivariate: Country, Date, {sidebar}
    ''')
    # Request List of Countries
    countries_raw = req.get('https://api.covid19api.com/countries').json()
    countries = pd.DataFrame.from_dict(countries_raw).sort_values(by='Country')
    countries.reset_index(drop=True, inplace=True)
    select_country = st.selectbox('Select Country', countries['Country'], index=200)
    select_slug = countries[countries['Country']==select_country]['Slug'].values[0]
    try:
        # Request Time Series
        time_series_raw = req.get(f"https://api.covid19api.com/live/country/{select_slug}").json()
        time_df = pd.DataFrame.from_dict(time_series_raw)
        if (time_df.empty):
            raise Exception 
        time_df['Date'] = pd.to_datetime(time_df['Date'])
        # Visualisation
        time_series_chart = px.line(
            time_df,
            x='Date', 
            y=sidebar,
            hover_data=['Country'],
            title=select_country
        )
        time_series_chart.update_layout(
            height=450, 
            margin={"r":5,"t":50,"l":5,"b":50},
            paper_bgcolor='white',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=14,
                            label="2W",
                            step="day",
                            stepmode="backward"),
                        dict(count=1,
                            label="1M",
                            step="month",
                            stepmode="backward"),
                        dict(label='All',
                            step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
            title={
                'x':0.5,
                'xanchor': 'center'
            }
        )
        st.plotly_chart(time_series_chart)
    except Exception as e:
        st.code('''
    # Time-Series Data not available.
        ''')

st.write('---')


# Bar Chart - According to Confirmed Cases across the world
with st.container():
    st.write(f"### Top 10 Countries by '{sidebar}'")
    st.code(f'''
    # Bar Chart to show the rankings between countries according to '{sidebar}'
    # Description: {description[sidebar]}
    # Bivariate : Country, {sidebar}
    ''')
    threshold = 10
    bar = px.bar(covid_df[['Country', sidebar]].dropna().sort_values(sidebar, ascending=False)[:threshold], 
        y=sidebar,
        x='Country', 
        color=sidebar,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    bar.update_layout(
        height=400, 
        margin={"r":15,"t":15,"l":15,"b":15},
        paper_bgcolor='white'
    )

    bar.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    st.plotly_chart(bar)
