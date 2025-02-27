import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def get_data():
    """
    This function will only be re-run when the data is changed.
    Read
    """
    data = pd.read_csv("/workspaces/Flights_Data_Analysis/data/data.csv")
    # Drop the 'departure_time_day_of_week' column
    data = data.drop(columns=['departure_time_day_of_week'])
    data['departure_time'] = pd.to_datetime(data['departure_time'])
    return data

@st.cache_data
def get_columns_desc():
    """
    Read the Terror Attacks data from the CSV file.
    """
    df = pd.read_csv("/workspaces/Flights_Data_Analysis/data/column_desc.csv", encoding='ISO-8859-1')
    return df


st.title("✈️ Flight Data Analysis")
st.write(
    """
    This is my project about flights from Israel to the world. The flights is from October 2022 to October 2024.\n
    On October 7, 2023, a terror attack in Israel led to the cancellation of all flights, significantly impacting air travel in the region. This project will explore these effects.\n
    The data, sourced from https://opensky-network.org/ via API requests, has been pre-processed by me, with all relevant code available in the repository.\n
    Both the data and the code can be found in the repository.
    """
)

st.write("For the preprocessing step, you can click [here](https://github.com/Yarin-Shohat/Flights_Data_Analysis/tree/main/1-flight_data_preprocessing)")
st.write("For the first data analysis step, you can click [here](https://github.com/Yarin-Shohat/Flights_Data_Analysis/tree/main/2-flight_data_analysis)")

st.write("---")

# Data Overview
st.write("## Data Overview")
data = get_data()
columns_decs = get_columns_desc()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rows", f"{len(data):,}")
with col2:
    st.metric("Total Columns", f"{len(data.columns):,}")
with col3:
    st.metric("Missing Values", f"{data.isna().sum().sum():,}")

# Create a summary table with color coding
summary_data = []
for column in data.columns:
    col_type = data[column].dtype
    unique_count = data[column].nunique()
    missing_count = data[column].isna().sum()
    missing_percentage = (missing_count / len(data)) * 100
    
    try:
        numeric_col = pd.to_numeric(data[column], errors='coerce')
        if str(col_type) != "object":
            min_val = f"{numeric_col.min():,.2f}"
            max_val = f"{numeric_col.max():,.2f}"
            mean_val = f"{numeric_col.mean():,.2f}"
        else:
            min_val = max_val = mean_val = "N/A"
    except:
        min_val = max_val = mean_val = "N/A"
    
    summary_data.append({
        "Column": columns_decs[columns_decs.iloc[:, 0] == column].iloc[:, 2].values[0],
        "Type": str(col_type),
        "Unique Values": unique_count,
        "Missing Values (%)": f"{missing_percentage:.1f}%",
        "Min": min_val,
        "Max": max_val,
        "Mean": mean_val,
        "Description": columns_decs[columns_decs.iloc[:, 0] == column].iloc[:, 1].values[0] 
                if not columns_decs[columns_decs.iloc[:, 0] == column].empty 
                else "N/A"
    })

summary_df = pd.DataFrame(summary_data)
st.dataframe(
    summary_df.style.background_gradient(
        subset=['Unique Values'], 
        cmap='YlOrRd'
    ),
    use_container_width=True,
    height=400
)

st.write("You can see the data in the table above. The table shows the data type of each column, the number of unique values, the percentage of missing values, and the minimum, maximum, and mean values for numeric columns.")
st.write("Now we will see the distribution of the data.")

# ['departure_time_month', 'departure_time_day', 'departure_time_hour','departure_time_minute', 'departure_time_day_name', 'airportName', 'continent', 'municipality', 'country_name']
all_cols = ['departure_time_month', 'departure_time_day', 'departure_time_hour','departure_time_minute', 'departure_time_day_name', 'airportName', 'continent', 'municipality', 'country_name']
limit_cols =  ['airportName', 'municipality', 'country_name']

# Data Distribution
st.write("### Data Distribution")
st.write("The following chart shows the distribution of the data.")

st.write("You can select a column from the dropdown menu to see its distribution.")
column_names = {row[0]: row[2] for _, row in columns_decs.iterrows() if row[0] in all_cols}
selected_column = st.selectbox("Select a column", options=list(column_names.keys()), format_func=lambda x: column_names[x])

# Get display name for the selected column
display_name = columns_decs[columns_decs.iloc[:, 0] == selected_column].iloc[:, 2].values[0]

# Visualization based on data type
if pd.api.types.is_numeric_dtype(data[selected_column]):

    # For numeric data, create a histogram with separate bins
    unique_values = sorted(data[selected_column].unique())
    
    fig = px.histogram(
        data, 
        x=selected_column,
        nbins=len(unique_values),  # One bin per unique value
        title=f"Distribution of {display_name}",
        template="plotly_white",
        labels={selected_column: display_name, "Count": "Frequency"},
        color_discrete_sequence=['#1f77b4']
    )
    
    # Add gap between bars using update_traces instead
    fig.update_traces(marker_line_width=1, marker_line_color="white", opacity=0.8)
    
    # Set x-axis ticks to show all unique values
    fig.update_xaxes(
        tickmode='array',
        tickvals=unique_values,
    )
    
    # Set the gap between bars
    fig.update_layout(bargap=0.2)  # 0.2 means 20% gap between bars

    st.plotly_chart(fig, use_container_width=True)
else:
    # For categorical data, show top 15 values
    value_counts = data[selected_column].value_counts().head(15)
    fig = px.bar(
        x=value_counts.index,
        y=value_counts.values,
        title=f"Top 15 Values in {display_name}",
        labels={"x": display_name, "y": "Count"},
        template="plotly_white",
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig, use_container_width=True)


st.write("---")

# Data Analysis
st.write("## Data Analysis")
st.write("In this section, we will analyze the flights data.")

######### Flights Before and After 7/10/2023 #########
st.write("### Flights Before and After 7/10/2023")

# Sum flights before and after October 7, 2023
df_grouped = data[["before_7_10_2023", "after_7_10_2023"]].sum().reset_index()
df_grouped.columns = ["Period", "Number of Flights"]

# Change period labels to "Before Attack" and "After Attack"
df_grouped["Period"] = df_grouped["Period"].map({
    "before_7_10_2023": "Before Attack", 
    "after_7_10_2023": "After Attack"
})

# Create a bar chart using Plotly
fig = px.bar(
    df_grouped,
    x="Period",
    y="Number of Flights",
    color="Period",
    color_discrete_sequence=["#3498db", "#e74c3c"])  # Blue and red

# Update layout for better visualization
fig.update_layout(
    xaxis_title="",
    yaxis_title="Number of Flights",
    xaxis_tickangle=0
)

# Display the chart in Streamlit
fig.update_layout(width=600)  # Set a specific width in pixels
st.plotly_chart(fig, use_container_width=False)

st.write("The chart above shows the number of flights before and after the terror attack on 7/10/2023. As expected, there is a significant drop in the number of flights after the attack.")

######### Flights Per Month #########
st.write("### Flights Per Month")

# Filter out October 2024 data
filtered_data = data[data["departure_time"] < pd.Timestamp('2024-10-01')]
flights_per_month = filtered_data.groupby(filtered_data["departure_time"].dt.to_period("M")).size().reset_index(name='Number of Flights')
flights_per_month['departure_time'] = flights_per_month['departure_time'].dt.to_timestamp()

# Calculate percent change for tooltip comparison
flights_per_month['pct_change'] = flights_per_month['Number of Flights'].pct_change() * 100

# Create a line chart using Plotly Express with custom hover info
fig = px.line(
    flights_per_month,
    x='departure_time',
    y='Number of Flights',
    markers=True,
    hover_data={
        'departure_time': False,  # Hide default date format
        'Number of Flights': ':.0f',  # Format with no decimal places
        'pct_change': ':.1f'  # Format with 1 decimal place
    }
)

# Customize hover template
fig.update_traces(
    hovertemplate='<b>%{x|%b %Y}</b><br>Flights: %{y:,.0f}<br>Change: %{customdata[0]:.1f}%<extra></extra>'
)

# Update layout for better visualization
fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Flights",
    xaxis_tickangle=45,
    width=800,
    height=400
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.write("""
         The chart above shows the number of flights per month from October 2022 to September 2024. There is a clear downward trend in the number of flights, with a significant drop in October 2023 due to the terror attack.\n
         We can see that after the November 2023, the number of flights started to increase again, slowly, but increase between 1-20%.\n
         In the year after the October 2023, the number of flights increased in every month except in August, in this month occurred [August 2024 Israel–Lebanon strikes](https://en.wikipedia.org/wiki/August_2024_Israel%E2%80%93Lebanon_strikes) so this is maybe the reason for the decrease in the number of flights.
         """)


######### The difference between the flights before and after #########
st.write("### The difference between the flights before and after 7/10/2023")
st.write("Now we will see the difference between the flights before and after the terror attack on 7/10/2023.")
# Classify flights into before/after October 7
event_date = pd.to_datetime("2023-10-07").date()
data['departure_date'] = data['departure_time'].dt.date
data['period'] = data['departure_date'].apply(lambda x: 'Before' if x < event_date else 'After')

######### Hourly Departure Time Distribution #########
# Count flights per hour before and after
hourly_flights = data.groupby(['departure_time_hour', 'period']).size().unstack().fillna(0).reset_index()

# Melt the dataframe for Plotly
hourly_flights_melted = hourly_flights.melt(id_vars='departure_time_hour', value_vars=['Before', 'After'], var_name='Period', value_name='Number of Flights')

# Create a bar chart using Plotly
fig = px.bar(
    hourly_flights_melted,
    x='departure_time_hour',
    y='Number of Flights',
    color='Period',
    barmode='group',
    title="Hourly Departure Time Distribution (Before vs. After Oct 7)",
    labels={'departure_time_hour': 'Hour of Day', 'Number of Flights': 'Number of Flights'},
    color_discrete_sequence=["#3498db", "#e74c3c"]  # Blue and red
)

# Update layout for better visualization
fig.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Number of Flights",
    xaxis_tickangle=0,
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(24)),  # Show all 24 hours (0-23)
        ticktext=[str(h) for h in range(24)]  # Label each hour
    ),
    width=800,
    height=400
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.write("The chart above shows the distribution of flights by hour of the day before and after the terror attack on 7/10/2023. We can see that there isn't a change in the distribution of the flight hours before and after the attack.")

######### Daily Departure Time Distribution #########
# Count flights per hour before and after
daily_flights = data.groupby(['departure_time_day', 'period']).size().unstack().fillna(0).reset_index()

# Melt the dataframe for Plotly
daily_flights_melted = daily_flights.melt(id_vars='departure_time_day', value_vars=['Before', 'After'], var_name='Period', value_name='Number of Flights')

# Create a bar chart using Plotly
fig = px.bar(
    daily_flights_melted,
    x='departure_time_day',
    y='Number of Flights',
    color='Period',
    barmode='group',
    title="Daily Departure Time Distribution (Before vs. After Oct 7)",
    labels={'departure_time_day': 'Day in Month', 'Number of Flights': 'Number of Flights'},
    color_discrete_sequence=["#3498db", "#e74c3c"]  # Blue and red
)

# Update layout for better visualization
fig.update_layout(
    xaxis_title="Day in Month",
    yaxis_title="Number of Flights",
    xaxis_tickangle=0,
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(32)),  # Show all 31 days (1-31)
        ticktext=[str(h) for h in range(32)]  # Label each day
    ),
    width=800,
    height=400
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.write("The chart above shows the distribution of flights by Day in Month before and after the terror attack on 7/10/2023. We can see that there isn't a change in the distribution of the day of the flights before and after the attack, there is a uniform distribution.")

######### Top 15 Country Destinations Before Attack #########
st.write("### Top 15 Country Destinations Before Attack")

# Filter data for the period before the attack
before_attack_data = data[data['period'] == 'Before']

# Filter data for before and after periods
before_attack_data = data[data['period'] == 'Before']
after_attack_data = data[data['period'] == 'After']

# Count flights by country for both periods
countries_before = before_attack_data['country_name'].value_counts().reset_index()
countries_before.columns = ['country_name', 'count']
countries_before['period'] = 'Before'

countries_after = after_attack_data['country_name'].value_counts().reset_index()
countries_after.columns = ['country_name', 'count']
countries_after['period'] = 'After'

# Combine data
combined_countries = pd.concat([countries_before, countries_after])

# Get top 15 countries by total flights across both periods
top_countries = combined_countries.groupby('country_name')['count'].sum().nlargest(15).index.tolist()

# Filter to only include top countries
filtered_combined = combined_countries[combined_countries['country_name'].isin(top_countries)]

# Create a grouped bar chart
fig = px.bar(
    filtered_combined,
    x='country_name',
    y='count',
    color='period',
    title="Top 15 Country Destinations: Before vs. After Oct 7, 2023",
    labels={"country_name": "Country", "count": "Number of Flights", "period": "Period"},
    color_discrete_sequence=["#3498db", "#e74c3c"],  # Blue and red
    barmode='group'
)

# Update layout for better visualization
fig.update_layout(
    xaxis_title="Country",
    yaxis_title="Number of Flights",
    xaxis_tickangle=45,
    width=800,
    height=500
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.write("We can see that all the countries in the top 15 destinations have a decrease in the number of flights after the terror attack on 7/10/2023, but specifically, the number of flights to Turkey decreased significantly. Every other country decrease in more than 50%, Turkey decreased in 95%.")

# Map


# Most difference in country destinations


st.write("---")
st.write(data)