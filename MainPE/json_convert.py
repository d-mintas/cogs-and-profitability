"""
Created: 1/11/2016
d.mintas


Description:

Converts incoming JSON data to NumPy ndArrays -- necessary
for compatability with the ML in the main module.

Accepts: A JSON-formatted string representing the design specs for \
one or more designs.

Returns: Two ndArrays, able to be used by the xgBoost code in the \
top-level module.

"""


# TODO: Include in docstring the scheme for the JSON object.
# TODO: Include in docstring schema for the returned ndArrays.


import json
import numpy as np


def get_ndas(json_string):
    js = json.loads(json_string)

    if len(js[0] == 5):
        nda_list = ndas_no_id(js)
    else:
        nda_list = ndas_with_id(js)

    return(nda_list)


def ndas_no_id(js):
    np_data = [v in r for r in js]
