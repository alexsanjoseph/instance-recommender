
import pandas as pd
from pulp import *


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def best_reco(required_resources, instance_df):
    prob = LpProblem("InstanceRecommender", LpMinimize)

    instances = instance_df['name'].values
    instance_dict = instance_df.set_index('name').T.to_dict()
    instance_vars = LpVariable.dicts(
        "Instance", instances, lowBound=0, cat='Integer')

    prob += lpSum([instance_dict[i]['price'] * instance_vars[i]
                   for i in instances])
    prob += lpSum([instance_dict[i]['vcpus'] * instance_vars[i]
                   for i in instances]) >= required_resources['vcpus']
    prob += lpSum([instance_dict[i]['memory'] * instance_vars[i]
                   for i in instances]) >= required_resources['memory']

    prob.solve()
    print("Status:", LpStatus[prob.status])
    best_reco = pd.DataFrame([
        {'name': remove_prefix(v.name, "Instance_"), 'units': v.varValue}
        for v in prob.variables() if v.varValue > 0]
    )

    best_reco = best_reco.merge(instance_df)
    return best_reco
