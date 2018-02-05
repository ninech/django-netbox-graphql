
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




class RoleTestCase(TestCase):
    def test_creating_new_role(self):
        query = '''
        mutation{
          newVlanRole(input: { name: "VlanRole 1", slug: "vlanrole-1", weight: 1001}) {
            vlanRole{
              id
              name
              slug
              weight
            }
          }
        }
        '''
        expected = {'newVlanRole': {'vlanRole': {'id': 'Um9sZU5vZGU6MQ==',
                                                 'name': 'VlanRole 1', 'slug': 'vlanrole-1', 'weight': 1001}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_role(self):
        initialize_vlan_role('11')
        query = '''
        {
          vlanRoles(id: "Um9sZU5vZGU6MTE=") {
            edges {
              node {
                id
                slug
                name
                weight
              }
            }
          }
        }
        '''
        expected = {'vlanRoles': {'edges': [{'node': {
            'id': 'Um9sZU5vZGU6MTE=', 'slug': 'vlanrole-11', 'name': 'VlanRole11', 'weight': 1000}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_role(self):
        initialize_vlan_role('13')
        query = '''
        mutation{
          updateVlanRole(input: { id: "Um9sZU5vZGU6MTM=", name: "VlanRole A", slug: "vlanrole-a", weight: 1002}) {
            vlanRole{
              id
              name
              slug
              weight
            }
          }
        }
        '''
        expected = {'updateVlanRole': {'vlanRole': {'id': 'Um9sZU5vZGU6MTM=',
                                                    'name': 'VlanRole A', 'slug': 'vlanrole-a', 'weight': 1002}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_role(self):
        initialize_vlan_role('12')
        query = '''
        mutation{
          deleteVlanRole(input: { id: "Um9sZU5vZGU6MTI=" }) {
            vlanRole{
              id
              name
              slug
              weight
            }
          }
        }
        '''
        expected = {'deleteVlanRole': {'vlanRole': {'id': 'Um9sZU5vZGU6Tm9uZQ==',
                                                    'name': 'VlanRole12', 'slug': 'vlanrole-12', 'weight': 1000}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
