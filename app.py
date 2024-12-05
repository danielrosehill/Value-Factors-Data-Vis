import streamlit as st
import pandas as pd
import plotly.express as px

# Define file paths and human-readable names
file_paths = {
    "streamlit-data/airpollution.csv": "Air Pollution",
    "streamlit-data/landconversion.csv": "Land Conversion",
    "streamlit-data/landuse.csv": "Land Use",
    "streamlit-data/waste.csv": "Waste",
    "streamlit-data/waterconsumption.csv": "Water Consumption",
    "streamlit-data/waterpollution.csv": "Water Pollution"
}

# Sidebar for file selection
st.sidebar.title("Select Data")

# Choose a dataset option
selected_file = st.sidebar.selectbox("Choose a dataset", list(file_paths.values()))

# Add markdown badges
st.sidebar.markdown("[![View repo on GitHub](https://img.shields.io/badge/View%20repo-GitHub-blue?style=flat-square)](https://github.com/danielrosehill/Value-Factors-Data-Vis)")
st.sidebar.markdown("[![IFVI Website](https://img.shields.io/badge/IFVI-Website-blue?style=flat-square)](https://ifvi.org)")

# Expandable items
with st.sidebar.expander("About this data"):
    st.write("This app is a non-official visualization of the value factors released by the International Foundation for Valuing Impact in 2024.")

with st.sidebar.expander("Created by"):
    st.markdown("[Daniel Rosehill](https://danielrosehill.com)")

# Map the human-readable name back to the file path
selected_file_path = [key for key, value in file_paths.items() if value == selected_file][0]

# Load the selected CSV file
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data(selected_file_path)

# Main content
st.title(f"Data Visualization: {selected_file}")

# Selection tools
country = st.selectbox("Select Country", data['Country'].unique())
impact = st.selectbox("Select Impact", data['Impact'].unique())
category = st.selectbox("Select Category", ['All'] + list(data['Category'].unique()))

# Filter data based on selection
filtered_data = data[(data['Country'] == country) & (data['Impact'] == impact)]

# Further filter data by category if a specific category is selected
if category != 'All':
    filtered_data = filtered_data[filtered_data['Category'] == category]

# Ensure the 'Value' column is treated as a string before using the .str accessor
filtered_data['Value'] = filtered_data['Value'].astype(str)

# Remove commas and convert the 'Value' column to numeric
filtered_data['Value'] = pd.to_numeric(filtered_data['Value'].str.replace(',', ''), errors='coerce')

# Display the filtered data with formatted values
st.subheader("Filtered Data")
formatted_filtered_data = filtered_data.copy()
formatted_filtered_data['Value'] = formatted_filtered_data['Value'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else '')
st.table(formatted_filtered_data[['Country', 'Impact', 'Category', 'Value']])

# Plotting the bar chart using Plotly
st.subheader("Bar Chart")
if category == 'All':
    # Group by Category and sum the values if 'All' is selected
    category_data = filtered_data.groupby('Category')['Value'].sum().reset_index()
    fig = px.bar(category_data, x='Category', y='Value', title=f'Total Value by Category for {impact} in {country}')
    fig.update_yaxes(title='Value ($)', tickformat='$,.0f')
    fig.update_xaxes(title='Category')
else:
    # Filter by Category if a specific category is selected
    category_data = filtered_data
    fig = px.bar(category_data, x='Country', y='Value', title=f'Value by Country for {category} and {impact}')
    fig.update_yaxes(title='Value ($)', tickformat='$,.0f')
    fig.update_xaxes(title='Country')

# Display the Plotly figure
st.plotly_chart(fig)