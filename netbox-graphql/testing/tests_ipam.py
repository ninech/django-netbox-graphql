import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_vlan_role, initialize_vlan_group, initialize_site, initialize_vlan, initialize_tenant, initialize_vrf, initialize_rir, initialize_aggregate, initialize_ip_address
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

    def test_rir(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          rirs {
            edges {
              node {
                id
                name
                slug
                isPrivate
              }
            }
          }
        }
        '''))

    def test_aggregate(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          aggregates {
            edges {
              node {
                id
                family
                prefix
                rir {
                  id
                  name
                }
                dateAdded
                description
              }
            }
          }
        }
        '''))

    def test_ip_address(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          ipAddress {
            edges {
              node {
                id
                family
                address
                vrf {
                  name
                }
                tenant {
                  name
                }
                interface {
                  name
                }
                natInside {
                  id
                }
                natOutside {
                  id
                }
                description
                status
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

class RIRTestCase(TestCase):
    def test_creating_new_rir(self):
        query = '''
        mutation{
          newRir(input: { name: "rir",  slug: "rir", isPrivate: true }) {
            rir{
                id
                name
                slug
                isPrivate
            }
          }
        }
        '''
        expected = {'newRir': {'rir': {'id': 'UklSTm9kZTox', 'name': 'rir', 'slug': 'rir', 'isPrivate': True}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_rir(self):
        initialize_rir('2')
        query = '''
        {
          rirs(id: "UklSTm9kZToy") {
            edges {
              node {
                id
                name
                slug
                isPrivate
              }
            }
          }
        }
        '''
        expected = {'rirs': {'edges': [{'node': {'id': 'UklSTm9kZToy', 'name': 'rir2', 'slug': 'rir2', 'isPrivate': True}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_rir(self):
        initialize_rir('3')
        query = '''
        mutation{
          updateRir(input: { id:"UklSTm9kZToz", name: "rirA",  slug: "rira", isPrivate: true }) {
            rir{
                id
                name
                slug
                isPrivate
            }
          }
        }
        '''
        expected = {'updateRir': {'rir': {'id': 'UklSTm9kZToz', 'name': 'rirA', 'slug': 'rira', 'isPrivate': True}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_rir(self):
        initialize_rir('1')
        query = '''
        mutation{
          deleteRir(input: { id:"UklSTm9kZTox" }) {
            rir{
                id
                name
                slug
                isPrivate
            }
          }
        }
        '''
        expected = {'deleteRir': {'rir': {'id': 'UklSTm9kZTpOb25l', 'name': 'rir1', 'slug': 'rir1', 'isPrivate': True}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

class AggregateTestCase(TestCase):
    def test_creating_new_aggregate(self):
        initialize_rir('11')
        query = '''
        mutation {
          newAggregate(input: { family: 4, rir: "UklSTm9kZToxMQ==", prefix: "192.0.0.0/12", dateAdded: "2015-01-01", description: "desc" }) {
            aggregate{
                id
                family
                prefix
                rir {
                  id
                  name
                }
                dateAdded
                description
            }
          }
        }
        '''
        expected = {'newAggregate': {'aggregate': {'id': 'QWdncmVnYXRlTm9kZTox', 'family': 'A_4', 'prefix': '192.0.0.0/12', 'rir': {'id': 'UklSTm9kZToxMQ==', 'name': 'rir11'}, 'dateAdded': '2015-01-01', 'description': 'desc'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_aggregate(self):
        initialize_aggregate('14')
        query = '''
        {
          aggregates(id: "QWdncmVnYXRlTm9kZToxNA==") {
            edges {
              node {
                id
                family
                prefix
                rir {
                  id
                  name
                }
                dateAdded
               description
              }
            }
          }
        }
        '''
        expected = {'aggregates': {'edges': [{'node': {'id': 'QWdncmVnYXRlTm9kZToxNA==', 'family': 'A_4', 'prefix': '14.0.0.0/8', 'rir': {'id': 'UklSTm9kZToxNA==', 'name': 'rir14'}, 'dateAdded': '2017-12-12', 'description': 'desc'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_aggregate(self):
        initialize_aggregate('13')
        query = '''
        mutation{
          updateAggregate(input: { id: "QWdncmVnYXRlTm9kZToxMw==", dateAdded: "2017-01-01", description: "desc", prefix: "54.0.0.0/8"}) {
            aggregate{
                id
                family
                prefix
                rir {
                  id
                  name
                }
                dateAdded
                description
            }
          }
        }
        '''
        expected = {'updateAggregate': {'aggregate': {'id': 'QWdncmVnYXRlTm9kZToxMw==', 'family': 'A_4', 'prefix': '54.0.0.0/8', 'rir': {'id': 'UklSTm9kZToxMw==', 'name': 'rir13'}, 'dateAdded': '2017-01-01', 'description': 'desc'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_aggregate(self):
        initialize_aggregate('12')
        query = '''
        mutation{
          deleteAggregate(input: { id: "UklSTm9kZToxMg=="}) {
            aggregate{
                id
            }
          }
        }
        '''
        expected = {'deleteAggregate': {'aggregate': {'id': 'QWdncmVnYXRlTm9kZTpOb25l'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

class IpAddressTestCase(TestCase):
    def test_creating_new_ip_address(self):
        initialize_ip_address('19')
        query = '''
         mutation{
          newIpAddress(input: { address: "173.16.0.0/12", vrf: "VlJGTm9kZToxOQ==", status: 3}) {
            ipAddress{
                id
                family
                address
                vrf {
                  name
                }
                description
                status
            }
          }
        }
        '''
        expected = {'newIpAddress': {'ipAddress': {'id': 'SVBBZGRyZXNzTm9kZToz', 'family': 'A_4', 'address': '173.16.0.0/12', 'vrf': {'name': 'vrf19'}, 'description': '', 'status': 'A_3'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_ip_address(self):
        initialize_ip_address('16')
        query = '''
            {
              ipAddress(id: "SVBBZGRyZXNzTm9kZTox") {
                edges {
                  node {
                    id
                    family
                    address
                    vrf {
                      name
                    }

                    description
                    status
                  }
                }
              }
            }
        '''
        expected = {'ipAddress': {'edges': [{'node': {'id': 'SVBBZGRyZXNzTm9kZTox', 'family': 'A_4', 'address': '16.0.2.1/24', 'vrf': {'name': 'vrf16'}, 'description': 'desc', 'status': 'A_1'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_ip_address(self):
        initialize_ip_address('15')

        query = '''
            mutation{
              updateIpAddress(input: { id:"SVBBZGRyZXNzTm9kZTo1", description: "txt", status: 2}) {
                ipAddress{
                    id
                    family
                    address
                    vrf {
                      name
                    }
                    description
                    status
                }
              }
            }
        '''
        expected = {'updateIpAddress': {'ipAddress': {'id': 'SVBBZGRyZXNzTm9kZTo1', 'family': 'A_4', 'address': '15.0.2.1/24', 'vrf': {'name': 'vrf15'}, 'description': 'txt', 'status': 'A_2'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_ip_address(self):
        initialize_ip_address('17')
        query = '''
        mutation{
          deleteIpAddress(input: { id:"SVBBZGRyZXNzTm9kZTox"}) {
            ipAddress{
                id
            }
          }
        }
        '''
        expected = {'deleteIpAddress': {'ipAddress': {'id': 'SVBBZGRyZXNzTm9kZTpOb25l'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
