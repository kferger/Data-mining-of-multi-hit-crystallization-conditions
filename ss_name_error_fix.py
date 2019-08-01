"""
import csv
newfile = open("/Users/kaileyferger/Downloads/sensible_structures.csv","r")
outfile = open("/Users/kaileyferger/Downloads/sensible_structures_edit.csv","w")
csv_reader = csv.reader(newfile, delimiter = '\t')
for line in csv_reader:
    if 'tris-HCl' in line:
        index = line.index('tris-HCl')
        line[index] = 'Tris HCl'
    writer = csv.writer(outfile, delimiter = '\t')
    writer.writerow(line)
"""


import xml.etree.ElementTree as ET

tree = ET.parse("/Users/kaileyferger/Downloads/sensible_structures/sensible_structures_v3.xml")
root = tree.getroot()
for name in root.iter('name'):
    #if name.text == 'tris-HCl':
        #new_name = 'Tris HCl'
        #name.text = new_name
    #if name.text == 'DTT':
        #new_name = 'Dithioerythritol'
        #name.text = new_name
    #if name.text == 'ammonium citrate':
        #new_name = 'Ammonium citrate tribasic'
        #name.text = new_name
    #if name.text == 'sodium dihydrogen phosphate':
        #new_name = 'Sodium phosphate monobasic'
        #name.text = new_name
    #if name.text == 'potassium dihydrogen phosphate':
        #new_name = 'Potassium phosphate monobasic'
        #name.text = new_name
    #if name.text == 'MES':
        #new_name = 'MES hydrate'
        #name.text = new_name
    if name.text == 'potassium phosphate':
        new_name = 'Potassium phosphate tribasic'
        name.text = new_name

#for structure in root:

    #for cmpds in structure[3]:
        #for cmpd in cmpds:
            #if cmpd.text == 'SAM':
                #root.remove(structure)
            #if cmpd.text == 'DDT':
                #root.remove(structure)


#tree.write("/Users/kaileyferger/Downloads/sensible_structures/sensible_structures_v3.xml", encoding='utf8')
