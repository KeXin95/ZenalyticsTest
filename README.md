# Zenalytics Test
*by [Ke Xin](https://github.com/KeXin95)*

*Date last updated: 8th May 2018 </i>*
___

This project is created as part of interview process in application to **Graduate Analyst position** at [Zenalytics](http://www.zenalytics.org/). It will extract information from the table on https://remit.bp.com/ and store it into a database.

## Task given:
### Python coding exercise - Data
Design a client that visits the website https://remit.bp.com/ to extract data

Basic Requirements:
 - You are required to extract information from the table and store it into a database
 - The data is to be stored in a SQL database (eg. Sqlite) and is meant to be updated everyday. (hint below)
 - There should not be duplicates in the database.
 - Data type, such as datetime, float, and integer, must be properly defined.
 - All datetime fields have to be adjusted for timezone.
 - If the time of some entries in a datetime field is ‘unknown’, set it to null
 - All nan values and '-' should be converted to null.
 - Include documentation for your code
 - Keep the code as DRY and readable as possible.
 
 - Additional requirements (Bonus):
    - The client should allow for exception handling and retry in case of failure.
    - Include tests for your functions where applicable.
    - The column ‘MessageID’ may contain links that provides more information. Include these information in the same database. (Hint: you may need to use other HTTP methods)

## My Solution:
### Requirements to run this program
Please ensure you have the following packages installed:
  - selenium
  - pandas
  - sqlite3
  - os
  - datetime
  - logging
  
\* I am using firefox webdriver in this project, hence, please ensure that you have **geckodriver.exe** file (download [here](https://github.com/mozilla/geckodriver/releases) ) in the same directory as this Python file. :)

### Rough idea on the solution
#### For scrapping data from the website:
1. First of all, notice that **table header** and **table contents** are being stored in two different table tags, one with class name  "data data--head", the other with "data data--body":

![table.png](screenshots/table.png?raw=true)

2. Secondly, each cell are being stored nicely according to attributes **data-label** with value same as header name

![table_content.png](screenshots/table_content.png?raw=true)

3. Scrape all the headers first and then use each values in headers to extract columns of each header name.

\* Note that as there are some hidden rows, I use selenium to expand all the tabs, and then scrapping out all the hidden records.

#### For storing data into sqlite:
1. I first check if the table exist in the database, create a new one if it is not. (\*Note that it is kind of inefficient as if the table existed in the database is very large!)

2. Read the table into dataframe, and then combine with the new data.

3. Stored the concatenated table into the database again and close the connection.

\* It is always nice to check if the table have stored properly. Good database viewer (for SQLite) -> [DB Browser for SQLite](http://sqlitebrowser.org/). :)

