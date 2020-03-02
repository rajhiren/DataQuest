#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning and Analysis of DETE & TAFE Employee exit surveys
# 
# We have been given the data set of exit survey from Department of Education, Training and Employment (DETE) and TAFE. 
# Our task is to clean and analysis data and try to answer following questions and insight to the stake holders
# 
# * Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
# 
# * Are younger employees resigning due to some kind of dissatisfaction? What about older employees?
# 
# ** we have been advised by stake holder that they would like to see combined results**

# In[2]:


# import libraries
import pandas as pd
import numpy as np


# In[3]:


# read csv files 
dete_survey = pd.read_csv('dete_survey.csv')
tafe_survey = pd.read_csv('tafe_survey.csv')


# In[4]:


def survey_summary(survey):
    """
        Summary of given dataframe.
        shows info() and head()
    """
    print(survey.info())
    print(survey.head())


# In[5]:


# lets check what's in dete_survey
survey_summary(dete_survey)


# In[6]:


# lets check what's in tafe_survey
survey_summary(tafe_survey)


# We have derived following observations from looking at summary of these data frames
# 
# * The dete_survey dataframe contains 'Not Stated' values that indicate values are missing, but they aren't represented as NaN.
# * Both the dete_survey and tafe_survey dataframes contain many columns that we don't need to complete our analysis.
# * Each dataframe contains many of the same columns, but the column names are different.
# * There are multiple columns/answers that indicate an employee resigned because they were dissatisfied.

# In[7]:


# simple clean of dataframe where we replace `Not Stated` with `NaN`
dete_survey = pd.read_csv('dete_survey.csv', na_values='Not Stated')

# quick glance at data
dete_survey.head()


# In[8]:


# lets drop dead weight for dete_survey
dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis=1)

# quick glance again to confirm 
# dete_survey_updated.head()
print(dete_survey_updated.columns)


# In[9]:


# lets drop dead weight for tafe_survey
tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66], axis=1)

# quick glance again to confirm 
# tafe_survey_updated.head()
print(tafe_survey_updated.columns)


# # Rename Columns
# 
# We are going to standardise the columns names so we can eventually use them when we combined dataset

# In[10]:


# replace  space with _ and lowercase all column names
dete_survey_updated.columns = dete_survey_updated.columns.str.replace(' ', '_').str.lower()

# Check that the column names were updated correctly
dete_survey_updated.columns


# In[11]:


# Update column names to match the names in dete_survey_updated
mapping = {'Record ID': 'id', 'CESSATION YEAR': 'cease_date', 'Reason for ceasing employment': 'separationtype', 'Gender. What is your Gender?': 'gender', 'CurrentAge. Current Age': 'age',
       'Employment Type. Employment Type': 'employment_status',
       'Classification. Classification': 'position',
       'LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service',
       'LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'}
tafe_survey_updated = tafe_survey_updated.rename(mapping, axis = 1)

# Check that the specified column names were updated correctly
tafe_survey_updated.columns


# In[12]:



# Check the unique values for the separationtype column
tafe_survey_updated['separationtype'].value_counts()


# In[13]:


# Check the unique values for the separationtype column
dete_survey_updated['separationtype'].value_counts()


# In[14]:


# Update all separation types containing the word "resignation" to 'Resignation'
dete_survey_updated['separationtype'] = dete_survey_updated['separationtype'].str.split('-').str[0]

# Check the values in the separationtype column were updated correctly
dete_survey_updated['separationtype'].value_counts()


# In[15]:


# Select only the resignation separation types from each dataframe
dete_resignations = dete_survey_updated[dete_survey_updated['separationtype'] == 'Resignation'].copy()
tafe_resignations = tafe_survey_updated[tafe_survey_updated['separationtype'] == 'Resignation'].copy()


# # Data Verification
# 
# We are now going to verify the `cease_date` and `dete_start_date` to make sure it makes sense and we would not end up with wrong analysis

# In[16]:


dete_resignations['cease_date'].value_counts()


# In[17]:


# Extract the years and convert them to a float type
dete_resignations['cease_date'] = dete_resignations['cease_date'].str.split('/').str[-1]
dete_resignations['cease_date'] = dete_resignations['cease_date'].astype("float")

# Check the values again and look for outliers
dete_resignations['cease_date'].value_counts()


# In[18]:


# Check the unique values and look for outliers
dete_resignations['dete_start_date'].value_counts().sort_values()


# In[19]:


# Check the unique values
tafe_resignations['cease_date'].value_counts().sort_values()


# Below are our findings:
# 
# * The years in both dataframes don't completely align. The tafe_survey_updated dataframe contains some cease dates in 2009, but the dete_survey_updated dataframe does not. The tafe_survey_updated dataframe also contains many more cease dates in 2010 than the dete_survey_updaed dataframe. Since we aren't concerned with analyzing the results by year, we'll leave them as is.

# # Create a New Column
# 
# Since our end goal is to answer the question below, we need a column containing the length of time an employee spent in their workplace, or years of service, in both dataframes.
# 
# End goal: Are employees who have only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been at the job longer?
# The tafe_resignations dataframe already contains a "service" column, which we renamed to institute_service.
# 
# Below, we calculate the years of service in the dete_survey_updated dataframe by subtracting the dete_start_date from the cease_date and create a new column named institute_service.

# In[20]:


# Calculate the length of time an employee spent in their respective workplace and create a new column
dete_resignations['institute_service'] = dete_resignations['cease_date'] - dete_resignations['dete_start_date']

# Quick check of the result
dete_resignations['institute_service'].head()


# # Dissatisfied employee identification
# 
# Next, we'll identify any employees who resigned because they were dissatisfied. Below are the columns we'll use to categorize employees as "dissatisfied" from each dataframe:
# 
# 1. tafe_survey_updated:
#     * Contributing Factors. Dissatisfaction
#     * Contributing Factors. Job Dissatisfaction
# 2. dafe_survey_updated:
#     * job_dissatisfaction
#     * dissatisfaction_with_the_department
#     * physical_work_environment
#     * lack_of_recognition
#     * lack_of_job_security
#     * work_location
#     * employment_conditions
#     * work_life_balance
#     * workload
#     
# If the employee indicated any of the factors above caused them to resign, we'll mark them as dissatisfied in a new column. After our changes, the new dissatisfied column will contain just the following values:
# 
# * True: indicates a person resigned because they were dissatisfied in some way
# * False: indicates a person resigned because of a reason other than dissatisfaction with the job
# * NaN: indicates the value is missing

# In[21]:


# Check the unique values
tafe_resignations['Contributing Factors. Dissatisfaction'].value_counts()


# In[22]:


# Check the unique values
tafe_resignations['Contributing Factors. Job Dissatisfaction'].value_counts()


# In[23]:


# Update the values in the contributing factors columns to be either True, False, or NaN
def update_vals(x):
    if x == '-':
        return False
    elif pd.isnull(x):
        return np.nan
    else:
        return True
tafe_resignations['dissatisfied'] = tafe_resignations[['Contributing Factors. Dissatisfaction', 'Contributing Factors. Job Dissatisfaction']].applymap(update_vals).any(1, skipna=False)
tafe_resignations_up = tafe_resignations.copy()

# Check the unique values after the updates
tafe_resignations_up['dissatisfied'].value_counts(dropna=False)


# In[24]:


# Update the values in columns related to dissatisfaction to be either True, False, or NaN
dete_resignations['dissatisfied'] = dete_resignations[['job_dissatisfaction',
       'dissatisfaction_with_the_department', 'physical_work_environment',
       'lack_of_recognition', 'lack_of_job_security', 'work_location',
       'employment_conditions', 'work_life_balance',
       'workload']].any(1, skipna=False)
dete_resignations_up = dete_resignations.copy()
dete_resignations_up['dissatisfied'].value_counts(dropna=False)


# In[25]:


# Add an institute column
dete_resignations_up['institute'] = 'DETE'
tafe_resignations_up['institute'] = 'TAFE'


# In[26]:


# Combine the dataframes
combined = pd.concat([dete_resignations_up, tafe_resignations_up], ignore_index=True)

# Verify the number of non null values in each column
combined.notnull().sum().sort_values()


# In[27]:


# Drop columns with less than 500 non null values
combined_updated = combined.dropna(thresh = 500, axis =1).copy()


# In[28]:


# Check the unique values
combined_updated['institute_service'].value_counts(dropna=False)


# In[29]:


# Extract the years of service and convert the type to float
combined_updated['institute_service_up'] = combined_updated['institute_service'].astype('str').str.extract(r'(\d+)')
combined_updated['institute_service_up'] = combined_updated['institute_service_up'].astype('float')

# Check the years extracted are correct
combined_updated['institute_service_up'].value_counts()


# In[30]:


# Convert years of service to categories
def transform_service(val):
    if val >= 11:
        return "Veteran"
    elif 7 <= val < 11:
        return "Established"
    elif 3 <= val < 7:
        return "Experienced"
    elif pd.isnull(val):
        return np.nan
    else:
        return "New"
combined_updated['service_cat'] = combined_updated['institute_service_up'].apply(transform_service)

# Quick check of the update
combined_updated['service_cat'].value_counts()


# In[31]:


# Verify the unique values
combined_updated['dissatisfied'].value_counts(dropna=False)


# In[32]:


# Replace missing values with the most frequent value, False
combined_updated['dissatisfied'] = combined_updated['dissatisfied'].fillna(False)


# In[33]:


dis_pct = combined_updated.pivot_table(index='service_cat', values='dissatisfied')

# Plot the results
get_ipython().magic('matplotlib inline')
dis_pct.plot(kind='bar', rot=30)

