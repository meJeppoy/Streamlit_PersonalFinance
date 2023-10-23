import streamlit as st
import plotly.express as px
import pandas as pd
import duckdb
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
df.rename(columns={"Category Type": "Transaction_type"}, inplace=True)

# Change negative values in Amount column to positive
df["Amount"] = df["Amount"].astype("str")
df["Amount"] = df["Amount"].str.replace("-", "").astype("float")


# Create new columns for Month and Year
date_col = pd.DatetimeIndex(df["Date"])
df["Year"] = date_col.year
df["Month"] = date_col.month
df["year_str"] = df["Date"].dt.strftime("%Y").astype("string")
df["month_name"] = df["Date"].dt.strftime("%b").astype("string")

with st.expander("Preview Finance Transactions data"):
    st.dataframe(
        df,
        column_config={
            "Date": st.column_config.DateColumn(format="MMM, D, YYYY"),
            "Year": st.column_config.NumberColumn(format="%d"),
            "Debit": st.column_config.NumberColumn(format="$ %.2f"),
            "Credit": st.column_config.NumberColumn(format="$ %.2f"),
            "Amount": st.column_config.NumberColumn(format="$ %.2f"),
        },
    )

all_months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
all_year = df["Year"].unique()


selected_month = st.selectbox("Choose applicable Month", all_months)
selected_year = st.selectbox("Choose applicable Year", all_year)
# st.write(df["Amount"].dtype)


def plot_bottom_left():
    expenses_data = duckdb.sql(
        f"""
            SELECT
            Transaction_type, month_name, SUM(Amount)
            FROM df
            WHERE Year={selected_year}
            AND Transaction_type='Expense'
            GROUP BY Transaction_type, month_name, Month
            ORDER BY Month ASC
        """
    ).df()

    expense_graph = px.bar(
        expenses_data,
        x="month_name",
        y="sum(Amount)",
        color="Transaction_type",
        color_discrete_sequence=["salmon"],
        text_auto=True,
        title="Monthly Expenses",
    )
    st.plotly_chart(expense_graph, use_container_width=True)

    income_data = duckdb.sql(
        f"""
            SELECT
            Transaction_type, month_name, SUM(Amount)
            FROM df
            WHERE Year={selected_year}
            AND Transaction_type='Income'
            GROUP BY Transaction_type, month_name, Month
            ORDER BY Month ASC
        """
    ).df()

    income_graph = px.bar(
        income_data,
        x="month_name",
        y="sum(Amount)",
        color="Transaction_type",
        color_discrete_sequence=["green"],
        text_auto=True,
        title="Monthly Income",
    )
    st.plotly_chart(income_graph, use_container_width=True)


plot_bottom_left()
