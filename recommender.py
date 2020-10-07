# from

from instance_list import get_list_of_instances
from scipy.optimize import linprog
import numpy as np
import pandas as pd


def best_reco(required_resources, instance_df):
    A = -np.array(instance_df.loc[:, ['vcpu', 'mem']]).T
    c = np.array(instance_df.loc[:, ['price']])
    b = -np.array([required_resources[x] for x in ['vcpu', 'memory']])
    res = linprog(c, A_ub=A, b_ub=b)

    return pd.DataFrame({
        'name': instance_df['name'],
        'units': np.ceil(np.round(res.x, 2)).astype(int)
    })


def display_output(output):
    print(output[(output.units > 0)])


if __name__ == "__main__":
    constraints = {"vcpu": {"min": 4, "max": 64}}

    instance_df = get_list_of_instances(constraints)

    required_resources = {"vcpu": 17, "memory": 86}

    output = best_reco(required_resources, instance_df)
    display_output(output)
