import string
import urllib.request 
import pandas as pd


oscars = pd.read_csv("../data/clean_names.csv")

actors = oscars[oscars['category'] == ['ACTOR', 'ACTRESS', 'ACTRESS IN SUPPORTING ROLE', 'ACTOR IN SUPPORTING ROLE']]

actors.head(30)