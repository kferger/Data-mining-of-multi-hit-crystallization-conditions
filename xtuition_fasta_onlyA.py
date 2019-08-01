outfile = open("/Users/kaileyferger/Downloads/xtuition_pdbs_Aonly.fasta", "w")
with open("/Users/kaileyferger/Downloads/xtuition_singleline_pdbs.fasta", "r") as fastafile:
    fasta_list = fastafile.readlines()
    for line in fasta_list:
        if ":A" in line:
            #print(line, fasta_list[fasta_list.index(line)+1])
            outfile.write(line)
            outfile.write(fasta_list[fasta_list.index(line)+1])

outfile.close()

