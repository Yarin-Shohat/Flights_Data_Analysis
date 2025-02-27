# Flight Data Preprocessing Project

## Overview
This project focuses on **preprocessing flight data** collected from multiple sources, including **CSV datasets** and **JSON files** obtained from an external API. The cleaned and processed data will be used for further analysis.

## Directory Structure
```
/flight_data_preprocessing/
│── data/
│   │── airports.csv
│   │── CityCountryContinent.csv
│   │── data_onlyFromAPI.csv
│   │── world-airports.csv
│   │── data.csv
│
│── json_data/
│   │── last_year_flights_1.json
│   │── last_year_flights_2.json
│   │── last_year_flights_Final.json
│   │── two_years_ago_flights_1.json
│   │── two_years_ago_flights_2.json
│   │── two_years_ago_flights_Final.json
│
│── Flights_Project_Preprocess.ipynb
│── README.md
```

## Data Sources
- **CSV Files:**
  - Contain airport locations, world airport lists, and continent mappings.
  - Provide structured data for joining flight records.
- **JSON Files:**
  - Contain raw flight data extracted from an **API**.
  - Data includes past flight records, destinations, and timestamps.

## Libraries Used
The following Python libraries were used for data preprocessing:
```python
import pandas as pd
import numpy as np
import json
import requests
import os
from datetime import datetime
```

## API Data Retrieval
The flight data was retrieved using the **OpenSky Network API** for past departures from Ben Gurion Airport (LLBG). The request process follows these steps:

1. **Define API Request Function:**
   ```python
   import requests
   import time
   
   url = "https://opensky-network.org/api/flights/departure"
   airport = "LLBG"
   
   def get_flights(begin, end) -> list:
       """
       Get flights from Israel in the specific range.
       
       Args:
           begin: the start date in timestamp format.
           end: the end date in timestamp format.
       
       Returns:
           List of flights including callsign, departure airport, arrival airport, and timestamps.
       """
       time.sleep(1)  # Prevent hitting API rate limits
       params = {"airport": airport, "begin": int(begin), "end": int(end)}
       response = requests.get(url, params=params)
       data = []
       
       if response.status_code == 200:
           flights = response.json()
           for flight in flights:
               data.append({
                   "callsign": flight['callsign'],
                   "departure_airport": flight['estDepartureAirport'],
                   "arrival_airport": flight['estArrivalAirport'],
                   "departure_time": datetime.datetime.fromtimestamp(flight['firstSeen']).strftime('%Y-%m-%d %H:%M:%S'),
                   "arrival_time": datetime.datetime.fromtimestamp(flight['lastSeen']).strftime('%Y-%m-%d %H:%M:%S')
               })
       else:
           print(f"Error fetching data: {response.status_code}, {response.text}")
           return []
       
       return data
   ```

2. **Handle API Rate Limits:**
   - Requests were made iteratively until encountering `Error fetching data: 429, Too many requests`.
   - Data was saved in JSON files after each request to prevent data loss.
   ```python
   import json
   with open('json_data/last_year_flights_1.json', 'w') as f:
       json.dump(last_year_flights, f)
   ```

3. **Merge JSON Files:**
   - Individual JSON files were merged yearly and then across years.
   ```python
   import json
   
   with open('json_data/last_year_flights_Final.json', 'r') as f:
       last_year_flights = json.load(f)
   with open('json_data/two_years_ago_flights_Final.json', 'r') as f:
       two_years_ago_flights = json.load(f)
   
   print(len(last_year_flights), last_year_flights)
   print(len(two_years_ago_flights), two_years_ago_flights)
   ```

## Data Preprocessing Steps
1. **Feature Engineering:**
   - Create new time-based features for departure time.
   ```python
   data['departure_time'] = pd.to_datetime(data['departure_time'])
   data['departure_time_month'] = data['departure_time'].dt.month
   data['departure_time_day'] = data['departure_time'].dt.day
   data['departure_time_hour'] = data['departure_time'].dt.hour
   data['departure_time_minute'] = data['departure_time'].dt.minute
   data['departure_time_day_name'] = data['departure_time'].dt.day_name()
   data['departure_time_day_of_week'] = data['departure_time'].dt.dayofweek
   ```

2. **Create Arrival Country Column:**
   - Extract country data using `world-airports.csv` from OurAirports dataset.
   ```python
   airports = pd.read_csv('data/world-airports.csv')
   ```

3. **Handle Missing Country Values:**
   - Identify rows with missing `country_name`.
   - Use `airportsdata` library to fill missing values.
   ```python
   import airportsdata
   airports_info = airportsdata.load('IATA')
   ```

4. **Manually Fill Missing Municipality Data:**
   - Identify missing municipality values.
   - Fill manually from `https://metar-taf.com`.

5. **Fix Missing Continent Values:**
   - Use `CityCountryContinent.csv` dataset.
   ```python
   continent_data = pd.read_csv('data/CityCountryContinent.csv')
   ```

6. **Manually Fill Continent Missing Values:**
   ```python
   continent_mapping = {
       "Belgrad": "Europe",
       "Frankfurt am Main": "Europe",
       # Add more mappings as needed
   }
   data.loc[data['continent'].isna(), 'continent'] = data['municipality'].map(continent_mapping)
   ```

7. **Save the Final Processed Data:**
   ```python
   df_combined.to_csv("data.csv", index=False)
   ```