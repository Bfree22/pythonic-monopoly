#!/usr/bin/env python
# coding: utf-8

# # Rental Analysis
# ________________________________

# ### Housing Units Per Year
# 
# #### In this section, you will calculate the number of housing units per year and visualize the results as a bar chart using the Pandas plot function.
# 

# In[ ]:





# In[1]:


# imports

import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

import warnings
warnings.filterwarnings('ignore')


# In[2]:


load_dotenv()


# In[3]:


# Read the Mapbox API key

mapbox_api = os.getenv("MAPBOX_API_KEY")
type(mapbox_api)


# In[4]:


# Read the census data into a Pandas DataFrame

census=pd.read_csv("Census_data.csv")
coordinates=pd.read_csv("neighborhood_coordinates.csv")


# In[5]:


census.head()


# In[6]:


# Calculate the mean number of housing units per year (hint: use groupby) 

groupby=census.groupby("year")["housing_units"].mean()
groupby


# In[7]:


# Use the Pandas plot function to plot the average housing units per year.

groupby.plot(kind="bar", title="Housing Units Per Year", ylim=(365000,390000))


# In[8]:


groupby


# In[ ]:





# ## Average Housing Costs in San Francisco Per Year
# 
# #### In this section, you will calculate the average monthly rent and the average price per square foot for each year. An investor may wish to better understand the sales price of the rental property over time. For example, a customer will want to know if they should expect an increase or decrease in the property value over time so they can determine how long to hold the rental property.  Plot the results as two line charts.
# 

# In[ ]:





# In[9]:


# Calculate the average sale price per square foot and average gross rent

rent_per_year=census.groupby(["year"])["gross_rent"].mean()
rent_per_year=pd.DataFrame(rent_per_year)
rent_per_year


# In[10]:


price_per_sqr_foot=census.groupby(["year"])["sale_price_sqr_foot"].mean()
price_per_sqr_foot=pd.DataFrame(price_per_sqr_foot)
price_per_sqr_foot


# In[11]:


new_df=pd.concat([rent_per_year,price_per_sqr_foot], axis =1)
new_df


# In[12]:


# Create two line charts, one to plot the average sale price per square foot and another for average montly rent

# Line chart for average montly rent

rent_per_year.plot(kind="line", title="Average Gross Rent Per Year").set_ylabel("Average Gross Rent")


# In[13]:


# Line chart for average sale price per square foot

price_per_sqr_foot.plot(kind="line", title="Average Price Per SqFt by Year").set_ylabel("Price Per SqFt")


# ## Average Prices by Neighborhood
# 
# 
# #### In this section, you will use hvplot to create two interactive visulizations of average prices with a dropdown selector for the neighborhood. The first visualization will be a line plot showing the trend of average price per square foot over time for each neighborhood.  The second will be a line plot showing the trend of average montly rent over time for each neighborhood.

# In[14]:


# Group by year and neighborhood and then create a new dataframe of the mean values

census.head()


# In[15]:


neighborhood_df=census.groupby(["year","neighborhood"]).mean()
neighborhood_df.head()


# In[16]:


# Use hvplot to create an interactive line chart of the average price per sq ft.

neighborhood_df.hvplot.line(x="year",y="sale_price_sqr_foot", groupby="neighborhood", ylabel="Average Sale Price Per SqFt")


# In[17]:


# Use hvplot to create an interactive line chart of the average monthly rent.

neighborhood_df.hvplot.line(x="year",y="gross_rent", groupby="neighborhood", ylabel="Average Gross Rent Per Year", color="green")


# In[ ]:





# In[ ]:





# # The Top 10 Most Expensive Neighborhoods

# #### In this section, you will need to calculate the mean sale price per square foot for each neighborhood and then sort the values to obtain the top 10 most expensive neighborhoods on average. Plot the results as a bar chart

# In[18]:


grouped_df=neighborhood_df.groupby(["neighborhood"]).mean()
grouped_df=grouped_df.reset_index()
grouped_df


# In[19]:


top10_df_plot=grouped_df.sort_values("sale_price_sqr_foot",ascending=False).head(10)
top10_df_plot


# In[20]:


# Plot the results as a bar chart.

top10_df_plot.head(10).plot(kind="bar",y="sale_price_sqr_foot")


# In[ ]:





# # Comparing Cost to Purchase Versus Rental Income

# #### In this section, you will use hvplot to create an interactive visualization with a dropdown selector for the neighborhood. This visualization will feature a side-by-side comparison of average price per square foot versus average monthly rent by year.
# 

# In[21]:


neighborhood_df.head(10)


# In[ ]:





# In[ ]:





# # Neighborhood Map
# ___________________________________________
# 
# ### In this section, you will read in neighborhoods location data and build an interactive map with the average house value per neighborhood. Use a scatter_mapbox from Plotly express to create the visualization.

# ### Load Location Data
# _______________________________

# In[22]:


# Load neighborhoods coordinates data

coord=pd.read_csv("neighborhood_coordinates.csv")
coord.columns=["neighborhood","Lat","Lon"]
coord.head()


# ### Data Preparation

# #### 1. Calculate the mean values for each neighborhood.
# 
# #### 2. Join the average values with the neighborhood locations.

# In[23]:


top10_df_plot=top10_df_plot.reset_index()
top10_df_plot


# In[24]:


joined_df= pd.concat([coord,grouped_df], axis="columns",join='outer')
joined_df.columns


# In[25]:


joined_df.columns = ['neighborhood', 'Lat', 'Lon', 'NaN', 'sale_price_sqr_foot',
       'housing_units', 'gross_rent']


# In[26]:


joined_df.drop("NaN",axis=1, inplace=True)


# In[27]:


# Join the average values with the neighborhood locations

joined_df.head()


# In[ ]:





# # Mapbox Visualization
# ____________________________________________
# 
# #### Plot the average values per neighborhood using a Plotly express scatter_mapbox visualization.

# In[28]:


# Set the mapbox access token

mapbox_api=os.getenv("MAPBOX_API_KEY")
px.set_mapbox_access_token(mapbox_api)
type(mapbox_api)


# In[29]:


# Create a scatter mapbox to analyze neighborhood info

px.scatter_mapbox(joined_df,
                 lat="Lat",
                 lon="Lon",
                 size="sale_price_sqr_foot",
                 color="gross_rent",
                 title="Average Values Per Neighborhood In San Francisco")


# In[ ]:





# #  Cost Analysis
# ________________________________________
# 
# #### In this section, you will use Plotly express to create visualizations that investors can use to interactively filter and explore various factors related to the house value of the San Francisco's neighborhoods. 

# ### Create a DataFrame showing the most expensive neighborhoods in San Francisco by year

# In[30]:


# Parallel Coordinates Plot

parallel_plot=px.parallel_coordinates(top10_df_plot, color="sale_price_sqr_foot")
parallel_plot


# In[31]:


# Create Parallel Categories Plot

category_plot=px.parallel_categories(
    top10_df_plot,
    dimensions=["neighborhood","sale_price_sqr_foot","housing_units","gross_rent"],
    color="sale_price_sqr_foot")
category_plot


# In[ ]:




