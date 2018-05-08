
from selenium import webdriver
import pandas as pd
import datetime
import os
import logging
import sqlite3 as lite 

def run_job(my_path):
    logging.basicConfig(filename=my_path+'\\records.log',level=logging.INFO)
    logger = logging.getLogger(__name__)
   
    try:

        # Extract information from the website
        url = 'https://remit.bp.com/'
        driver = webdriver.Firefox()
        driver.get(url)
        
        head = driver.find_element_by_xpath('//table[@class="data data--head"]')
        head = head.text.replace('/\n','/').split('\n')
        
        data = pd.DataFrame(columns=head)
        
        for i in range(len(head)):
            temp = driver.find_elements_by_xpath('//td[@data-label="'+head[i].replace(' /',' /<br />')+'"]')
            data[head[i]] = [x.text if x.text!='' else None for x in temp ]
        
        # Extract information in the hidden tags
        buttons = driver.find_elements_by_tag_name('button')
        for button in buttons:
            button.click() # Expands all tabs
                    
        temp = pd.DataFrame(columns=head)
        for i in range(len(head)):
            hidden = driver.find_elements_by_xpath('//tr[@class="revision hidden"]//td[@data-label="'+head[i].replace(' /',' /<br />')+'"]')
            if len(hidden)!=0:
                # Make sure all missing values have been replaced with None (equivalent to Null)
                temp[head[i]] = [x.text if x.text!='' else None for x in hidden]
        data = data.append(temp,ignore_index=True)
        
        ### --- All the data have been scrapped nicely --- ###
        
        # Remove the word 'view revisions' which had been extracted above
        data['Message ID'] = [data['Message ID'].iloc[i].split(' ')[0] for i in range(len(data))]
        
        # Convert data types 
        data['Publication date/time'] = pd.to_datetime(data['Publication date/time'])
        data['Event Start'] = pd.to_datetime(data['Event Start'])
        data['Event Stop'] = pd.to_datetime(data['Event Stop'])
        
        data['Unavailable Capacity'] = pd.to_numeric(data['Unavailable Capacity'])
        data['Available Capacity'] = pd.to_numeric(data['Available Capacity'])
        data['Installed Capacity /Technical Capacity'] = pd.to_numeric(data['Installed Capacity /Technical Capacity'])
        
        # Make sure all missing values have been replaced with None (equivalent to Null)
        data['Message ID Num'] = [int(x) if x!=None else None for x in data['Message ID Num'] ]
        
        # Make sure there is no duplicate records that have been scrapped
        data = data.drop_duplicates()
        
        return data
    
    except Exception as e:
           logger.error('%s ; %s',str(datetime.datetime.now()),e)
           # If any error occurred, return blank dataframe
           return pd.DataFrame()

if __name__ == "__main__":
    
    my_path = os.getcwd()
    data = run_job(my_path)
    
    # Store data into database
    db_filename = 'bp_remit.db'
    con = lite.connect(db_filename) # build connection
    
    db_table = 'bp_remit'
    cur = con.cursor()
    
    # Create a new table if the table is not exist in the database
    ## The created table will only have one column name 'index'
    cur.execute("create table if not exists %s ('index');"%(db_table))
    
    ## Use any of the column names in newly scrapped data as benchmark (as if 
    ## the table was newly created by command above, it will only contain a single
    ## column). Here I use 'Publication date/time' as benchmark.
    old_data = pd.read_sql_query("SELECT * from %s"%(db_table), con,index_col='index')
    if 'Publication date/time' in old_data.columns:
        old_data['Publication date/time'] = pd.to_datetime(old_data['Publication date/time'])
        old_data['Event Start'] = pd.to_datetime(old_data['Event Start'])
        old_data['Event Stop'] = pd.to_datetime(old_data['Event Stop'])

    # Combining existing table from database with newly scrapped data
    concat_data = data.append(old_data,ignore_index=True)
    
    # Remove duplicated records in the combining dataframe
    concat_data = concat_data.drop_duplicates()
    
    concat_data.to_sql(db_table, con, flavor='sqlite',
                schema=None, if_exists='replace', index=True,
                index_label=None, chunksize=None, dtype=None)

    con.close()



