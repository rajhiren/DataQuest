#!/usr/bin/env python
# coding: utf-8

# # Data Analysis for Hacker News Posts
# 
# In this notebook we will be analysing the data to determing two things
# 
# * Do Ask HN or Show HN receive more comments on average?
# * Do posts created at a certain time receive more comments on average?

# In[2]:


import csv 

file = open("hacker_news.csv")
hn = list(csv.reader(file))

print(hn[:5])


# In[3]:


# removing header and displaying first 5 rows of data only
headers = hn[0]
hn = hn[1:]
print(headers)
print(hn[:5])


# In[4]:


# lets create new lists to hold data
ask_posts = []
show_posts = []
other_posts = []

# looping through `hn` to get titles
for row in hn:
    title = row[1]
    title = title.lower()
    if title.startswith('ask hn'):
        ask_posts.append(row)
    elif title.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
      
    
print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))


# # Lets identify if ask posts or show posts receive more comments on average 

# In[5]:


# average of comments on `Ask HN`
total_ask_comments = 0

for row in ask_posts:
    total_ask_comments += int(row[4])
    

avg_ask_comments = total_ask_comments / len(ask_posts)
print(avg_ask_comments)


# In[6]:


# average of comments on `Show HN`
total_show_comments = 0

for row in show_posts:
    total_show_comments += int(row[4])
    

avg_show_comments = total_show_comments / len(show_posts)
print(avg_show_comments)


# # Finding the Amount of Ask Posts and Comments by Hour Created

# In[7]:


import datetime as dt

result_list = []

for post in ask_posts:
    result_list.append(
        [post[6], int(post[4])]
    )

comments_by_hour = {}
counts_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

for each_row in result_list:
    date = each_row[0]
    comment = each_row[1]
    time = dt.datetime.strptime(date, date_format).strftime("%H")
    if time in counts_by_hour:
        comments_by_hour[time] += comment
        counts_by_hour[time] += 1
    else:
        comments_by_hour[time] = comment
        counts_by_hour[time] = 1

comments_by_hour


# In[8]:


# Calculate the average amount of comments `Ask HN` posts created at each hour of the day receive.
avg_by_hour = []

for hr in comments_by_hour:
    avg_by_hour.append([hr, comments_by_hour[hr] / counts_by_hour[hr]])

avg_by_hour


# In[9]:


swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
    
print(swap_avg_by_hour)

sorted_swap = sorted(swap_avg_by_hour, reverse=True)

sorted_swap


# In[10]:


# Sort the values and print the the 5 hours with the highest average comments.

print("Top 5 Hours for 'Ask HN' Comments")
for avg, hr in sorted_swap[:5]:
    print(
        "{}: {:.2f} average comments per post".format(
            dt.datetime.strptime(hr, "%H").strftime("%H:%M"),avg
        )
    )


# In[ ]:




