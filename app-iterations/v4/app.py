import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

# Further filter data by category if a specific category is selected
if category != 'All':
    filtered_data = filtered_data[filtered_data['Category'] == category]

# Remove commas and convert the 'Value' column to numeric
filtered_data['Value'] = pd.to_numeric(filtered_data['Value'].str.replace(',', ''), errors='coerce')

# Display the filtered data with formatted values
st.subheader("Filtered Data")
formatted_filtered_data = filtered_data.copy()
formatted_filtered_data['Value'] = formatted_filtered_data['Value'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else '')
st.table(formatted_filtered_data[['Country', 'Impact', 'Category', 'Value']])

# Plotting the bar chart
st.subheader("Bar Chart")
fig, ax = plt.subplots()

if category == 'All':
    # Group by Category and sum the values if 'All' is selected
    category_data = filtered_data.groupby('Category')['Value'].sum().reset_index()
    ax.bar(category_data['Category'], category_data['Value'], label='Value')
    ax.set_xlabel('Category')
    # Annotate each bar with its value
    for i, v in enumerate(category_data['Value']):
        ax.text(i, v + 5, f'${v:,.0f}', ha='center', va='bottom', fontsize=9)
else:
    # Filter by Category if a specific category is selected
    category_data = filtered_data
    ax.bar(category_data['Country'], category_data['Value'], label='Value')
    ax.set_xlabel('Country')
    # Annotate each bar with its value
    for i, v in enumerate(category_data['Value']):
        ax.text(i, v + 5, f'${v:,.0f}', ha='center', va='bottom', fontsize=9)

# Common settings for both cases
ax.set_ylabel('Value ($)')
ax.set_title(f'Value by {"Category" if category == "All" else "Country"} for {impact} in {country}')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:,.0f}'))
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=50))  # Set y-axis increments to 50

st.pyplot(fig)