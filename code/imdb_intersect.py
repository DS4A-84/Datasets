import json, requests
import string
import re
import gzip
import shutil
import urllib.request 
import pandas as pd
# import imdbpy


# Downloading IMDB dataset of names
imdb_url = 'https://datasets.imdbws.com/name.basics.tsv.gz'
imdb_file = requests.get(imdb_url, stream=True)
open('../data/namebasics.tsv.gz', 'wb').write(imdb_file.content)    # https://www.tutorialspoint.com/downloading-files-from-web-using-python

with gzip.open('../data/namebasics.tsv.gz', 'rb') as f_in:          # https://stackoverflow.com/questions/31028815/how-to-unzip-gz-file-using-python
    with open('../data/namebasics.tsv', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


# df = pd.read_csv("../data/the_oscar_award.csv")
imdb = pd.read_csv("../data/namebasics.tsv", sep='\t')
oscars = pd.read_csv("../data/oscar_winners_clean.csv")
oscars["primaryName"]=oscars["name"]

del imdb["knownForTitles"]

winners = pd.merge(oscars, imdb, how='inner', on=['primaryName'])

winners = winners.drop_duplicates(['name','category', 'film'], keep='first').reset_index() # dropping duplicates with the same name, category, year, and film. 2 people have been nominated for 2 different films
winners = winners.replace(r'\\N', 0, regex=True)


# Age when they were nominated. NOTE: This might not have been their actual age as we don't have their birth days. A better approach would be to find a dataset with their age at nomination
winners["ceremonyAge"]=pd.to_numeric(winners['year_ceremony'], errors='coerce')-pd.to_numeric(winners['birthYear'], errors='coerce')  # Age at the time of the ceremony. NOTE: Some people were nominated after they died, how should we handle this?
winners.loc[ (winners.ceremonyAge>1000), 'ceremonyAge'] = 0  ## Some entries don't have a birth so making them 0

# # Checking if nominees are alive
winners.loc[ (winners.deathYear==0) & (winners.birthYear!=0), 'alive'] = True   
winners.loc[ (winners.deathYear!=0) & (winners.birthYear!=0), 'alive'] = False
winners.loc[ (winners.deathYear==0) & (winners.birthYear==0), 'alive'] = False ## if no birth and death year, then not alive
winners['birthYear'] = winners['birthYear'].astype(int)

# # Calculating current age. subtract birthYear from currentYear then if alive=
winners['currentYear']=int(2021)

# 
winners["currentAge"] = winners['currentYear']- winners['birthYear']
winners.loc[winners.alive==False, 'currentAge'] = 0

# # Deleting duplicate name column
del(winners["primaryName"])


winners.to_csv('../data/clean_names.csv', index=False)
