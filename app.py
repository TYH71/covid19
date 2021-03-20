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
st.markdown('''
<style>
    body {
        background-color:#f8f5f1;
    }
    h1, h2, h3, h4, h5, h6, p {
        color:#130654;
    }
</style>
''', unsafe_allow_html=True)

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
    "Active": 'Current Active COVID-19 Cases', 
    "Incident_Rate": 'Incident Rate', 
    "Mortality_Rate": 'Mortality Rate'
}
description = {
    "Confirmed": 'Counts include confirmed and probable (where reported).', 
    "Deaths": 'Counts include confirmed and probable (where reported).', 
    "Recovered": 'Recovered cases are estimates based on local media reports, and state and local reporting when available, and therefore may be substantially lower than the true number.', 
    "Active": 'Active cases = total cases - total recovered - total deaths.', 
    "Incident_Rate": 'Incidence Rate = cases per 100,000 persons.', 
    "Mortality_Rate": 'Case-Fatality Ratio (%) = Number recorded deaths / Number cases.'
}


# side bar
st.sidebar.title('COVID-19 Dashboard')
sidebar = st.sidebar.selectbox(
    "Feature Selection",
    ("Confirmed", "Deaths", "Recovered", "Active", "Incident_Rate", "Mortality_Rate")
)
st.sidebar.header('About')
st.sidebar.info('''
This web application is authored and maintained by TYH71, with aims to create visualisations for COVID-19 Data.
''')

# Header on Streamlit
with st.beta_container():

    st.markdown('''
    # COVID-19 Dashboard
    ''')
    st.info('''
        This web application aims to deliver interative dashboard with relevant visualisations based on real time COVID-19 Pandemic Data.
        It was first identified in December 2019 in Wuhan, China. 
        The World Health Organization declared the outbreak a Public Health Emergency of International Concern in January 2020 and a pandemic in March 2020.
    ''')
    st.markdown('''
        > - Author :\tTYH71
        > - Data :\tCOVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
        > - Source: https://github.com/CSSEGISandData/COVID-19/
    ''')
    dependency = st.beta_expander('Dependencies')
    dependency.code('''
    import pandas as pd
    import plotly.express as px
    import streamlit as st
    ''')

st.write('---')


# Displaying Data
with st.beta_container():
    st.markdown('''
    ### COVID-19 Data
    ''')
    st.code('''
    covid_df = pd.read_csv(source)
    print(covid_df)
    ''')
    st.dataframe(covid_df.style.highlight_max(axis=0))

st.write('---')


# Bubble Map - Total COVID-19 Cases across the world
with st.beta_container():
    st.write(f"### {title[sidebar]}")
    st.code(f'''
    # Bubble Map to show the {title[sidebar]} around the world.
    # Description: {description[sidebar]}
    # Multivariate : Latitude, Longitude, Country, {sidebar}
    ''')
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
    st.plotly_chart(bubble_map)

st.write('---')


# Bar Chart - According to Confirmed Cases across the world
with st.beta_container():
    st.write(f"### Top 10 ranking by '{sidebar}'")
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
    st.plotly_chart(bar)
