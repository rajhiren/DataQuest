## 3. Connecting to the Database ##

import sqlite3

conn = sqlite3.connect('jobs.db')


## 6. Creating a Cursor and Running a Query ##

import sqlite3
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

query = "select Major from recent_grads;"
cursor.execute(query)
majors = cursor.fetchall()
print(majors[0:2])

## 8. Fetching a Specific Number of Results ##

import sqlite3
conn = sqlite3.connect("jobs.db")
query = "select Major,Major_category from recent_grads;"

five_results = conn.execute(query).fetchmany(5)

## 9. Closing the Database Connection ##

conn = sqlite3.connect("jobs.db")
conn.close()

## 10. Practice ##

import sqlite3

conn = sqlite3.connect('jobs.db')

query = "select Major from recent_grads order by Major desc;"

reverse_alphabetical = conn.execute(query).fetchall()

conn.close()