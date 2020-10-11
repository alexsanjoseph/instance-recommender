# from

from instance_recommender.instance_list import get_list_of_instances
from scipy.optimize import linprog
import numpy as np
import pandas as pd


def best_reco(required_resources, instance_df):
    A = -np.array(instance_df.loc[:, ['vcpus', 'memory']]).T
    c = np.array(instance_df.loc[:, ['price']])
    b = -np.array([required_resources[x] for x in ['vcpus', 'memory']])
    res = linprog(c, A_ub=A, b_ub=b)

    return pd.DataFrame({
        'name': instance_df['name'],
        'units': np.ceil(np.round(res.x, 2)).astype(int)
    })
