import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import folium_static 
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("schools_combined.csv")

my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2', 'page 3', 'page 4', 'page 5'])
if my_page == 'page 1':
    data_load_state = st.text('Loading data...')
    st.write(df.head(20))
    data_load_state.text('Loading data...done!')
    
elif my_page == 'page 2':
    option = st.sidebar. selectbox(
        'Which number do you like best?',
         df['region'].unique())
    'You selected: ', option

    grade_level = df[df["region"]==option].groupby("year_level")["enrollment"].sum()

    # store figure in fig variable
    fig = plt.figure(figsize=(8,6)) 

    plt.bar(grade_level.index, grade_level.values) 

    plt.title("Students in Public Schools", fontsize=16)
    plt.ylabel("Number of Enrollees", fontsize=12)
    plt.xlabel("Year Level", fontsize=12)
    year = ["grade 1","grade 2", "grade 3", "grade 4", "grade 5", "grade 6",
            "first year", "second year", "third year", "fourth year"]
    plt.xticks(range(len(grade_level.index)), year, rotation=45)

    # display graph
    st.pyplot(fig)
    
elif my_page == 'page 3':
    st.title("Geospatioal Analysis of Schools : Folium")
    schools = gpd.read_file('./phl_schp_deped/phl_schp_deped.shp')
    schools["x"] = schools.geometry.centroid.x
    schools["y"] = schools.geometry.centroid.y
    #st.write(schools.head(20))
    # Coordinates to show
    map_center = [14.583197, 121.051538]

    # Styling the map
    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=14)
    option_city = st.sidebar.selectbox(
        'Which city',
        schools["Division"].unique())
    'You selected: ', option_city
    city = option_city

    df_city = schools[schools["Division"]==city]

    for i in np.arange(len(df_city)):
        lat = df_city["y"].values[i]
        lon = df_city["x"].values[i]
        name = df_city["School"].values[i]
        folium.Marker([lat, lon], popup=name).add_to(mymap)
    folium_static(mymap)
    
elif my_page == 'page 4':
    st.title("Geospatioal Analysis of Schools : st.map()")
    schools = gpd.read_file('./phl_schp_deped/phl_schp_deped.shp')
    schools["lon"] = schools.geometry.centroid.x
    schools["lat"] = schools.geometry.centroid.y
    st.map(schools)
    
elif my_page == 'page 5':
    st.title("Geospatioal Analysis of Schools : Geopandas")
    # To plot easier, a new shapefile was created with the cleaned data
    merged_data = gpd.read_file("map_data_clean.shp")
   
    # Copied from Mapping exercise
    variable = 'Total_Enro'
    vmin, vmax = merged_data["Total_Enro"].min(), merged_data["Total_Enro"].max()

    fig, ax = plt.subplots(1, figsize=(15, 10))
    merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)
    st.pyplot(fig)