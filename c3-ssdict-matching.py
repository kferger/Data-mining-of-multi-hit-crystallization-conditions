import json, re, statistics
from itertools import combinations
import pubchempy as pcp
from statistics import mode

ROOT_PATH = "/projects/academic/esnell/kferger"
global smiles_json
smiles_json = dict()

global cas_json #new
cas_json = dict() #new


def merge_cmpd_dict():

    file = open(ROOT_PATH+"/PDB-input/compound_dictionary.json", "r")
    json_file = json.load(file)

    final_dict = dict()
    values = json_file.values()

    seen = set()
    uniq_values = []

    for x in values:
        if x not in seen:
            uniq_values.append(x)
            seen.add(x)

    for item in json_file.items():
        final_dict[item[1]] = []
    for item in json_file.items():
        final_dict[item[1]].append(item[0])

    return final_dict #keys now match sensible_structure names

    file.close()
    #with open("/Users/kaileyferger/Downloads/compound_dictionary_compile.json", "w") as outfile:
        #json.dump(final_dict, outfile)


def name_edits(name):
    """
    Makes pairwise replacements of all characters below for passed name, and makes same replacements for all-
    lowercase version of name as well as a first word capitalized version.
    :param name:
    :return: list of name edits
    """

    name_edits = []
    characters = ["", " ", "-"]

    for a, b in combinations(characters, 2):
        if (a == "" and b == " ") or (a == "" and b == "-"):
            continue
        name_edits.append(name.replace(a, b))
        if (b == "" and a == " ") or (b == "" and a == "-"):
            continue
        name_edits.append(name.replace(b, a))

    if "/" in name:
        name_edits.append(name.replace("/", " "))
        name_edits.append(name.replace("/", "-"))

    name_edits = list(dict.fromkeys(name_edits))

    for i in name_edits:
        if i == name:
            name_edits.remove(i)

    return name_edits


def smiles_extraction(cas_keys, main):

    if len(cas_keys) != 0:
        try:
            top_ck = mode(cas_keys)  # take most frequent cas key
            cas_json[main] = top_ck #new
            #top_cmpds = pcp.get_compounds(top_ck, 'name')
            #if len(top_cmpds) != 0:
                #top_smiles = top_cmpds[0].isomeric_smiles  # pick top result (best match) for cas key
                #smiles_json[main] = top_smiles

        except statistics.StatisticsError:  # two are equally frequent
            top_ck = []
            smiles = []
            lst_count = [x for x in set(cas_keys) if cas_keys.count(x) > 1]

            for i in range(len(lst_count)):
                top_ck.append(lst_count[i])
            #for j in top_ck:
                #top_cmpds = pcp.get_compounds(j, 'name')
                #if len(top_cmpds) != 0:
                    #top_smiles = top_cmpds[0].isomeric_smiles
                    #smiles.append(top_smiles)

            #smiles_json[main] = [smiles]

            cas_json[main] = top_ck


file = open(ROOT_PATH+"/PDB-input/c3_chemicals.json", "r")
c3_chem = json.load(file)
merge_cmpds = merge_cmpd_dict()

#elements = []
for element in merge_cmpds:
    #elements.append(element)
#print(len(elements))

#for e in elements[0:24]:

    main = element
    new_mains = name_edits(main) #name edits
    #syn_names = merge_cmpds[element]

    for item in c3_chem:
        cas_keys = []

        for name in c3_chem[item]['names']:
            if re.fullmatch(main, name, re.IGNORECASE):
                pcp_cmpds = pcp.get_compounds(item, 'name')

                for result in pcp_cmpds:
                    for res in result.synonyms:
                        if re.search('[0-9-]', res) and not re.search('[a-zA-Z]', res):  # find cas keys
                            cas_keys.append(res)
                            break

                        if re.search('^(CAS-)\d+-', res):  # find cas keys in format CAS-###-##-#
                            split = res.split("-")[1:]
                            s = "-"
                            cas_keys.append(s.join(split))
                            break

                if len(cas_keys) == 0:
                    cas_keys.append(name) # get smiles via c3 name not cas key

                smiles_extraction(cas_keys, main)

                break  #once match is found in set of names and cas keys extracted, move to next chemical
"""

            for edit in new_mains: #check each change in each key in merge_cmpds

                for syn in syn_names: #filter out redundant name checks
                    if edit == syn:
                        syn_names.remove(syn)

                if edit == name: #check for match of each edited name in each set of c3 names
                    pcp_cmpds = pcp.get_compounds(name, 'name')
                    # if any hit within individual name group, search all names in name group through pubchem

                    for result in pcp_cmpds:
                        for res in result.synonyms:
                            if re.search('[0-9-]', res) and not re.search('[a-zA-Z]', res): #find cas keys
                                cas_keys.append(res)
                            if re.search('^(CAS-)\d+-', res): #find cas keys in format CAS-###-##-#
                                split = res.split("-")[1:]
                                s = "-"
                                cas_keys.append(s.join(split))
                                break
                    break # if match found, next name

                   # else:

                if len(syn_names) != 0:

                    for syn_name in syn_names:
                        if syn_name == name:
                            pcp_cmpds = pcp.get_compounds(name, 'name')

                            for result in pcp_cmpds:
                                for res in result.synonyms:
                                    if re.search('[0-9-]', res) and not re.search('[a-zA-Z]', res):  # find cas keys
                                        cas_keys.append(res)
                                    if re.search('^(CAS-)\d+-', res):  # find cas keys in format CAS-###-##-#
                                        split = res.split("-")[1:]
                                        s = "-"
                                        cas_keys.append(s.join(split))
                                        break
                            break # if match found, next name

                        else:
                            ind_edits = name_edits(syn_name)#name edits

                            for edits in ind_edits:
                                if edits == main:
                                    continue #filter out redundant name checks

                                if edits == name:
                                    pcp_cmpds = pcp.get_compounds(name, 'name')

                                    for result in pcp_cmpds:
                                        for res in result.synonyms:
                                            if re.search('[0-9-]', res) and not re.search('[a-zA-Z]', res):  # find cas keys
                                                cas_keys.append(res)
                                            if re.search('^(CAS-)\d+-', res):  # find cas keys in format CAS-###-##-#
                                                split = res.split("-")[1:]
                                                s = "-"
                                                cas_keys.append(s.join(split))
                                                break
                                    break # if match found, next name
"""
"""
        if len(cas_keys) != 0:
            try:
                top_ck = mode(cas_keys)  # take most frequent cas key
                top_cmpds = pcp.get_compounds(top_ck, 'name')
                top_smiles = top_cmpds[0].isomeric_smiles #pick top result (best match) for cas key
                smiles_json[main] = top_smiles

            except statistics.StatisticsError: #two are equally frequent
                lst_count = [x for x in set(cas_keys) if cas_keys.count(x) > 1]
                top_ck1, top_ck2 = lst_count[0], lst_count[1]
                top_cmpds1 = pcp.get_compounds(top_ck1, 'name')
                top_cmpds2 = pcp.get_compounds(top_ck2, 'name')
                top_smiles1 = top_cmpds1[0].isomeric_smiles
                top_smiles2 = top_cmpds2[0].isomeric_smiles
                smiles_json[main] = [top_smiles1, top_smiles2]
"""

with open(ROOT_PATH+"/PDB-input/cas_dictionary_c3.json", "w") as json_output:
    json.dump(cas_json, json_output, indent=4, separators=(',', ': '))

file.close()
