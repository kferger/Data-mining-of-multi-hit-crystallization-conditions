import requests

base_uri = 'http://xtuition.org/api'
search_endpoint = base_uri + '/search'
auth = {'Authorization': 'Bearer 9d89e79c-ed4d-11e5-8042-00270e10b7a7'}


# Fetch all samples with verified crystals
payload = {'query': 'crystals +pdb'}
r = requests.get(search_endpoint, headers=auth, params=payload)
samples = r.json()
#print(samples['samples'][1])
"""
{'sample_id': 930, 'screen_id': 6, 'xnumber': 'X000008303', 'pnumber': 'P000008323', 'molar_concentration': None, 
'difference_from_purification': None, 'date_purified': '2007-01-24T00:00:00Z', 'setup_date': '2007-02-02T00:00:00Z',
 'instructions': None, 'setup_notes_before': None, 'post_translational_modification': None, 
 'sample_additional_notes': None, 'setup_notes_after_delivery': None, 'volume_units': None, 'volume_sent': None, 
 'experimental_molecular_weight': None, 'sample_ph': None, 'concentration': None, 'concentration_units': None, 
 'name': 'UPF0341 protein yhiQ', 'spine_target_id': 'SfR275', 'spine_status': 'X-Ray structure', 'pfam': 'PF04445', 
 'pi': '6.60', 'ext': 18450, 'length': '250 aa', 'mass': '26.92 kD', 'organism': 'Shigella flexneri', 'sequence': None,
  'gene': None, 'genus': None, 'species': None, 'strain': None, 'wells': 9216, 'verified_crystals': 461, 
  'classified': 9216, 'screen_name': 'HWI Generation 7', 'structures': None, 'dbrefs': None}
"""

#fetch all wells for first sample
sample1 = samples['samples'][0]
endpoint = base_uri + '/sample/' + str(sample1['sample_id']) + '/list'
payload = {'crystals': '1'}
r = requests.get(endpoint, headers=auth, params=payload)
wells = r.json()
print(wells['wells'][])
"""
{'well_id': 5660167, 'cocktail_name': '7_C0569', 'cocktail_id': 9183, 'sample_id': 916, 'name': 'X0000082731505', 
'read_number': 'X0000082731505200702021518', 'read_date': '2007-02-02T15:18:00Z', 'week': 2, 'verified_crystal': True, 
'class_3way': 'crystal', 'class_10way': 'crystal', 'cocktail': None}
"""