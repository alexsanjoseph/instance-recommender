#!/bin/python3
import argparse
import math
from .recommender import best_reco
from .instance_list import get_list_of_instances

argument_parser = argparse.ArgumentParser(description='Get instance recommendations for a distributed EC2 setup')
argument_parser.add_argument('--vcpus', required=True, help='Total number of vcpus required', type=int)
argument_parser.add_argument('--max-vcpus', required=True, help='Maximum number of vCPUs per instance', type=int)
argument_parser.add_argument('--min-vcpus', default=0, help='Minimum number of vCPUs per instance', type=int)
argument_parser.add_argument('--memory', required=True, help='Total amount of memory needed in GB', type=int)
argument_parser.add_argument('--max-memory', required=True, help='Maximum memory in GBs per instance', type=int)
argument_parser.add_argument('--min-memory', default=0, help='Minimum memory in GBs per instance', type=int)
argument_parser.add_argument('--exclude-burstable', action='store_true', default=False, help='Exclude instance types of burstable type: t2, t3, t3a, etc.')
argument_parser.add_argument('--arch', default='x86_64', help='Architecture of instances in the group', type=str)
argument_parser.add_argument('--region', default='us-east-1', help='Region for the instance', type=str)

args = argument_parser.parse_args()
output = best_reco(
    required_resources = {
        "memory": args.memory,
        "vcpus": args.vcpus
    },
    instance_df=get_list_of_instances({
        "vcpus": {
            "min": args.min_vcpus,
            "max": args.max_vcpus
        },
        "memory": {
            "min": args.min_memory,
            "max": args.max_memory
        },
        "exclude_burstable": args.exclude_burstable,
        "arch": args.arch,
        "region": args.region
    }))
print(output[output.units > 0])
