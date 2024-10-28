import streamlit as st
import plotly.express as px
import pandas as pd
import json
import dtmapi

# Get IDP Admin 2 Data for Lebanon
idp_admin2_data = dtmapi.get_idp_admin2_data(Operation="Displacement due to conflict", FromReportingDate='2023-10-08', ToReportingDate='2024-10-28', CountryName='Lebanon', to_pandas=True)

# Load your GeoJSON data
with open('geoBoundaries-LBN-ADM2.geojson') as f:
    geojson_data = json.load(f)


reversed_mapping = {
    'Bent Jbeil': 'Bent Jbail',
    'Sour': 'Sour',
    'Marjaayoun': 'Marjaayoun',
    'Hasbaya': 'Hasbaya',
    'El Nabatieh': 'Nabatiye',
    'Jezzine': 'Jezzine',
    'Saida': 'Saida',
    'Rachaya': 'Rachaya',
    'West Bekaa': 'West Bekaa',
    'Zahle': 'Zahle',
    'Chouf': 'Chouf',
    'Aley': 'Aley',
    'Baabda': 'Baabda',
    'Beirut': 'Beirut',
    'El Meten': 'El Metn',
    'Kesrwane': 'Kesrouan',
    'Jbeil': 'Jbail',
    'El Batroun': 'Batroun',
    'El Koura': 'Koura',
    'Tripoli': 'Tripoli',
    'Bcharre': 'Bcharre',
    'Zgharta': 'Zgharta',
    'El Minieh-Dennie': 'Minieh-Dinnieh',
    'Akkar': 'Akkar',
    'El Hermel': 'Hermel',
    'Baalbek': 'Baalbek'
}
idp_admin2_data['admin2Name'] = idp_admin2_data['admin2Name'].apply(lambda x: reversed_mapping[x])
# Plot the updated map with mapped names
fig = px.choropleth_mapbox(
    idp_admin2_data,
    geojson=geojson_data,  # GeoJSON data with updated names
    locations='admin2Name',  # Match the DataFrame 'admin1Name' with GeoJSON 'shapeName'
    featureidkey="properties.shapeName",  # GeoJSON property that now contains the English region names
    color='numPresentIdpInd',  # Use the count of IDPs to color the map
    mapbox_style="carto-positron",
    zoom=6,  # Adjust zoom level as needed
    center={"lat": 33.8547, "lon": 35.8623},  # Lebanon's coordinates
    opacity=0.5,
    range_color=[idp_admin2_data['numPresentIdpInd'].min(),idp_admin2_data['numPresentIdpInd'].max()],
    color_continuous_scale="Viridis",  # Color scale for visualizing the counts
    animation_frame='reportingDate',  # This adds the timeframe slider based on 'year'

)

# Set layout options for animation
fig.update_layout(
    title="IDP Count Over Time by Region"
)

# Display the Plotly figure in Streamlit
st.title('Interactive IDP Map with Time Slider')
st.plotly_chart(fig)