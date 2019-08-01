import os, re, json, cockatoo
import pandas as pd
from itertools import repeat, combinations

root_path = '/projects/academic/esnell/kferger/'
directory = os.fsencode(root_path+'/xtuition-data/sample_cocktails')
pdb_cocktails = open(root_path+'/PDB-input/sensible_structures.json', "r")
pdb_data = json.load(pdb_cocktails)

#single pairwise comparison of all xtuition hits vs pdb cocktail (make new function?)
for file in os.listdir(directory):

    cocktail_list_complete = []
    cocktail_names = []

    with open(file, "r") as json_file:

        #function currently not working
        #sample_screen = cockatoo.screen.parse_json(json_file) #compute internal screen similarity
        #internal_sim = cockatoo.screen.internal_similarity(sample_screen)
        #export

        c = json.load(json_file)
        identifier = re.compile('\{"name":')
        cocktail_list = identifier.split(c)


        for item in cocktail_list[1:]:
            cocktail = '{}:{item}'.format('{"name"', item=item)
            cocktail_list_complete.append(cocktail)
            cocktail_names.append(cocktail["name"])
            ck1 = cockatoo.screen.parse_cocktail(cocktail)
            ck2 = cockatoo.screen.parse_cocktail(ind_pdb_cocktail[os.listdir(directory).index(file)])
            cocktail_distance = cockatoo.metric.distance(ck1, ck2, weights=None)
            #output to matrix

#within-screen distance calculations (make new function?)
        d = [[] for i in repeat(None, len(cocktail_list_complete))]
        d[0].append(0)
        d[-1].append(0)
        
        for a, b in itertools.combinations(cocktail_list_complete, 2): #pairwise distance combinations
            #insert cocktail distance calculations
            diff = a*b
            d[a-1].append(diff)

        for l in d: #making all lists 12x12 by filling 0's (combinations function doesn't output redundant pairs)
            if len(l) < len(cocktail_list_complete):
                len_diff = len(cocktail_list_complete) - len(l)
                for i in range(len_diff):
                    l.insert(i,0)

        df = pd.DataFrame(d, index=cocktail_names columns = cocktail_names)
        df[cocktail_names] = df[cocktail_names].replace({0:np.nan, 0:np.nan})
        df.to_csv("/projects/academic/esnell/kferger/within-screen-dist/"+, sep=",", na_rep="Na", header=True, index=True)

