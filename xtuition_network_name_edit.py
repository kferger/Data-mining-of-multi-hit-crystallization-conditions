import csv

#new_csv = open("/Users/kaileyferger/Downloads/xtuition_pdbs_fasta Full Network short description.csv", "w")


with open("/Users/kaileyferger/Downloads/xtuition_pdbs_fasta Full Network short description.csv", "w") as new_csv:
    pdb_writer = csv.writer(new_csv, delimiter=",")
    pdb_writer.writerow(['SUID', 'Description', 'name', 'Other IDs', 'selected', 'Sequence', 'Sequence Length',
                         'Sequence Source', 'shared name'])
    with open("/Users/kaileyferger/Downloads/xtuition_pdbs_fasta Full Network default node.csv", "r") as csvfile:
        network_nodes = csv.reader(csvfile, delimiter = ",")
        next(network_nodes, None)
        for line in network_nodes:
            pdb_id = line[1].split("|")
            line[1] = pdb_id[0]
        #print(line)
            pdb_writer.writerow(line)

#new_csv.close()

