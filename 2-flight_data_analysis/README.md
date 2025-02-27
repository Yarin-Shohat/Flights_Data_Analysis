# Flight Data Analysis Project

## Overview
This project focuses on analyzing flight data from Israel to other countries for the year preceding and the year following October 7, 2023. The goal is to assess the impact of the terror attack on Israel on various aspects of life, including potential effects on outbound flights.

## Directory Structure
```
/flight_data_analysis/
│── Flights_Project_Analysis.ipynb
│── report.html
│── report.Rmd
```

## Files
- **Flights_Project_Analysis.ipynb**: Jupyter Notebook containing the analysis of the flight data.
- **report.html**: HTML report generated from the R Markdown file.
- **report.Rmd**: R Markdown file used to generate the HTML report.

## Data Sources
The analysis uses the following data sources:
- **CSV Files**: Contain structured flight data.
- **JSON Files**: Contain raw flight data extracted from an external API.

## Libraries Used
The following Python and R libraries were used for data analysis:
```python
# Python Libraries
import pandas as pd
import numpy as np
```

```r
# R Libraries
library(tidyverse)
```

## Analysis Steps
1. **Data Loading**: Load the flight data from CSV files.
   ```python
   data = pd.read_csv('data.csv')
   ```

2. **Data Preprocessing**: Convert date columns to datetime format.
   ```python
   data['departure_time'] = pd.to_datetime(data['departure_time'])
   data['arrival_time'] = pd.to_datetime(data['arrival_time'])
   ```

3. **Data Analysis**: Perform various analyses to assess the impact of the terror attack on flight data.

## Results
The results of the analysis are documented in the `Flights_Project_Analysis.ipynb` notebook and the `report.html` file.