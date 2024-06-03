from docx import Document;
import openpyxl
import io;
import pandas as pd;
import re;
import numpy as np
from pymongo import MongoClient
import mysql.connector
from sqlalchemy import create_engine

##################################################TASK 1 BEGIN###########################################################################
# Read the Excel file and store it into a DataFrame
pathname = "C:\\Users\\Senthil\\Desktop\\GuviPracticeClass\\GuviCapstoneproject\\census_2011.xlsx"
data = pd.read_excel(pathname)

# Keep a copy of the original data
orgdata = data.copy()

# Function implementation for renaming the columns
def rename_function(datatorename):
    # Store the data frame with modified column names
     renameddata = datatorename.rename(columns={\
    'District code':'District_code',\
    'State name':'StateUT',\
    'District name':'District',\
    'Male_Literate':'Literate_Male',\
    'Female_Literate':'Literate_Female',\
    'Rural_Households':'Households_Rural',\
    'Urban_Households':'Households_Urban',\
    'Age_Group_0_29':'Young_and_Adult',\
    'Age_Group_30_49':'Middle_Aged',\
    'Age_Group_50':'Senior_Citizen',\
    'Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car': 'Households_with_TV_Comp_Laptop_Phone_and_Vehicle',\
    'Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households': 'Latrine_facility_Night_soil_open_drain_Households',\
    'Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households': 'Latrine_Flush_connected_to_system_Households',\
    'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households': 'No_latrine_Alternative_source_Open_Households',\
    'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households': 'Main_drinking_water_Handpump_Tubewell_Borewell_Households',\
    'Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households': \
    'Main_drinking_water_Other_sources_Households',\
    'Age not stated':'Age_Not_Stated'})
     return renameddata  # Return the modified DataFrame

# Calling the rename function, passing the DataFrame 'data' as argument
data = rename_function(data)

# Print the DataFrame to verify changes (optional)
print(data)

##################################################TASK 1 completed###########################################################################

####################################################TASK 2 BEGIN#############################################################################

# Function to standardize state names by capitalizing each word except 'AND' and 'OF'
def standardize_state_names(name):
    # Split the state name into individual words
    words = name.split()
    # Capitalize each word unless it is 'AND' or 'OF'
    standardized_words = [word.capitalize() if word not in ['AND', 'OF'] else word.lower() for word in words]
    # Join the words back into a single string with spaces in between
    return ' '.join(standardized_words)
# Apply the standardize_state_names function to each element in the 'StateUT' column of the DataFrame
data['StateUT'] = data['StateUT'].apply(standardize_state_names)
# Print the DataFrame to see the standardized state names
print(data)

##################################################TASK 2 completed###########################################################################

####################################################TASK 3 BEGIN#############################################################################
from docx import Document

# Define the path to the Word document
doc_path = 'C:\\Users\\Senthil\\Desktop\\GuviPracticeClass\\GuviCapstoneproject\\Telangana.docx'

# Load the Word document
document = Document(doc_path)

# Extract text from paragraphs using a set comprehension to remove duplicates and strip whitespace
districts = {p.text.strip() for p in document.paragraphs if p.text.strip()}

# Update the 'StateUT' column to 'Telangana' for rows where 'District' is in the extracted districts
data.loc[data['District'].isin(districts), 'StateUT'] = 'Telangana'

# Define the districts for Ladakh
ladakh_districts = ['Leh(Ladakh)', 'Kargil']

# Update the 'StateUT' column to 'Ladakh' for rows where 'District' is in the Ladakh districts
data.loc[data['District'].isin(ladakh_districts), 'StateUT'] = 'Ladakh'
##################################################TASK 3 completed###########################################################################

##################################################TASK 4 BEGIN###############################################################################

import pandas as pd

# Calculate and print the initial percentage of missing values for each column
missing_percentages_initial = data.isnull().mean() * 100
print("Initial missing percentages:\n", missing_percentages_initial)

# Function to fill missing values in the DataFrame
def fill_missing_values(df):
    # Fill 'Population' with the sum of 'Male' and 'Female'
    df['Population'] = df['Population'].fillna(df['Male'] + df['Female'])
    
    # Fill 'Literate' with the sum of 'Literate_Male' and 'Literate_Female'
    df['Literate'] = df['Literate'].fillna(df['Literate_Male'] + df['Literate_Female'])
    
    # Fill 'Households' with the sum of 'Households_Rural' and 'Households_Urban'
    df['Households'] = df['Households'].fillna(df['Households_Rural'] + df['Households_Urban'])
    
    # Alternative way to fill 'Population' with the sum of age groups
    df['Population'] = df['Population'].fillna(df['Young_and_Adult'] + df['Middle_Aged'] + df['Senior_Citizen'] + df['Age_Not_Stated'])
    
    # Fill 'SC' with the sum of 'Male_SC' and 'Female_SC'
    df['SC'] = df['SC'].fillna(df['Male_SC'] + df['Female_SC'])
    
    # Fill 'ST' with the sum of 'Male_ST' and 'Female_ST'
    df['ST'] = df['ST'].fillna(df['Male_ST'] + df['Female_ST'])
    
    # Fill 'Workers' with the sum of 'Male_Workers' and 'Female_Workers'
    df['Workers'] = df['Workers'].fillna(df['Male_Workers'] + df['Female_Workers'])
    
    # Fill 'Non_Workers' by subtracting 'Workers' from 'Population'
    df['Non_Workers'] = df['Non_Workers'].fillna(df['Population'] - df['Workers'])
    
    # Alternative way to fill 'Workers' with the sum of 'Main_Workers' and 'Marginal_Workers'
    df['Workers'] = df['Workers'].fillna(df['Main_Workers'] + df['Marginal_Workers'])
    
    # Fill 'Literate_Male' by subtracting 'Literate_Female' from 'Literate'
    df['Literate_Male'] = df['Literate_Male'].fillna(df['Literate'] - df['Literate_Female'])
    
    # Fill 'Literate_Female' by subtracting 'Literate_Male' from 'Literate'
    df['Literate_Female'] = df['Literate_Female'].fillna(df['Literate'] - df['Literate_Male'])
    
    # Fill 'Cultivator_Workers' by subtracting other types of workers from 'Workers'
    df['Cultivator_Workers'] = df['Cultivator_Workers'].fillna(df['Workers'] - df['Agricultural_Workers'] - df['Household_Workers'] - df['Other_Workers'])
    
    # Fill 'Agricultural_Workers' by subtracting other types of workers from 'Workers'
    df['Agricultural_Workers'] = df['Agricultural_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Household_Workers'] - df['Other_Workers'])
    
    # Fill 'Household_Workers' by subtracting other types of workers from 'Workers'
    df['Household_Workers'] = df['Household_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Agricultural_Workers'] - df['Other_Workers'])
    
    # Fill 'Other_Workers' by subtracting other types of workers from 'Workers'
    df['Other_Workers'] = df['Other_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Agricultural_Workers'] - df['Household_Workers'])
    
    # Fill 'Total_Education' with the sum of various education levels
    df['Total_Education'] = df['Below_Primary_Education'] + df['Primary_Education'] + df['Middle_Education'] + df['Secondary_Education'] + df['Higher_Education'] + df['Graduate_Education'] + df['Other_Education'] + df['Literate_Education'] + df['Illiterate_Education']
    
    # Fill 'Location_of_drinking_water_source_Total' with the sum of different water source locations
    df['Location_of_drinking_water_source_Total'] = df['Location_of_drinking_water_source_Near_the_premises_Households'] + df['Location_of_drinking_water_source_Within_the_premises_Households'] + df['Location_of_drinking_water_source_Away_Households']
    
    # Fill 'Household_size_Total' with the sum of various household sizes
    df['Household_size_Total'] = df['Household_size_1_person_Households'] + df['Household_size_2_persons_Households'] + df['Household_size_3_persons_Households'] + df['Household_size_4_persons_Households'] + df['Household_size_5_persons_Households'] + df['Household_size_6_8_persons_Households'] + df['Household_size_9_persons_and_above_Households']
    
    # Fill 'Total_Power_Parity' with the sum of different power parity categories
    df['Total_Power_Parity'] = df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + df['Power_Parity_Rs_150000_240000'] + df['Power_Parity_Rs_240000_330000'] + df['Power_Parity_Rs_330000_425000'] + df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']
    
    return df

# Apply the filling logic to the DataFrame
data_filled = fill_missing_values(data)

# Calculate and print the percentage of missing values after filling
missing_percentages_final = data_filled.isnull().mean() * 100
print("Final missing percentages:\n", missing_percentages_final)

# Update the original DataFrame with the filled data
data = data_filled

# Compare the missing data percentages before and after filling
comparison = pd.DataFrame({
    'Initial': missing_percentages_initial,
    'Final': missing_percentages_final
})
print("Comparison of missing percentages:\n", comparison)

# Optional: Save missing data comparison to a CSV file for reporting
# comparison.to_csv('missing_data_comparison.csv', index=True)
##################################################TASK 4 completed###########################################################################

####################################################TASK 5 BEGIN#############################################################################
# Step 1: Define the MongoDB connection URI
# This URI is used to connect to the MongoDB database
uri = "mongodb+srv://devisenthilkumar2024:tamil@cluster0.lzkkk4j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Step 2: Connect to the MongoDB cluster and clear existing data in the target collection
# The 'delete_many({})' method is used to remove all documents from the collection to avoid duplication
MongoClient(uri).testdb.collection2.delete_many({})

# Step 3: Access the specific MongoDB collection where the data will be inserted
# The 'client' variable is used to interact with the MongoDB collection
client = MongoClient(uri).testdb.collection2

# Uncomment the next line if you want to print the current documents in the collection
# print(list(client.find()))

# Step 4: Convert the DataFrame to a list of dictionaries
# This format is required for inserting the data into MongoDB
data_dict = data.to_dict(orient='records')

# Step 5: Insert the data into the MongoDB collection
# The 'insert_many' method is used to insert the list of dictionaries
client.insert_many(data_dict)

# Step 6: Query the collection to verify insertion
# In this example, we query for documents where the 'Population' field is 870354
id = client.find({'Population': 870354})

# Uncomment the next line if you want to print the queried documents
# print(list(id))

# Step 7: Print a success message to confirm data insertion
print("Data inserted successfully into MongoDB")
##################################################TASK 5 completed###########################################################################

##################################################TASK  6 BEGIN##############################################################################
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from pymongo import MongoClient

# Step 1: Fetch data from MongoDB
# Convert the MongoDB cursor object to a list of dictionaries
data = list(client.find())

# Step 2: Convert the list of dictionaries to a pandas DataFrame
data_df = pd.DataFrame(data)

# Step 3: Drop the MongoDB specific '_id' column if it exists
# This column is auto-generated by MongoDB and not required in MySQL
if '_id' in data_df.columns:
    data_df = data_df.drop('_id', axis=1)

# Database connection details for MySQL
db_name = 'test'
db_user = 'root'
db_password = ''
db_host = 'localhost'

# Step 4: Create a connection to MySQL using mysql.connector
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Step 5: Use SQLAlchemy to create an engine for MySQL
# This engine is used to interact with the MySQL database
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Step 6: Retrieve column names from the DataFrame
columns = data_df.columns

# Print the data for verification
print("Data fetched from MongoDB:")
print(data)

# Step 7: Define the data types for the columns
# 'INT AUTO_INCREMENT PRIMARY KEY' is used for the first column (assumed to be an ID column)
# 'VARCHAR(255)' is used for the next two columns (assumed to be string data)
# 'INT' is used for the remaining columns (assumed to be numeric data)
data_types = ['INT AUTO_INCREMENT PRIMARY KEY'] + ['VARCHAR(255)'] * 2 + ['INT'] * (len(columns) - 3)

# Step 8: Create a SQL statement to create the table in MySQL
create_table_query = "CREATE TABLE IF NOT EXISTS census ("
for column, data_type in zip(columns, data_types):
    create_table_query += f"{column} {data_type}, "
create_table_query = create_table_query.rstrip(", ") + ");"

# Print the create table query for verification
print("Create table query:")
print(create_table_query)

# Step 9: Execute the create table query
# This creates the 'census' table in the MySQL database if it does not already exist
with connection.cursor() as cursor:
    cursor.execute(create_table_query)
    connection.commit()

# Step 10: Insert data into the MySQL table using pandas to_sql method
# This method replaces any existing data in the 'census' table
data_df.to_sql('census', con=engine, if_exists='replace', index=False)

# Step 11: Print a success message to confirm data insertion
print("Data inserted successfully into MySQL")

# Print the data again for final verification
print(data)
##################################################TASK 6 completed###########################################################################



##################################################TASK  7 BEGIN##############################################################################
'''import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px


# Use SQLAlchemy to create engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Custom hash function for LRUCache
def hash_lru_cache(obj):
    return hash(str(obj))

# Function to run queries with proper transaction handling
#@st.cache(hash_funcs={sqlalchemy.util._collections.LRUCache: hash_lru_cache})
def run_query(query):
    try:
        with engine.connect() as connection:
            result = pd.read_sql(query, connection)
        return result
    except Exception as e:
        connection.rollback()
        raise e

# Query: Total population of each district
total_population_query = """
SELECT District, SUM(Population) as Total_Population
FROM census
GROUP BY District
"""
total_population_df = run_query(total_population_query)

# Query: Literate males and females in each district
literate_males_females_query = """
SELECT District, SUM(Literate_Male) as Literate_Males, SUM(Literate_Female) as Literate_Females
FROM census
GROUP BY District
"""
literate_males_females_df = run_query(literate_males_females_query)

# Query: Percentage of workers in each district
percentage_workers_query = """
SELECT District, 
       (SUM(Male_Workers) + SUM(Female_Workers)) / SUM(Population) * 100 as Workers_Percentage
FROM census
GROUP BY District
"""
percentage_workers_df = run_query(percentage_workers_query)

# Query: Households with LPG or PNG
households_lpg_png_query = """
SELECT District, SUM(Households_with_LPG_PNG) as Households_LPG_PNG
FROM census
GROUP BY District
"""
households_lpg_png_df = run_query(households_lpg_png_query)

# Query: Religious composition of each district
religious_composition_query = """
SELECT District, SUM(Hindus) as Hindus, SUM(Muslims) as Muslims, SUM(Christians) as Christians, SUM(Others) as Others
FROM census
GROUP BY District
"""
religious_composition_df = run_query(religious_composition_query)

# Query: Households with internet access in each district
households_internet_access_query = """
SELECT District, SUM(Households_with_Internet_Access) as Households_Internet_Access
FROM census
GROUP BY District
"""
households_internet_access_df = run_query(households_internet_access_query)

# Query: Educational attainment distribution in each district
educational_attainment_query = """
SELECT District, 
       SUM(Below_Primary_Education) as Below_Primary_Education, 
       SUM(Primary_Education) as Primary_Education, 
       SUM(Middle_Education) as Middle_Education, 
       SUM(Secondary_Education) as Secondary_Education, 
       SUM(Higher_Education) as Higher_Education, 
       SUM(Graduate_Education) as Graduate_Education, 
       SUM(Other_Education) as Other_Education
FROM census
GROUP BY District
"""
educational_attainment_df = run_query(educational_attainment_query)

# Query: Households with various modes of transportation
households_transportation_query = """
SELECT District, 
       SUM(Households_with_Bicycle) as Households_with_Bicycle, 
       SUM(Households_with_Car) as Households_with_Car, 
       SUM(Households_with_Radio) as Households_with_Radio, 
       SUM(Households_with_Television) as Households_with_Television
FROM census
GROUP BY District
"""
households_transportation_df = run_query(households_transportation_query)

# Query: Condition of occupied census houses
census_houses_condition_query = """
SELECT District, 
       SUM(Dilapidated_Houses) as Dilapidated_Houses, 
       SUM(Houses_with_Separate_Kitchen) as Houses_with_Separate_Kitchen, 
       SUM(Houses_with_Bathing_Facility) as Houses_with_Bathing_Facility, 
       SUM(Houses_with_Latrine_Facility) as Houses_with_Latrine_Facility
FROM census
GROUP BY District
"""
census_houses_condition_df = run_query(census_houses_condition_query)

# Query: Household size distribution in each district
household_size_distribution_query = """
SELECT District, 
       SUM(Household_size_1_person) as Household_size_1_person, 
       SUM(Household_size_2_persons) as Household_size_2_persons, 
       SUM(Household_size_3_5_persons) as Household_size_3_5_persons, 
       SUM(Household_size_6_8_persons) as Household_size_6_8_persons, 
       SUM(Household_size_9_or_more_persons) as Household_size_9_or_more_persons
FROM census
GROUP BY District
"""
household_size_distribution_df = run_query(household_size_distribution_query)

# Query: Total number of households in each state
total_households_state_query = """
SELECT StateUT, SUM(Households) as Total_Households
FROM census
GROUP BY StateUT
"""
total_households_state_df = run_query(total_households_state_query)

# Query: Households with latrine facility within the premises in each state
households_latrine_state_query = """
SELECT StateUT, SUM(Households_with_Latrine_Facility) as Households_with_Latrine_Facility
FROM census
GROUP BY StateUT
"""
households_latrine_state_df = run_query(households_latrine_state_query)

# Query: Average household size in each state
average_household_size_query = """
SELECT StateUT, AVG(Household_Size) as Average_Household_Size
FROM census
GROUP BY StateUT
"""
average_household_size_df = run_query(average_household_size_query)

# Query: Owned vs rented households in each state
owned_rented_households_query = """
SELECT StateUT, SUM(Owned_Households) as Owned_Households, SUM(Rented_Households) as Rented_Households
FROM census
GROUP BY StateUT
"""
owned_rented_households_df = run_query(owned_rented_households_query)

# Query: Types of latrine facilities in each state
latrine_facilities_query = """
SELECT StateUT, 
       SUM(Pit_Latrine) as Pit_Latrine, 
       SUM(Flush_Latrine) as Flush_Latrine, 
       SUM(Others_Latrine) as Others_Latrine
FROM census
GROUP BY StateUT
"""
latrine_facilities_df = run_query(latrine_facilities_query)

# Query: Households with drinking water sources near the premises in each state
drinking_water_sources_query = """
SELECT StateUT, SUM(Households_with_Drinking_Water_Near_Premises) as Households_with_Drinking_Water_Near_Premises
FROM census
GROUP BY StateUT
"""
drinking_water_sources_df = run_query(drinking_water_sources_query)

# Query: Average household income distribution based on power parity categories in each state
household_income_distribution_query = """
SELECT StateUT, 
       SUM(Power_Parity_Less_than_45000) as Income_Less_than_45000, 
       SUM(Power_Parity_45000_90000) as Income_45000_90000, 
       SUM(Power_Parity_90000_150000) as Income_90000_150000, 
       SUM(Power_Parity_150000_240000) as Income_150000_240000, 
       SUM(Power_Parity_240000_330000) as Income_240000_330000, 
       SUM(Power_Parity_330000_425000) as Income_330000_425000, 
       SUM(Power_Parity_425000_545000) as Income_425000_545000, 
       SUM(Power_Parity_Above_545000) as Income_Above_545000
FROM census
GROUP BY StateUT
"""
household_income_distribution_df = run_query(household_income_distribution_query)

# Query: Percentage of married couples with different household sizes in each state
married_couples_household_size_query = """
SELECT StateUT, 
       (SUM(Households_with_Married_Couples) / SUM(Households)) * 100 as Married_Couples_Percentage
FROM census
GROUP BY StateUT
"""
married_couples_household_size_df = run_query(married_couples_household_size_query)

# Query: Households below the poverty line based on power parity categories in each state
households_below_poverty_line_query = """
SELECT StateUT, 
       SUM(Households_Below_Poverty_Line) as Households_Below_Poverty_Line
FROM census
GROUP BY StateUT
"""
households_below_poverty_line_df = run_query(households_below_poverty_line_query)

# Query: Overall literacy rate in each state
literacy_rate_query = """
SELECT StateUT, 
       (SUM(Literate_Population) / SUM(Population)) * 100 as Literacy_Rate
FROM census
GROUP BY StateUT
"""
literacy_rate_df = run_query(literacy_rate_query)
# Streamlit app
st.title("Census Data Analysis")
st.header("Total Population by District")

# Display the data in a table
st.dataframe(total_population_df)

# Plot the data using Plotly
fig = px.bar(total_population_df, x='District', y='Total_Population', title='Total Population by District')
st.plotly_chart(fig)

# Execute the script with `streamlit run script_name.py`
# Literate males and females in each district
st.header("Literate Males and Females in Each District")
st.write(literate_males_females_df)
fig = px.bar(literate_males_females_df, x='District', y=['Literate_Males', 'Literate_Females'], title="Literate Males and Females by District")
st.plotly_chart(fig)

# Percentage of workers in each district
st.header("Percentage of Workers in Each District")
st.write(percentage_workers_df)
fig = px.bar(percentage_workers_df, x='District', y='Workers_Percentage', title="Workers Percentage by District")
st.plotly_chart(fig)

# Households with LPG or PNG
st.header("Households with LPG or PNG in Each District")
st.write(households_lpg_png_df)
fig = px.bar(households_lpg_png_df, x='District', y='Households_LPG_PNG', title="Households with LPG or PNG by District")
st.plotly_chart(fig)

# Religious composition of each district
st.header("Religious Composition of Each District")
st.write(religious_composition_df)
fig = px.bar(religious_composition_df, x='District', y=['Hindus', 'Muslims', 'Christians', 'Others'], title="Religious Composition by District")
st.plotly_chart(fig)

# Households with internet access in each district
st.header("Households with Internet Access in Each District")
st.write(households_internet_access_df)
fig = px.bar(households_internet_access_df, x='District', y='Households_Internet_Access', title="Households with Internet Access by District")
st.plotly_chart(fig)

# Educational attainment distribution in each district
st.header("Educational Attainment Distribution in Each District")
st.write(educational_attainment_df)
fig = px.bar(educational_attainment_df, x='District', y=['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education'], title="Educational Attainment by District")
st.plotly_chart(fig)

# Households with various modes of transportation
st.header("Households with Various Modes of Transportation in Each District")
st.write(households_transportation_df)
fig = px.bar(households_transportation_df, x='District', y=['Households_with_Bicycle', 'Households_with_Car', 'Households_with_Radio', 'Households_with_Television'], title="Transportation Modes by District")
st.plotly_chart(fig)

# Condition of occupied census houses
st.header("Condition of Occupied Census Houses in Each District")
st.write(census_houses_condition_df)
fig = px.bar(census_houses_condition_df, x='District', y=['Dilapidated_Houses', 'Houses_with_Separate_Kitchen', 'Houses_with_Bathing_Facility', 'Houses_with_Latrine_Facility'], title="Condition of Census Houses by District")
st.plotly_chart(fig)

# Household size distribution in each district
st.header("Household Size Distribution in Each District")
st.write(household_size_distribution_df)
fig = px.bar(household_size_distribution_df, x='District', y=['Household_size_1_person', 'Household_size_2_persons', 'Household_size_3_5_persons', 'Household_size_6_8_persons', 'Household_size_9_or_more_persons'], title="Household Size Distribution by District")
st.plotly_chart(fig)

# Total number of households in each state
st.header("Total Number of Households in Each State")
st.write(total_households_state_df)
fig = px.bar(total_households_state_df, x='StateUT', y='Total_Households', title="Total Households by State")
st.plotly_chart(fig)

# Households with latrine facility within the premises in each state
st.header("Households with Latrine Facility within the Premises in Each State")
st.write(households_latrine_state_df)
fig = px.bar(households_latrine_state_df, x='StateUT', y='Households_with_Latrine_Facility', title="Households with Latrine Facility by State")
st.plotly_chart(fig)

# Average household size in each state
st.header("Average Household Size in Each State")
st.write(average_household_size_df)
fig = px.bar(average_household_size_df, x='StateUT', y='Average_Household_Size', title="Average Household Size by State")
st.plotly_chart(fig)

# Owned vs rented households in each state
st.header("Owned vs Rented Households in Each State")
st.write(owned_rented_households_df)
fig = px.bar(owned_rented_households_df, x='StateUT', y=['Owned_Households', 'Rented_Households'], title="Owned vs Rented Households by State")
st.plotly_chart(fig)

# Types of latrine facilities in each state
st.header("Types of Latrine Facilities in Each State")
st.write(latrine_facilities_df)
fig = px.bar(latrine_facilities_df, x='StateUT', y=['Pit_Latrine', 'Flush_Latrine', 'Others_Latrine'], title="Types of Latrine Facilities by State")
st.plotly_chart(fig)

# Households with drinking water sources near the premises in each state
st.header("Households with Drinking Water Sources Near the Premises in Each State")
st.write(drinking_water_sources_df)
fig = px.bar(drinking_water_sources_df, x='StateUT', y='Households_with_Drinking_Water_Near_Premises', title="Drinking Water Sources by State")
st.plotly_chart(fig)

# Average household income distribution based on power parity categories in each state
st.header("Average Household Income Distribution in Each State")
st.write(household_income_distribution_df)
fig = px.bar(household_income_distribution_df, x='StateUT', y=['Income_Less_than_45000', 'Income_45000_90000', 'Income_90000_150000', 'Income_150000_240000', 'Income_240000_330000', 'Income_330000_425000', 'Income_425000_545000', 'Income_Above_545000'], title="Household Income Distribution by State")
st.plotly_chart(fig)

# Percentage of married couples with different household sizes in each state
st.header("Percentage of Married Couples with Different Household Sizes in Each State")
st.write(married_couples_household_size_df)
fig = px.bar(married_couples_household_size_df, x='StateUT', y='Married_Couples_Percentage', title="Married Couples Percentage by State")
st.plotly_chart(fig)

# Households below the poverty line based on power parity categories in each state
st.header("Households Below the Poverty Line in Each State")
st.write(households_below_poverty_line_df)
fig = px.bar(households_below_poverty_line_df, x='StateUT', y='Households_Below_Poverty_Line', title="Households Below the Poverty Line by State")
st.plotly_chart(fig)

# Overall literacy rate in each state
st.header("Overall Literacy Rate in Each State")
st.write(literacy_rate_df)
fig = px.bar(literacy_rate_df, x='StateUT', y='Literacy_Rate', title="Literacy Rate by State")
st.plotly_chart(fig)

# Run Streamlit app
if __name__ == "__main__":
    st.title("Census Data Analysis Dashboard")'''

import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px

# Database connection parameters
db_name = 'test'
db_user = 'root'
db_password = ''
db_host = 'localhost'

# Use SQLAlchemy to create engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Custom hash function for LRUCache
def hash_lru_cache(obj):
    return hash(str(obj))

# Function to run queries with proper transaction handling
def run_query(query):
    try:
        with engine.connect() as connection:
            result = pd.read_sql(query, connection)
        return result
    except Exception as e:
        connection.rollback()
        raise e

# Queries dictionary
queries = {
    "Total Population by District": """
        SELECT District, SUM(Population) as Total_Population
        FROM census
        GROUP BY District
    """,
    "Literate Males and Females by District": """
        SELECT District, SUM(Literate_Male) as Literate_Males, SUM(Literate_Female) as Literate_Females
        FROM census
        GROUP BY District
    """,
    "Workers Percentage by District": """
        SELECT District, 
               (SUM(Male_Workers) + SUM(Female_Workers)) / SUM(Population) * 100 as Workers_Percentage
        FROM census
        GROUP BY District
    """,
    "Households with LPG or PNG by District": """
        SELECT District, SUM(Households_with_LPG_PNG) as Households_LPG_PNG
        FROM census
        GROUP BY District
    """,
    "Religious Composition by District": """
        SELECT District, SUM(Hindus) as Hindus, SUM(Muslims) as Muslims, SUM(Christians) as Christians, SUM(Others) as Others
        FROM census
        GROUP BY District
    """,
    "Households with Internet Access by District": """
        SELECT District, SUM(Households_with_Internet_Access) as Households_Internet_Access
        FROM census
        GROUP BY District
    """,
    "Educational Attainment by District": """
        SELECT District, 
               SUM(Below_Primary_Education) as Below_Primary_Education, 
               SUM(Primary_Education) as Primary_Education, 
               SUM(Middle_Education) as Middle_Education, 
               SUM(Secondary_Education) as Secondary_Education, 
               SUM(Higher_Education) as Higher_Education, 
               SUM(Graduate_Education) as Graduate_Education, 
               SUM(Other_Education) as Other_Education
        FROM census
        GROUP BY District
    """,
    "Households with Various Modes of Transportation by District": """
        SELECT District, 
               SUM(Households_with_Bicycle) as Households_with_Bicycle, 
               SUM(Households_with_Car) as Households_with_Car, 
               SUM(Households_with_Radio) as Households_with_Radio, 
               SUM(Households_with_Television) as Households_with_Television
        FROM census
        GROUP BY District
    """,
    "Condition of Occupied Census Houses by District": """
        SELECT District, 
               SUM(Dilapidated_Houses) as Dilapidated_Houses, 
               SUM(Houses_with_Separate_Kitchen) as Houses_with_Separate_Kitchen, 
               SUM(Houses_with_Bathing_Facility) as Houses_with_Bathing_Facility, 
               SUM(Houses_with_Latrine_Facility) as Houses_with_Latrine_Facility
        FROM census
        GROUP BY District
    """,
    "Household Size Distribution by District": """
        SELECT District, 
               SUM(Household_size_1_person) as Household_size_1_person, 
               SUM(Household_size_2_persons) as Household_size_2_persons, 
               SUM(Household_size_3_5_persons) as Household_size_3_5_persons, 
               SUM(Household_size_6_8_persons) as Household_size_6_8_persons, 
               SUM(Household_size_9_or_more_persons) as Household_size_9_or_more_persons
        FROM census
        GROUP BY District
    """,
    "Total Households by State": """
        SELECT StateUT, SUM(Households) as Total_Households
        FROM census
        GROUP BY StateUT
    """,
    "Households with Latrine Facility by State": """
        SELECT StateUT, SUM(Households_with_Latrine_Facility) as Households_with_Latrine_Facility
        FROM census
        GROUP BY StateUT
    """,
    "Average Household Size by State": """
        SELECT StateUT, AVG(Household_Size) as Average_Household_Size
        FROM census
        GROUP BY StateUT
    """,
    "Owned vs Rented Households by State": """
        SELECT StateUT, SUM(Owned_Households) as Owned_Households, SUM(Rented_Households) as Rented_Households
        FROM census
        GROUP BY StateUT
    """,
    "Types of Latrine Facilities by State": """
        SELECT StateUT, 
               SUM(Pit_Latrine) as Pit_Latrine, 
               SUM(Flush_Latrine) as Flush_Latrine, 
               SUM(Others_Latrine) as Others_Latrine
        FROM census
        GROUP BY StateUT
    """,
    "Households with Drinking Water Sources by State": """
        SELECT StateUT, SUM(Households_with_Drinking_Water_Near_Premises) as Households_with_Drinking_Water_Near_Premises
        FROM census
        GROUP BY StateUT
    """,
    "Household Income Distribution by State": """
        SELECT StateUT, 
               SUM(Power_Parity_Less_than_45000) as Income_Less_than_45000, 
               SUM(Power_Parity_45000_90000) as Income_45000_90000, 
               SUM(Power_Parity_90000_150000) as Income_90000_150000, 
               SUM(Power_Parity_150000_240000) as Income_150000_240000, 
               SUM(Power_Parity_240000_330000) as Income_240000_330000, 
               SUM(Power_Parity_330000_425000) as Income_330000_425000, 
               SUM(Power_Parity_425000_545000) as Income_425000_545000, 
               SUM(Power_Parity_Above_545000) as Income_Above_545000
        FROM census
        GROUP BY StateUT
    """,
    "Married Couples with Different Household Sizes by State": """
        SELECT StateUT, 
               (SUM(Households_with_Married_Couples) / SUM(Households)) * 100 as Married_Couples_Percentage
        FROM census
        GROUP BY StateUT
    """,
    "Households Below the Poverty Line by State": """
        SELECT StateUT, 
               SUM(Households_Below_Poverty_Line) as Households_Below_Poverty_Line
        FROM census
        GROUP BY StateUT
    """,
    "Overall Literacy Rate by State": """
        SELECT StateUT, 
               (SUM(Literate_Population) / SUM(Population)) * 100 as Literacy_Rate
        FROM census
        GROUP BY StateUT
    """
}

# Streamlit app
st.title("Census Data Analysis Dashboard")

# User selects the query
query_selection = st.selectbox("Select a query to visualize:", list(queries.keys()))

# Run the selected query
selected_query = queries[query_selection]
df = run_query(selected_query)

# Display the data
#st.dataframe(df)

# Plot the data using Plotly
if query_selection == "Total Population by District":
    fig = px.bar(df, x='District', y='Total_Population', title='Total Population by District')
elif query_selection == "Literate Males and Females by District":
    fig = px.bar(df, x='District', y=['Literate_Males', 'Literate_Females'], title="Literate Males and Females by District")
elif query_selection == "Workers Percentage by District":
    fig = px.bar(df, x='District', y='Workers_Percentage', title="Workers Percentage by District")
elif query_selection == "Households with LPG or PNG by District":
    fig = px.bar(df, x='District', y='Households_LPG_PNG', title="Households with LPG or PNG by District")
elif query_selection == "Religious Composition by District":
    fig = px.bar(df, x='District', y=['Hindus', 'Muslims', 'Christians', 'Others'], title="Religious Composition by District")
elif query_selection == "Households with Internet Access by District":
    fig = px.bar(df, x='District', y='Households_Internet_Access', title="Households with Internet Access by District")
elif query_selection == "Educational Attainment by District":
    fig = px.bar(df, x='District', y=['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education'], title="Educational Attainment by District")
elif query_selection == "Households with Various Modes of Transportation by District":
    fig = px.bar(df, x='District', y=['Households_with_Bicycle', 'Households_with_Car', 'Households_with_Radio', 'Households_with_Television'], title="Households with Various Modes of Transportation by District")
elif query_selection == "Condition of Occupied Census Houses by District":
    fig = px.bar(df, x='District', y=['Dilapidated_Houses', 'Houses_with_Separate_Kitchen', 'Houses_with_Bathing_Facility', 'Houses_with_Latrine_Facility'], title="Condition of Occupied Census Houses by District")
elif query_selection == "Household Size Distribution by District":
    fig = px.bar(df, x='District', y=['Household_size_1_person', 'Household_size_2_persons', 'Household_size_3_5_persons', 'Household_size_6_8_persons', 'Household_size_9_or_more_persons'], title="Household Size Distribution by District")
elif query_selection == "Total Households by State":
    fig = px.bar(df, x='StateUT', y='Total_Households', title='Total Households by State')
elif query_selection == "Households with Latrine Facility by State":
    fig = px.bar(df, x='StateUT', y='Households_with_Latrine_Facility', title='Households with Latrine Facility by State')
elif query_selection == "Average Household Size by State":
    fig = px.bar(df, x='StateUT', y='Average_Household_Size', title='Average Household Size by State')
elif query_selection == "Owned vs Rented Households by State":
    fig = px.bar(df, x='StateUT', y=['Owned_Households', 'Rented_Households'], title='Owned vs Rented Households by State')
elif query_selection == "Types of Latrine Facilities by State":
    fig = px.bar(df, x='StateUT', y=['Pit_Latrine', 'Flush_Latrine', 'Others_Latrine'], title='Types of Latrine Facilities by State')
elif query_selection == "Households with Drinking Water Sources by State":
    fig = px.bar(df, x='StateUT', y='Households_with_Drinking_Water_Near_Premises', title='Households with Drinking Water Sources by State')
elif query_selection == "Household Income Distribution by State":
    fig = px.bar(df, x='StateUT', y=['Income_Less_than_45000', 'Income_45000_90000', 'Income_90000_150000', 'Income_150000_240000', 'Income_240000_330000', 'Income_330000_425000', 'Income_425000_545000', 'Income_Above_545000'], title='Household Income Distribution by State')
elif query_selection == "Married Couples with Different Household Sizes by State":
    fig = px.bar(df, x='StateUT', y='Married_Couples_Percentage', title='Married Couples with Different Household Sizes by State')
elif query_selection == "Households Below the Poverty Line by State":
    fig = px.bar(df, x='StateUT', y='Households_Below_Poverty_Line', title='Households Below the Poverty Line by State')
elif query_selection == "Overall Literacy Rate by State":
    fig = px.bar(df, x='StateUT', y='Literacy_Rate', title='Overall Literacy Rate by State')
else:
    fig = None

if fig:
    st.plotly_chart(fig)