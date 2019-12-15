#!/usr/bin/env python
# coding: utf-8

# # Data Visualization of Collage Majors Earnings
# 
# In this project I'll be demonstrating my learning of `plyplot` and `matplotlib`.
# 
# In this project we will be exploring dataset on the job outcomes of students who graduated from collage between `2010 to 2012`. Ideally we will be looking at what we can uncover from dataset using visualizations. 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

recent_grads = pd.read_csv('recent-grads.csv')


# In[2]:


recent_grads.iloc[0]


# In[3]:


recent_grads.head()


# In[4]:


recent_grads.tail()


# In[5]:


recent_grads.describe()


#  we can see that we need to do some clean up as `Total, Men , Women, ShareWomen` has different total rows than others

# In[9]:


recent_grads = recent_grads.dropna()


# In[8]:


recent_grads.describe()


# # Let's Plot and Scatter with Pandas

# In[10]:


recent_grads.plot(x='Sample_size', y='Median', kind='scatter')


# In[11]:


recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter')


# In[12]:


recent_grads.plot(x='Full_time', y='Median', kind='scatter')


# In[13]:


recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter')


# In[14]:


recent_grads.plot(x='Men', y='Median', kind='scatter')


# In[15]:


recent_grads.plot(x='Women', y='Median', kind='scatter')


# In[19]:


recent_grads.plot(x='Major_code', y='Median', kind='scatter')


# # Histogram with Pandas 

# In[20]:


cols = ["Sample_size", "Median", "Employed", "Full_time", "ShareWomen", "Unemployment_rate", "Men", "Women"]

fig = plt.figure(figsize=(5,12))
for r in range(1,5):
    ax = fig.add_subplot(4,1,r)
    ax = recent_grads[cols[r]].plot(kind='hist', rot=40)


# In[21]:


cols = ["Sample_size", "Median", "Employed", "Full_time", "ShareWomen", "Unemployment_rate", "Men", "Women"]

fig = plt.figure(figsize=(5,12))
for r in range(4,8):
    ax = fig.add_subplot(4,1,r-3)
    ax = recent_grads[cols[r]].plot(kind='hist', rot=40)


# # Scatter Matrix Plot with Pandas

# In[22]:


from pandas.plotting import scatter_matrix
scatter_matrix(recent_grads[['Sample_size', 'Median']], figsize=(6,6))


# In[23]:


scatter_matrix(recent_grads[['Sample_size', 'Median', 'Unemployment_rate']], figsize=(10,10))


# # Bar Plots on Pandas

# In[25]:


recent_grads[:10].plot.bar(x='Major', y='ShareWomen', legend=False)
recent_grads[163:].plot.bar(x='Major', y='ShareWomen', legend=False)

