import json, sys

with open(sys.argv[1], 'r') as file_handle:
    bp_data = json.load(file_handle)

final = []

# Delete empty, invalid props
for object_property in bp_data:
    property_keys = object_property.keys()
    if len(property_keys) == 1:
        if "export_type" in property_keys:
            print("DELETE: dict (size=1) - [0] == export_type, value ==", object_property["export_type"])
            continue
        else:
            print("INTACT: dict (size=1) - [0] != export_type, [0] ==", property_keys[0])
    final.append(object_property)

with open(sys.argv[2], 'w') as file_handle:
    file_handle.write(json.dumps(final, indent=2, sort_keys=True))
