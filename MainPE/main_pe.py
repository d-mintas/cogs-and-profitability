"""
Created: 1/08/2016
d.mintas


Description:

Top-level module for profitability estimation.

Accepts: For now- a text file containing JSON-formatted data, representing \
one or more orders (which comprise one or more design tabs - this is the \
level of granularity the algorithm actually operates at).

Returns: Dollar cost, auto/manual prediction (auto=1, manual=0), auto/manual \
'confidence' level (really the raw probability returned by xgBoost), \
and predicted cost of auto vs. manual printing for the given design(s) - \
also JSON-formatted.

"""


import argparse
import json

import numpy as np
import xgboost as xgb

import json_convert


# Parse name of text file passed through CLI and store as variable.
parser = argparse.ArgumentParser()

parser.add_argument(
    "json_file", help="Accepts JSON data stored in a text file, in the \
    following format: \
    [ {qty, totImps, maxInks, totInks, printAreas, id}, {...}, ... ]")

args = parser.parse_args()
input_filename = args.json_file


# Read file contents -> convert from JSON string to Python dict.
with open(input_filename) as jf:
    jd = json.load(jf)


# Call function in 'json_convert' module to prepare data for xgBoost.
xg_full_mat = json_convert.get_ndas(jd)


"""
jd = {"qty": qty, "totImps": totImps, "maxInks": maxInks, "totInks": \
totInks, "locs": locs, "gini": gini}

in_values = json.loads(jd)
"""


dim_names = ['qty', 'totImps', 'maxInks', 'totInks', 'locs', 'gini']

dtrain = xgb.DMatrix('dtrain_DMatrix.data')
dtest = xgb.DMatrix('dtest_DMatrix.data')

params = {'bst:max_depth': 2, 'bst:eta': 1,
          'silent': 1, 'objective': 'binary:logistic'}
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

# results = {'press_type': }

print(y_label, y_prob, alc, mlc)
