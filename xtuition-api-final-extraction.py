import requests, json, cockatoo, re, os, xmltodict, ast
from collections import OrderedDict
from xml.dom.minidom import parseString
import pandas as pd
from itertools import combinations_with_replacement, repeat
import numpy as np

"""
This script extracts cocktail information for x-ray protein structures from the xtuition database (xtuition.org).  All 
cocktails analyzed produced verified crystal structures. 

A reference cocktail from the Protein Data Bank (PDB) is then extracted from a local database (see 
https://github.com/maxdudek/crystallizationDatabase) (called sensible_structures). 

Cockatoo, a python software developed to measure the relative 'distance' between two protein cocktails, is implemented 
to calculate the distance between the reference cocktail, and each crystal 'hit' cocktail from the same protein in 
xtuition.

Distances are also calculated in a pairwise fashion between all crystal 'hit' cocktails in the xtuition data for each
protein.
"""

ROOT_PATH = "/projects/academic/esnell/kferger"
os.environ['XTUITION_TOKEN'] = '9d89e79c-ed4d-11e5-8042-00270e10b7a7'


def reference_cocktail(*argv):
    """
    This function takes a list of cocktail pH, and several other lists of compound names, concentrations, and units
    within a single cocktail. It uses the cockatoo command cocktail.add_compound() to create and output a cockatoo-
    formatted cocktail for use in its distance function.
    """

    for compound in argv:
        cocktail = cockatoo.screen.Cocktail('REF', ph=compound[0])
        for s in range(len(compound) - 1):
            comp = cockatoo.xtuition.fetch_compound_by_name(compound[s+1][0])
            comp.conc = compound[s+1][1]
            comp.unit = compound[s+1][2]
            cocktail.add_compound(comp)

    return cocktail


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


def pdb_structures(): #pdb file handling
    """
    Takes single local database file (sensible_structures) and parses each entry into a readable file for further
    processing.
    """

    file = open(ROOT_PATH+"/PDB-input/sensible_structures_final_edit.json", "r")
    doc = json.load(file)
    length = len(doc['structures'])

    return doc, length

    file.close()


def main():
    """
    Extracts each sample and its corresponding cocktails from xtuition, filters only samples with verified x-ray
    structures and cocktails with verified crystal hits, and implements cockatoo to calculate distances between the
    reference cocktail for that sample and each crystal hit cocktail. Distances are written to a file on an individual
    sample basis.
    """

    base_uri = 'http://xtuition.ccr.buffalo.edu/api'
    search_endpoint = base_uri + '/search'
    auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}

    # Fetch all samples with verified crystals
    payload = {'query': 'crystals +pdb'}
    r = requests.get(search_endpoint, headers=auth, params=payload)
    samples = r.json()

    for s in samples['samples']:

        cocktails = []
        cocktail_names = []
        distances = []

        endpoint = base_uri + '/sample/' + str(s['sample_id']) + '/list'
        payload = {'crystals': '1'} #only select wells with verified crystals
        r = requests.get(endpoint, headers=auth, params=payload)
        ind = r.json()

        if "X-Ray structure" in ind['sample']['spine_status']:
            pdbid = ind['sample']['structures'][0]['structure_id']
            json_structure, structure_length = pdb_structures()

            for j in range(structure_length):
                structures = ast.literal_eval(json_structure['structures'][j])

                if structures['pdbid'] == pdbid:
                    compound_list = []  # compound_list: [compound name, concentration, unit]
                    pH = structures['pH']

                    if pH == 'None':
                        break
                    compound_list.append(float(pH))

                    if isinstance(structures['compounds']['compound'], dict):
                        one_cmpd = []
                        one_cmpd.append(structures['compounds']['compound']['name'])

                        conc = structures['compounds']['compound']['concentration']
                        if conc == 'None':
                            break

                        if '%' not in conc:
                            molar_convert = float(conc) / 1000  # convert mM to M
                            one_cmpd.append(molar_convert)  # compound conc
                            one_cmpd.append('M')  # compound unit
                        else:
                            one_cmpd.append(float(conc.strip('% w/v')))
                            one_cmpd.append('% (w/v)')
                        compound_list.append(one_cmpd)

                    elif isinstance(structures['compounds']['compound'], list):
                        num_compounds = len(structures['compounds']['compound'])

                        for k in range(num_compounds):
                            over_two_cmpds = []
                            over_two_cmpds.append(structures['compounds']['compound'][k]['name'])  # compound name

                            sev_conc = structures['compounds']['compound'][k]['concentration']
                            if sev_conc == 'None':
                                break

                            if '%' not in sev_conc:
                                molar_convert = float(sev_conc) / 1000  # convert mM to M
                                over_two_cmpds.append(molar_convert)  # compound conc
                                over_two_cmpds.append('M')  # compound unit
                            else:
                                over_two_cmpds.append(float(sev_conc.strip('% w/v')))
                                over_two_cmpds.append('% (w/v)')

                            compound_list.append(over_two_cmpds)

                    ref_cocktail = reference_cocktail(compound_list) #call reference cocktail function

                    for w in ind['wells']: #loop through all wells for this sample and get cocktail information
                        cocktail = cockatoo.xtuition.fetch_cocktail(w['cocktail_id'])
                        #cocktail = m.json()

                        cocktails.append(cocktail)
                        cocktail_names.append(str(w['name']))

                        #ck = cockatoo.screen.parse_cocktail(str(cocktail))
                        dist = cockatoo.metric.distance(ref_cocktail, cocktail, [1.0,1.0])

                        distances.append(dist)

        if len(distances) == 0: #if xtuition PDB ID cannot be found in PDB local database (in the case of structure
            #deletions due to absence in xtuition compound database)
            continue

        dist_df = pd.DataFrame([distances], columns = cocktail_names)
        dist_df.to_csv(ROOT_PATH+"/cockatoo-distances/"+pdbid+"-"+str(s['xnumber'])+"-dist.csv", sep=",", header=True,
                       index=False)

        cocktail_df = within_screen_dist(cocktails, cocktail_names)
        cocktail_df.to_csv(ROOT_PATH+"/within-screen-dist/"+str(s['xnumber'])+".csv", sep=",",na_rep="NA",
                           header=True, index=True)


if __name__ == '__main__':
    main()