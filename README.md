# Red Bus Scraping Project

Redbus Data Scraping with Selenium &amp; Dynamic Filtering using Streamlit

This repository contains a comprehensive solution for scraping, storing, and visualizing bus travel data from the Red Bus website. The project utilizes Selenium for web scraping, SQL for data storage, and Streamlit for data visualization.

**Packages Used:**

- **Selenium:**

The selenium package is used to automate web browser interaction from Python.

To know more about **selenium**. Click here <https://selenium-python.readthedocs.io/>

- **Streamlit:**

  Streamlit turns data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience required.

  To know more about **Streamlit**. Click here <https://docs.streamlit.io/>

- **Pandas:**

  Pandas is a powerful and open-source Python library. The Pandas library is used for data manipulation and analysis.

  Pandas consist of data structures and functions to perform efficient operations on data.

  To know more about **Pandas.** Click here [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20) 

- **MySQL:**

  MySQL, the most popular Open-Source SQL database management system, is developed, distributed, and supported by 

  Oracle Corporation. 

  To know more about **MySQL**. Click here <https://dev.mysql.com/doc/refman/9.0/en/>

- **Streamlit-Option-Menu:**
  
  Streamlit-option-menu is a simple Streamlit component that allows users to select a single item from alist of options in a menu.

  To know more about Streamlit-Option-Menu. Click here [https://discuss.streamlit.io/t/streamlit-option-menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu/20514](https://discuss.streamlit.io/t/streamlit-option-%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu/20514)

**Install Packages:**

- **Selenium** – pip install selenium
- **Pandas** – pip install pandas
- **Streamlit** – pip install streamlit
- **MySQL** **Connector**– pip install mysql-connector-python
- **Streamlit-Option-Menu** – pip install streamlit-option-menu

**Code Flow Plan:**

This project contains three files

[text](datainsertion.py)
[text](redbusmain.py)
[text](streamlit.py)
[text](streamlit.py)


**1) [text](redbusmain.py)**

This Python script uses the Selenium library to automate web scraping from the Redbus website and process the data using pandas. The script follows these main steps:

1. **Import Libraries**: Necessary packages for web scraping, database operations, and data handling are imported.
1. **HomePage\_driver Function**: Opens the Redbus website, maximizes the browser window, and scrolls down the page to make elements visible.
1. **StatesPage\_Link Function**: Navigates to the provided state link, extracts the state names and their respective links, and stores them in lists.
1. **BusRoutes\_link Function**: For each state link, navigates to the state page, extracts bus route links from all available pages, and compiles a list of these routes along with state names.
1. **BUSDETAILS Function**: Iterates through the bus route links, navigates to each route page, extracts detailed bus information (such as bus names, types, departure times, travel durations, ratings, prices, and seat availability), and stores these details in a list.
1. **Closingdriver Function**: Closes the browser window to end the session.
1. **Main Script Execution**: Initializes the Chrome driver and calls the functions in sequence:
   1. Opens the Redbus home page.
   1. Extracts state page links and names, and saves them to a CSV file.
   1. Extracts bus route links and saves them to another CSV file.
   1. (Commented out) Extracts detailed bus information and saves it to a CSV file.
   1. Closes the browser.

**2) [text](datainsertion.py)**

- This Python script facilitates the extraction, transformation, and loading (ETL) of bus route and bus details data into a MySQL database. It begins by importing the necessary modules, including mysql.connector for database operations and pandas for data manipulation. The script defines several functions for different stages of the ETL process:
- **SQL\_Connection**: Establishes a connection to a MySQL database using provided configuration details and returns the connection and cursor objects.
- **ReadData\_From\_Excel**: Reads data from a CSV file and returns it as a pandas DataFrame. It includes error handling to catch issues that might occur during file reading.
- **Create\_Table**: Executes a SQL query to create a table in the MySQL database. It includes error handling to manage exceptions during table creation.
- **Insert\_Table**: Inserts data into a specified MySQL table using a provided query and data. It commits the changes to the database and handles any insertion errors.
- **Close\_Connection**: Closes the database connection and cursor, with error handling to ensure proper closure even if issues arise.
- The script's main execution sequence involves:
- Establishing a connection to the MySQL database.
- Reading bus route links and bus details from CSV files (route\_data.csv and bus\_data.csv, respectively) into pandas DataFrames.
- Filling missing star ratings in the bus details DataFrame with 0.
- Creating the BusRoutesAndLinks and BusDetails tables in the MySQL database if they do not already exist. The BusDetails table includes a foreign key reference to BusRoutesAndLinks.
- Inserting the bus route links and bus details data into their respective tables using the INSERT statements with ON DUPLICATE KEY UPDATE to handle duplicates.
- Closing the database connection and cursor to clean up resources.
- This script ensures that data is accurately transferred from CSV files to a MySQL database, with robust error handling at each step to manage potential issues..

**3) [text](streamlit.py)**

This Streamlit application enables users to search and book bus tickets using the Redbus platform. It integrates with a MySQL database to fetch and display bus information based on user-selected filters.

The script begins by importing necessary modules, including Streamlit for the web interface, MySQL connector for database interaction, pandas for data manipulation, and time for delays.

A configuration function sets up database connection parameters, while the connection function establishes a connection to the MySQL database using these parameters. If the connection fails, appropriate error messages are displayed.

Two helper functions are defined for database interaction:

- fetch\_distinct\_value executes queries to retrieve distinct values from the database (e.g., bus types, states).
- fetch\_filtered\_value executes queries to retrieve filtered bus data based on user criteria, returning the data as a pandas DataFrame. It also converts 0.0 star ratings to "NA".

The Streamlit page is configured with a title, icon, and layout. Custom CSS is loaded to enhance the styling of the application.

The sidebar contains an image and filter options for seat type, price range, star rating, and departure time. These options are populated dynamically with data fetched from the database.

The main page layout includes two columns for selecting the state and route. The state dropdown is populated with distinct states, and based on the selected state, the route dropdown is populated with corresponding routes.

When the "Search" button is clicked, a SQL query is constructed based on the selected filters. This query is executed, and the results are displayed in a table. If no buses match the criteria, an appropriate message is shown.

Overall, this application provides a user-friendly interface for searching and booking bus tickets, offering various filters to refine search results and display relevant bus information.


**How to run the code:**

Initially run the “[text](redbusmain.py)”  in terminal. Wait until it completely scraping the 10 bus routes data.

After the data is scraped and the data are stored as a csv file run "[text](datainsertion.py)" to store the data the SQL database.

[text](bus_data.csv) & [text](route_data.csv) will be the csv files to store in the database 

After finishing the scraping process run “[text](streamlit.py)” using command “**streamlit run [text](streamlit.py)**”