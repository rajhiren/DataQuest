## 1. Introducing Data Cleaning ##

# Read the text on the left, and then scroll to the bottom
# to find the instructions for the coding exercise

# Write your answer to the instructions below -- the list of
# lists is stored using the variable name `moma`
num_rows = len(moma)
print(num_rows)

## 2. Reading our MoMA Data Set ##

# import the reader function from the csv module
from csv import reader

# use the python built-in function open()
# to open the children.csv file
opened_file = open('artworks.csv')

# use csv.reader() to parse the data from
# the opened file
read_file = reader(opened_file)

# use list() to convert the read file
# into a list of lists format
moma = list(read_file)

# remove the first row of the data, which
# contains the column names
moma = moma[1:]

# Write your code here

## 3. Replacing Substrings with the replace Method ##

age1 = "I am thirty-one years old"
age2 = age1.replace('one','two')

## 4. Cleaning the Nationality and Gender Columns ##

# Variables you create in previous screens
# are available to you, so you don't need
# to read the CSV again
def remove_brackets(value):
    value = value.replace('(','')
    value = value.replace(')','')
    
    return value

for row in moma:
    # nationality = row[2]
    # nationality = nationality.replace('(','')
    # nationality = nationality.replace(')','')
    row[2] = remove_brackets(row[2])
    row[5] = remove_brackets(row[5])

## 5. String Capitalization ##

def convert_title_case(value,index):
    value = value.title()
    
    if not value and index == 5:
        value = "Gender Unknown/Other"
    elif not value and index == 2:
        value = "Nationality Unknown"
    
    return value

for row in moma:
    row[5] = convert_title_case(row[5],5)
    row[2] = convert_title_case(row[2],2)

## 6. Errors During Data Cleaning ##

def clean_and_convert(date):
    # check that we don't have an empty string
    if date != "":
        # move the rest of the function inside
        # the if statement
        date = date.replace("(", "")
        date = date.replace(")", "")
        date = int(date)
    return date
for row in moma:
    row[3] = clean_and_convert(row[3])
    row[4] = clean_and_convert(row[4])
    

## 7. Parsing Numbers from Complex Strings, Part One ##

test_data = ["1912", "1929", "1913-1923",
             "(1951)", "1994", "1934",
             "c. 1915", "1995", "c. 1912",
             "(1988)", "2002", "1957-1959",
             "c. 1955.", "c. 1970's", 
             "C. 1990-1999"]

bad_chars = ["(",")","c","C",".","s","'", " "]

def strip_characters(string):
    for char in bad_chars:
        string = string.replace(char,'')
    return string

stripped_test_data = []
for string in test_data:
    stripped_test_data.append(strip_characters(string))

## 8. Parsing Numbers from Complex Strings, Part Two ##

test_data = ["1912", "1929", "1913-1923",
             "(1951)", "1994", "1934",
             "c. 1915", "1995", "c. 1912",
             "(1988)", "2002", "1957-1959",
             "c. 1955.", "c. 1970's", 
             "C. 1990-1999"]

bad_chars = ["(",")","c","C",".","s","'", " "]

def strip_characters(string):
    for char in bad_chars:
        string = string.replace(char,"")
    return string

stripped_test_data = ['1912', '1929', '1913-1923',
                      '1951', '1994', '1934',
                      '1915', '1995', '1912',
                      '1988', '2002', '1957-1959',
                      '1955', '1970', '1990-1999']

def process_date(date):
    if '-' in date:
        split_date = date.split("-")
        date_one = split_date[0]
        date_two = split_date[1]       
        date = (int(date_one) + int(date_two)) / 2
        date = round(date)
    else:
        date = int(date)
                
    return date

processed_test_data = []

for string in stripped_test_data:
    processed_test_data.append(process_date(string))

for row in moma:
    row[6] = strip_characters(row[6])
    row[6] = process_date(row[6])
    