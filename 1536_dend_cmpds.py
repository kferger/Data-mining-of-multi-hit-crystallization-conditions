import requests, json, re, os, xmltodict, ast, csv, operator
from collections import OrderedDict
from xml.dom.minidom import parseString
import pandas as pd
from itertools import combinations_with_replacement, repeat
import numpy as np

"""
Counts and ranks compounds by their occurrence per dendrogram cluster.  Reads in hit cocktails and outputs ranked list of compounds.
"""

os.environ['XTUITION_TOKEN'] = '9d89e79c-ed4d-11e5-8042-00270e10b7a7'
ROOT_PATH = "/projects/academic/esnell/kferger"

cutfile = open("/Users/kaileyferger/Downloads/1055_cut_hits.csv", "r")
cut_hits_csv = pd.read_csv(cutfile, sep = ",")
#print(cut_csv.at[1535, "cutree(clust, k = 10)"])

base_uri = 'http://xtuition.ccr.buffalo.edu/api'
search_endpoint = base_uri + '/search'
auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}

endpoint = base_uri + '/sample/1055/list'
r = requests.get(endpoint, headers=auth)
ind = r.json()

c1 = {}
c2 = {}
c3 = {}
c4 = {}
c5 = {}
c6 = {}
c7 = {}
c8 = {}
c9 = {}
c10 = {}

cut_ind = 0

for w in ind['wells']:
    if cut_ind < 55:

        clust_lab = cut_hits_csv.at[cut_ind, "cut_hit_rows"]
        id, name = w['cocktail_id'], w['name']

        if cut_hits_csv.iloc[cut_ind, 0] == name:

            cut_ind += 1
            #cmpds = []
            endpoint = base_uri + '/cocktail/' + str(id)
            m = requests.get(endpoint, headers=auth)
            cocktail = m.json()

            for i in range(len(cocktail['components'])):

                if clust_lab == 1:
                    if cocktail['components'][i]['compound']['name'] not in c1:
                        c1[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        #print(cocktail['components'][i]['compound']['name'])
                        c1[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 2:
                    if cocktail['components'][i]['compound']['name'] not in c2:
                        c2[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c2[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 3:
                    if cocktail['components'][i]['compound']['name'] not in c3:
                        c3[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c3[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 4:
                    if cocktail['components'][i]['compound']['name'] not in c4:
                        c4[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c4[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 5:
                    if cocktail['components'][i]['compound']['name'] not in c5:
                        c5[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c5[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 6:
                    if cocktail['components'][i]['compound']['name'] not in c6:
                        c6[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c6[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 7:
                    if cocktail['components'][i]['compound']['name'] not in c7:
                        c7[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c7[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 8:
                    if cocktail['components'][i]['compound']['name'] not in c8:
                        c8[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c8[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 9:
                    if cocktail['components'][i]['compound']['name'] not in c9:
                        c9[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c9[cocktail['components'][i]['compound']['name']] += 1
                if clust_lab == 10:
                    if cocktail['components'][i]['compound']['name'] not in c10:
                        c10[cocktail['components'][i]['compound']['name']] = 1
                    else:
                        c10[cocktail['components'][i]['compound']['name']] += 1

    else:
        break
print("1: {}".format(OrderedDict(sorted(c1.items(), key=lambda x: x[1], reverse=True))))
print("2: {}".format(OrderedDict(sorted(c2.items(), key=lambda x: x[1], reverse=True))))
print("3: {}".format(OrderedDict(sorted(c3.items(), key=lambda x: x[1], reverse=True))))
print("4: {}".format(OrderedDict(sorted(c4.items(), key=lambda x: x[1], reverse=True))))
print("5: {}".format(OrderedDict(sorted(c5.items(), key=lambda x: x[1], reverse=True))))
print("6: {}".format(OrderedDict(sorted(c6.items(), key=lambda x: x[1], reverse=True))))
print("7: {}".format(OrderedDict(sorted(c7.items(), key=lambda x: x[1], reverse=True))))
print("8: {}".format(OrderedDict(sorted(c8.items(), key=lambda x: x[1], reverse=True))))
print("9: {}".format(OrderedDict(sorted(c9.items(), key=lambda x: x[1], reverse=True))))
print("10: {}".format(OrderedDict(sorted(c10.items(), key=lambda x: x[1], reverse=True))))



