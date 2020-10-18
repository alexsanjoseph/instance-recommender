from instance_recommender.inventory import Inventory
from unittest import TestCase
import json
import pandas

class TestInventory(TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.source_path = 'inventory/instances.json'
        self.dest_path = '/tmp/test_inventory.json'

    def create_inventory(self):
        return Inventory(source_url='file://{}'.format(self.source_path), inventory_file_path=self.dest_path, refresh=True)

    
    def test_inventory_object_creates(self):
        inventory = self.create_inventory()
        with open(self.source_path, 'r') as source_file:
            source = json.loads(source_file.read())
        with open(self.dest_path, 'r') as dest_file:
            dest = json.loads(dest_file.read())
        assert source == dest

    def test_get_inventory_constraints(self):
        inventory = self.create_inventory()
        pricing_with_constraints = inventory.get_pricing_with_constraints(constraints={'region': 'us-east-1', 'exclude_burstable': False, 'arch': 'x86_64'})
        assert len(pricing_with_constraints.columns) == 5


        


