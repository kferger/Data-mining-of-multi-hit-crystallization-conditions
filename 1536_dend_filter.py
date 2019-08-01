import requests, json, cockatoo, re, os, xmltodict, ast
from collections import OrderedDict
from xml.dom.minidom import parseString
import pandas as pd
from itertools import combinations_with_replacement, repeat
import numpy as np

"""
Extract all cocktails from 1536 screen for sample 1055
"""

os.environ['XTUITION_TOKEN'] = '9d89e79c-ed4d-11e5-8042-00270e10b7a7'
ROOT_PATH = "/projects/academic/esnell/kferger"

def within_screen_dist(cocktail_list, names):
    """
    Takes a list of all crystal 'hit' cocktails for a single protein from xtuition and calculates the distance between
    them in a pairwise fashion.  Outputs a csv matrix of every distance metric for every pair of cocktails in list.
    """
    d = [[] for i in repeat(None, len(cocktail_list))]
    for i in range(len(cocktail_list)):
        d[i] = [0] * len(cocktail_list)

    for a, b in combinations_with_replacement(cocktail_list, 2):  # pairwise distance combinations

        score = cockatoo.metric.distance(a,b)
        index_a = cocktail_list.index(a)
        index_b = cocktail_list.index(b)
        d[index_a][index_b] = score
        d[index_b][index_a] = score

    #for l in d:  # making all lists same size by filling 0's (combinations function doesn't output redundant pairs)
        #if len(l) < len(cocktails):
            #len_diff = len(cocktails) - len(l)
            #for i in range(len_diff):
                #l.insert(i, "NA")

    df = pd.DataFrame(d, index=names, columns=names)
    #df[names] = df[names].replace({0: np.nan, 0: np.nan})

    return df


base_uri = 'http://xtuition.ccr.buffalo.edu/api'
search_endpoint = base_uri + '/search'
auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}

endpoint = base_uri + '/sample/1055/list'
r = requests.get(endpoint, headers=auth)
ind = r.json()

cocktails = []
cocktail_names = []

for w in ind['wells']:  # loop through all wells for this sample and get cocktail information
    cocktail = cockatoo.xtuition.fetch_cocktail(w['cocktail_id'])
    # cocktail = m.json()

    cocktails.append(cocktail)
    cocktail_names.append(str(w['name']))

#print(len(cocktails))

cocktail_df = within_screen_dist(cocktails[:1536], cocktail_names[:1536])
cocktail_df.to_csv(ROOT_PATH + "/within-screen-dist/1055_whole_screen.csv", sep=",", na_rep="NA", header=True, index=True)
