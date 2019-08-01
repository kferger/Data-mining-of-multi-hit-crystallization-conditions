import pandas as pd, requests, numpy as np, re, os, cockatoo
from itertools import repeat, combinations_with_replacement

os.environ['XTUITION_TOKEN'] = '9d89e79c-ed4d-11e5-8042-00270e10b7a7'

def fp_dist(cocktails, names):


    d = [[] for i in repeat(None, len(cocktails))]
    for i in range(len(cocktails)):
        d[i] = [0] * len(cocktails)

    for a, b in combinations_with_replacement(cocktails, 2):  # pairwise distance combinations

        fp_dist = cockatoo.metric.fp_distance(a,b)
        index_a = cocktails.index(a)
        index_b = cocktails.index(b)
        d[index_a][index_b] = fp_dist
        d[index_b][index_a] = fp_dist

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

cocktails = []
cocktail_names = []
distances = []

endpoint = base_uri + '/sample/1055/list'
payload = {'crystals': '1'}  # only select wells with verified crystals
r = requests.get(endpoint, headers=auth, params=payload)
ind = r.json()


for w in ind['wells']:  # loop through all wells for this sample and get cocktail information

    #endpoint = base_uri + '/cocktail/' + str(w['cocktail_id'])
    #m = requests.get(endpoint, headers=auth)
    #cocktail = m.json()
    cocktail = cockatoo.xtuition.fetch_cocktail(w['cocktail_id'])

    #cocktail = cockatoo.xtuition.fetch_cocktail(w['cocktail_id'])
    cocktails.append(cocktail)
    cocktail_names.append(str(w['name']))

fp_dist_df = fp_dist(cocktails, cocktail_names)
fp_dist_df.to_csv("/projects/academic/esnell/kferger/PDB-input/ck1055_fp_dist.csv", sep=",", header=True, index=True)