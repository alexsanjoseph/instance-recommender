import os
import requests

import json
import boto3
from botocore import UNSIGNED
from botocore.client import Config

def update_instances_json():
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    s3.download_file('www.ec2instances.info', 'instances.json', 'utils/instances.json')


def build_regional_pricing(region):
    with open('utils/instances.json', 'r') as instances_json_file:
        instances_json = json.loads(instances_json_file.read())
    final_list = []
    for instance in instances_json:
        try:
            final_list.append({
                    "name": instance['instance_type'],
                    "mem": instance['memory'],
                    "vcpu": instance["vCPU"],
                    "price": instance['pricing'][region]['linux']['ondemand']
                })
        except KeyError as e:
            print("WARNING  Cannot find {0} in region {1}".format(instance["instance_type"], region))
    with open('regions/{}'.format(region), 'w+') as region_file:
        region_file.write(json.dumps(final_list))


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--refresh', action='store_true', default=False)
    args = argparser.parse_args()

    if args.refresh:
        update_instances_json()
    
    build_regional_pricing('us-east-1')

