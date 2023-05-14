"""This is a Python Statistics Essentials Exercise 1, Personal Email Analytics, started on May 13, 2023.  I don't know why it
is called email analytics because it isn't about emails."""

#Input 
# Desired output: table with numberical index column, country code, year, age, sex, cases

import pandas as pd
import numpy as np

#-----------------------------Functions Definition --------------------------------
#This is a function to find the number of missing values per column in a dataframe
def missing_values(df_name):
    """This function iterates to find the number of missing values per column"""
    print ("Missing values by Column")
    for col in df_name.columns:
        missing = df_name[col].isna().sum()
        print (str(col) + ": " + str(missing) + " missing values")
    return

#------------------------------------------------------------------------------------

#read CSV of Tuberculosis Data
table = pd.read_csv('/home/bringingthesparkle/LinkedInChallenges/tb.csv')

#print(table.head(3))
#print(table.shape)
#missing_values(table) #strangely, there are missing values in the country column

#Separate this into gendered tables

#These are the columns that are independent of gender
basic_table = table.iloc[:,0:2]

# male data table (with independent columns), rename columns
m_table = table.iloc[:,0:12]
m_table.columns = ['country', 'year', '0-4', '5-14', '0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+', 'unk']
df_melted_m = m_table.melt( id_vars=['country','year'], value_vars=['0-4', '5-14', '0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+', 'unk'], var_name = 'age', value_name = 'Cases')
df_melted_m.dropna(subset=['Cases'], inplace=True)
df_melted_m.dropna(subset=['country'], inplace=True)
df_melted_m['Gender'] = 'M'

# female data table (without independent columns, need to add back)
female_table = table.iloc[:,12:22]
f_table = pd.merge(basic_table,female_table,left_index=True,right_index=True)

# Rename columns
f_table.columns = ['country', 'year', '0-4', '5-14', '0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+', 'unk']

# Melt table to get into long format
df_melted = f_table.melt( id_vars=['country','year'], value_vars=['0-4', '5-14', '0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+', 'unk'], var_name = 'age', value_name = 'Cases')

#Remove all rows where cases are Nans, add gender column, and reset the index
df_melted.dropna(subset=['Cases'], inplace=True)
df_melted.dropna(subset=['country'], inplace=True)
df_melted['Gender'] = 'F'

# Concatenate files and check that they were added properly
#print(df_melted.shape)
#print(df_melted_m.shape)
df = pd.concat([df_melted, df_melted_m], axis = 0) #This didn't exactly work
#print(df.shape) 

# asserting that there are no missing values in the dataframe (commented out for final product)
# missing_values(df)

# reorder columns
df = df[['country', 'year', 'age', 'Gender', 'Cases']]
#Sort by country, year, age
df = df.sort_values(by=['country', 'year', 'age'])
# reset index
df.reset_index(drop=True, inplace = True)

# Final beautiful table (this is the kind of work I enjoy doing and should be doing full-time.)
print(df.head(10))






#-----------------------------REMOVED CODE-------------------------------------
#for row_id in idx:
#    f_table.drop(row_id, inplace = True)
#print(f_table.shape) # resulting in a shape of 2437 x 12

# Find the rows which have no recorded data to delete after concatenation (Apparently there are 3,332 years for which there is no recorded data)
#idx = female_table.index[female_table.isnull().all(1)]
#print(len(idx)) #There are 3332 completely 

#assert df.isnull().any() == False # I can't remember exactly the right syntax, need to check