import mysql.connector
import pandas as pd
import streamlit as st  
connection = mysql.connector.connect()
cursor = connection.cursor()

# Create a MySQL connection
def connection():

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='secure_check'
        )
        return connection
    except mysql.connector.Error as e:
        # If using Streamlit:
        st.error(f"Database connection error: {e}")
        print(f"Database connection error: {e}")
        return None

# Fetch data from the database
def fetch_data(query):
    connection = connection()

    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Fetch rows as dicts
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            return df
        except mysql.connector.Error as e:
            print(f"Query execution error: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            connection.close()
    else:
        return pd.DataFrame()
     


dashboard_code = """
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Traffic Stop Dashboard 🚓", layout="wide")

st.title("Traffic Stop Dashboard 🚦")

df = pd.read_csv("your_data.csv")  # Replace with your actual file

st.dataframe(df)
"""

with open("dashboard.py", "w", encoding="utf-8") as f:
    f.write(dashboard_code)




st.set_page_config(page_title="Traffic Dashboard", layout="wide")

st.title("🚓 Traffic Stop Dashboard")
# Read the dataset
df = pd.read_csv("traffic_data.csv")
df.to_csv("traffic_data.csv", index=False)
#st.dataframe(df)
st.write(df)



# Example filter
if st.checkbox("Show only stops with searches conducted"):
    df = df[df['search_conducted'] == True]
    st.write(df)

st.set_page_config(
    page_title="securecheck Police Dashboard",
    layout="wide"
)
st.title("secure-check: police check Digital log")
st.markdown("real-time monitoring system insights for law enforcement")
#show full table
st.header("POLICE LOGS OVERVIEW")
query="select * from police_logs"
df = pd.read_sql(query, connection)
data=fetch_data(query)
st.dataframe(data,use_container_width=True)
#Quick metrics
st.header("Key Metrics")
col1,col2,col3,col4=st.columns(4)
print(data.columns)
with col1:
 totalstops=data.shape[0]
 st.metric("Total Police stops",totalstops)
with col2:
   if 'stop_outcome' in data.columns:
    arrests = data[data['stop_outcome'].str.contains("arrest", case=False, na=False)].shape[0]
    st.metric("Total arrests", arrests)
   else:
    st.warning("Column 'stop_outcome' not found in data.")

 #arrests=data[data['outcome'].str.contains("arrest",case=False ,na=False)].shape[0]
 #st.metric("Total arrests",arrests)
with col3:
   if 'stop_outcome' in data.columns:
    warnings = data[data['stop_outcome'].str.contains("warnings", case=False, na=False)].shape[0]
    st.metric("Total warnings", warnings)
   else:
    st.warning("'stop_outcome' column not found in police_log data.")
   #warnings=data[data['stop_outcome'].str.contains("warnings",case=False ,na=False)].shape[0]
   #st.metric("Total warnings",warnings)
with col4:
   if 'drug_related_stop' in data.columns:
    drug_related = data[data['drug_related_stop'] == 1].shape[0]
    st.metric("Drug Related Stop", drug_related)
   else:
    st.warning("'drug_related_stop' column not found.")

   #drug_related=data[data['drug_related_stop']==1].shape[0]
   #st.metric("Drug Related Stop",drug_related)
#queries
st.header("Advanced Insights")
selected_query=st.selectbox("select a query to run",[
   # --- Basic Selection & Filtering ---
   "All Records",
   "Specific Columns (Date, Time, Gender, Violation)",
   "Male Drivers Only",
   "Drivers with Warnings or Arrests",
    # --- Aggregation & Grouping ---
    "Total Number of Stops",
    "Stops by Driver Gender",
    "Stops by Violation Type (Most Frequent)",
    "Average Driver Age",
    "Min and Max Driver Age",
    # --- Date & Time Based Queries ---
    "Stops per Day",
    "Stops per Month",
    "Stops After 6 PM",
    # --- Boolean Column Queries ---
    "All Drug-Related Stops",
    "All Stops with Search Conducted",
     "Count of Drug-Related vs. Non-Drug-Related Stops",
     # --- Specific Analysis Queries (from your project list) ---
     #---vechile-Based
     "Top 10 Vehicles in Drug-Related Stops",
     "Top 10 Most Frequently Searched Vehicles",
     #---Demographic-Based---
     "Driver Age Group with Highest Arrest Rate",
     "Gender Distribution of Drivers Stopped by Country",
     "Race & Gender Combination with Highest Search Rate",
     #---Time & Duration Based---
    "Time of Day with Most Traffic Stops (Hourly)",
    "Average Stop Duration for Different Violations (Counts)",
    "Arrest Rate: Night vs. Day Stops",
    #---Violation=Based---
    "Top 10 Violations Associated with Searches or Arrests",
    "Top 10 Violations Among Younger Drivers (<25)",
    "Violations Rarely Resulting in Search or Arrest (High Volume, Low Rate)",
    #---Location-Based---
    "Top 10 Countries with Highest Rate of Drug-Related Stops",
    "Arrest Rate by Country and Violation",
    "Country with Most Stops with Search Conducted",
    #---complex---
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race (Most Common)",
    "Number of Stops by Year",
    "Number of Stops by Month",
    "Number of Stops by Hour of the Day",
    "Violations with High Search/Arrest Rates (Ranked)",
    "Driver Demographics by Country (Age, Gender, Race)",
    "Top 5 Violations with Highest Arrest Rates",
])




query_map = {
    # --- Basic Selection & Filtering ---
    "All Records": """
        SELECT *
        FROM police_logs
        LIMIT 10
    """,
    "Specific Columns (Date, Time, Gender, Violation)": """
        SELECT
            stop_date,
            stop_time,
            driver_gender,
            violation
        FROM
            police_logs
        LIMIT 1000;
    """,
    "Male Drivers Only": """
        SELECT *
        FROM police_logs
        WHERE driver_gender = 'male'
        LIMIT 1000;
    """,
    "Drivers with Warnings or Arrests": """
        SELECT *
        FROM police_logs
        WHERE stop_outcome LIKE '%Warning%' OR stop_outcome LIKE '%Arrest%'
        LIMIT 1000;
    """,

    # --- Aggregation & Grouping ---
    "Total Number of Stops": """
        SELECT COUNT(*) AS total_stops
        FROM police_logs;
    """,
    "Stops by Driver Gender": """
        SELECT driver_gender, COUNT(*) AS num_stops
        FROM police_logs
        GROUP BY driver_gender
        ORDER BY num_stops DESC;
    """,
    "Stops by Violation Type (Most Frequent)": """
        SELECT violation, COUNT(*) AS num_stops
        FROM police_logs
        GROUP BY violation
        ORDER BY num_stops DESC
        LIMIT 10;
    """,
    "Average Driver Age": """
        SELECT AVG(driver_age) AS average_driver_age
        FROM police_logs;
    """,
    "Min and Max Driver Age": """
        SELECT MIN(driver_age) AS min_age, MAX(driver_age) AS max_age
        FROM police_logs;
    """,

    # --- Date & Time Based Queries ---
    "Stops per Day": """
        SELECT stop_date, COUNT(*) AS stops_per_day
        FROM police_logs
        GROUP BY stop_date
        ORDER BY stop_date DESC
        LIMIT 30; -- Last 30 days with stops
    """,
    "Stops per Month": """
        SELECT
            DATE_FORMAT(stop_date, '%Y-%m') AS stop_month,
            COUNT(*) AS num_stops
        FROM
            police_logs
        WHERE stop_date IS NOT NULL
        GROUP BY
            stop_month
        ORDER BY
            stop_month DESC;
    """,
    "Stops After 6 PM": """
        SELECT *
        FROM police_logs
        WHERE stop_time > '18:00:00'
        LIMIT 1000;
    """,

    # --- Boolean Column Queries ---
    "All Drug-Related Stops": """
        SELECT *
        FROM police_logs
        WHERE drugs_related_stop = TRUE
        LIMIT 1000;
    """,
    "All Stops with Search Conducted": """
        SELECT *
        FROM police_logs
        WHERE search_conducted = TRUE
        LIMIT 1000;
    """,
    "Count of Drug-Related vs. Non-Drug-Related Stops": """
        SELECT
            CASE WHEN drugs_related_stop = TRUE THEN 'Drug-Related' ELSE 'Not Drug-Related' END AS stop_category,
            COUNT(*) AS num_stops
        FROM
            police_logs
        GROUP BY
            stop_category;
    """,

    # --- Specific Analysis Queries (from your list) ---
    #---Vehicle-Based---
    "Top 10 Vehicles in Drug-Related Stops": """
        SELECT
            vehicle_number,
            COUNT(*) AS drug_stop_count
        FROM
            police_logs
        WHERE
            drugs_related_stop = TRUE
            AND vehicle_number IS NOT NULL
        GROUP BY
            vehicle_number
        ORDER BY
            drug_stop_count DESC
        LIMIT 10;
    """,
    "Top 10 Most Frequently Searched Vehicles": """
        SELECT
            vehicle_number,
            COUNT(*) AS search_count
        FROM
            police_logs
        WHERE
            search_conducted = TRUE
            AND vehicle_number IS NOT NULL
        GROUP BY
            vehicle_number
        ORDER BY
            search_count DESC
        LIMIT 10;
    """,
    #---Demographic-Based---
    "Driver Age Group with Highest Arrest Rate": """
        SELECT
            CASE
                WHEN driver_age BETWEEN 18 AND 24 THEN '18-24'
                WHEN driver_age BETWEEN 25 AND 34 THEN '25-34'
                WHEN driver_age BETWEEN 35 AND 44 THEN '35-44'
                WHEN driver_age BETWEEN 45 AND 54 THEN '45-54'
                WHEN driver_age >= 55 THEN '55+'
                ELSE 'Unknown'
            END AS age_group,
            COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests,
            COUNT(*) AS total_stops,
            (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
        FROM
            police_logs
        WHERE
            driver_age IS NOT NULL
        GROUP BY
            age_group
        ORDER BY
            arrest_rate_percentage DESC
        LIMIT 5; -- Showing top 5 age groups
    """,
    "Gender Distribution of Drivers Stopped by Country": """
        SELECT
            country_name,
            driver_gender,
            COUNT(*) AS num_stops,
            (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY country_name)) AS percentage_in_country
        FROM
            police_logs
        WHERE
            country_name IS NOT NULL AND driver_gender IS NOT NULL
        GROUP BY
            country_name,
            driver_gender
        ORDER BY
            country_name, num_stops DESC;
    """,
    "Race & Gender Combination with Highest Search Rate": """
        SELECT
            driver_race,
            driver_gender,
            COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) AS total_searches,
            COUNT(*) AS total_stops,
            (COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) * 100.0 / COUNT(*)) AS search_rate_percentage
        FROM
            police_logs
        WHERE
            driver_race IS NOT NULL
            AND driver_gender IS NOT NULL
        GROUP BY
            driver_race,
            driver_gender
        ORDER BY
            search_rate_percentage DESC
        LIMIT 5; 
    """,
    #---Time & Duration Based---
    "Time of Day with Most Traffic Stops (Hourly)": """
        SELECT
            HOUR(stop_time) AS hour_of_day,
            COUNT(*) AS num_stops
        FROM
            police_logs
        WHERE
            stop_time IS NOT NULL
        GROUP BY
            hour_of_day
        ORDER BY
            num_stops DESC;
    """,
    "Average Stop Duration for Different Violations (Counts)": """
        SELECT
            violation,
            stop_duration,
            COUNT(*) AS count_of_duration_for_violation
        FROM
            police_logs
        WHERE
            violation IS NOT NULL AND stop_duration IS NOT NULL
        GROUP BY
            violation,
            stop_duration
        ORDER BY
            violation, count_of_duration_for_violation DESC;
    """,
    "Arrest Rate: Night vs. Day Stops": """
        SELECT
            CASE
                WHEN HOUR(stop_time) >= 22 OR HOUR(stop_time) < 6 THEN 'Night (10 PM - 6 AM)'
                ELSE 'Day (6 AM - 10 PM)'
            END AS time_of_day,
            COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests,
            COUNT(*) AS total_stops,
            (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
        FROM
            police_logs
        WHERE
            stop_time IS NOT NULL
        GROUP BY
            time_of_day
        ORDER BY
            arrest_rate_percentage DESC;
    """,
     #---Violation=Based---
    "Top 10 Violations Associated with Searches or Arrests": """
        SELECT
            violation,
            COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) AS searches_count,
            COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS arrests_count,
            COUNT(*) AS total_stops_for_violation,
            (COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) * 100.0 / COUNT(*)) AS search_rate_percentage,
            (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
        FROM
            police_logs
        WHERE
            violation IS NOT NULL
        GROUP BY
            violation
        ORDER BY
            search_rate_percentage DESC, arrest_rate_percentage DESC
        LIMIT 10;
    """,
    "Top 10 Violations Among Younger Drivers (<25)": """
        SELECT
            violation,
            COUNT(*) AS num_stops
        FROM
            police_logs
        WHERE
            driver_age IS NOT NULL AND driver_age < 25
        GROUP BY
            violation
        ORDER BY
            num_stops DESC
        LIMIT 10;
    """,
    "Violations Rarely Resulting in Search or Arrest (High Volume, Low Rate)": """
        SELECT
            violation,
            COUNT(*) AS total_stops,
            COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) AS total_searches,
            COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests,
            (COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) * 100.0 / COUNT(*)) AS search_rate_percentage,
            (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
        FROM
            police_logs
        WHERE
            violation IS NOT NULL
        GROUP BY
            violation
        HAVING
            total_stops > 50
        ORDER BY
            search_rate_percentage ASC, arrest_rate_percentage ASC
        LIMIT 5;
    """,
    #---Location-Based---
    "Top 10 Countries with Highest Rate of Drug-Related Stops": """
        SELECT
            country_name,
            COUNT(CASE WHEN drugs_related_stop = TRUE THEN 1 END) AS total_drug_stops,
            COUNT(*) AS total_stops,
            (COUNT(CASE WHEN drugs_related_stop = TRUE THEN 1 END) * 100.0 / COUNT(*)) AS drug_stop_rate_percentage
        FROM
            police_logs
        WHERE
            country_name IS NOT NULL
        GROUP BY
            country_name
        HAVING
            total_stops > 10
        ORDER BY
            drug_stop_rate_percentage DESC
        LIMIT 10;
    """,
    "Arrest Rate by Country and Violation": """
        SELECT
            country_name,
            violation,
            COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests,
            COUNT(*) AS total_stops,
            (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
        FROM
            police_logs
        WHERE
            country_name IS NOT NULL AND violation IS NOT NULL
        GROUP BY
            country_name,
            violation
        ORDER BY
            country_name, arrest_rate_percentage DESC;
    """,
    "Country with Most Stops with Search Conducted": """
        SELECT
            country_name,
            COUNT(*) AS search_conducted_stops_count
        FROM
            police_logs
        WHERE
            search_conducted = TRUE
            AND country_name IS NOT NULL
        GROUP BY
            country_name
        ORDER BY
            search_conducted_stops_count DESC
        LIMIT 5; -- Showing top 5 countries
    """,
    #---complex---
    "Yearly Breakdown of Stops and Arrests by Country": """
        SELECT
            stop_year,
            country_name,
            total_stops_country_year,
            total_arrests_country_year,
            (total_arrests_country_year * 100.0 / total_stops_country_year) AS arrest_rate_percentage_yearly,
            SUM(total_stops_country_year) OVER (PARTITION BY stop_year) AS total_stops_this_year_globally,
            RANK() OVER (PARTITION BY stop_year ORDER BY total_stops_country_year DESC) AS rank_by_stops_in_year
        FROM (
            SELECT
                YEAR(stop_date) AS stop_year,
                country_name,
                COUNT(*) AS total_stops_country_year,
                COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests_country_year
            FROM
                police_logs
            WHERE
                stop_date IS NOT NULL AND country_name IS NOT NULL
            GROUP BY
                stop_year,
                country_name
        ) AS yearly_country_stats
        ORDER BY
            stop_year, total_stops_country_year DESC;
    """,
    "Driver Violation Trends Based on Age and Race (Most Common)": """
        SELECT
            t1.driver_age,
            t1.driver_race,
            t1.violation,
            t1.violation_count
        FROM (
            SELECT
                driver_age,
                driver_race,
                violation,
                COUNT(*) AS violation_count,
                ROW_NUMBER() OVER (PARTITION BY driver_age, driver_race ORDER BY COUNT(*) DESC) AS rn
            FROM
                police_logs
            WHERE
                driver_age IS NOT NULL AND driver_race IS NOT NULL AND violation IS NOT NULL
            GROUP BY
                driver_age,
                driver_race,
                violation
        ) AS t1
        WHERE
            t1.rn = 1
        ORDER BY
            t1.driver_age, t1.driver_race;
    """,
    "Number of Stops by Year": """
        SELECT
            YEAR(stop_date) AS stop_year,
            COUNT(*) AS num_stops
        FROM
            police_logs
        WHERE
            stop_date IS NOT NULL
        GROUP BY
            stop_year
        ORDER BY
            stop_year;
    """,
    "Number of Stops by Month": """
        SELECT
            YEAR(stop_date) AS stop_year,
            MONTH(stop_date) AS stop_month,
            COUNT(*) AS num_stops
        FROM
            police_logs
        WHERE
            stop_date IS NOT NULL
        GROUP BY
            stop_year,
            stop_month
        ORDER BY
            stop_year, stop_month;
    """,
    "Number of Stops by Hour of the Day": """
        SELECT
            HOUR(stop_time) AS stop_hour,
            COUNT(*) AS num_stops
        FROM
            police_logs
        WHERE
            stop_time IS NOT NULL
        GROUP BY
            stop_hour
        ORDER BY
            stop_hour;
    """,
    "Violations with High Search/Arrest Rates (Ranked)": """
        SELECT
            violation,
            total_stops,
            total_searches,
            total_arrests,
            search_rate_percentage,
            arrest_rate_percentage,
            RANK() OVER (ORDER BY search_rate_percentage DESC) AS search_rate_rank,
            RANK() OVER (ORDER BY arrest_rate_percentage DESC) AS arrest_rate_rank
        FROM (
            SELECT
                violation,
                COUNT(*) AS total_stops,
                COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) AS total_searches,
                COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests,
                (COUNT(CASE WHEN search_conducted = TRUE THEN 1 END) * 100.0 / COUNT(*)) AS search_rate_percentage,
                (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
            FROM
                police_logs
            WHERE
                violation IS NOT NULL
            GROUP BY
                violation
        ) AS violation_stats
        WHERE
            total_stops > 100
        ORDER BY
            search_rate_rank, arrest_rate_rank
        LIMIT 10;
    """,
    "Driver Demographics by Country (Age, Gender, Race)": """
        SELECT
            country_name,
            CASE
                WHEN driver_age BETWEEN 18 AND 24 THEN '18-24'
                WHEN driver_age BETWEEN 25 AND 34 THEN '25-34'
                WHEN driver_age BETWEEN 35 AND 44 THEN '35-44'
                WHEN driver_age BETWEEN 45 AND 54 THEN '45-54'
                WHEN driver_age >= 55 THEN '55+'
                ELSE 'Unknown Age'
            END AS age_group,
            driver_gender,
            driver_race,
            COUNT(*) AS total_stops_in_group,
            (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY country_name)) AS percentage_of_country_stops
        FROM
            police_log
        WHERE
            country_name IS NOT NULL
            AND driver_age IS NOT NULL
            AND driver_gender IS NOT NULL
            AND driver_race IS NOT NULL
        GROUP BY
            country_name,
            age_group,
            driver_gender,
            driver_race
        ORDER BY
            country_name,
            total_stops_in_group DESC;
    """,
    "Top 5 Violations with Highest Arrest Rates": """
        SELECT
            violation,
            COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) AS total_arrests,
            COUNT(*) AS total_stops,
            (COUNT(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 END) * 100.0 / COUNT(*)) AS arrest_rate_percentage
        FROM
            police_logs
        WHERE
            violation IS NOT NULL
        GROUP BY
            violation
        HAVING
            COUNT(*) > 10
        ORDER BY
            arrest_rate_percentage DESC
        LIMIT 5;
    """
}
if st.button("Run query"):
  result=fetch_data(query_map[selected_query])
  if not result.empty:
     st.write(result)
else:
     st.warning("No results found for the selected query.")
st.markdown("-----")
st.markdown("Built with for law Enforcement by securecheck")
st.markdown("fill in the details below to get a natural language prediction of the stop outcome based on existing data. ")
st.header("Add New Police log & predict outcome and violation")
#input form
with st.form("new_log_form"):
   stop_date=st.date_input("stop_date")
   stop_time=st.time_input("stop_time")
   country_name=st.text_input("country_name") 
   driver_gender=st.selectbox(("Driver gender"),["male","female"])
   driver_age=st.number_input("Driver Age",min_value=18, max_value=70, value=30)
   driver_race=st.text_input("Driver Race")
   search_conducted=st.selectbox("was a search conducted?",["0","1"])
   search_type=st.text_input("search_type")
   drugs_related_stop=st.selectbox("was it drug related?",["0","1"])
   stop_duration = st.selectbox("stop duration", data['stop_duration'].dropna().unique())
   vehicle_number=st.text_input("Vehicle number")
   timestamp=pd.Timestamp.now()

   submitted=st.form_submit_button("predict stop outcome & violation")
   if submitted:
 #filtered data for prediction
      filter_data=[
         (data['driver_gender']== driver_gender)&
         (data['driver_age']== driver_age)&
         (data['search_conducted']== int('search_conducted'))&
         (data['stop_duration']== stop_duration)&
         (data['drug_related_stop']== int(drugs_related_stop))
      ]
      #predict stop_outcome
      if not filter_data.empty:
         predicted_outcome=filter_data['stop_outcome'].mode()[0]
         predicted_violation=filter_data['voilation'].mode()[0]
      else:
         predict_outcome="warnings"
         predict_violation="speeding"  
#Natural language summary
search_text="A search was conducted" if int(search_conducted)else "no search was conducted"
drug_text="Was drug-related" if int(drugs_related_stop)else "was not drug-related"
st.markdown(f"""
    ### **Prediction Summary**
    - **Predicted violation:** **{predicted_violation}**
    - **Predicted Stop Outcome:** **{predicted_outcome}**
    A **{driver_age}**-year-old **{driver_gender}** driver in **{country_name}** was stopped at **{stop_time.strftime('%I:%M %p')}** on *{stop_date.strftime('%Y-%m-%d')}**. {search_text.capitalize()}. The stop **{drug_text}**. The predicted outcome is **{predicted_outcome}**, and the predicted violation is **{predicted_violation}**.

    - **Stop Duration:** **{stop_duration}**
    - **Vehicle Number:** **{vehicle_number}**
""")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Traffic Dashboard", layout="wide")

st.title("🚓 Traffic Stop Dashboard")

# Load data (replace with your file)
df = pd.read_csv("your_data.csv")

st.dataframe(df)

# Example filter
if st.checkbox("Show only stops with searches conducted"):
    df = df[df['search_conducted'] == True]
    st.write(df)














   



      
   





                   
     