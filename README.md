# Restaurant-Recommendation-System

## 📌 Project Overview

This project is a **Restaurant Recommendation System** that helps users find restaurants in Lahore based on their location, customer reviews, and ratings. The system scrapes restaurant data from Google Maps, analyzes user reviews for sentiment, and provides a visualization dashboard using **Tableau**.

## 🚀 Features

- **Web Scraping with Selenium:** Extracts restaurant data (Location, Rating, Reviews) from Google Maps.
- **Random Store ID Assignment:** Each restaurant is assigned a unique Store ID.
- **Location-Based Filtering:** Detects user location and finds the closest town.
- **Sentiment Analysis:** Uses **NLTK's SentimentIntensityAnalyzer** to classify reviews as Positive, Neutral, or Negative.
- **Interactive Map:** Displays restaurants on a map using **Folium**.
- **Tableau Dashboard:** Provides visual insights into restaurant performance.

## 🛠️ Technologies Used

- **Python** (Pandas, Selenium, Geopy, NLTK, Folium, Streamlit)
- **Tableau** (Dashboard for restaurant analysis)
- **Jupyter Notebook** (Data processing and analysis)

## 📂 Project Structure

```
📦 Restaurant-Recommendation-System
│── 📂 data                  # Dataset and scraped data
│── 📂 notebooks             # Jupyter notebooks for data processing
│── 📂 streamlit_app         # Streamlit-based web app
│── 📜 README.md            # Project Documentation
```

## 📊 Tableau Dashboard

The **Tableau Dashboard** includes:

- **Sentiment Distribution** (Pie Chart)
- **Top Restaurants by Ratings** (Bar Chart)
- **Restaurant Locations** (Geospatial Visualization)

## 🔧 How to Run the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/humayun-raza-030/restaurant-recommendation-system.git
   cd restaurant-recommendation
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit App**
   ```bash
   streamlit run main.py
   ```

## 📌 Future Improvements

- **Expand to More Cities**
- **Use Machine Learning for Better Recommendations**
- **Improve Scraping Efficiency**

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the project.

## 📜 License

This project is licensed under the **MIT License**.

---

📌 **Author:** Humayun Raza\
📌 **GitHub Repo:** [https://github.com/humayun-raza-030/Restaurant-Recommendation-System](https://github.com/humayun-raza-030/Restaurant-Recommendation-System)\
📌 **Contact:** [humayunraza030@gmail.com](mailto\:humayunraza030@gmail.com)

