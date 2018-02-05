
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




class VlANTestCase(TestCase):
    def test_creating_new_vlan(self):
        initialize_vlan_role('189')
        initialize_tenant('189')
        query = '''
        mutation{
          newVlan(input: { tenant: "VGVuYW50Tm9kZToxODk=", role: "Um9sZU5vZGU6MTg5", vid: 2, name: "vlan2", description: "test"}) {
            vlan{
              id
              name
              tenant{
                name
              }
              role{
                name
              }
              vid
              name
              description
            }
          }
        }
        '''
        expected = {'newVlan': {'vlan': {'id': 'VkxBTk5vZGU6MQ==', 'name': 'vlan2', 'tenant': {
            'name': 'Tenant 189'}, 'role': {'name': 'VlanRole189'}, 'vid': 2, 'description': 'test'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_vlan(self):
        initialize_vlan('188')
        query = '''
        {
          vlans(id: "VkxBTk5vZGU6MTg4") {
            edges {
              node {
                id
                name
                description
                vid
                tenant {
                  name
                }
                role {
                  name
                }
              }
            }
          }
        }
        '''
        expected = {'vlans': {'edges': [{'node': {'id': 'VkxBTk5vZGU6MTg4', 'name': 'vlan188', 'description': 'desc', 'vid': 2, 'tenant': {
            'name': 'Tenant 188'}, 'role': {'name': 'VlanRole188'}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_vlan(self):
        initialize_vlan('191')
        query = '''
        mutation{
          updateVlan(input: { id:"VkxBTk5vZGU6MTkx", vid: 3, name: "vlanA", description: "desc"}) {
            vlan{
              id
              name
              vid
              name
              description
            }
          }
        }
        '''
        expected = {'updateVlan': {'vlan': {'id': 'VkxBTk5vZGU6MTkx',
                                            'name': 'vlanA', 'vid': 3, 'description': 'desc'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_vlan(self):
        initialize_vlan('183')
        query = '''
        mutation{
          deleteVlan(input: { id:"VkxBTk5vZGU6MTgz"}) {
            vlan{
              id
            }
          }
        }
        '''
        expected = {'deleteVlan': {'vlan': {'id': 'VkxBTk5vZGU6Tm9uZQ=='}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
