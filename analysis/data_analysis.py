"""
Analysis of 3 months of data
Data spans from January 1st 2021 until March 31st 2021.
Information we want from this analysis:
- What time do we activate the detector for the first time of the day?
- How much time do we spend in the kitchen per day?

For both questions, the goal is to provide the mean, standard deviation and a graph that shows the first time over the days and outlines the mean +/- 1 standard deviation
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#===============================================================================================================
#Get the dataframe ready for analysis
df = pd.read_csv("data3months.csv", sep = '\t')
# Replace the ',' in the value column by '.'
df["Value"] = df["Value"].str.replace(',','.')
# Convert data type in the column 'Value' from object to float
df["Value"] = df['Value'].astype(float)
# Drop the column we don't need
df = df.drop(["Equipment"], axis = 'columns')
#Rename column head
df = df.rename(columns={"Type": "Parameter"})
#Convert the dates into timestamps
df["Date"] = pd.to_datetime(df["Date"], format= '%Y-%m-%d %H:%M:%S')
#Select the rows with the presence parameter
presence = df.loc[df["Parameter"] == "PRESENCE"]

#============================================================================================================
#Select rows where PRESENCE == 1 for the 1st time of the day
#The data is presented with an alternance of 1 and 0, 1 being presence detected and 0 being no presence.
#Extract the date from the top row of the dataframe "presence" and change the time to midnight.
#normalize() changes the time to midnight
start_date = presence['Date'][presence.index.min()].normalize()

#Extract the date from the bottom row of the dataframe "presence"
last_date = presence['Date'][presence.index.max()]

#Create an empty DataFrame called first_time
first_time = pd.DataFrame()

while start_date < last_date:
    #select_start is a selection of the DataFrame "presence" that will change at every iteration.
    select_start = presence[(presence['Date'] >= start_date)]
#if/else is to make sure that PRESENCE == 1 for the top row.
#If PRESENCE is not 1 for the top row, then top_row starts on the 2nd row.
    if select_start['Value'].iloc[0,] == 1:
        #Select the 1st row from the DataFrame "select_start"
        top_row = select_start.iloc[0,]
    else:
        top_row = select_start.iloc[1,]
    #If we are at home:
    if top_row['Date'].normalize() == start_date:
        #Add top_row to the DataFrame "first_time"
        first_time = first_time.append(top_row)
        #Moves the start_date forward 1 day
        start_date = start_date + pd.Timedelta(days = 1)
    #If we are not at home:
    else:
        days_away = top_row['Date'].normalize() - start_date + pd.Timedelta(days = 1)
        start_date = start_date + pd.Timedelta(days = days_away/ pd.Timedelta(days = 1))

#=================================================================================================================
#Calculate the mean and the standard deviation
#Change the timestamps into timedeltas
time_only = pd.Series([(x-x.normalize()) for x in first_time['Date']], index = first_time.index)
#Add a column in the table with the Timedeltas
first_time['Time'] = time_only
#Calculate the mean
first_time_mean = first_time['Time'].mean()
#Calculate the standard deviation
first_time_std = first_time['Time'].std()

#======================================================================================================================
#Plot
#Convert `first_time_mean` and `first_time_std` into seconds (data type = float).
first_time_mean_sec = first_time_mean/pd.Timedelta(seconds = 1)
first_time_std_sec = first_time_std/pd.Timedelta(seconds = 1)

#Convert `first_time_mean_sec` and `first_time_std_sec` into a float that represents the hours.
first_time_mean_float = first_time_mean_sec/3600
first_time_std_float = first_time_std_sec/3600

#Convert elements in `first_time['Time']` into a float that we can plot
first_time['Time_float'] = (first_time['Time']/pd.Timedelta(seconds = 1))/3600

#Get mean +/- 1 standard deviation for plotting
first_time_mean_plus = first_time_mean_float + first_time_std_float
first_time_mean_minus = first_time_mean_float - first_time_std_float

a = first_time.plot.scatter(x = "Date", y = "Time_float", title = "First entry in kitchen", legend = False, figsize = (10,7))
a.axhline(first_time_mean_float, color = "red")
a.axhline(first_time_mean_plus, color = 'green')
a.axhline(first_time_mean_minus, color = 'green')
a.set_ylabel("Time (h)")
a.set_xlabel('Day')
plt.savefig("first_time_in_kitchen.png")

#============================================================================================================
#============================================================================================================
"""
Time spent in kitchen per day (Analysis of the 3 months of data)
Below is the code used to figure out how much time we spent in the kitchen everyday:
- Items in the list `timestamps_24h` are the Timestamps recorded for 1 day.
- Items in the list `timedeltas_24h` are the length of time spent in the kitchen for 1 day.
- **Each** item in the list `time_spent` represents the length of time spent in the kitchen for 1 day.

**Note**: presence values fluctuate between 1 and 0, 1 being presence (or movement) detected and 0 being no movement.
The duration is evaluated by substracting the row where value = 0 by the row above it.
The code below needs improvement: for example, if we are not at home for a few days in a row, it does not remove
the data from when we leave or come back home. Because this data would not accurately represent the amount of time
we spend in the kitchen, it should be excluded from the analysis.
"""
# Create a list that only contains the dates included in the dataframe "presence"
# This list takes care of our absence.
day_list = []
for x in presence['Date']:
    if x.normalize() not in day_list:
        day_list.append(x.normalize())
# Add a day after the last day of the list
day_list.append(day_list[-1] + pd.Timedelta(days=1))

ind_list = 0
start_date = day_list[ind_list]
stop_date = start_date + pd.Timedelta(days=1)
last_row = day_list[-1]
time_spent = []
while start_date < last_row:
    # Create a dataframe containing data from 1 day
    df_1day = presence.loc[(presence['Date'] >= start_date) & (presence['Date'] < stop_date)]
    timestamps_24h = []
    # In case we are in the kitchen at around midnight
    # Create a list timestamp_24h with timestamps of the day
    # If the Value is 0 for the top row of the df-1day dataframe,
    # it means that we were probably in the kitchen around midnight, add a timestamp saying midnight.
    if df_1day['Value'].iloc[0,] == 0:
        timestamps_24h.append(start_date)
    for x in df_1day['Date']:
        timestamps_24h.append(x)
    # If the Value is 1 for the last row of the df_1day dataframe,
    # it means that we were probably in the kitchen around midnight, add a timestamp w/ next day and time is midnight.
    if df_1day['Value'].iloc[-1,] == 1:
        timestamps_24h.append(stop_date)
    timedeltas_24h = []
    n = 0
    duration = pd.Timedelta(days=0)
    # Loop to gen2021-01-30erate the list timedeltas_24h with the amount of time spent in the kitchen
    while n < len(timestamps_24h):
        timedeltas_24h.append(timestamps_24h[n + 1] - timestamps_24h[n])
        n += 2
    # Add all items of timedeltas_24h into duration
    for i in timedeltas_24h:
        duration += i
    # Generate a list with the total amount of time spent in 24h
    time_spent.append(duration)
    ind_list += 1
    start_date = day_list[ind_list]
    stop_date = start_date + pd.Timedelta(days=1)

# Create a dataframe that contains the time spent and the days
time_kitchen = pd.DataFrame({'day_list': day_list[:-1], 'time_spent': time_spent})

#============================================================================================================
#Calculate the mean and standard deviation for the time spent in the kitchen
time_kitchen_mean = time_kitchen['time_spent'].mean()
time_kitchen_std = time_kitchen['time_spent'].std()

#============================================================================================================
#Plot
#Convert `time_kitchen_mean` and `time_kitchen_std` into seconds.
time_kitchen_mean_sec = time_kitchen_mean/pd.Timedelta(seconds = 1)
time_kitchen_std_sec = time_kitchen_std/pd.Timedelta(seconds = 1)

#Convert `time_kitchen_mean_sec` and `time_kitchen_std_sec` into a float
time_kitchen_mean_float = time_kitchen_mean_sec/3600
time_kitchen_std_float = time_kitchen_std_sec/3600

#Convert elements in `first_time['Time']` into a float that we can plot
time_kitchen['time_spent_float'] = (time_kitchen['time_spent']/pd.Timedelta(seconds = 1))/3600

#Get mean +/- 1 standard deviation for plotting
time_kitchen_mean_plus = time_kitchen_mean_float + time_kitchen_std_float
time_kitchen_mean_minus = time_kitchen_mean_float - time_kitchen_std_float

b = time_kitchen.plot.scatter(x = "day_list", y = "time_spent_float", title = "Time spent in kitchen", legend = False, figsize = (10,7))
b.axhline(time_kitchen_mean_float, color = "red")
b.axhline(time_kitchen_mean_plus, color = 'green')
b.axhline(time_kitchen_mean_minus, color = 'green')
b.set_ylabel("Time (h)")
b.set_xlabel('Day')
plt.savefig("time_spent_kitchen.png")

#============================================================================================================
#============================================================================================================
#============================================================================================================
"""
Analysis of 24h of data
From the 3 months data analysis, we obtained a mean and standard deviation for a couple of parameters. Any value that is within 1 standard deviation from the mean for the parameter is considered normal (right range).
Goals of this analysis:
- Find out what time we entered the kitchen for the first time of the day
- How much time we spent in the kitchen
- Find out whether the first entry time and the time spent in the kitchen are within 1 standard deviation from the mean obtained in the 3 months data analysis.
- Send an email if it is not in the right range.
"""
ind = 1
next_day = day_list[-1] + pd.Timedelta(days = 1)
day_to_day = pd.DataFrame()
while next_day <= pd.to_datetime('today').date():
    #print(next_day)
    if (next_day < pd.to_datetime('2021-04-10')) | (next_day == pd.to_datetime('2021-04-14')) | (next_day == pd.to_datetime('2021-04-19')) | (next_day == pd.to_datetime('2021-04-23')) | (next_day == pd.to_datetime('2021-06-04')):
        next_day = datetime.strftime(next_day, '%Y-%m-%d')
        next_data = pd.read_csv(f'Adelego_{next_day}_00h00.csv', sep = '\t')
    elif next_day == pd.to_datetime('2021-05-30'):
        next_day = datetime.strftime(next_day, '%Y-%m-%d')
        next_data = pd.read_csv(f'Adelego_{next_day}_00h00.csv')
    else:
        next_day = datetime.strftime(next_day, '%Y-%m-%d')
        next_data = pd.read_csv(f'Adelego_{next_day}_00h00.csv', sep = ';')
    next_data = next_data.drop(['Objet', "Équipement", "Commande"], axis=1)
    next_day = pd.to_datetime(next_day) + pd.Timedelta(days = 1)
    next_data = next_data.rename(columns={'Type Générique': 'Parameter', 'Valeur': 'Value', 'Unité': 'Unit'})
    next_data['Date'] = pd.to_datetime(next_data['Date'])
    presence_next_day = next_data.loc[(next_data['Parameter'] == 'PRESENCE')]
    initial_next = presence_next_day.iloc[0, 0] - presence_next_day.iloc[0, 0].normalize()
    if (first_time_mean - first_time_std) <= initial_next <= (first_time_mean + first_time_std):
        initial_next_in_range = 'Normal'
    elif initial_next < (first_time_mean - first_time_std):
        initial_next_in_range = 'Early'
    else:
        initial_next_in_range = 'Late'
    timedeltas_24h = []
    duration_next = pd.Timedelta(days=0)
    n = presence_next_day.index.min()
    while n < presence_next_day.index.max():
        if presence_next_day['Value'].iloc[0,] == 0:
            timedeltas_24h.append(presence_next_day['Date'].iloc[0,] - presence_next_day['Date'].iloc[0,].normalize())
        timedeltas_24h.append(presence_next_day['Date'][n + 1] - presence_next_day['Date'][n])
        n += 2
    for i in timedeltas_24h:
        duration_next += i
    if (time_kitchen_mean - time_kitchen_std) < duration_next < (time_kitchen_mean + time_kitchen_std):
        duration_next_in_range = 'Normal'
    elif duration_next < (time_kitchen_mean - time_kitchen_std):
        duration_next_in_range = 'Low'
    else:
        duration_next_in_range = 'High'
    next_day = presence_next_day.iloc[0, 0].date() + pd.Timedelta(days=2)
    today_info = pd.Series([presence_next_day.iloc[0, 0].date(), str(initial_next)[7:], initial_next_in_range, str(duration_next)[7:], duration_next_in_range],
                           index=['Date', 'First time', 'First time range', 'Time spent', 'Time spent range'],
                           name=ind)
    day_to_day = day_to_day.append(today_info)
    #print(day_to_day)
    ind += 1

#=============================================================================================================
#Save file
file_date = next_day - pd.Timedelta(days=2)
file_date = datetime.strftime(file_date, '%Y-%m-%d')
day_to_day.to_csv(f'kitchen_data_{file_date}.csv')

#=============================================================================================================
#Send an email with the time we enter the kitchen for the first time and the time we spent in the kitchen from the 24h data analysis
#Set up some variables to enter in the email
str_initial_time = day_to_day['First time'].iloc[-1]
str_initial_day = day_to_day['Date'].iloc[-1]
str_duration_time = day_to_day['Time spent'].iloc[-1]

import smtplib, ssl

smtp_server = 'smtp.gmail.com'
port = 465
sender = 'adeletest231@gmail.com'
password = input('Enter your password here: ')


#We need to know who we are going to send the email to & the message
receiver = "bonnemaison.mathilde@gmail.com"
#message is the content of the email.
#Note: w/o From, to and  the format method, the receiver is bcc and the message is not directly sent to the receiver
message_entry = """\
From:{}
To:{}
Subject: First entry & time spent in kitchen on {}
Hello,

On {}, we entered the kitchen for the first time at {}, which is {} compared to the most recent history.
On that day, we were in the kitchen for {} total, which is {} compared to the most recent history.

Adelego Team
""".format(sender,receiver, str_initial_day, str_initial_day, str_initial_time, day_to_day['First time range'].iloc[-1].lower(), str_duration_time, day_to_day['Time spent range'].iloc[-1].lower())

#To get the encryption context:
context = ssl.create_default_context()

#if (day_to_day['First time range'].iloc[-1] != 'Normal') | (day_to_day['Time spent range'].iloc[-1] != 'Normal'):
with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
    server.login(sender, password)
    #send email here
    server.sendmail(sender, receiver, message_entry)
