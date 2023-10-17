import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Personal Finance Tracker", page_icon=":bar_chart:", layout="wide"
)

st.title(":bar_chart: Personal Finance Tracker")
st.markdown("_ver. 1.0.0_")


# Getting data from an excel file and cast as dataframe using pandas
@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    # Data cleaning and prep can be done here
    return data


# Streamlit widget to upload data file
with st.sidebar:
    st.header("Configure Tracker")
    upload_file = st.file_uploader("Choose a file")

if upload_file is None:
    st.info(" Upload a file through config", icon="🚨")
    st.stop

df = load_data(upload_file)

# Create new columns for Month and Year
date_col = pd.DatetimeIndex(df["Date"])
df["Year"] = date_col.year
df["Month"] = date_col.month

with st.expander("Preview Finance Transactions data"):
    st.dataframe(
        df,
        column_config={
            "Date": st.column_config.DateColumn(format="MMM, D, YYYY"),
            "Month": st.column_config.DateColumn(format="MMM"),
            "Year": st.column_config.NumberColumn(format="%d"),
            "Debit": st.column_config.NumberColumn(format="$ %.2f"),
            "Credit": st.column_config.NumberColumn(format="$ %.2f"),
            "Amount": st.column_config.NumberColumn(format="$ %.2f"),
        },
    )
