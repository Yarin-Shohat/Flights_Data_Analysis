# ✈️ Flights Data Analysis

This project analyzes flight data from Israel to various destinations around the world, covering the period from October 2022 to October 2024. The analysis focuses on the impact of the terror attack on October 7, 2023, which led to the cancellation of all flights and significantly affected air travel in the region.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://flights-data-analysis.streamlit.app/)

## Overview

The project aims to explore the changes in flight patterns before and after the attack, providing insights into how the event influenced air travel from Israel.

## Data Sources

The data used in this project is sourced from [OpenSky Network](https://opensky-network.org/) via API requests. The data has been pre-processed and is available in the repository.

## Repository Structure

```
/Flights_Data_Analysis/
│── 1-flight_data_preprocessing/
│   ├── README.md
│   ├── Flights_Project_Preprocess.ipynb
│   ├── data/
│   │   ├── airports.csv
│   │   ├── CityCountryContinent.csv
│   │   ├── data_onlyFromAPI.csv
│   │   ├── world-airports.csv
│   │   ├── data.csv
│   ├── json_data/
│   │   ├── last_year_flights_1.json
│   │   ├── last_year_flights_2.json
│   │   ├── last_year_flights_Final.json
│   │   ├── two_years_ago_flights_1.json
│   │   ├── two_years_ago_flights_2.json
│   │   ├── two_years_ago_flights_Final.json
│── 2-flight_data_analysis/
│   ├── README.md
│   ├── Flights_Project_Analysis.ipynb
│   ├── report.html
│   ├── report.Rmd
│── data/
│   ├── data.csv
│   ├── column_desc.csv
│── app_pages/
│   ├── homePage.py
│── streamlit_app.py
│── requirements.txt
│── README.md
```

## How to Run the Project

### Prerequisites

Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository:

   ```bash
   $ git clone https://github.com/Yarin-Shohat/Flights_Data_Analysis.git
   $ cd Flights_Data_Analysis
   ```

2. Install the required packages:

   ```bash
   $ pip install -r requirements.txt
   ```

### Running the App

To run the Streamlit app, use the following command:

```bash
$ streamlit run streamlit_app.py
```

## Project Structure

- **1-flight_data_preprocessing/**: Contains the preprocessing scripts and instructions.
  - **README.md**: Details the preprocessing steps and scripts used.
  - **Flights_Project_Preprocess.ipynb**: The notebook used for preprocessing the flight data.
  - **data/**: Contains the raw and processed data files.
  - **json_data/**: Contains the raw flight data in JSON format.
- **2-flight_data_analysis/**: Contains the analysis scripts and instructions.
  - **README.md**: Details the analysis steps and scripts used.
  - **Flights_Project_Analysis.ipynb**: The notebook used for analyzing the flight data.
  - **report.html**: HTML report generated from the R Markdown file.
  - **report.Rmd**: R Markdown file used to generate the HTML report.
- **data/**: Contains the flight data and column descriptions.
  - **data.csv**: The main dataset used for analysis.
  - **column_desc.csv**: Descriptions of the columns in the dataset.
- **app_pages/**: Contains the Streamlit app pages.
  - **homePage.py**: The main page of the Streamlit app.
- **streamlit_app.py**: The main Streamlit app file.
- **requirements.txt**: Lists the Python packages required to run the app.
- **README.md**: This README file.

## Analysis Steps

1. **Data Loading**: Load the flight data from CSV files.
2. **Data Preprocessing**: Convert date columns to datetime format and clean the data.
3. **Data Analysis**: Perform various analyses to assess the impact of the terror attack on flight data.
4. **Visualization**: Create visualizations to present the findings.

## Results

The results of the analysis are documented in the Streamlit app. You can explore the data and visualizations by running the app locally or accessing it [here](https://flights-data-analysis.streamlit.app/).

## Author

- **Yarin Shohat**
  - [LinkedIn](https://www.linkedin.com/in/yarinsh/)
  - [GitHub](https://github.com/Yarin-Shohat)