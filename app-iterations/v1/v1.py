import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and description
st.title("IFVI Value Factors Visualization Tool")
st.markdown("This tool is a non-official visualization tool to explore the International Foundation for Valuing Impacts Value Factors.")

# Load the data
data_path = "streamlit-data/airpollution.csv"
data = pd.read_csv(data_path)

# Convert 'Value' column to numeric, handling commas
data['Value'] = data['Value'].str.replace(',', '').astype(float)

# Sidebar for country selection
selected_country = st.sidebar.selectbox("Select a Country", data['Country'].unique())

# Note in the sidebar
st.sidebar.markdown("Currently air pollution is the only value factor in this demonstration website but more value factors will be added shortly.")

st.markdown(
    """
    [![Additional Value Factors](https://img.shields.io/badge/Additional%20Value%20Factors-GitHub-blue)](https://github.com/danielrosehill/Global-Value-Factors-Explorer)
    [![Visit IFVI](https://img.shields.io/badge/Visit-IFVI-green)](http://ifvi.org)
    """
)

# Filter data based on selected country
filtered_data = data[data['Country'] == selected_country]

# Visualization
st.subheader(f"Visualization of Value Factors for {selected_country}")
fig, ax = plt.subplots(figsize=(10, 6))
filtered_data.plot(kind='bar', x='Location', y='Value', ax=ax)
plt.xticks(rotation=45)
plt.title(f"Value Factors by Location in {selected_country}")
plt.xlabel("Location")
plt.ylabel("Value ($)")
st.pyplot(fig)

# Filters for Category, Location, and Impact
st.subheader(f"Air Pollution Value Factors for {selected_country}")

col1, col2, col3 = st.columns(3)

with col1:
    selected_category = st.selectbox("Filter by Category", ["All"] + filtered_data['Category'].unique().tolist())
with col2:
    selected_location = st.selectbox("Filter by Location", ["All"] + filtered_data['Location'].unique().tolist())
with col3:
    selected_impact = st.selectbox("Filter by Impact", ["All"] + filtered_data['Impact'].unique().tolist())

# Apply filters
filtered_data_display = filtered_data.copy()
if selected_category != "All":
    filtered_data_display = filtered_data_display[filtered_data_display['Category'] == selected_category]
if selected_location != "All":
    filtered_data_display = filtered_data_display[filtered_data_display['Location'] == selected_location]
if selected_impact != "All":
    filtered_data_display = filtered_data_display[filtered_data_display['Impact'] == selected_impact]

# Prepare data for display in the table
filtered_data_display['Value'] = filtered_data_display['Value'].apply(lambda x: f"${x:,.2f}")
filtered_data_display = filtered_data_display.rename(columns={'Value': 'Value Factor'})

# Reorder columns to have 'Value Factor' as the third column
cols = list(filtered_data_display.columns)
cols.insert(2, cols.pop(cols.index('Value Factor')))
filtered_data_display = filtered_data_display[cols]

# Display the filtered data in a table
st.dataframe(filtered_data_display)

# Markdown badge for GitHub repository
