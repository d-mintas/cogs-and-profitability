import argparse
import json

import numpy as np
import xgboost as xgb



"""
jd = {"qty": qty, "totImps": totImps, "maxInks": maxInks, "totInks": totInks, "locs": locs, "gini": gini}

in_values = json.loads(jd) 
"""



dim_names = ['qty', 'totImps', 'maxInks', 'totInks', 'locs', 'gini']

dtrain = xgb.DMatrix('dtrain_DMatrix.data')
dtest = xgb.DMatrix('dtest_DMatrix.data')

params = {'bst:max_depth': 2, 'bst:eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
params['eval_metric'] = ['auc', 'error']

eval_list = [(dtest, 'eval'), (dtrain, 'train')]

num_rounds = 10

bst = xgb.train(params, dtrain, num_rounds, eval_list)

in_data = np.ndarray([1, 6])
out_data = np.ndarray([1, 1])


# TODO: This will accept JSON data rather than stdin.
# Import module that parses JSON to numpy arrays and
# also module that calculate Gini coefficient, then
# feed in here.

for col in list(range(6)):
	print(dim_names[col] + ': ', end='')
	in_data[0, col] = float(input())

xgmat = xgb.DMatrix(in_data)

ypred = bst.predict(xgmat)


# TODO: Job time placeholder - import module that predicts the
# actual value and feed it in here. Same goes for fixed cost
# placeholders.

y_label = round(ypred[0])
y_prob = ypred[0]
alc = auto_labor_cost = (in_data[0, 1] / 62.5) * 13.
mlc = manual_labor_cost = (in_data[0, 1] / 37.5) * 11.

#results = {'press_type': }

print(y_label, y_prob, alc, mlc)


