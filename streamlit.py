import streamlit as st
import mysql.connector as sconn
from mysql.connector import Error
import pandas as pd
import time
import numpy as np

st.set_page_config(page_title="Redbus", page_icon=":oncoming_bus:", layout="wide")

def timedelta_to_hhmm(value):
    #this function will convert the timedelta format into HH:MM
    t_seconds = value.seconds
    hours = t_seconds//3600  # 1hour = 3600 seconds
    minutes = (t_seconds%3600)//60 #1hour = 60minutes and 3600seconds
    return f"{hours:02}:{minutes:02}" #formatiing to display the time in 00:00 format

def configuration():
    try:
        config = {
            "user": "root",
            "password": "Guvi8754241299",
            "host": "localhost",
            "database": "project_redbus"
        }
        return config
    except Error as e:
        st.error(f"Error occurred during configuration: {e}")
        return None


def connection():
    try:
        config = configuration()
        if config is None:
            return None
        conn = sconn.connect(**config)
        if conn.is_connected():
            return conn
        else:
            st.error("Failed to connect to the database.")
            return None
    except Error as e:
        st.error(f"Error occurred when opening connection: {e}")
        return None

def fetch_distinct_value(conn, query):
    c = conn.cursor()
    try:
        c.execute(query)
        return [item[0] for item in c.fetchall()]
    except Error as e:
        st.error(f"Error occurred when fetching distinct values: {e}")
        return []

def fetch_filtered_value(conn, query):
    c = conn.cursor()
    try:
        c.execute(query)
        columns = [col[0] for col in c.description]
        data = c.fetchall()
        df = pd.DataFrame(data, columns=columns)
        if "Departure_Time" in df.columns:
            df["Departure_Time"] = df["Departure_Time"].apply(timedelta_to_hhmm)
        if "Reaching_Time" in df.columns:
            df["Reaching_Time"] = df["Reaching_Time"].apply(timedelta_to_hhmm)
        if "star_rating" in df.columns:
            df['star_rating'] = df['star_rating'].replace(0.0, np.nan)
        return df
    except Error as e:
        st.error(f"Error occurred when fetching filtered value: {e}")
        return pd.DataFrame()

conn = connection()

# Load custom CSS from file
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Title and welcome message
st.title("REDBUS - Bus Ticket Booking 🚍")
st.markdown("**Welcome to Redbus! 👉 Find and book bus tickets easily. Use the filters below to search for buses 🔍.**")

# Sidebar with image and filter options
bus_image_url = "https://media.istockphoto.com/id/1312644983/vector/modern-city-passenger-bus-against-the-background-of-an-abstract-cityscape-vector-illustration.jpg?s=612x612&w=0&k=20&c=QNTyvmklpvs4cT-JzD-DjmdK_EsN8Wh6I5sLZ9UoB_E="
st.sidebar.image(bus_image_url, use_container_width=True)




st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #FFFFFF;
        margin-right: 20px;
        border-right: 2px solid #FFFFFF
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.header("Filter Options 🔽")
bus_type_query = """
    SELECT DISTINCT 
        CASE 
            WHEN Bus_Type LIKE '%Seater%' AND Bus_Type NOT LIKE '%Sleeper%'  THEN 'AC Seater' 
            WHEN Bus_Type LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Seater%' THEN 'Sleeper' 
            WHEN Bus_Type LIKE '%NON AC%' OR '%Sleeper%' AND Bus_Type NOT LIKE '%AC%' THEN 'NON AC' 
            WHEN Bus_Type LIKE '%AC%' OR Bus_Type LIKE '%A/C%' AND Bus_Type NOT LIKE '%Non AC%' THEN 'AC' 
            ELSE 'Others' 
        END AS Bus_Category,
        COUNT(*) AS Bus_Count
    FROM BusDetails 
    GROUP BY Bus_Category 
    ORDER BY Bus_Count DESC;
"""
st.sidebar.markdown("#### BUS TYPE")
bus_type_seater = st.sidebar.checkbox("Seater", key="bus_type_seater")
bus_type_sleeper = st.sidebar.checkbox("Sleeper", key="bus_type_sleeper")
bus_type_ac = st.sidebar.checkbox("AC", key="bus_type_ac")
bus_type_nonac = st.sidebar.checkbox("Non AC", key="bus_type_nonac")


filtered_df = pd.DataFrame()  # Initialize filtered_df



st.sidebar.markdown("#### PRICE RANGE")
min_price = 0  # Adjusted minimum price
max_price = 5000  # Adjusted maximum price
price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price), 100)

st.sidebar.markdown("#### RATING RANGE")
rating_3_plus = st.sidebar.checkbox("3+ Stars", key="rating_3_plus")
rating_4_plus = st.sidebar.checkbox("4+ Stars", key="rating_4_plus")
rating_5 = st.sidebar.checkbox("5 Stars", key="rating_5")

st.sidebar.markdown("#### DEPARTURE RANGE")
dt_before_6am = st.sidebar.checkbox("Before 6 am", key="dt_before_6am")
dt_6am_to_12pm = st.sidebar.checkbox("6 am to 12 pm", key="dt_6am_to_12pm")
dt_12pm_to_6pm = st.sidebar.checkbox("12 pm to 6 pm", key="dt_12pm_to_6pm")
dt_after_6pm = st.sidebar.checkbox("After 6 pm", key="dt_after_6pm")


# Main Page Layout
col1, col2 = st.columns(2)

bus_services = {
    'APSRTC': 'Andhra Pradesh State Road Transport Corporation (APSRTC)',
    'KSRTC (Kerala)': 'Kerala State Road Transport Corporation (KSRTC)',
    'PEPSU (Punjab)': 'Patiala and East Punjab States Union (PEPSU)',
    'RSRTC': 'Rajasthan State Road Transport Corporation (RSRTC)',
    'HRTC': 'Himachal Road Transport Corporation (HRTC)',
    'Kadamba Transport Corporation Limited (KTCL)': 'Kadamba Transport Corporation Limited (KTCL)',
    'MTC': 'Meghalaya Transport Corporation (MTC)',
    'ASTC': 'Assam State Transport Corporation (ASTC)',
    'KAAC Transport': 'Karbi Anglong Autonomous Council Transport (KAAC Transport)',
    'CTU': 'Chandigarh Transport Undertaking (CTU)'
}

with col1:
    state_query = "SELECT DISTINCT State_TransportationName FROM BusRoutesAndLinks;"
    states = fetch_distinct_value(conn, state_query)
    
    # Create a dictionary to map abbreviations to display names
    display_names = {k: f"{v}" for k, v in bus_services.items() if k in states}
    
    # Create a list of display names for the selectbox
    display_name_list = ['--- select state ---'] + [display_names.get(state, state) for state in states]
    
    # Create the selectbox with display names
    selected_display_name = st.selectbox("**States Transportation Name**", display_name_list)
    
    # Find the abbreviation corresponding to the selected display name
    selected_state = next((k for k, v in display_names.items() if v == selected_display_name), selected_display_name)

    st.write(f"Selected State: {selected_state}")

with col2:
    if selected_state != '--- select state ---':
        route_query = f"SELECT Bus_Routes FROM BusRoutesAndLinks WHERE State_TransportationName = '{selected_state}';"
        routes = fetch_distinct_value(conn, route_query)
        route = st.selectbox("**Routes**", ['--- select route ---'] + routes)
    else:
        route = st.selectbox("**Routes**", ['--- select route ---'])

# Construct rating condition
rating_conditions = []
if rating_3_plus:
    rating_conditions.append("b.Bus_rating >= 3")
if rating_4_plus:
    rating_conditions.append("b.Bus_rating >= 4")
if rating_5:
    rating_conditions.append("b.Bus_rating = 5")
rating_condition = " OR ".join(rating_conditions) if rating_conditions else "1=1"

# Construct departure condition
departure_conditions = []
if dt_before_6am:
    departure_conditions.append("HOUR(b.Departure_Time) < 6")
if dt_6am_to_12pm:
    departure_conditions.append("HOUR(b.Departure_Time) BETWEEN 6 AND 12")
if dt_12pm_to_6pm:
    departure_conditions.append("HOUR(b.Departure_Time) BETWEEN 12 AND 18")
if dt_after_6pm:
    departure_conditions.append("HOUR(b.Departure_Time) > 18")
departure_condition = " OR ".join(departure_conditions) if departure_conditions else "1=1"

# Search Button
if st.button("**Search**"):
    if selected_state != '--- select state ---' and route != '--- select route ---':
        bus_type_conditions = []
        if bus_type_seater:
            bus_type_conditions.append("Bus_Type LIKE '%Seater%' AND Bus_Type NOT LIKE '%Sleeper%'")
        if bus_type_sleeper:
            bus_type_conditions.append("Bus_Type LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Seater%'")
        if bus_type_ac:
            bus_type_conditions.append("(Bus_Type LIKE '%AC%' OR Bus_Type LIKE '%A/C%') AND Bus_Type NOT LIKE '%Non AC%'")
        if bus_type_nonac:
            bus_type_conditions.append("Bus_Type LIKE '%NON AC%'")
        bus_type_condition = " OR ".join(bus_type_conditions) if bus_type_conditions else "1=1"
    
        
        query = f"""
            SELECT r.Bus_Routes, r.Routes_Links, b.Bus_Name, b.Bus_Type, 
                   b.Departure_Time, b.Travelling_Time, b.Reaching_Time, 
                   b.Bus_rating, b.Ticket_Price, b.Seat_Availability
            FROM BusRoutesAndLinks r
            JOIN BusDetails b ON r.Route_NO = b.Bus_No
            WHERE r.State_TransportationName = '{selected_state}' 
            AND r.Bus_Routes = '{route}'
            AND ({bus_type_condition})
            AND ({rating_condition})
            AND b.Ticket_Price BETWEEN {price_range[0]} AND {price_range[1]}
            AND ({departure_condition});
        """
        with st.spinner('Loading...'):
            time.sleep(2)
            result_df = fetch_filtered_value(conn, query)
        if not result_df.empty:
            st.dataframe(result_df)
        else:
            st.write("No buses available for the selected criteria.")
    else:
        st.write("Please select a state and route to search for buses.")

