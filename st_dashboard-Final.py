

import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
import seaborn as sns

##### Initial settings for the dashboard#############

st.set_page_config(page_title = 'New York Citi Bike', layout='wide')
st.title("Citi Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page",
   "Weather component and bike usage",
   "Most popular stations",
   "Ride Duration Distribution",  # ← Add this line
   "Interactive map with aggregated bike trips",
   "Recommendations"])


###### Import data ########

df_1 = pd.read_csv('df_rides_trimmed.csv', index_col=0)
df_daily = pd.read_csv('df_dashboard_ready.csv', index_col=0)
top20 = pd.read_csv('top20.csv', index_col=0)

###### DEFINE THE PAGES ###########################

### Intro Page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems CitiBikes currently faces.")
    st.markdown("Right now, CitiBikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Ride Duration Distribution")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("bikes.jpg")  # source: https://unsplash.com/s/photos/citibikes
    st.image(myImage)


##### Create the dual axis line chart page### 

elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(
            x=df_daily.index,
            y=df_daily['bike_rides_daily'],
            name='Daily bike rides',
            line=dict(color='blue')
        ),
        secondary_y=False
    )

    fig_2.add_trace(
        go.Scatter(
            x=df_daily.index,
            y=df_daily['avgTemp'],
            name='Daily temperature',
            line=dict(color='red')
        ),
        secondary_y=True
    )

    fig_2.update_layout(
        title='Daily Bike Trips and Temperatures in 2022',
        height=600
    )

    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("""
    - **Seasonal Correlation**: Bike usage rises with warmer temperatures, peaking in late spring and summer. Colder months show a steep decline, indicating that weather is a key driver of demand.
    - **Operational Planning**: The shortage problem is likely concentrated in warmer months (May–October). Citi Bike should prioritize fleet expansion, rebalancing, and staffing during this period.
    """)


### Most Popular stations page
        
elif page == 'Most popular stations':

    # Total rides metric
    total_rides = float(top20['value'].sum())
    st.metric(label='Total Bike Rides', value=numerize(total_rides))

    # Plot bar chart
    fig = go.Figure(
        go.Bar(
            x=top20['start_station_name'],
            y=top20['value'],
            marker={'color': top20['value'], 'colorscale': 'Blues'}
        )
    )

    fig.update_layout(
        title='Top 20 Most Popular Bike Stations in New York',
        xaxis_title='Start Stations',
        yaxis_title='Sum of Trips',
        width=900,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    - **New High-Demand Leaders**: Stations like *W 21 St & 6 Ave*, *West St & Chambers St*, and *Broadway & W 58 St* now top the list, suggesting strong commuter traffic near Midtown and Lower Manhattan.
    - **Commuter Corridors**: The dominance of Broadway and 6th Ave stations points to heavy weekday usage, likely tied to office hours and transit connections.
    - **Redistribution Priorities**: These stations may face frequent bike shortages during morning and evening peaks. Citi Bike should prioritize rebalancing efforts here.
    """)

elif page == 'Ride Duration Distribution':

   #### FacetGrid Plot###
    st.title("Distribution of Ride Duration by User Type")
    # Create the FaceGrid Plot
    sns.set(style="whitegrid")
    g = sns.FacetGrid(df_1, col='member_casual', height=5, aspect=1.2)
    g.map(sns.histplot, 'ride_length', bins=30, color='steelblue')
    g.set_axis_labels("Ride Duration (minutes)", "Frequency")
    g.set_titles("{col_name} Users")
    g.fig.suptitle("Distribution of Ride Duration by User Type", fontsize=16)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)

    # Display in Streamlit
    st.pyplot(g.fig)

    st.markdown("""
### Behavioral Insight: Ride Duration Patterns by User Type

The histogram reveals that **member users dominate in frequency**, indicating they account for the majority of daily rides. Interestingly, **both casual and member users share a common peak ride duration between 10–15 minutes**, suggesting this is the most typical trip length across the board.

This pattern highlights the consistency of urban travel behavior, regardless of user type. While members tend to ride more frequently and predictably—likely for commuting—casual users show a wider spread in ride duration, hinting at more exploratory or leisure-oriented trips.

These insights can help Citi Bike optimize:
- **Station placement** for high-frequency commuter corridors
- **Pricing strategies** tailored to short vs. long-duration riders
- **Bike redistribution** to match peak usage patterns across user types
"""
)
    
elif page == 'Interactive map with aggregated bike trips': 

    # Create the map
    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "citibike map.html"

    # Read file and keep in variable
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    # Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data, height=1000)

    st.markdown("#### Using the filter on the left-hand side of the map, we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("W 21 St & 6 Ave, West St & Chambers St, Broadway & W 60 St, 6 Ave & W 33 St, Broadway & E 14 St.")
    st.markdown("""
    These stations are clustered around Midtown and Lower Manhattan, which suggests:
    - High commuter traffic near business districts and transit hubs.
    - Consistent demand throughout the week, especially during peak hours.
    - Operational pressure points where bike shortages or docking congestion may occur.
    """)


elif page == "Recommendations":

    st.header("Conclusions and recommendations")
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- Expand station capacity or add new stations near high-demand areas such as W 21 St & 6 Ave, West St & Chambers St, Broadway & W 60 St, 6 Ave & W 33 St, and Broadway & E 14 St. These locations consistently show the highest trip volumes.")
    st.markdown("- Prioritize bike availability during warmer months (May–October), when ridership peaks. Ensure these top stations are fully stocked to meet commuter and tourist demand.")
    st.markdown("- Reduce bike supply during colder months (November–March) to optimize logistics and minimize operational costs, while maintaining coverage for essential commuter routes.")
    st.markdown("- Consider predictive rebalancing strategies using weather forecasts and historical usage patterns to proactively manage inventory across stations.")






