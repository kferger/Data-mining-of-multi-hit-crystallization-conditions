import json, re, statistics
from itertools import combinations
import pubchempy as pcp
from statistics import mode

ROOT_PATH = "/projects/academic/esnell/kferger"

global new_smiles
file = open(ROOT_PATH+"/PDB-input/smiles_dictionary_c3_compiled_final.json", "r")
new_smiles = json.load(file)

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


def filter_dict(cmp_dict):

    file1 = open(ROOT_PATH+"/PDB-input/smiles_dictionary.json", "r")
    old_smiles = json.load(file1)

    for k,v in list(new_smiles.items()):
        if v == [[]]:
            del new_smiles[k]

    for old_name in old_smiles:
        if old_smiles[old_name] != "":
            if old_name not in new_smiles:
                new_smiles[old_name] = old_smiles[old_name]

    with open(ROOT_PATH+"/PDB-input/smiles_dictionary_c3v1.json", "w") as outfile:
        json.dump(new_smiles, outfile, indent=4, separators=(',', ': '))

    for j,k in list(cmp_dict.items()): #remove cmpds in compound_dictionary that are present in new_smiles
        if " / " in j:
            del cmp_dict[j]

        for new_name in new_smiles:
            if j == new_name:
                del cmp_dict[j]


    return cmp_dict

    file1.close()


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
            top_cmpds = pcp.get_compounds(top_ck, 'name')
            if len(top_cmpds) != 0:
                top_smiles = top_cmpds[0].isomeric_smiles  # pick top result (best match) for cas key
                new_smiles[main] = top_smiles

        except statistics.StatisticsError:  # two are equally frequent
            top_ck = []
            smiles1 = []
            lst_count = [x for x in set(cas_keys) if cas_keys.count(x) > 1]

            for i in range(len(lst_count)):
                top_ck.append(lst_count[i])
            for j in top_ck:
                top_cmpds = pcp.get_compounds(j, 'name')
                if len(top_cmpds) != 0:
                    top_smiles = top_cmpds[0].isomeric_smiles
                    smiles1.append(top_smiles)

            new_smiles[main] = [smiles1]


file = open(ROOT_PATH+"/PDB-input/c3_chemicals.json", "r")
c3_chem = json.load(file)

merge_cmpds = merge_cmpd_dict() #change formatting of compound_dictionary.json
filter_merge = filter_dict(merge_cmpds) #remove names in compound_dictionary.json that are already present in new_smiles (see function)


elements = []
for element in filter_merge:
    elements.append(element)
#print(len(elements))

for e in elements[:3]:

    main = e
    new_mains = name_edits(main) #name edits

    for item in c3_chem:
        cas_keys = []
        names = []

        for name in c3_chem[item]['names']:
            if len(names) == 1:
                break
            for edit in new_mains:

                if re.fullmatch(edit, name, re.IGNORECASE):  # check for match of each edited name in each set of c3 names
                    names.append(item)
                    break

        if len(names) != 0:
            pcp_cmpds = pcp.get_compounds(names[0], 'name')
                        # if any hit within individual name group, search all names in name group through pubchem
            for result in pcp_cmpds:
                for res in result.synonyms:
                    if re.search('[0-9-]', res) and not re.search('[a-zA-Z]', res):  # find cas keys
                        cas_keys.append(res)
                    if re.search('^(CAS-)\d+-', res):  # find cas keys in format CAS-###-##-#
                        split = res.split("-")[1:]
                        s = "-"
                        cas_keys.append(s.join(split))
                        break

                    break  # once match is found in set of names and cas keys extracted, move to next name

        if len(cas_keys) == 0:
            cas_keys.append(name)  # get smiles via c3 name not cas key

        smiles_extraction(cas_keys, main)

with open(ROOT_PATH+"/PDB-input/smiles_dictionary_c3_mainedits_1-3.json", "w") as json_output:
    json.dump(new_smiles, json_output, indent=4, separators=(',', ': '))



