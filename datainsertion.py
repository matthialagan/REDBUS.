# intially import all the required modules for this project
import mysql.connector as db
from mysql.connector import Error
import pandas as pd

# this SQL_Connection will create the connection between python and mysql
def SQL_Connection():

    config = {
    "user":"root",
    "password":"Guvi8754241299",
    "host":"localhost",
    "database":"project_redbus"
    }
    
    conn = db.connect(**config)
    cursor = conn.cursor()

    return conn,cursor

def drop_table(conn,query_drop):
    # this function will drop the table
    c=conn.cursor()
    try:
        c.execute(query_drop)
        print("Table dropped successfully")
    
    except Error as e:
        print("Error occurred when dropping data",e)

#this ReadData_From_Excel will read the data from the .csv file
def ReadData_From_Excel(file_path):
    try:
        """Reads data from an Excel file and returns a DataFrame."""
        return pd.read_csv(file_path)
    except Exception as e:
        print(f'\nError in Reading the data from {file_path}: ', e)

#this Create_Table will create a table in the database
def Create_Table(cursor,table_query):
    try:
        cursor.execute(table_query)
        print("\nSuccessfully Created Table")
    except Error as e:
        print("\nCreateTable_Error: ", e)    

#this Insert_Table will insert the data into the table
def Insert_Table(cursor,query,data):
    try:
        cursor.executemany(query,data)
        conn.commit()
        print("\nSuccessfully Inserted Data") 

    except Error as e:
        print("\nInsertData_Error: ", e)    

#this function will close the connection 
def Close_Connection(conn,cursor):
    try:
        conn.close()
    except Exception as e:
        print('\nError in closing the connection: ',e)    

    try:
        cursor.close()
    except Exception as e:
        print('\nError in closing the cursor: ', e)          



#Connect the Sql Server 
conn,cursor = SQL_Connection()    



# if the table already exists drop it to avoid the append of datas
drop_table(conn,"drop table if exists BusDetails")
drop_table(conn,"drop table if exists BusRoutesAndLinks")  



#Read Data from the Excel
busrouteslinks = 'route_data.csv'
df = ReadData_From_Excel(busrouteslinks)
print("\n",df)




#Read Data From the Excel
busdetails = 'bus_data.csv'
df1= ReadData_From_Excel(busdetails)
df1["Bus Rating"] = df1["Bus Rating"].fillna(0)
print("\n",df1)



# checking the Bus_NO values are present in the Route_NO
for bus_no in df1['Bus_NO']:
    if bus_no not in df['Route_NO'].values:
        print(f"Bus_No {bus_no} in bus_data.csv does not match any Route_NO in route_data.csv")
        break




#Create Table BusroutesLinks in MySql
Create_Table(cursor,"""CREATE table IF NOT EXISTS BusRoutesAndLinks(
             Route_NO int Primary Key not null,
             State_TransportationName varchar(100) not null,
             Bus_Routes varchar(50) not null,
             Routes_Links varchar(100) not null unique);""")



#Create Table BusDetails in MySql
Create_Table (cursor,"""CREATE table IF NOT EXISTS BusDetails(
              BusDetails_ID int Primary Key auto_increment,
              Bus_No int not null,
              Bus_Name varchar(100) not null,
              Bus_Type varchar(100) not null,
              Departure_Time time not null,
              Travelling_Time varchar(50) not null,
              Reaching_Time time not null,
              Bus_rating FLOAT not null,
              Ticket_Price decimal not null,
              Seat_Availability int not null);"""
              )



#Insert Data's into BusRoutesAndLinks Table
Insert_query = """
                INSERT into BusRoutesAndLinks(Route_NO,State_TransportationName, Bus_Routes,Routes_Links) 
                values(%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    Route_NO = VALUES(Route_NO),    
                    State_TransportationName = VALUES(State_TransportationName), 
                    Bus_Routes = VALUES(Bus_Routes), 
                    Routes_Links = VALUES(Routes_Links)
                """

data = df.to_numpy().tolist() #converting the data into list of tuples to insert into the table
Insert_Table(cursor,Insert_query,data)



#Insert Data's into BusRoutesLinks Table
Insert_query1 = """
    INSERT INTO BusDetails (Bus_No,Bus_Name, Bus_Type, Departure_Time, Travelling_Time, Reaching_Time, Bus_rating, Ticket_Price, Seat_Availability)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        Bus_No = VALUES(Bus_No),
        Bus_Name = VALUES(Bus_Name), 
        Bus_Type = VALUES(Bus_Type), 
        Departure_Time = VALUES(Departure_Time),
        Travelling_Time = VALUES(Travelling_Time),
        Reaching_Time = VALUES(Reaching_Time),
        Bus_rating = VALUES(Bus_rating),
        Ticket_Price = VALUES(Ticket_Price),
        Seat_Availability = VALUES(Seat_Availability)
"""

data1 = df1[['Bus_NO', 'Bus Name', 'Bus Type', 'Departure Time', 'Travelling Time', 'Reaching Time', 'Bus Rating', 'Ticket Price', 'Seat Availability']].to_numpy().tolist() #converting the data into list of tuples to insert into the table
Insert_Table(cursor,Insert_query1,data1)
 


#Close the MySql COnnection 
Close_Connection(conn,cursor)