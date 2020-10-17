import os
import requests
import copy
import json
import boto3
from botocore import UNSIGNED
from botocore.client import Config

def update_instances_json():
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    s3.download_file('www.ec2instances.info', 'instances.json', 'utils/instances.json')


def build_regional_pricing():
    with open('utils/instances.json', 'r') as instances_json_file:
        instances_json = json.loads(instances_json_file.read())
    final_list = []
    for instance in instances_json:
        instance_copy = copy.deepcopy(instance)
        try:
            for region, prices in instance['pricing'].items():
                print(prices.keys())
                try:
                    instance_copy['pricing'][region] = prices['linux']['ondemand']
                except KeyError as e:
                    print('Cannot parse linux pricing for instance {0} in region {1}'.format(instance['instance_type'], region))
        except Exception  as e:
            print('Cannot parse pricing for instance {0}'.format(instance['instance_type']))
        final_list.append(instance_copy)
    with open('instance_recommender/static/regions/all', 'w+') as region_file:
        region_file.write(json.dumps(final_list))


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--refresh', action='store_true', default=False)
    args = argparser.parse_args()

    if args.refresh:
        update_instances_json()
    
    build_regional_pricing()

