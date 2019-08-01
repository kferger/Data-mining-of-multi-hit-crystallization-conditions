import pubchempy as pcp
import requests, sys, json, re
import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from xml.dom import minidom

#loop through all xtuition compounds

base_uri = 'http://xtuition.ccr.buffalo.edu/api/'
auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}

tree = ET.parse("/projects/academic/esnell/kferger/PDB-input/sensible_structures.xml")
root = tree.getroot()


def smiles_extraction(smiles, cas, xname):

    #file = open(
       # "/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3v1.json", "r")
    file = open(
        "/projects/academic/esnell/kferger/PDB-input/cas_dictionary_c3_final.json", "r")
    json_file = json.load(file)

    for item in json_file.items():
        if isinstance(item[1], list):
            if len(item[1]) == 2: #contains both cas number and smiles or chemical name and smiles
                 if isinstance(item[1][0], str) and isinstance(item[1][1], str):
                    if item[1][1] == smiles or item[1][0] == cas or re.fullmatch(item[1][0], xname, re.IGNORECASE):
                        return item[0]
                        break

            elif len(item[1]) == 1: #contains only smiles
                if isinstance(item[1][0], str):
                    if item[1][0] == smiles:
                        return item[0]
                        break

        else: #if item[1] is just the name
            if re.fullmatch(item[1], xname, re.IGNORECASE):
                return item[0]
                break


def weight_check(molecular_weight, average_mass, pcp_weight, x_formula):

    if molecular_weight != None:  # entry has value for molecular weight
        mol_weight = round(molecular_weight, 2)

        if average_mass != None:  # entry has values for both molecular weight and average mass
            ave_mass = round(average_mass, 2)

            if (pcp_weight <= mol_weight + 0.05 and pcp_weight >= mol_weight - 0.05) or \
                    (pcp_weight <= ave_mass + 0.05 and pcp_weight >= ave_mass - 0.05):  # create 0.05 buffer for mass to account for slight variations
                new_formula = re.sub('[\{}_]', '', x_formula)  # edit xtuition formula to eliminate {} and _'s
                return new_formula

        elif (pcp_weight <= mol_weight + 0.05 and pcp_weight >= mol_weight - 0.05):  # entry has value for molecular weight but not average mass
            new_formula = re.sub('[\{}_]', '', x_formula)
            return new_formula

    elif average_mass != None:  # entry doesn't have value for molecular weight, but does for average_mass
        ave_mass = round(average_mass, 2)

        if (pcp_weight <= ave_mass + 0.05 and pcp_weight >= ave_mass - 0.05):
            new_formula = re.sub('[\{}_]', '', x_formula)
            return new_formula


names = dict()  # (ss_name:xtuition_name)

for i in range(324):

    r = requests.get(base_uri + "compound/" + str(i + 1), headers=auth)
    cmpd = r.json()
    xtuition_name = cmpd['name']

    if cmpd['cas'] != None: #last checked number of xtuition cmpds with cas keys: 309
        pcp_cmpds = pcp.get_compounds(cmpd['cas'], 'name')

        if len(pcp_cmpds) != 0: #last checked successful extractions: 275 (including same line in else stmt)
            for result in pcp_cmpds:
                pcp_weight = round(result.molecular_weight, 2)  # measure to tenths place
                formula = weight_check(cmpd['molecular_weight'], cmpd['average_mass'], pcp_weight, cmpd['formula'])

                if formula: #last checked successful extractions: 231 (including same line in else stmt)

                    if result.molecular_formula == formula: #last checked successful matches: 224 (including same line in else stmt)
                        smiles = result.isomeric_smiles  # extract smiles
                        ss_name = smiles_extraction(smiles, cmpd['cas'], xtuition_name)

                        if ss_name != "" and ss_name: #last checked successful smiles matches: 83
                            names[ss_name] = xtuition_name
                            break
                        else:
                            break

                else: #if compound doesn't have both average mass and molecular weight listed
                    continue #move to next in list, skip compound if none match

    else: #if compound doesn't have cas number listed
        cmpd_list = pcp.get_compounds(cmpd['name'], 'name') #use name instead

        if len(cmpd_list) != 0:
            for result in cmpd_list:
                pcp_weight = round(result.molecular_weight, 2)  # measure to tenths place
                formula = weight_check(cmpd['molecular_weight'], cmpd['average_mass'], pcp_weight, cmpd['formula'])

                if formula:

                    if result.molecular_formula == formula:
                        smiles = result.isomeric_smiles #extract smiles
                        ss_name = smiles_extraction(smiles, cmpd['cas'], xtuition_name)

                        if ss_name != "" and ss_name:
                            names[ss_name] = xtuition_name
                            break
                        else:
                            break

                else: #if compound doesn't have both average mass and molecular weight listed
                    break #skip compound (doesn't match/have cas or either weight metric)

#print("Total number of xtuition cmpds with cas keys: {}".format(m))

j=0
for old, new in names.items():
    print('{}:{}'.format(old, new))
    j+=1
print("Number of changes: {}".format(j))

for old, new in names.items():
    for name in root.iter('name'):
        if name.text == old:
            new_name = new
            name.text = new_name

for structure in root:
    for old, new in names.items():

        for cmpds in structure:
            for cmpd in cmpds:
                if cmpd.text == 'SAM':
                    root.remove(structure)

tree.write("/projects/academic/esnell/kferger/PDB-input/sensible_structures_final.xml", encoding='utf8')



