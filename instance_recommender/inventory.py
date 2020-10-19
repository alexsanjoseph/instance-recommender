import requests
import json
import pandas
import copy

DEFAULT_INVENTORY_FILE_PATH = '/tmp/recommender_instances_inventory.json'


class Inventory():

    def __init__(
            self,
            source_url,
            inventory_file_path=DEFAULT_INVENTORY_FILE_PATH,
            refresh=False):
        self._source_url = source_url
        self._inventory_file_path = inventory_file_path
        self._inventory = {}
        self.update(force_refresh=refresh)

    def refresh(self):
        if not self._source_url.startswith('file://'):
            r = requests.get(self._source_url)
            content = r.content
        else:
            with open(self._source_url.replace('file://', ''), 'r') as source_inventory_file:   # noqa
                content = source_inventory_file.read()
        with open(self._inventory_file_path, 'w+') as inventory_file:
            inventory_file.write(content)

    def update(self, force_refresh=False):
        if force_refresh:
            self.refresh()
        complete = False
        while not complete:
            try:
                with open(self._inventory_file_path, 'r') as inventory_file:
                    self._inventory = json.loads(inventory_file.read())
                complete = True
            except FileNotFoundError as e:
                self.refresh()

    def get_pricing_with_constraints(self, constraints):
        regional_list = []
        for instance in self._inventory:
            filtered_instance_dict = copy.deepcopy(instance)
            try:
                filtered_instance_dict['price'] = instance['pricing'][constraints['region']]    # noqa
                filtered_instance_dict.pop('pricing')
                regional_list.append(filtered_instance_dict)
            except KeyError:
                pass
        df = pandas.DataFrame(regional_list)
        if 'vcpus' in constraints:
            df = df[(df.vcpus >= constraints['vcpus']['min']) &
                    (df.vcpus <= constraints['vcpus']['max'])]
            print(df)
        if 'memory' in constraints:
            df = df[(df.memory >= constraints['memory']['min']) &
                    (df.memory <= constraints['memory']['max'])]
            print(df)
        if 'exclude_burstable' in constraints and constraints['exclude_burstable']:  # noqa
            for burstable_instance_type in ['t4', 't3', 't2']:
                df = df[~df.name.str.startswith(burstable_instance_type)]
            print(df)
        df = df[df.arch == constraints['arch']]
        df['price'] = df['price'].astype(float)
        print(df)
        return df

    def get_available_regions(self):
        regions = []
        for instance in self._inventory:
            regions += instance['pricing'].keys()
        return list(set(regions))
