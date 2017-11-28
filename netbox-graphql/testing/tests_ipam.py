import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_vlan_role, initialize_vlan_group, initialize_site, initialize_vlan, initialize_tenant, initialize_vrf
from ..schema import schema
from ..helper_methods import print_result

pytestmark = pytest.mark.django_db

class FieldsTestCase(TestCase):
    def test_vlan_roles(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          vlanRoles {
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
        '''))
    def test_vlan_groups(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          vlanGroups {
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
        '''))

    def test_vlan(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        { vlans {
            edges {
              node {
                id
                name
                description
                vid
                site{
                  name
                }
                group{
                  name
                }
                tenant{
                  name
                }
                role{
                  name
                }
              }
            }
        }
        '''))

    def test_vrf(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          vrfs {
            edges {
              node {
                id
                name
                rd
                description
                enforceUnique
                tenant {
                  name
                }
              }
            }
          }
        }
        '''))

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
        expected = {'newVlanRole': {'vlanRole': {'id': 'Um9sZU5vZGU6MQ==', 'name': 'VlanRole 1', 'slug': 'vlanrole-1', 'weight': 1001}}}

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
        expected = {'vlanRoles': {'edges': [{'node': {'id': 'Um9sZU5vZGU6MTE=', 'slug': 'vlanrole-11', 'name': 'VlanRole11', 'weight': 1000}}]}}

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
        expected = {'updateVlanRole': {'vlanRole': {'id': 'Um9sZU5vZGU6MTM=', 'name': 'VlanRole A', 'slug': 'vlanrole-a', 'weight': 1002}}}

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
        expected = {'deleteVlanRole': {'vlanRole': {'id': 'Um9sZU5vZGU6Tm9uZQ==', 'name': 'VlanRole12', 'slug': 'vlanrole-12', 'weight': 1000}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

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
        expected = {'newVlanGroup': {'vlanGroup': {'id': 'VkxBTkdyb3VwTm9kZTox', 'name': 'VlanRole 1', 'slug': 'vlanrole-1', 'site': {'name': 'Site Name 164'}}}}

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
        expected = {'vlanGroups': {'edges': [{'node': {'id': 'VkxBTkdyb3VwTm9kZToxNjU=', 'name': 'VlanGroup165', 'slug': 'vlangroup-165', 'site': {'name': 'Site Name 165'}}}]}}

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
        expected = {'updateVlanGroup': {'vlanGroup': {'id': 'VkxBTkdyb3VwTm9kZToxNjk=', 'name': 'VlanRole A', 'slug': 'vlanrole-A', 'site': {'name': 'Site Name 169'}}}}

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
        expected = {'deleteVlanGroup': {'vlanGroup': {'id': 'VkxBTkdyb3VwTm9kZTpOb25l', 'name': 'VlanGroup168', 'slug': 'vlangroup-168', 'site': {'name': 'Site Name 168'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

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
        expected = {'newVlan': {'vlan': {'id': 'VkxBTk5vZGU6MQ==', 'name': 'vlan2', 'tenant': {'name': 'Tenant 189'}, 'role': {'name': 'VlanRole189'}, 'vid': 2, 'description': 'test'}}}

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
        expected = {'vlans': {'edges': [{'node': {'id': 'VkxBTk5vZGU6MTg4', 'name': 'vlan188', 'description': 'desc', 'vid': 2, 'tenant': {'name': 'Tenant 188'}, 'role': {'name': 'VlanRole188'}}}]}}

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
        expected = {'updateVlan': {'vlan': {'id': 'VkxBTk5vZGU6MTkx', 'name': 'vlanA', 'vid': 3, 'description': 'desc'}}}

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

class VRFTestCase(TestCase):
    def test_creating_new_vrf(self):
        initialize_vrf('1091')
        query = '''
        mutation{
          newVrf(input: { tenant: "VGVuYW50Tm9kZToxMDkx",  name: "vrf", rd: "rd", enforceUnique: true, description: "desc" }) {
            vrf{
                id
                name
                rd
                description
                enforceUnique
                tenant {
                name
              }
            }
          }
        }
        '''
        expected = {'newVrf': {'vrf': {'id': 'VlJGTm9kZTox', 'name': 'vrf', 'rd': 'rd', 'description': 'desc', 'enforceUnique': True, 'tenant': {'name': 'Tenant 1091'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_vrf(self):
        initialize_vrf('1092')
        query = '''
        {
          vrfs(id: "VGVuYW50Tm9kZToxMDky") {
            edges {
              node {
                id
                name
                rd
                description
                enforceUnique
                tenant {
                  name
                }
              }
            }
          }
        }
        '''
        expected = {'vrfs': {'edges': [{'node': {'id': 'VlJGTm9kZToxMDky', 'name': 'vrf1092', 'rd': 'rd1092', 'description': 'description', 'enforceUnique': True, 'tenant': {'name': 'Tenant 1092'}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_vrf(self):
        initialize_vrf('2099')
        query = '''
        mutation{
          updateVrf(input: { id: "VlJGTm9kZToyMDk5", name: "vrfUpdate", rd: "rdUpdate", description: "desc" }) {
            vrf{
                id
                name
                rd
                description
                enforceUnique
            }
          }
        }
        '''
        expected = {'updateVrf': {'vrf': {'id': 'VlJGTm9kZToyMDk5', 'name': 'vrfUpdate', 'rd': 'rdUpdate', 'description': 'desc', 'enforceUnique': True}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_vrf(self):
        initialize_vrf('1094')
        query = '''
        mutation{
          deleteVrf(input: { id: "VlJGTm9kZToxMDk0" }) {
            vrf{
               name
            }
          }
        }
        '''
        expected = {'deleteVrf': {'vrf': {'name': 'vrf1094'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
