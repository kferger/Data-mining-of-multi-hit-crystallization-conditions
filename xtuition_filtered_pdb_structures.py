import csv

ids = open("/Users/kaileyferger/Desktop/Max Dudek HWI Project/xTuitionXrayPdbs.txt", "r")
filtered_structures = open("/Users/kaileyferger/Downloads/xtuition_filtered_sensible_structures.csv", "w")
id_list = []

for id in ids:
    id_list.append(id.strip('\n'))


pdb_structures = open("/Users/kaileyferger/Desktop/Max Dudek HWI Project/crystallizationDatabase/Output/"
                      "sensible_structures.csv", "r")
pdbs = csv.reader(pdb_structures, delimiter='\t')
pdb_lines = list(pdbs)

pdb_writer = csv.writer(filtered_structures, delimiter='\t')

for i in id_list:
    for row in pdb_lines:
        if i in row:
            pdb_writer.writerow(row)
       # else:
            #print("not found")

filtered_structures.close()
pdb_structures.close()


