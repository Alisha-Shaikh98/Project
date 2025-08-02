import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("../datasets/city_hour.csv")
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.dropna(subset=['City'])
    return df

df = load_data()
print(df.columns)
cities = df['City'].unique()

st.sidebar.title("Air Quality Explorer")
selected_city = st.sidebar.selectbox("Selected a City", sorted(cities))
date_range = st.sidebar.date_input("Select Date Range", [df['Datetime'].min(), df['Datetime'].max()])

#filter Data(mask)
mask = (
    (df['City'] == selected_city) &
    (df['Datetime'] >= pd.to_datetime(date_range[0])) &
    (df['Datetime'] <= pd.to_datetime(date_range[1]))
)

city_data = df[mask]

#Data Printing
st.header("Presenting Data")
st.write("Filtered Data Shape:", city_data.shape)
st.dataframe(city_data.head())

st.html("<hr>")            
st.title(f"Air Quality in {selected_city}")
st.markdown(f"Showing data from **{date_range[0]}** to **{date_range[1]}**")

fig_pm25 = px.line(city_data, x='Datetime', y='PM2.5', title='PM2.5 Levels Over Time')
st.plotly_chart(fig_pm25)
st.subheader("Other Pollutants")
st.html("<hr>") 

for pollutant in ['PM10', 'NO', 'NO2', 'NOx', 'CO', 'SO2', 'O3']:
    fig = px.line(city_data, x='Datetime', y= pollutant, title=f"{pollutant} Levels")
    st.plotly_chart(fig)
    st.html("<hr>") 