import json
import ast
file = open("/projects/academic/esnell/kferger/PDB-input/sensible_structures_final.json", "r")
outfile = open("/projects/academic/esnell/kferger/PDB-input/sensible_structures_final_edit.json", "w")

new_data = " ".join(line.strip() for line in file)

outdict = {}
d = "}{"
if "}{" in new_data:
    s = new_data.split("}{")
for i in range(len(s)-1):
    s[i+1] = "{"+s[i+1]+"}"

outdict['structures'] = s
json.dump(outdict, outfile, indent=4, separators=(',', ': '))

"""
for line in data:
    if "}{" not in line:
        outfile.write(line)
    else:
        split = line.split("}")
        outfile.write("},\n")
        outfile.write(split[1])
        #lines.append(line)
outfile.write("\n}")
#for elem in lines:
    #outfile.write(elem)

file.close()
outfile.close()
"""