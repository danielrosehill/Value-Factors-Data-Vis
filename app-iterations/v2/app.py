import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
selected_file = st.sidebar.selectbox("Choose a dataset", list(file_paths.values()))

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

# Remove commas and convert the 'Value' column to numeric
filtered_data['Value'] = pd.to_numeric(filtered_data['Value'].str.replace(',', ''), errors='coerce')

# Display the filtered data with formatted values
st.subheader("Filtered Data")
filtered_data['Value'] = filtered_data['Value'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else '')
st.table(filtered_data[['Country', 'Impact', 'Category', 'Value']])

# Plotting the bar chart
st.subheader("Bar Chart")
fig, ax = plt.subplots()

if category == 'All':
    # Group by Category and sum the values if 'All' is selected
    category_data = filtered_data.groupby('Category')['Value'].sum().reset_index()
    ax.bar(category_data['Category'], category_data['Value'])
    ax.set_xlabel('Category')
    ax.set_ylabel('Value ($)')
    ax.set_title(f'Total Value by Category for {impact} in {country}')
else:
    # Filter by Category if a specific category is selected
    category_data = filtered_data[filtered_data['Category'] == category]
    ax.bar(category_data['Country'], category_data['Value'])
    ax.set_xlabel('Country')
    ax.set_ylabel('Value ($)')
    ax.set_title(f'Value by Country for {category} and {impact}')

st.pyplot(fig)