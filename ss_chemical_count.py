import xml.etree.ElementTree as ET

uniq_names = []

tree = ET.parse("/projects/academic/esnell/kferger/PDB-input/sensible_structures.xml")
root = tree.getroot()
for name in root.iter('name'):
    if name not in uniq_names:
        uniq_names.append(name)
print('Total number of unique compounds: {}'.format(len(uniq_names)))