# Costco Products and Locations Scraper

## Overview

This Python project scrapes Costco's popular products by state and finds the nearest Costco locations based on the capital cities of those states. It outputs the data to a CSV file, which includes each state, the top product available at Costco, and a Google Maps link to the nearest Costco. I chose this website out of pure interest and uniqueness. I love Costco when I'm home in the suburbs so I just thought it'd be fun.

## Data Description

The project gathers two types of data:

1. **Popular Products**: The top products available at Costco, scraped from the Food & Wine website. Each state has a unique top product that reflects regional preferences.
2. **Costco Locations**: The geographical coordinates of the capital cities of the states are used to find the nearest Costco locations via the Google Maps API. The data includes the Google Maps link to the nearest Costco store.

### Purpose of the Data

The purpose of this dataset is to provide users with insights into what products are popular in their respective states at Costco and to make it easier for them to locate the nearest Costco. This can benefit various users, including:

- **Consumers**: Individuals can quickly find the best products at Costco relevant to their region and locate the nearest store for convenience.
- **Market Researchers**: Analysts can study product popularity trends across states and regions.
- **Developers**: This dataset can serve as a basis for building applications that offer enhanced shopping experiences.

### Why This Dataset is Valuable

This dataset provides practical insights into regional shopping habits, which are often not readily available in public datasets. Companies usually keep such data private for competitive reasons. Additionally, the dynamic nature of products available at retail stores means that this data can change frequently. I also think it's just a fun dataset to provide users in case they're curious about what Costco products are popular in their state.

## Features

- Scrapes popular Costco products by state from Food & Wine website.
- Uses the Google Maps API to get the geographical coordinates of state capitals.
- Finds the nearest Costco locations using the Google Places API.
- Generates a CSV file with the state, product, and Costco location link.

## Requirements

- Python 3.x
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `csv`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. Install Libaries:

- pip install -r requirements.txt

3. Run code
