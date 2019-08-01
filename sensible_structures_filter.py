import json, xmltodict, requests
from xml.dom.minidom import parseString
from collections import OrderedDict

base_uri = 'http://xtuition.ccr.buffalo.edu/api'
search_endpoint = base_uri + '/search'
auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}

name_changes = open("/projects/academic/esnell/kferger/pubchem_extraction.out", "r")
names = name_changes.readlines()

outfile = open("/projects/academic/esnell/kferger/PDB-input/sensible_structures_final_oneentry.json", "w")

file = open("/projects/academic/esnell/kferger/PDB-input/sensible_structures.xml", "r")
data = file.read()
dom = parseString(data)
doc = xmltodict.parse(data)
length = len(dom.getElementsByTagName('structure'))

#print(doc['structures']['structure'][2]['compounds']['compound'])
name_dict = {}
for name in names:
    split = name.split(":")
    old = split[0]
    new = split[1].strip("\n")
    name_dict[old] = new

for j in range(length):
    for item in name_dict.items():
        if type(doc['structures']['structure'][j]['compounds']['compound']) == OrderedDict:

            if doc['structures']['structure'][j]['compounds']['compound']['name'] == item[0]:
                doc['structures']['structure'][j]['compounds']['compound']['name'] = item[1]

        elif type(doc['structures']['structure'][j]['compounds']['compound']) == list:
            num_compounds = len(doc['structures']['structure'][j]['compounds']['compound'])

            for k in range(num_compounds):
                if doc['structures']['structure'][j]['compounds']['compound'][k]['name'] == item[0]:
                    doc['structures']['structure'][j]['compounds']['compound'][k]['name'] = item[1]


structures = []
structure_dict = {}
for k in range(length):
    count = 0

    for i in range(324):

        r = requests.get(base_uri + "/compound/" + str(i + 1), headers=auth)
        cmpd = r.json()
        xtuition_name = cmpd['name']

        if type(doc['structures']['structure'][k]['compounds']['compound']) == OrderedDict:
            if doc['structures']['structure'][k]['compounds']['compound']['name'] == xtuition_name:
                #json.dump(doc['structures']['structure'][k]'\n', outfile, indent=4, separators=(',', ': '))#don't know if the newline character will actually work
                structures.append(doc['structures']['structure'][k])

        elif type(doc['structures']['structure'][k]['compounds']['compound']) == list:
            num_compounds = len(doc['structures']['structure'][k]['compounds']['compound'])
            #print(num_compounds)

            for m in range(num_compounds):
                if doc['structures']['structure'][k]['compounds']['compound'][m]['name'] == xtuition_name:
                    count += 1
                    continue

            if count == num_compounds:
                print(doc['structures']['structure'][k])
                structures.append(doc['structures']['structure'][k])
                #json.dump(doc['structures']['structure'][k]'\n', outfile, indent=4, separators=(',', ': '))
                break

structure_dict['structures'] = structures
json.dump(structure_dict, outfile, indent=4, separators=(',', ': '))
