"""
converts a regular xml input file of PDB IDs, Phs, crystallization conditions, quantities, etc. to json for use in
cockatoo
"""

import xmltodict
import pprint
import json
import sys

with open(sys.argv[1], "r") as xmlfile:
    doc = xmltodict.parse(xmlfile.read())

pp = pprint.PrettyPrinter(indent=4)
with open('sensible_structures.json', 'w') as outfile:
    pp.pprint(json.dumps(doc, outfile))
