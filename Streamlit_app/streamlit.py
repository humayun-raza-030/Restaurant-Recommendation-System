# -*- coding: utf-8 -*-
"""testing2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cDh_B1T9i847_RoQCTmVAF2Xg5rpK5nn
"""

import streamlit as st
import pandas as pd
from geopy.distance import geodesic
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Part 1: Fetching User's Location
def fetch_user_location():
    # Simulated coordinates for testing; replace with actual device location coordinates if available
    user_lat = 31.4645821  # Example: Lahore coordinates
    user_lon = 74.2563626
    return (user_lat, user_lon)

# Part 2: Getting Closest Town Based on User's Location
def get_closest_town(user_location, town_coordinates):
    closest_town = None
    min_distance = float('inf')

    for _, row in town_coordinates.iterrows():
        # Ensure the row has valid latitude and longitude
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            town_location = (row['Latitude'], row['Longitude'])
            distance = geodesic(user_location, town_location).kilometers
            if distance < min_distance:
                min_distance = distance
                closest_town = row['Town']

    return closest_town

# Part 3: Sentiment Analysis and Ranking Restaurants
def analyze_sentiment_and_rank(filtered_data):
    sid = SentimentIntensityAnalyzer()

    # Convert the 'text' column to string type, handling potential NaN values
    filtered_data['text'] = filtered_data['text'].astype(str)

    # Analyze sentiment of reviews
    filtered_data['SentimentScore'] = filtered_data['text'].apply(lambda x: sid.polarity_scores(x)['compound'])

    # Ranking restaurants based on weighted score (70% rating + 30% sentiment)
    filtered_data['WeightedScore'] = (
        filtered_data['AverageRating'] * 0.7 + filtered_data['SentimentScore'] * 0.3
    )

    # Remove duplicates based on restaurant name (CompleteStoreName)
    recommended_restaurants = filtered_data.drop_duplicates(subset=['CompleteStoreName'], keep='first')

    # Sort by WeightedScore and AverageRating
    recommended_restaurants = recommended_restaurants.sort_values(by=['WeightedScore', 'AverageRating'], ascending=False)

    return recommended_restaurants

# Part 4: Filtering Restaurants by Location and Food Type
def filter_restaurants(data, detected_town, food_type_input):
    # Filter data by detected town and food type
    filtered_data = data[
        (data['Location'].str.contains(detected_town, case=False)) &
        (data['FoodType'].str.contains(food_type_input, case=False))
    ]

    return filtered_data

# Part 5: Display Restaurant Details
def display_restaurant_details(filtered_data, selected_restaurant, max_reviews=20):
    # Filter data for the selected restaurant
    selected_restaurant_data = filtered_data[filtered_data['CompleteStoreName'] == selected_restaurant]

    # Check if the filtered data is empty
    if selected_restaurant_data.empty:
        st.write("No data found for the selected restaurant.")
        return

    # Get reviews from the 'text' column
    reviews = selected_restaurant_data['text'].tolist()

    # Display the restaurant details
    st.write(f"**Restaurant:** {selected_restaurant}")
    st.write(f"**Location:** {selected_restaurant_data['Location'].values[0]}")
    st.write(f"**Average Rating:** {selected_restaurant_data['AverageRating'].values[0]} / 5")
    st.write(f"**Number of Reviews:** {selected_restaurant_data['Reviewers'].values[0]}")

    # Show at least 5 reviews
    if len(reviews) < 5:
        st.write("Not enough reviews available.")
    else:
        # Display the first 5 reviews by default
        st.write("**Reviews:**")
        for i in range(min(5, len(reviews))):
            st.write(f"{i + 1}. {reviews[i]}")

        # Button to show more reviews (up to max_reviews, default 20)
        if len(reviews) > 5:
            show_more = st.button("See more reviews")
            if show_more:
                st.write("**More Reviews:**")
                for i in range(5, min(len(reviews), max_reviews)):
                    st.write(f"{i + 1}. {reviews[i]}")

# Part 6: Plotting the Top Restaurants
def plot_top_restaurants(recommended_restaurants, top_n=10):
    # Select the top N recommended restaurants
    top_restaurants = recommended_restaurants.head(top_n)

    # Plotting the bar chart for top recommended restaurants
    plt.figure(figsize=(12, 6))
    plt.barh(top_restaurants['CompleteStoreName'], top_restaurants['WeightedScore'], color='skyblue')
    plt.title(f"Top {top_n} Recommended Restaurants Based on Weighted Score")
    plt.xlabel('Weighted Score')
    plt.ylabel('Restaurant Name')
    plt.gca().invert_yaxis()  # Invert y-axis to display the highest score at the top
    plt.tight_layout()
    st.pyplot(plt)

# Part 7: Main Program Logic
def main():
    # Load data
    data = pd.read_csv("reviewsLoc.csv")  # Replace with the correct path to your reviewsLoc.csv

    # Load coordinates of towns (latitude, longitude)
    town_coordinates = pd.read_csv("town_coordinates.csv")  # Assumes town names with lat/lon

    # Drop towns with missing (NaN) latitude or longitude values
    town_coordinates = town_coordinates.dropna(subset=['Latitude', 'Longitude'])

    # Step 1: Fetch the user's location
    user_location = fetch_user_location()
    st.write(f"User's location: {user_location}")

    # Step 2: Find the closest town based on the user's location
    detected_town = get_closest_town(user_location, town_coordinates)

    if detected_town:
        st.write(f"Detected town based on location: {detected_town}")
    else:
        st.write("Unable to detect a nearby town. Please enter your town manually.")
        detected_town = st.text_input("Enter your town: ").strip()

    # Step 3: Get user input for food type
    food_type_input = st.selectbox("Select Food Type", data['FoodType'].unique()).strip()

    # Step 4: Filter the restaurants by location and food type
    filtered_data = filter_restaurants(data, detected_town, food_type_input)

    # Step 5: Analyze sentiment and rank the restaurants
    recommended_restaurants = analyze_sentiment_and_rank(filtered_data)

    # Step 6: Display the top recommended restaurants
    st.write("Top Recommended Restaurants:")
    st.dataframe(recommended_restaurants[['CompleteStoreName', 'FoodType', 'AverageRating', 'Reviewers', 'Location']].head())

    # Step 7: Plot the top recommended restaurants based on weighted score
    plot_top_restaurants(recommended_restaurants)

    # Step 8: Allow user to select a restaurant to view its details
    selected_restaurant = st.selectbox("Select a Restaurant", recommended_restaurants['CompleteStoreName'].unique())

    # Step 9: Display restaurant details and reviews (with a "See more reviews" option)
    display_restaurant_details(filtered_data, selected_restaurant)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from geopy.distance import geodesic
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import folium
from streamlit_folium import folium_static

# Part 1: Fetching User's Location
def fetch_user_location():
    # Simulated coordinates for testing; replace with actual device location coordinates if available
    user_lat = 31.4645821  # Example: Lahore coordinates
    user_lon = 74.2563626
    return (user_lat, user_lon)

# Part 2: Getting Closest Town Based on User's Location
def get_closest_town(user_location, town_coordinates):
    closest_town = None
    min_distance = float('inf')

    for _, row in town_coordinates.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            town_location = (row['Latitude'], row['Longitude'])
            distance = geodesic(user_location, town_location).kilometers
            if distance < min_distance:
                min_distance = distance
                closest_town = row['Town']

    return closest_town

# Part 3: Merging Restaurant Data with Town Coordinates
def merge_restaurant_coordinates(data, town_coordinates):
    # Merge restaurants with town coordinates based on town names
    merged_data = pd.merge(data, town_coordinates, left_on="Location", right_on="Town", how="left")
    merged_data.rename(columns={"Latitude": "TownLatitude", "Longitude": "TownLongitude"}, inplace=True)
    return merged_data

# Part 4: Filtering Restaurants by Town
def filter_restaurants_by_town(data, detected_town):
    # Filter data for the detected town
    filtered_data = data[data['Location'].str.contains(detected_town, case=False)]
    return filtered_data

# Part 5: Display Map with Restaurants
def display_restaurants_map(filtered_data, detected_town):
    st.write(f"**Map of Restaurants in {detected_town}:**")

    # Create a Folium map centered on Lahore
    lahore_center = [31.5204, 74.3587]
    map_lahore = folium.Map(location=lahore_center, zoom_start=12)

    # Add markers for each restaurant in the filtered data
    for _, row in filtered_data.iterrows():
        latitude = row['TownLatitude']
        longitude = row['TownLongitude']
        restaurant_name = row['CompleteStoreName']
        address = row['Location']

        # Add a marker if latitude and longitude are valid
        if not pd.isna(latitude) and not pd.isna(longitude):
            folium.Marker(
                location=[latitude, longitude],
                popup=f"<b>{restaurant_name}</b><br>{address}",
                tooltip=restaurant_name,
            ).add_to(map_lahore)

    # Render the map in Streamlit
    folium_static(map_lahore)

# Main Program Logic
def main():
    # Load data
    data = pd.read_csv("reviewsLoc.csv")  # Replace with the correct path to your reviewsLoc.csv
    town_coordinates = pd.read_csv("town_coordinates.csv")  # Replace with the correct path to town_coordinates.csv

    # Ensure town coordinates have latitude and longitude
    town_coordinates = town_coordinates.dropna(subset=['Latitude', 'Longitude'])

    # Step 1: Fetch the user's location
    user_location = fetch_user_location()
    st.write(f"User's location: {user_location}")

    # Step 2: Find the closest town based on the user's location
    detected_town = get_closest_town(user_location, town_coordinates)

    if detected_town:
        st.write(f"Detected town based on location: {detected_town}")
    else:
        st.error("No nearby town detected. Please enter your town manually.")
        return

    # Step 3: Merge restaurant data with town coordinates
    data_with_coordinates = merge_restaurant_coordinates(data, town_coordinates)

    # Step 4: Filter restaurants by detected town
    filtered_data = filter_restaurants_by_town(data_with_coordinates, detected_town)

    if filtered_data.empty:
        st.write("No restaurants found in the detected town.")
    else:
        # Step 5: Display restaurants on the map
        display_restaurants_map(filtered_data, detected_town)

        # Step 6: Display restaurant details in a table
        st.write(f"Restaurants in {detected_town}:")
        st.dataframe(filtered_data[['CompleteStoreName', 'Location', 'AverageRating', 'Reviewers']])

if __name__ == "__main__":
    main()