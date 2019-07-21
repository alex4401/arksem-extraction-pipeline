import sys
import json
from collections import OrderedDict

IGNORED_EMPTY_PROPERTIES = [
    "BoolProperty", "ObjectProperty", "FloatProperty", "Function"
]

def make_unique(key, dct):
    counter = 0
    unique_key = key

    while unique_key in dct:
        counter += 1
        unique_key = '{}_{}'.format(key, counter)
    return unique_key

def parse_object_pairs(pairs):
    dct = OrderedDict()
    for key, value in pairs:
        if key == 'export_type' \
            and type(value) is str \
            and value in IGNORED_EMPTY_PROPERTIES:
            continue
        if key in dct:
            key = make_unique(key, dct)
        dct[key] = value
    return dct

def clean_final_object(arr):
    final_arr = []
    for index in range(len(arr)):
        obj = arr[index]
        if type(obj) is OrderedDict \
            and len(obj) == 0:
            continue
        final_arr.append(obj)
    return final_arr

decoder = json.JSONDecoder(object_pairs_hook=parse_object_pairs)
with open(sys.argv[1], 'r') as file_handle:
    bp_data = decoder.decode(file_handle.read())
    bp_data = clean_final_object(bp_data)
    with open(sys.argv[2], 'w') as file_handle:
        file_handle.write(json.dumps(bp_data, indent=2, sort_keys=True))
