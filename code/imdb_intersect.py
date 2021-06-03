
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
winners.to_csv('../data/clean_names.csv', index=False)

# print(winners.head())