import requests
from bs4 import BeautifulSoup
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your Google Maps API key from .env file
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Debugging: Check if the API key is loaded
print(f"Google Maps API Key: {GOOGLE_MAPS_API_KEY}")

# Dictionary mapping states to their capital cities
state_capitals = {
    "Alabama": "Montgomery", "Alaska": "Juneau", "Arizona": "Phoenix", "Arkansas": "Little Rock",
    "California": "Sacramento", "Colorado": "Denver", "Connecticut": "Hartford", "Delaware": "Dover",
    "Florida": "Tallahassee", "Georgia": "Atlanta", "Hawaii": "Honolulu", "Idaho": "Boise",
    "Illinois": "Springfield", "Indiana": "Indianapolis", "Iowa": "Des Moines", "Kansas": "Topeka",
    "Kentucky": "Frankfort", "Louisiana": "Baton Rouge", "Maine": "Augusta", "Maryland": "Annapolis",
    "Massachusetts": "Boston", "Michigan": "Lansing", "Minnesota": "Saint Paul", "Mississippi": "Jackson",
    "Missouri": "Jefferson City", "Montana": "Helena", "Nebraska": "Lincoln", "Nevada": "Carson City",
    "New Hampshire": "Concord", "New Jersey": "Trenton", "New Mexico": "Santa Fe", "New York": "Albany",
    "North Carolina": "Raleigh", "North Dakota": "Bismarck", "Ohio": "Columbus", "Oklahoma": "Oklahoma City",
    "Oregon": "Salem", "Pennsylvania": "Harrisburg", "Rhode Island": "Providence", "South Carolina": "Columbia",
    "South Dakota": "Pierre", "Tennessee": "Nashville", "Texas": "Austin", "Utah": "Salt Lake City",
    "Vermont": "Montpelier", "Virginia": "Richmond", "Washington": "Olympia", "West Virginia": "Charleston",
    "Wisconsin": "Madison", "Wyoming": "Cheyenne"
}

# Function to get latitude and longitude by capital city
def get_lat_lng(city, state):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city},{state}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    print(f"Error getting lat/lng for {city}, {state}: {response.status_code}")
    return None, None

# Function to find the nearest Costco
def find_nearest_costco(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=50000&type=store&keyword=costco&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        places = response.json()
        if places['results']:
            location = places['results'][0]['geometry']['location']
            maps_link = f"https://www.google.com/maps/dir/{lat},{lng}/{location['lat']},{location['lng']}"
            return maps_link
    print(f"Error finding nearest Costco for lat={lat}, lng={lng}: {response.status_code}")
    return "No Costco found"

# Function to scrape popular Costco products
def scrape_costco_products():
    url = "https://www.foodandwine.com/what-to-buy-costco-8636545"
    response = requests.get(url)

    products = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_div = soup.find('div', class_='mntl-sc-block-universal-callout__body')

        if product_div:
            items = product_div.find_all('strong')
            for item in items:
                state = item.text.strip()
                product = item.next_sibling.strip() if item.next_sibling else 'N/A'
                if product.startswith(":"):
                    product = product[1:].strip()
                products[state] = product
        else:
            print("No product div found on the page.")  # Debugging line
    else:
        print(f"Failed to retrieve products. Status code: {response.status_code}")  # Debugging line
    return products

# Function to write data to CSV
def write_to_csv(products):
    with open('costco_products_and_locations.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['State', 'Top Product', 'Google Maps Link to Nearest Costco'])

        for state, product in products.items():
            capital = state_capitals.get(state)
            if capital:
                lat, lng = get_lat_lng(capital, state)
                if lat is not None and lng is not None:
                    costco_link = find_nearest_costco(lat, lng)
                    writer.writerow([state, product, costco_link])
                else:
                    writer.writerow([state, product, 'Invalid capital location'])
                    print(f"Invalid location for state: {state}")  # Debugging line
            else:
                writer.writerow([state, product, 'No capital found'])
                print(f"No capital found for state: {state}")  # Debugging line

# Main program to generate the CSV
products_by_state = scrape_costco_products()
if products_by_state:
    write_to_csv(products_by_state)
else:
    print("No products retrieved.")
