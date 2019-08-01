import json

"""

f1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_1-15.json", "r")
f2 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_15-60.json", "r")
f3 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_61-100.json", "r")
f4 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_101-150.json", "r")
f5 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_151-200.json", "r")
f6 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_201-275.json", "r")
f7 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_276-356.json", "r")

c3_1_15 = json.load(f1)
c3_15_60 = json.load(f2)
c3_61_100 = json.load(f3)
c3_101_150 = json.load(f4)
c3_151_200 = json.load(f5)
c3_201_275 = json.load(f6)
c3_276_356 = json.load(f7)

f1_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_1-15_1.json", "r")
f2_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_15-60_1.json", "r")
f3_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_61_100_1.json", "r")
f4_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_101-150_1.json", "r")
f5_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_151-200_1.json", "r")
f6_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_201-275_1.json", "r")
f7_1 = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_276-356_1.json", "r")

c3_1_15_1 = json.load(f1_1)
c3_15_60_1 = json.load(f2_1)
c3_61_100_1 = json.load(f3_1)
c3_101_150_1 = json.load(f4_1)
c3_151_200_1 = json.load(f5_1)
c3_201_275_1 = json.load(f6_1)
c3_276_356_1 = json.load(f7_1)

ogs = [c3_1_15, c3_15_60, c3_61_100, c3_101_150,  c3_151_200, c3_201_275, c3_276_356]
reruns = [c3_1_15_1, c3_15_60_1, c3_61_100_1, c3_101_150_1,  c3_151_200_1, c3_201_275_1, c3_276_356_1]

"""


"""
f1 = open("/projects/academic/esnell/kferger/PDB-input/cas_dictionary_c3.json", "r")
f2 = open("/projects/academic/esnell/kferger/PDB-input/cas_dictionary_c3_1.json", "r")

c3 = json.load(f1)
c3_1 = json.load(f2)


#for element in ogs:
#for k,v in list(element.items()):
for k,v in list(c3.items()):
    if v == [[]]:
        del c3[k]

#for i in range(len(ogs)):
    #for name in reruns[i]:
for name in c3_1:
        #if name not in ogs[i]:
    if name not in c3:
            #if reruns[i][name] != [[]]:
        if c3_1[name] != []:
                #ogs[i][name] = reruns[i][name]
            c3[name] = c3_1[name]

#for og in ogs:
    #for rerun in reruns:
        #for name in rerun:
            #if name not in og:
                #if rerun[name] != [[]]:
                    #og[name] = rerun[name] #adding elements to og files only present in rerun files

#compiled = [c3_1_15, c3_15_60, c3_61_100, c3_101_150,  c3_151_200, c3_201_275, c3_276_356]

#for i in range(len(compiled)-1):
    #c3_1_15.update(compiled[i+1])

#with open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_compiled.json", "w") as outfile:

with open("/projects/academic/esnell/kferger/PDB-input/cas_dictionary_c3_compiled.json", "w") as outfile:
    #json.dump(c3_1_15, outfile, indent=4, separators=(',', ': '))
    json.dump(c3, outfile, indent=4, separators=(',', ': '))
"""
with open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_compiled_final.json", "r") as infile:
    c3_compiled = json.load(infile)

    c3_smiles = open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary.json", "r")
    c3_json = json.load(c3_smiles)

    cas_compiled = open("/projects/academic/esnell/kferger/PDB-input/cas_dictionary_c3.json", "r")
    cas_json = json.load(cas_compiled)

    for i, j in list(cas_json.items()): #add smiles (matched) info to each value in cas dictionary
        for name, smiles in list(c3_compiled.items()):
            if name == i:
                cas_json[name] = [j,smiles]


    for i, j in list(cas_json.items()): #add smiles info from orig. smiles_dictionary.json to each value in cas dictionary
        for name, smiles in list(c3_json.items()):
            if not isinstance(j, list):
                if name == i:
                    if smiles != "":
                        cas_json[name] = [j,smiles]
                    else:
                        cas_json[name] = name


    for name1 in c3_compiled:
        if name1 not in cas_json:
            if c3_compiled[name1] != [[]]:
                cas_json[name1] = [c3_compiled[name1]]

    for item in c3_json:
        if c3_json[item] != "":
            if item not in cas_json:
                cas_json[item] = [c3_json[item]]


    #with open("/projects/academic/esnell/kferger/PDB-input/smiles_dictionary_c3_compiled_final.json", "w") as outfile1:
    with open("/projects/academic/esnell/kferger/PDB-input/cas_dictionary_c3_final.json", "w") as outfile1:
        #json.dump(c3_compiled, outfile1, indent=4, separators=(',', ': '))
        json.dump(cas_json, outfile1, indent=4, separators=(',', ': '))
"""
import json
with open("/Users/kaileyferger/Downloads/cas_dictionary_c3_compiled_final.json", "r") as json_file:
    c3 = json.load(json_file)
    m = 0
    for element in c3:
        m+=1
    print(m)
"""