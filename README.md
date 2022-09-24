# Energy consumption Airbnb

## Objective
Develop a energy consumption management solution to an Airbnb Host at no cost.

## Contextualization
 An Airbnb host asked me help about how he could monitor his guests energy consumption during each guest rental period.
 Main problem statements were:
 -  He was concerned about current cost of R$200,00/year for having a dashboard, indeed the problem was the dashboard was not customizable and was cluttered with too much information he doesn't need.
 - Information update interval was not being achieved as well, the previous solution only provided the minimal interval of 30 minutes and he wanted 1 minute interval between measurements.
 - He wanted to have a easy way of filterimng energy consumption by guest's entrance date and leave date.
 - The host also wanted a free solution and wanted to parametize KWH price directly on the dashboard.
 
 ## Resources Avaiable
 
 - Internet Connection
 - A energy consumption equipment (model SM3W LITE)
 - Free Google Account
 
 # Solution Provided
 
 To deliver this project the following techologies were employed:
 
 - Google Cloud function (Python)
 - Google Cloud Storage
 - Google Sheets API
 - Google Drive API
 - Google secret
 - Microsoft POWER BI
 - Google sheet


# SOLUTION COST

All the project falls into the google free tier, hence the project doesn't incurred in costs to the Airbnb host.

# Explaining project Implementation

SM3W has an option to send metrics measured in a configured time interval over a HTTP connection.
Considering this reality I built a Google Cloud function that works with a HTTP trigger.

The file main.py contains all the logic for processing the data acquisition stage, which consists of:

- Receiving data from sensor over HTTP
- Processing http request to transform the input
- Save transformed data as a object in google cloud storage, naming it by the date of data arrival
- Make aditional transformation to tranform data into a format that was ready to be inserted in a previously created google sheet
- Authenticate to the google sheets and google drive api
- Insert data into the google sheets

After that a dashboard was developed in Power BI and used the google sheet as datasource

The dashbaord has the option to parametrize KWH price and a filter for guest accomodation time period
Below we have a diagram with the solution.

## SOLUTION DIAGRAM


 
 

 



