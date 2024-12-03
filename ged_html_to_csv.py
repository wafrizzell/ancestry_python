#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import pandas as pd
import os


# In[37]:


### SET GLOBAL VARIABLES ###

your_ged_id = "A445182"   # Put your GED Match ID here as a string
auto_id_list = True      # Set to true to create list of ged_ids from directory, false to manually select ged_ids
directory = "../Gephi2024/Import_Files/"    # Set directory to write csv output to

# Insert a list of ged_ids you want to parse
manual_id_list = []
ged_ids = []

edges = pd.DataFrame()
nodes = pd.DataFrame()


# In[39]:


### CREATE OR RESET CSV FILES ###

header = pd.DataFrame(["target","name", "main_cm", "main_long", "main_gen", "match_cm",
                       "match_long", "match_gen", "gen_diff", "tree", "email", "main_id", "match_id"]).T

if os.path.isfile(f"{directory}shared_master.csv"):
    print("shared_master.csv already exists")
else:
    header.to_csv(f"{directory}shared_master.csv", header=False, index=False)
    print("shared_master.csv created and header wrote to file")


# In[40]:


### CREATE GED_ID LIST ###

# Add from directory if auto is true, or from manual_id_list if auto is false
if auto_id_list == True:
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.html'):
            ged_ids.append(filename[:-5])
else:
    ged_ids = manual_id_list


# In[41]:


### USE BEAUTIFUL SOUP TO PARSE HTML FILES FROM GED ID LIST ###

# Iterate through each html file using ged_ids
for ged_id in ged_ids:
    match_id = ged_id
    
    # Parse the html file
    gedMatch_html = open(f"{match_id}.html",encoding="utf8")
    soup = BeautifulSoup(gedMatch_html, "html.parser")

    # Find table and get table rows and create match_data
    table = soup.find("table", attrs={"class":"results-table"})
    table_rows = table.find_all("tr")

    match_data = []
    for row in table.find_all("tr"):
        row_data = []
        for cell in row.find_all("td"):
            row_data.append(cell.text)
        match_data.append(row_data)
    
    # Create the dataframe
    df = pd.DataFrame(match_data)
    
    # Close the open file after dataframe is made
    gedMatch_html.close()
    
    
### CREATE NODES AND EDGES DATAFRAMES ###   
    
    # Create edge dataframes and then concat into one dataframe
    ### CLEAN AND PREPARE DATAFRAME ###
    
     # Add new columns
    df[12] = your_ged_id
    df[13] = f"{match_id}"

     # Drop empty rows and unused columns and reset the index
    df.drop([0, 1], inplace=True)
    df.drop([1], inplace=True, axis=1)
    df.reset_index(drop=True, inplace=True)

     # Rename columns
    df.columns =["target","name", "main_cm", "main_longest", "main_gen", "match_cm", "match_long",
    "match_gen", "gen_diff", "tree", "email", "main_id", "match_id"]

    # Recast numeric columns as floats
    df["main_cm"] = df["main_cm"].str.replace(',', '').astype("float")
    df["main_longest"] = df["main_longest"].astype("float")
    df["main_gen"] = df["main_gen"].astype("float")
    df["match_cm"] = df["match_cm"].str.replace(',', '').astype("float")
    df["match_long"] = df["match_long"].astype("float")
    df["match_gen"] = df["match_gen"].astype("float")
    df["gen_diff"] = df["gen_diff"].astype("float")

    # Save to shared_master.csv
    df.to_csv(f"{directory}shared_master.csv", mode="a", header=False, index=False)
    print(f"Appended {match_id} to shared_master.csv")    


# Need to fix values in GED, Wiki, GED Wiki
# Compare file size of complete web pages versus shared_master
# Find a way to check to see if file has already been saved - Add IDs saved to a csv and then compare with a list to download to make a final list - Use match_id unique
# Install Git and Visual Studio
