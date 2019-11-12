#!/usr/bin/env python
# coding: utf-8

# # CIA World Factbook Analysis

# In[7]:


import sqlite3
import pandas as pd 

conn = sqlite3.connect('factbook.db')

def run_query(query, conn = conn):
    return pd.read_sql_query(query, conn)

query_1 = "SELECT * FROM sqlite_master WHERE type='table';"
run_query(query_1)


# In[4]:


query_2 = "SELECT * FROM facts LIMIT 5;"
run_query(query_2)


# # Summary of Population and Growth

# In[9]:


query_3 = '''select min(population) min_pop, max(population) max_pop, 
min(population_growth) min_pop_grwth, max(population_growth) max_pop_grwth 
from facts'''
run_query(query_3)


# # Lets deep dive in 

# In[12]:


query_4  = '''
select * From facts where population == (select min(population) from facts)
'''
run_query(query_4)


# In[13]:


query_5 = '''
select * from facts where population == (select max(population) from facts)
'''
run_query(query_5)


# # Histograms of World

# In[16]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib inline')

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

query_6 = '''
select population, population_growth, birth_rate, death_rate
from facts
where population != (select max(population) from facts)
and population != (select min(population) from facts);
'''
pd.read_sql_query(query_6, conn).hist(ax=ax)


# # Top 20 Highly Densed Countries

# In[18]:


query_7 = '''
select name as 'Country', cast(population as float)/cast(area as float) density from facts order by density desc limit 20
'''
run_query(query_7)


# # Histogram for population Density

# In[23]:


fig = plt.figure(figsize=(10,10))
ax_1 = fig.add_subplot(111)

query_8 = '''
select name, cast(population as float)/cast(area as float) density from facts order by density desc
'''

pd.read_sql_query(query_8, conn).hist(ax=ax_1)

