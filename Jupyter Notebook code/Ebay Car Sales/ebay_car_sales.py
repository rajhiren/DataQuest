#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning and Analysis of Use Car Listing on eBay Kleinanzeigen
# 
# We will be working on dataset of eBay Kleinanzeigen of used cars.
# The dataset was originally scraped and uploaded to Kaggle. We've made a few modifications from the original dataset that was uploaded to Kaggle:
# 
# The data dictionary provided with data is as follows:
# 
# * dateCrawled - When this ad was first crawled. All field-values are taken from this date.
# * name - Name of the car.
# * seller - Whether the seller is private or a dealer.
# * offerType - The type of listing
# * price - The price on the ad to sell the car.
# * abtest - Whether the listing is included in an A/B test.
# * vehicleType - The vehicle Type.
# * yearOfRegistration - The year in which which year the car was first registered.
# * gearbox - The transmission type.
# * powerPS - The power of the car in PS.
# * model - The car model name.
# * kilometer - How many kilometers the car has driven.
# * monthOfRegistration - The month in which which year the car was first registered.
# * fuelType - What type of fuel the car uses.
# * brand - The brand of the car.
# * notRepairedDamage - If the car has a damage which is not yet repaired.
# * dateCreated - The date on which the eBay listing was created.
# * nrOfPictures - The number of pictures in the ad.
# * postalCode - The postal code for the location of the vehicle.
# * lastSeenOnline - When the crawler saw this ad last online.
# 
# The aim of this project is to clean the data and analyze the included used car listings.

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


autos = pd.read_csv("autos.csv", encoding="Latin-1")
autos.info()
autos.head()


# Our dataset contains 20 columns, most of which are stored as strings. There are a few columns with null values, but no columns have more than ~20% null values. There are some columns that contain dates stored as strings.
# 
# We'll have to clean the column names to make the data easier to work with.

# In[4]:


# lets have detailed look at column names
autos.columns


# In[5]:


autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'num_pictures', 'postal_code',
       'last_seen']


# We'll make a few changes here:
# 
# * Change the columns from camelcase to snakecase.
# * Change a few wordings to more accurately describe the columns.

# In[6]:


# lets check top 5 rows 
autos.head()


# # Time to explore Data 
# 
# We will have exolore the data and try to narrow it down what can we do to clean data

# In[7]:


autos.describe(include='all')


# From above we can see that we find few columns that can be dropped.
# * offer_type
# * seller
# * num_pictures
# 
# however before we do that lets examine first to absolutely make sure what's in these columns

# In[8]:


autos["seller"].describe()


# In[9]:


autos["offer_type"].describe()


# In[10]:


autos["num_pictures"].describe()


# Now we are absolutely sure and have data to back up that these columns doesn't add any value to our project and we should drop them from dataset

# In[11]:


autos = autos.drop(["num_pictures", "seller", "offer_type"], axis=1)


# On the closer look We should also explore following columns as well
# * ab_test
# * gearbox
# * unrepaired_damage

# In[12]:


autos["ab_test"].describe()


# In[13]:


autos["gearbox"].value_counts()


# In[14]:


autos["unrepaired_damage"].value_counts()


# We can conclude we need those columns as they hold key piece of information, so we will keep them

# We have also suspect that `price` and `odometer` column values are stored as text, so lets confirm if that is the case or not ? 

# In[15]:


autos["price"].describe()


# In[16]:


autos["odometer"].describe()


# So, our suspision is spot on. Both column values are stored as text.
# 
# We will now remove any `non-numeric` characters from it and convert column to a `numeric type`
# While doing so we will also rename `odometer` column to `odometer_km`

# In[17]:


autos["price"] = (autos["price"]
                          .str.replace("$","")
                          .str.replace(",","")
                          .astype(int)
                          )
autos["price"].head()


# In[18]:


autos["odometer"] = (autos["odometer"]
                                .str.replace("km","") 
                                .str.replace(",","")
                                .astype(int) 
                                )
autos.rename({"odometer":"odometer_km"}, axis=1 , inplace=True)
autos["odometer_km"].head()


# # Explore further and Data Cleaning 

# In[19]:


autos["odometer_km"].value_counts()


# We can certainly assume that all fields are rounded and most of the cars had high odometer reading

# In[20]:


print(autos["odometer_km"].describe())


# In[21]:


print(autos["odometer_km"].unique().shape)


# As we can see there are 13 unique value for `odometer_km`

# In[22]:


print(autos["price"].describe())
print(autos["price"].value_counts())
print(autos["price"].unique().shape)


# Wow there is lot going on here. Here is our observation
# * there are 2357 unique prices of the cars 
# * looks like website only allowed rounded value
# * there are 1421 cars given away for free which is less than 2% of dataset
# * maximum car price is 10 times more than most expesive car exists in the world. A staggering 100 Million and most expensive car in world costs around 12.5 Million. (go figure :) )
# 
# Lets have closer look at maximum prices 
# 

# In[23]:


autos["price"].value_counts().sort_index(ascending=False).head(20)


# In[24]:


autos["price"].value_counts().sort_index(ascending=True).head(20)


# In[25]:


autos["price"].value_counts().between(0,3260100)


# So we will keep our range from `$1` to `$3,260,100` as it was most expesive used car ever sold on ebay (ref https://www.ebay.com/motors/blog/most-expensive-cars-sold-ebay/)

# In[26]:


autos = autos[autos["price"].between(1,3260100)]
autos["price"].describe()


# # Date Exploration
# 
# There are total 5 columns that should represent date value. Some of them created by crawler and some are from website.
# 
# * date_crawled
# * registration_month
# * registration_year
# * ad_created
# * last_seen
# 
# Right now, the `date_crawled`, `last_seen`, and `ad_created` columns are all identified as string values by pandas. 
# 
# lets explore them and see what we discover

# In[27]:


autos[['date_crawled','ad_created','last_seen']][0:5]


# In[28]:


(autos["date_crawled"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )


# In[29]:


(autos["date_crawled"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_values()
        )


# We can see that site has been crawed for month of `March` and `April` and about roughly same time.

# In[34]:


(autos["last_seen"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )


# In[35]:


autos["registration_year"].describe()


# Well, obviously we can see that two values are not possible as `min = 1000` and `max = 9999`. Car was not invented in year 1000 and we are in `2019` so year `9999` doesn't make any sense.

# In[46]:


autos = autos[autos["registration_year"].between(1990,2016)]
autos["registration_year"].value_counts(normalize=True)


# # Explore the Brands

# In[50]:


autos["brand"].value_counts(normalize=True)


# We can see that almost 50% of car sold was produced by German car makers

# In[51]:


brand_counts = autos["brand"].value_counts(normalize=True)
common_brands = brand_counts[brand_counts > .05].index
print(common_brands)


# In[52]:


brand_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    brand_mean_prices[brand] = int(mean_price)

brand_mean_prices


# so we can see why `Volkswagen` is very popular because it is falls in mid range car price. We can see `Audi, BMW, and Mercedes Benz` is high value cars as `open and ford` is at the lower end of price range.

# # What about Mileage ? 

# In[53]:


bmp_series = pd.Series(brand_mean_prices)
pd.DataFrame(bmp_series, columns=["mean_price"])


# In[54]:


brand_mean_mileage = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()
    brand_mean_mileage[brand] = int(mean_mileage)

mean_mileage = pd.Series(brand_mean_mileage).sort_values(ascending=False)
mean_prices = pd.Series(brand_mean_prices).sort_values(ascending=False)

brand_info = pd.DataFrame(mean_mileage,columns=['mean_mileage'])
brand_info


# In[55]:


brand_info["mean_price"] = mean_prices
brand_info

