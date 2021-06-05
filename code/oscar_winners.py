import pandas as pd
import urllib.request
import json, requests
import os
import wget



df = pd.read_csv("../data/the_oscar_award.csv")
del df['ceremony']
del df['year_film']
df.to_csv('../data/oscar_winners_clean.csv', index=False)