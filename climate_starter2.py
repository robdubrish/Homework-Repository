


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[4]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[5]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[6]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Climate Analysis

# In[45]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results
mostRecent = session.query(Measurement.date).order_by(Measurement.date.desc()).all()

# Calculate the date 1 year ago from the last data point in the database
aYearAgo = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
prcpData = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > aYearAgo).order_by(Measurement.date.desc()).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(prcpData)

# Sort the dataframe by date
df.set_index(df['date'])
# Use Pandas Plotting with Matplotlib to plot the data
df.plot(x="date", y="prcp")


# ![precipitation](Images/precipitation.png)

# In[46]:


# Use Pandas to calcualte the summary statistics for the precipitation data
df.describe(include='all')


# ![describe](Images/describe.png)

# In[90]:


# Design a query to show how many stations are available in this dataset?
# print(len())
Sta_ind = session.query(Station.station).order_by(Station.station.desc()).all()
print(len(Sta_ind))


# In[146]:


# What are the most active stations? (i.e. what stations have the most rows)?
ActSta = session.query(Measurement.station, func.count(Measurement.station).label('count')).group_by(Measurement.station).order_by('count DESC').first()
print(ActSta)
# List the stations and the counts in descending order.
AllSta = session.query(Measurement.station, func.count(Measurement.station).label('count')).group_by(Measurement.station).order_by('count DESC').all()
print(AllSta)


# In[154]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
lowest_sta = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').order_by(Measurement.tobs.asc()).first()
# highest temperature recorded, and average temperature most active station?
highest_sta = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').order_by(Measurement.tobs.desc()).first()
avg_sta = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()


# In[160]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
Temp_station = session.query(Measurement.tobs).filter(Measurement.date > aYearAgo, Measurement.station == 'USC00519281').all()
df = pd.DataFrame(Temp_station)
df.plot(kind='hist', bins=12)
plt.show()
