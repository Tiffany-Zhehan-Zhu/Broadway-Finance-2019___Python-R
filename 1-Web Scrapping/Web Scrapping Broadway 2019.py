#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import requests
import urllib
import math
import copy
import pandas as pd	
import numpy as np
import datetime
from bs4 import BeautifulSoup 


# In[2]:


#####################################################################
###################### Prepare Functions ############################
#####################################################################

class html_tables(object):
    
    def __init__(self, url):
        
        self.url      = url
        self.r        = requests.get(self.url)
        self.url_soup = BeautifulSoup(self.r.text)
        
    def read(self):
        
        self.tables      = []
        self.tables_html = self.url_soup.find_all("table")
        
        # Parse each table
        for n in range(0, len(self.tables_html)):
            
            n_cols = 0
            n_rows = 0
            
            for row in self.tables_html[n].find_all("tr"):
                col_tags = row.find_all(["td", "th"])
                if len(col_tags) > 0:
                    n_rows += 1
                    if len(col_tags) > n_cols:
                        n_cols = len(col_tags)
            
            # Create dataframe
            df = pd.DataFrame(index = range(0, n_rows), columns = range(0, n_cols))
            
            # Create list to store rowspan values 
            skip_index = [0 for i in range(0, n_cols)]
            
            # Start by iterating over each row in this table...
            row_counter = 0
            for row in self.tables_html[n].find_all("tr"):
                
                # Skip row if it's blank
                if len(row.find_all(["td", "th"])) == 0:
                    next
                
                else:
                    
                    # Get all cells containing data in this row
                    columns = row.find_all(["td", "th"])
                    col_dim = []
                    row_dim = []
                    col_dim_counter = -1
                    row_dim_counter = -1
                    col_counter = -1
                    this_skip_index = copy.deepcopy(skip_index)
                    
                    for col in columns:
                        
                        # Determine cell dimensions
                        colspan = col.get("colspan")
                        if colspan is None:
                            col_dim.append(1)
                        else:
                            col_dim.append(int(colspan))
                        col_dim_counter += 1
                            
                        rowspan = col.get("rowspan")
                        if rowspan is None:
                            row_dim.append(1)
                        else:
                            row_dim.append(int(rowspan))
                        row_dim_counter += 1
                            
                        # Adjust column counter
                        if col_counter == -1:
                            col_counter = 0  
                        else:
                            col_counter = col_counter + col_dim[col_dim_counter - 1]
                            
                        while skip_index[col_counter] > 0:
                            col_counter += 1

                        # Get cell contents  
                        cell_data = col.get_text()
                        
                        # Insert data into cell
                        df.iat[row_counter, col_counter] = cell_data

                        # Record column skipping index
                        if row_dim[row_dim_counter] > 1:
                            this_skip_index[col_counter] = row_dim[row_dim_counter]
                
                # Adjust row counter 
                row_counter += 1
                
                # Adjust column skipping index
                skip_index = [i - 1 if i > 0 else i for i in this_skip_index]

            # Append dataframe to list of tables
            self.tables.append(df)
        
        return(self.tables)


# In[ ]:


#####################################################################
################# Scrap Information from Webpages ###################
#####################################################################

# Select all the Sundays of 2019
def allsundays(year):
    return pd.date_range(start=str(year), end=str(year+1), 
                         freq='W-SUN').strftime('%Y-%m-%d').tolist()
sunday2019 = list(allsundays(2019))

# Scrap the information of all broadway shows in 2019
data = pd.DataFrame()
for week in sunday2019:
    url = "https://www.playbill.com/grosses?week="+week
#    request = requests.get(url)
#    if request.status_code == 200:     # Check if the url exists
    df = html_tables(url).read()[0]
    df['Week'] = week
    data = data.append(df)

data.to_csv("broadwaydata2019.csv", index=False)
data.isnull().values.any() # None null 


# In[ ]:


#####################################################################
################ Processing Web Scraped Information #################
#####################################################################

listData = data.iloc[:, 0:len(data.columns)-1]

for i in range(len(listData.columns)):
    listData.iloc[:,i] = listData.iloc[:,i].str.split('\n')

Broadway2019 = pd.concat([
    listData.iloc[:,0].apply(pd.Series).iloc[:,[1,2]],
    listData.iloc[:,1].apply(pd.Series).iloc[:,[1,2]],
    listData.iloc[:,2].apply(pd.Series).iloc[:,1],
    listData.iloc[:,3].apply(pd.Series).iloc[:,[1,2]], 
    listData.iloc[:,4].apply(pd.Series).iloc[:,[1,2]], 
    listData.iloc[:,5].apply(pd.Series).iloc[:,[1,2]],
    listData.iloc[:,6].apply(pd.Series).iloc[:,1], 
    listData.iloc[:,7].apply(pd.Series).iloc[:,1]], 
    axis=1, ignore_index=True) 

Broadway2019.columns = ["Show Name", "Theatre", "Gross", "Potential Gross", "Gross Diff", 
                        "Avg Ticket Price", "Top Ticket Price", "Seats Sold", "Seats in the Theatre",
                        "Performances", "Previews", "Capacity", "Capacity Diff"]

Broadway2019['Week'] = data["Week"]
Broadway2019['Month'] = pd.DatetimeIndex(Broadway2019['Week']).month 
Broadway2019.loc[(Broadway2019['Month']==1) | (Broadway2019['Month']==2), 'Season'] = 'Winter'
Broadway2019.loc[(Broadway2019['Month']==3) | (Broadway2019['Month']==4), 'Season'] = 'Spring'
Broadway2019.loc[(Broadway2019['Month']==5) | (Broadway2019['Month']==6) | (Broadway2019['Month']==7), 'Season'] = 'Summer'
Broadway2019.loc[(Broadway2019['Month']==8) | (Broadway2019['Month']==9) | (Broadway2019['Month']==10), 'Season'] = 'Fall'
Broadway2019.loc[(Broadway2019['Month']==11) | (Broadway2019['Month']==12), 'Season'] = 'Holiday'

Broadway2019.isnull().values.any() # None null 

Broadway2019.to_csv("broadway2019.csv", index=False)

