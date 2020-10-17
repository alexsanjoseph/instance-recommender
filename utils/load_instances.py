import json

with open('utils/instances.json') as f:
    instances_json = json.loads(f.read())

print(json.dumps(instances_json[0]))