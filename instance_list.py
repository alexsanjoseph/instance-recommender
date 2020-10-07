import json
import pandas

def get_list_of_instances(constraints):
    with open('regions/us-east-1') as f:
        df = pandas.DataFrame(json.loads(f.read()))
    if 'vcpu' in constraints:
        df =  df[(df.vcpu > constraints['vcpu']['min']) & (df.vcpu < constraints['vcpu']['max'])]
    if 'mem' in constraints:
        df =  df[(df.mem > constraints['mem']['min']) & (df.mem < constraints['mem']['max'])]
    return df

