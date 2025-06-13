import streamlit as st
import pandas as pd
import numpy as np

# --- Configuration ---
# Set the page configuration for the Streamlit app.
# 'layout="wide"' uses the full width of the browser.
st.set_page_config(layout="wide", page_title="Simple Sales Dashboard", page_icon="📊")

# --- Data Generation ---
# Function to generate dummy sales data.
# This function creates a Pandas DataFrame with random sales figures
# over a specified number of days.
@st.cache_data # Cache the data to improve performance, especially for larger datasets.
def generate_sales_data(num_days=100):
    """
    Generates a DataFrame with dummy sales data.

    Args:
        num_days (int): The number of days for which to generate data.

    Returns:
        pd.DataFrame: A DataFrame with 'Date', 'Sales', and 'Region' columns.
    """
    dates = pd.date_range(start="2024-01-01", periods=num_days, freq="D")
    sales = np.random.randint(100, 1000, size=num_days)
    regions = np.random.choice(['North', 'South', 'East', 'West'], size=num_days)
    data = pd.DataFrame({
        'Date': dates,
        'Sales': sales,
        'Region': regions
    })
    return data

# Generate the data for the dashboard.
df = generate_sales_data(200)

# --- Dashboard Title and Introduction ---
st.title("📊 Simple Sales Dashboard")
st.markdown("""
This dashboard demonstrates a basic sales overview using Streamlit.
You can filter the data by date range and region using the sidebar controls.
""")

# --- Sidebar for Filters ---
# The 'with st.sidebar:' block places the following widgets in the sidebar.
with st.sidebar:
    st.header("Filters")

    # Date range slider
    # Allows users to select a range of dates to filter the data.
    min_date = df['Date'].min().to_pydatetime() # Convert Timestamp to datetime.date
    max_date = df['Date'].max().to_pydatetime() # Convert Timestamp to datetime.date

    date_range = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # Convert selected date range back to pandas Timestamps for filtering
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])


    # Region multiselect
    # Allows users to select one or more regions.
    all_regions = df['Region'].unique().tolist()
    selected_regions = st.multiselect(
        "Select Region(s)",
        options=all_regions,
        default=all_regions # All regions are selected by default.
    )

# --- Apply Filters ---
# Filter the DataFrame based on the selected date range and regions.
filtered_df = df[
    (df['Date'] >= start_date) &
    (df['Date'] <= end_date) &
    (df['Region'].isin(selected_regions))
]

# --- Display Key Metrics ---
st.subheader("Key Metrics")

# Create columns for metric display to arrange them side-by-side.
col1, col2, col3 = st.columns(3)

with col1:
    total_sales = filtered_df['Sales'].sum()
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

with col2:
    avg_daily_sales = filtered_df.groupby('Date')['Sales'].sum().mean()
    st.metric(label="Average Daily Sales", value=f"${avg_daily_sales:,.2f}")

with col3:
    num_transactions = len(filtered_df)
    st.metric(label="Number of Transactions", value=f"{num_transactions:,}")

# --- Data Table Display ---
st.subheader("Raw Data Preview")
# Display the filtered DataFrame.
st.dataframe(filtered_df)

# --- Visualizations ---
st.subheader("Sales Trend Over Time")
# Group data by date to plot the daily sales trend.
daily_sales_trend = filtered_df.groupby('Date')['Sales'].sum().reset_index()
# Plot a line chart using Streamlit's built-in chart function.
st.line_chart(daily_sales_trend, x='Date', y='Sales')

st.subheader("Sales by Region")
# Group data by region to plot sales distribution per region.
sales_by_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
# Plot a bar chart.
st.bar_chart(sales_by_region, x='Region', y='Sales')

# --- Additional Information ---
st.markdown("---")
st.write("This dashboard is a simple demonstration. Streamlit allows for much more complex visualizations and interactive elements.")
st.info("To modify this dashboard, edit the 'dashboard_app.py' file and save it. Streamlit will automatically detect changes and update the app.")
