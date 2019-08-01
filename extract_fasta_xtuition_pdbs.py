import requests


ids = open("/Users/kaileyferger/Desktop/Max Dudek HWI Project/xTuitionXrayPdbs.txt", "r")
"""
fasta_seqs = open("/Users/kaileyferger/Downloads/xtuition_pdbs.fasta", "w")

#request = requests.get('https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList=4HHB'
        #               '&compressionType=uncompressed', timeout=10)
for id in ids:
    id.strip('\n').strip('\n')
    request = requests.get('https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+id+
                           '&compressionType=uncompressed', timeout=10)
    fasta_seqs.write(request.text)

ids.close()
fasta_seqs.close()
"""
id_list = []
quality_metrics = open("/Users/kaileyferger/Downloads/xtuition_IDs_quality_metrics.csv", "w")
for line in ids:
    id_list.append(line.strip('\n'))
id_string = ','.join(id_list)

request = requests.get("http://www.rcsb.org/pdb/rest/customReport.xml?pdbids="+id_string+"&customReportColumns"
                       "=resolution,averageBFactor,rFree,rAll,rObserved,rWork,"
                       "&service=wsfile&format=csv", timeout=10)
quality_metrics.write(request.text)

ids.close()
quality_metrics.close()
