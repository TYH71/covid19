# COVID-19 Dashboard

This web application aims to deliver interative dashboard with relevant visualisations based on real time COVID-19 Pandemic Data. It was first identified in December 2019 in Wuhan, China. The World Health Organization declared the outbreak a Public Health Emergency of International Concern in January 2020 and a pandemic in March 2020. Data is sourced from Johns Hopkins University CSSE.

![image](https://user-images.githubusercontent.com/64251764/111898058-979ade00-8a5e-11eb-8510-ede37f461ef8.png)

- Author : TYH71
- Data : COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
- Source: https://github.com/CSSEGISandData/COVID-19/
- Dependencies: streamlit, pandas, plotly

![image](https://user-images.githubusercontent.com/64251764/111898076-c1ec9b80-8a5e-11eb-9e0a-3a6dc988d384.png)

This data set is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) by the Johns Hopkins University on behalf of its Center for Systems Science in Engineering.

Data URL: https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv

## Running the Web App

Ensure streamlit is being installed in the environment before hand

<code>pip install streamlit --upgrade</code>

Run this command in the console

<code>streamlit run app.py</code>

## Files

- app.py - main web application file deployed using streamlit
- updated.ipynb - jupyter notebook file to show initial numerical and graphical summaries based on live data
- time_series.ipynb - work around time series data

## Visualisations

### Scatter Map
Display data points across the map. <br>
Map projection: Robinson <br>
![image](https://user-images.githubusercontent.com/64251764/111898095-db8de300-8a5e-11eb-9877-e3f6588189f8.png)

### Time-Series Graph
Features a slider and country selection. <br>
![image](https://user-images.githubusercontent.com/64251764/111898105-eea0b300-8a5e-11eb-9e84-2f521de6be6f.png)

### Ranking Chart
Top 10 countries in terms of ranking <br>
![image](https://user-images.githubusercontent.com/64251764/111898119-fd876580-8a5e-11eb-8251-d2e503d75d6f.png)
