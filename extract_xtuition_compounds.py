import requests, sys, json
import pandas as pd

#sys.path.append("/Users/kaileyferger/PycharmProjects/BioXFEL_internship/venv/lib/python3.7/site_packages/")

base_uri = 'http://xtuition.ccr.buffalo.edu/api/'
auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}

cmpd_names = []
for i in range(324): #checked total number with try/except
    ind_cmpd = []
    try:
        r = requests.get(base_uri+"compound/"+str(i+1), headers=auth)
        cmpd = r.json()
        ind_cmpd.append(cmpd['name'])
        ind_cmpd.append(cmpd['iupac'])
        ind_cmpd.append(cmpd['common_name'])
        ind_cmpd.append(cmpd['smiles'])
        cmpd_names.append(ind_cmpd)

    except json.decoder.JSONDecodeError:
        print(i)
        sys.exit()

df = pd.DataFrame(cmpd_names, columns = ['name', 'iupac', 'common_name', 'smiles'], index = None)
df.to_csv("/Users/kaileyferger/Downloads/xtuition_compounds.csv", sep='\t', header=True, index=False)
