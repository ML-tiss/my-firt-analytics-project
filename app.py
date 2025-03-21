import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyse Carsharing", layout="wide")

# Titre de l'application
st.title("🔍 Car sharing Dashbord")

# Function to load CSV files into dataframes
@st.cache_data
def load_data():
    trips = pd.read_csv("datasets/trips.csv")  # Assurez-vous que le chemin est correct
    cars = pd.read_csv("datasets/cars.csv")
    cities = pd.read_csv("datasets/cities.csv")
    customers = pd.read_csv("datasets/customers.csv")
    ratings = pd.read_csv("datasets/ratings.csv")
    return trips, cars, cities, customers, ratings

# Charger les données
trips, cars, cities, customers, ratings = load_data()

# Convertir les dates en format datetime
trips['pickup_time'] = pd.to_datetime(trips['pickup_time'])
trips['dropoff_time'] = pd.to_datetime(trips['dropoff_time'])
trips['pickup_date'] = trips['pickup_time'].dt.date

# Merge trips with cars (joining on car_id)
trips_merged = trips.merge(cars, left_on="car_id", right_on="id", how="left")

# Merge with cities for car's city (joining on city_id)
trips_merged = trips_merged.merge(cities, left_on="city_id", right_on="city_id", how="left")

# Merge with customers (joining on customer_id)
trips_merged = trips_merged.merge(customers, left_on="customer_id", right_on="id", how="left")

# Supprimer les colonnes inutiles
trips_merged = trips_merged.drop(columns=["id_x", "id_y", "customer_id", "car_id", "city_id"], errors="ignore")

# Sidebar - Sélection de la marque de voiture
cars_brand = st.sidebar.multiselect("Select the Car Brand", trips_merged["brand"].dropna().unique())

# Filtrer le dataframe selon la sélection de la marque de voiture
if cars_brand:
    trips_merged = trips_merged[trips_merged["brand"].isin(cars_brand)]

# Compute business performance metrics
total_trips = trips_merged.shape[0]  # Nombre total de trajets
total_distance = trips_merged["distance"].sum()  # Somme de toutes les distances

# Trouver la voiture qui a généré le plus de revenus
if "revenue" in trips_merged.columns:
    top_car = trips_merged.groupby("model")["revenue"].sum().idxmax()
else:
    top_car = "Données non disponibles"

# Afficher les métriques dans Streamlit
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

# Affichage des premières lignes du dataframe
st.write("### Aperçu des données")
st.dataframe(trips_merged.head())

# Footer
st.write("🚗 Données issues d'un système de location de voitures. Projet Streamlit 🚀")

# Graphiques
st.subheader("📊 Visualisation des données")

# Trips by City
trips_by_city = trips_merged["city_name"].value_counts()
fig, ax = plt.subplots()
ax.bar(trips_by_city.index, trips_by_city.values, color='lightblue')
ax.set_title("Trips by City")
ax.set_ylabel("Number of Trips")
st.pyplot(fig)

# Revenue by Car Model
if "revenue" in trips_merged.columns:
    revenue_by_model = trips_merged.groupby("model")["revenue"].sum()
    fig, ax = plt.subplots()
    ax.bar(revenue_by_model.index, revenue_by_model.values, color='lightblue')
    ax.set_title("Revenue by Car Model")
    ax.set_ylabel("Total Revenue")
    st.pyplot(fig)

# Average Trip Duration per City
trips_merged["trip_duration"] = (trips_merged["dropoff_time"] - trips_merged["pickup_time"]).dt.total_seconds() / 60
avg_duration_by_city = trips_merged.groupby("city_name")["trip_duration"].mean()
fig, ax = plt.subplots()
ax.bar(avg_duration_by_city.index, avg_duration_by_city.values, color='lightblue')
ax.set_title("Average Trip Duration per City")
ax.set_ylabel("Duration (minutes)")
st.pyplot(fig)

# Revenue Over Time
if "revenue" in trips_merged.columns:
    revenue_over_time = trips_merged.groupby("pickup_date")["revenue"].sum()
    fig, ax = plt.subplots()
    ax.plot(revenue_over_time.index, revenue_over_time.values, color='lightblue')
    ax.set_title("💰 Revenue Over Time")
    ax.set_ylabel("Total Revenue")
    st.pyplot(fig)

# Affichage des premières lignes du dataframe
st.write("### Aperçu des données")
st.dataframe(trips_merged.head())

# Footer
st.write("🚗 Données issues d'un système de location de voitures. Projet Streamlit 🚀")