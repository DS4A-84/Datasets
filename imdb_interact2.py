#!/usr/bin/env python
# coding: utf-8

# In[1]:



import json, requests
import string
import re
import gzip
import shutil
import urllib.request 
import pandas as pd
# import imdbpy


# Downloading IMDB dataset of names
# imdb_url = 'https://datasets.imdbws.com/name.basics.tsv.gz'
# imdb_file = requests.get(imdb_url, stream=True)
# open('../data/namebasics.tsv.gz', 'wb').write(imdb_file.content)    # https://www.tutorialspoint.com/downloading-files-from-web-using-python

# with gzip.open('../data/namebasics.tsv.gz', 'rb') as f_in:          # https://stackoverflow.com/questions/31028815/how-to-unzip-gz-file-using-python
#     with open('../data/namebasics.tsv', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)


# df = pd.read_csv("../data/the_oscar_award.csv")
imdb = pd.read_csv("../data/namebasics.tsv", sep='\t')
oscars = pd.read_csv("../data/oscar_winners_clean.csv")
oscars["primaryName"]=oscars["name"]

del imdb["knownForTitles"]

# Merging data
# winners = pd.merge(oscars, imdb, how='inner', on=['primaryName'])
# ['year_ceremony', 'category', 'name', 'film', 'winner', 'primaryName','nconst', 'birthYear', 'deathYear', 'primaryProfession']
# winners.to_csv('../data/clean_names.csv', index=False)

# Calculating age they won the award
# subtract birth year from ceremony date, if winner==No then make won year 0
# winners["winAge"] = winners['year_ceremony'].notna().astype(int) - winners['birthYear'].notna().astype(int)
# Removing duplicates
# winners = winners.drop(winners[(winners['birthYear'])].index)
# winners = winners.groupby(['year_ceremony', 'category','birthYear'], as_index=False)

# # Current age --> Nominees are invited to the Academy
# # If deathYear empty then make current age Null

# # print(winners.head(if not winners["birthYear"]))
# print(winners.head(20))
# winners.to_csv('../data/clean_names.csv', index=False)


# In[21]:


winners = pd.merge(oscars, imdb, how='inner', on=['primaryName'])
winners.head(20)


# In[50]:


# win = winners
win = winners.drop_duplicates(['name','category', 'film'], keep='first').reset_index() # dropping duplicates with the same name, category, year, and film. 2 people have been nominated for 2 different films
win = win.replace(r'\\N', ' ', regex=True)


# Age when they were nominated. NOTE: This might not have been their actual age as we don't have their birth days. A better approach would be to find a dataset with their age at nomination
win["ceremonyAge"]=pd.to_numeric(win['year_ceremony'], errors='coerce')-pd.to_numeric(win['birthYear'], errors='coerce')  # Age at the time of the ceremony. NOTE: Some people were nominated after they died, how should we handle this?



## Current age --> Nominees are invited to the Academy, this would give us an idea of what the voting population is
# If deathYear empty then make current age Null
# win[(win.deathYear==' ')]["alive"] = 'succeed'

# Checking if nominees are alive
win.loc[ (win.deathYear==' ') & (win.birthYear!=' '), 'alive'] = True   
win.loc[ (win.deathYear!=' ') & (win.birthYear!=' '), 'alive'] = False

# Deleting duplicate name column
del(win["primaryName"])
# win.loc[]

# print(winners.head(if not winners["birthYear"]))
# print(win.head(20))
win.head(50)
win.to_csv('../data/clean_names.csv', index=False)
# l=win['birthYear']
# l.head(50)
# winners.head(20)

