import os
import requests
import copy
import json
import boto3
from botocore import UNSIGNED
from botocore.client import Config


def build_pricing_inventory(dest,
                            excluded_regions,
                            raw_inventory_path='utils/instances.json',
                            refresh=False,
                            indent=2):
    if refresh:
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

        s3.download_file('www.ec2instances.info', 'instances.json',
                         raw_inventory_path)

    with open(raw_inventory_path, 'r') as instances_json_file:
        instances_json = json.loads(instances_json_file.read())

    final_list = []
    for instance in instances_json:
        final_dict = {
            'name': instance['instance_type'],
            'vcpus': instance['vCPU'],
            'memory': instance['memory'],
            'arch': instance['arch'][0],
            'pricing': {}
        }
        try:
            for region, prices in instance['pricing'].items():
                if region not in excluded_regions:
                    try:
                        final_dict['pricing'][region] = prices['linux'][
                            'ondemand']
                    except KeyError as e:
                        print(
                            'Cannot parse linux pricing for instance {0} in region {1}'     # noqa
                            .format(instance['instance_type'], region))
        except Exception as e:
            print('Cannot parse pricing for instance {0}'.format(
                instance['instance_type']))
        final_list.append(final_dict)
    with open(dest, 'w+') as region_file:
        region_file.write(json.dumps(final_list, indent=indent))


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--download',
                           '-d',
                           action='store_true',
                           default=True,
                           help='Download new inventory')
    args = argparser.parse_args()
    build_pricing_inventory(dest='inventory/instances.json',
                            excluded_regions=['cn-north-1', 'cn-northwest-1'],
                            refresh=args.refresh)
