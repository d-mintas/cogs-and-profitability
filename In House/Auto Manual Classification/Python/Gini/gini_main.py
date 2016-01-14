from gini_coef import GRLC as gini
import json_load as jl

jd = jl.getJSON()

d = jd['RECORDS']

for r in d:
	r['gini'] = gini(r['inkCntList'])[0] 

