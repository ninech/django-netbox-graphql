import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class VlANGroupTestCase(TestCase):
    def test_creating_new_vlan_group(self):
        initialize_site('164')
        query = '''
        mutation{
          newVlanGroup(input: { name: "VlanRole 1", slug: "vlanrole-1", site: "U2l0ZU5vZGU6MTY0"}) {
            vlanGroup{
              id
              name
              slug
              site {
                name
              }
            }
          }
        }
        '''
        expected = {'newVlanGroup': {'vlanGroup': {'id': 'VkxBTkdyb3VwTm9kZTox',
                                                   'name': 'VlanRole 1', 'slug': 'vlanrole-1', 'site': {'name': 'Site Name 164'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_vlan_group(self):
        initialize_vlan_group('165')
        query = '''
        {
          vlanGroups(id: "VkxBTkdyb3VwTm9kZToxNjU=") {
            edges {
              node {
                id
                name
                slug
                site {
                  name
                }
              }
            }
          }
        }
        '''
        expected = {'vlanGroups': {'edges': [{'node': {'id': 'VkxBTkdyb3VwTm9kZToxNjU=',
                                                       'name': 'VlanGroup165', 'slug': 'vlangroup-165', 'site': {'name': 'Site Name 165'}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_vlan_group(self):
        initialize_vlan_group('169')
        query = '''
        mutation{
          updateVlanGroup(input: { id:"VkxBTkdyb3VwTm9kZToxNjk=", name: "VlanRole A", slug: "vlanrole-A"}) {
            vlanGroup{
              id
              name
              slug
              site {
                name
              }
            }
          }
        }
        '''
        expected = {'updateVlanGroup': {'vlanGroup': {'id': 'VkxBTkdyb3VwTm9kZToxNjk=',
                                                      'name': 'VlanRole A', 'slug': 'vlanrole-A', 'site': {'name': 'Site Name 169'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_vlan_group(self):
        initialize_vlan_group('168')
        query = '''
        mutation{
          deleteVlanGroup(input: { id:"VkxBTkdyb3VwTm9kZToxNjg="}) {
            vlanGroup{
              id
              name
              slug
              site {
                name
              }
            }
          }
        }
        '''
        expected = {'deleteVlanGroup': {'vlanGroup': {'id': 'VkxBTkdyb3VwTm9kZTpOb25l',
                                                      'name': 'VlanGroup168', 'slug': 'vlangroup-168', 'site': {'name': 'Site Name 168'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
