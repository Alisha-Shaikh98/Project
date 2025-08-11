import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data,preprocess_data
from prophet import Prophet 
import pickle

st.set_page_config(page_title="Time Series Forecast", layout="wide")

st.title("Local Forecasting and Visualizer")

#Sidebar
st.sidebar.header("Upload your CSV")
uploaded_file = st.sidebar.file_uploader("Choose a time series CSV", type=['csv'])

if uploaded_file is not None:
    df= load_data(uploaded_file)
    st.success("Data uploaded Successfully")

else:
    st.info("No file uploaded, Using simple Dataset (Air Passengers)")
    df=pd.read_csv(r"C:\Users\Lenovo\Desktop\pythonadvance\Project\4-6projects\5. Time Series\data\air_passengers.csv")

st.subheader("Raw Data")
st.dataframe(df.head())

#Select Datetime and target Column
columns = df.columns.tolist()
with st.sidebar:
    st.markdown("---")
    date_col = st.selectbox("Select Date Column", options=columns)
    target_col = st.selectbox("Select Target Columns", options=columns)

try:
    df_clean = preprocess_data(df, date_col,target_col)

    #Plot the time series
    st.subheader("Time Series Plot")
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df_clean[date_col], df_clean[target_col], marker= 'o', linestyle='-')
    ax.set_xlabel("Date")
    ax.set_ylabel(target_col)
    ax.set_title(f"{target_col} Over time")
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error preprocessing Date: {e}")

def forecaster(file):
    st.subheader("Forecasting!!")
    df = pd.read_csv(file)
    df['ds'] = pd.to_datetime(df['ds'])

    model = Prophet()
    model.fit(df)

    with open("model\forecast_model.pkl", "wb") as f:
        pickle.dump(model, f)

    st.write("Model trained and saved as forecast_model.pkl")

forecaster(df)