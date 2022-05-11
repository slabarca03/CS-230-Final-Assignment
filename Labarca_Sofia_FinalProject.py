"""
Class: CS230--Section 004
Name: Sofia Labarca
Description: Final Project CS 230
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

data = open

# Importing the Different Tools
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk

df = pd.read_csv("Fast Food Restaurants.csv",
                 header=0,
                 names=["ID", "Date", "Date Updated", "Address", "Categories", "City", "Country", "Keys", "latitude",
                        "longitude", "Name", "Postal Code", "Province", "Source", "Websites"])

# Creating Category, Province, and City List, Filtering and Count from Dataframe
def categories(df1 = df):
    categories_list = []
    for ind, row in df1.iterrows():
        if row['Categories'] not in categories_list:
            categories_list.append(row['Categories'])
    categories_list.sort()
    return categories_list

def provinces(df2):
    provinces_list = []
    for ind, row in df2.iterrows():
        if row['Province'] not in provinces_list:
            provinces_list.append(row['Province'])
    provinces_list.sort()
    return provinces_list

def names(df3):
    names_list = []
    for ind, row in df3.iterrows():
        if row['Name'] not in names_list:
            names_list.append(row['Name'])
    names_list.sort()
    return names_list

def cat_filtering(df4, list):
    new_df = pd.DataFrame()
    for i in list:
        new_df = new_df.append(df4[df4['Categories'] == i])
    return new_df

def pro_filtering(df5,list):
    new_df = pd.DataFrame()
    for i in list:
        new_df = new_df.append(df5[df5['Province'] == i])
    return new_df

def name_count(names_list, df6):
     return[df6.loc[df6['Name'].isin([n])].shape[0] for n in names_list]

def city(df7):
    city_list = []
    for ind, row in df7.iterrows():
        if row['City'] not in city_list:
            city_list.append(row['City'])
    city_list.sort()
    return city_list

# Creating a Map Function
def create_map(dataframe,title, color): #The different arguments in the function allowed for the two maps in the website to be different
        st.header(title)
        map_df = dataframe.filter(['Name', 'latitude', 'longitude'])
        view_state = pdk.ViewState(
            latitude=map_df["latitude"].mean(),
            longitude=map_df["longitude"].mean(),
            zoom=2,
            pitch=0.5)

        layer1 = pdk.Layer('ScatterplotLayer',
                           data=map_df,
                           get_position='[longitude,latitude]',
                           get_radius=10000,
                           get_color=color,
                           pickable=True)

        tool_tip = {"html": "Restaurant Name:<br/> <b>{Name}</b>",
                    "style": {"backgroundColor": "steelblue",
                             "color": "white"}}
        map1 = pdk.Deck(
           map_style='mapbox://style/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer1],
            tooltip=tool_tip)

        st.pydeck_chart(map1)

# Home page and dropdown menu
st.title("Restaurants in the US!")
st.subheader("Explore different fast food restaurants located in the US")
st.write("On this app, you will find information regarding the various fast food restaurants located in the US. "
         "The intention behind the website is for users to utilize it as a tool to plan their visit to the US "
         "and take advantage of what the area offers. Feel free to explore the page to find different "
         "restaurants located in the area and plan your visit!")

# Dropdown Menu
page = st.selectbox("Choose a page to explore:", ["Complete Data Set", "Map of Restaurants in the US",
                                                  "Interactive Map of Restaurants in the US",
                                                  "Restaurant Categories Bar Chart","Restaurant Frequency Pie Chart",
                                                  "Top 5 Restaurants Bar Chart", "Creator Information"])

# Page 1: Complete Data Set
if page == "Complete Data Set":
    st.title("Complete Data Set")
    st.write("Use the sidebar on the page to filter the data by different attributes."
                 "On the table, you can also sort the values in ascending to descending order by"
                 "clicking on the corner of each column name.")

    # Sidebar Menu Options
    options = st.sidebar.selectbox('Choose an option to filter the data:',
                             ['City', 'Postal Code', 'Province',
                              'Name', 'Categories'])
    df = df.sort_values(by=options, ascending=True)
    st.write(df)

# Page 2: Map
if page == "Map of Restaurants in the US":

    #All Restaurants Map
    create_map(df, "Map of Fast Food Restaurants in the US", [0,0,255])

# Page 3: Interactive Map
if page == "Interactive Map of Restaurants in the US":

    select_map = st.radio("Map Select", ['Category','City'])
    if select_map == "Category":
        category_list = st.multiselect("Restaurant Categories", categories(df), default="Fast Food")
        find = cat_filtering(df,category_list)
        st.write(find)

        create_map(find,"Map of Selected Restaurant Category or Categories", [255,0,0])
    if select_map == "City":
        state_select =st.selectbox("Enter a province:", provinces(df))
        p_df = df[df['Province'] == state_select]

        city_input = st.selectbox("Enter a city:", city(p_df))
        city_df = p_df[p_df['City'] == city_input]
        st.write(city_df)

        create_map(city_df,f"Restaurants in {city_input}", [100,0,0])

# Page 4: Bar Chart
if page == "Restaurant Categories Bar Chart":

    category_list = st.multiselect("Restaurant Categories", categories(), default=["Taco Place and Fast Food Restaurant", "Sandwich Place and Fast Food Restaurant",
                                                                                     "Sushi Restaurant and Fast Food Restaurant", "Burger Joint and Fast Food Restaurant"])

    new_df = cat_filtering(df,category_list)
    groups = new_df.groupby('Categories').count()
    group_dict = groups.Name.to_dict()

    color = st.sidebar.color_picker('Choose a color for the chart:',"#00c513")
    def bar_chart(x,y):
        fig, ax = plt.subplots()
        width = 0.4
        ax.bar(x,y,width=width, align='center', color= color, linewidth =width*2, edgecolor = 'black')
        # Plot Features
        plt.title("Restaurant Frequencies by Category")
        plt.ylabel('Number of Restaurants')
        plt.xlabel('Category')
        plt.xticks(rotation = 90)
        return plt

    st.pyplot(bar_chart(group_dict.keys(),group_dict.values()))

# Page 5: Pie Chart
if page == "Restaurant Frequency Pie Chart":

    province = st.multiselect("Province", provinces(df), default = ["CA", "FL", "GA", "MA", "AZ"])

    new_df2 = pro_filtering(df,province)
    groups = new_df2.groupby('Province').count()
    group_dict = groups.Name.to_dict()


    def pie_chart (sizes,list):
        fig, ax = plt.subplots()
        ax.pie(sizes, labels = list, autopct='%1.1f%%')
        ax.axis('equal')
        plt.title("Restaurant Frequency by State (in %)")
        return plt


    st.pyplot(pie_chart(group_dict.values(),group_dict.keys()))

# Page 6: Bar Chart
if page == "Top 5 Restaurants Bar Chart":

    select_pro = st.sidebar.selectbox("Provinces:", provinces(df))
    pro_df = df[df['Province'] == select_pro]

    x = names(pro_df)
    y = name_count(x, pro_df)

    count_dict = {}
    for key in x:
        for value in y:
            count_dict[key] = value
            y.remove(value)
            break

    count_dict_sorted = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
    amount = list(count_dict_sorted.values())
    name = list(count_dict_sorted.keys())

    color = st.sidebar.color_picker('Choose a color for the chart:', '#003399')

    def bar_chart(x,y):
        fig, ax = plt.subplots()
        width = 0.4
        ax.bar(x,y,width=width, align='center', color=color, linewidth =width*2, edgecolor = 'black')
        # Plot Features
        plt.title("Top 5 Restaurants per State")
        plt.ylabel('Number of Restaurants')
        plt.xlabel('Name')
        plt.xticks(rotation = 90)
        return plt

    barx = name[:5]
    bary = amount[:5]

    st.pyplot(bar_chart(barx, bary))

# Page 7: Creator Information
elif page == "Creator Information":
    st.image('favorite.jpg')
    title = '<p style="font-family:times-new-roman; color:Blue; font-size: 30px;">More information about the page</p>'
    st.markdown(title, unsafe_allow_html=True)
    subheader = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">CS 230 Final Project</p>'
    st.markdown(subheader, unsafe_allow_html=True)
    write = '<p style="font-family:sans-serif; color:Blue; font-size: 15px;">This page was created by Sofia Labarca as ' \
            'her final project for CS 230: Introduction to Python. The purpose of this assignment was to highlight the ' \
            'different skills that have been learned over the course of the semester and showcase them creatively. You ' \
            'will see a picture and video of Shake Shack because it is her favorite fast food restaurant in the US! ' \
            'Click on the following link to find out more about Shake Shack: <br> ' \
            '<a href="https://shakeshack.com/home?msclkid=734c48aed08f11ecbf32100ad0ec3276#/">Check it out here!</a></p>'
    st.markdown(write, unsafe_allow_html=True)
    st.video('https://www.youtube.com/watch?v=hiMbyDWTEJg')






