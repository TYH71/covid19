"""
# COVID-19 Dashboard

## User Guide
    Console:
    pip install streamlit
    streamlit run dashboard.py
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

# side bar
st.sidebar.title('COVID-19 Dashboard')
sidebar = st.sidebar.selectbox(
    "Feature Selection",
    ("Confirmed", "Deaths", "Recovered", "Active")
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
    st.write(f"### COVID-19 '{sidebar}' Cases")
    st.code(f'''
    # Bubble Map to show the COVID-19 related cases around the world.
    # Multivariate : Latitude, Longitude, Country, {sidebar}
    ''')
    bubble_map = px.scatter_geo(covid_df[['Lat', 'Long', 'Country', sidebar]].dropna(),
        lat='Lat',
        lon='Long',
        hover_name='Country', 
        size=sidebar, 
        projection='natural earth',
        color=sidebar,
        size_max=50,
        color_continuous_scale = ['deepskyblue','red']
    )
    bubble_map.update_layout(paper_bgcolor='white')
    st.plotly_chart(bubble_map)

st.write('---')


# Bar Chart - According to Confirmed Cases across the world
with st.beta_container():
    st.write(f"### Top 10 ranking by '{sidebar}' Cases")
    st.code(f'''
    # Bar Chart to show the rankings between countries according to '{sidebar}'
    # Bivariate : Country, {sidebar}
    ''')
    threshold = 10
    bar = px.bar(covid_df[['Country', sidebar]].dropna().sort_values(sidebar, ascending=False)[:threshold], 
        y=sidebar,
        x='Country', 
        color=sidebar,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    bar.update_layout(paper_bgcolor='white')
    st.plotly_chart(bar)
  