import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data  import initialize_circuit_type, initialize_circuit, initialize_provider, initialize_circuit_termination, initialize_site
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


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
        expected = {'newRir': {'rir': {'id': 'UklSTm9kZTox',
                                       'name': 'rir', 'slug': 'rir', 'isPrivate': True}}}

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
        expected = {'rirs': {'edges': [{'node': {
            'id': 'UklSTm9kZToy', 'name': 'rir2', 'slug': 'rir2', 'isPrivate': True}}]}}

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
        expected = {'updateRir': {'rir': {'id': 'UklSTm9kZToz',
                                          'name': 'rirA', 'slug': 'rira', 'isPrivate': True}}}

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
        expected = {'deleteRir': {'rir': {'id': 'UklSTm9kZTpOb25l',
                                          'name': 'rir1', 'slug': 'rir1', 'isPrivate': True}}}

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
        expected = {'newAggregate': {'aggregate': {'id': 'QWdncmVnYXRlTm9kZTox', 'family': 'A_4', 'prefix': '192.0.0.0/12',
                                                   'rir': {'id': 'UklSTm9kZToxMQ==', 'name': 'rir11'}, 'dateAdded': '2015-01-01', 'description': 'desc'}}}

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
        expected = {'aggregates': {'edges': [{'node': {'id': 'QWdncmVnYXRlTm9kZToxNA==', 'family': 'A_4', 'prefix': '14.0.0.0/8', 'rir': {
            'id': 'UklSTm9kZToxNA==', 'name': 'rir14'}, 'dateAdded': '2017-12-12', 'description': 'desc'}}]}}

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
        expected = {'updateAggregate': {'aggregate': {'id': 'QWdncmVnYXRlTm9kZToxMw==', 'family': 'A_4', 'prefix': '54.0.0.0/8',
                                                      'rir': {'id': 'UklSTm9kZToxMw==', 'name': 'rir13'}, 'dateAdded': '2017-01-01', 'description': 'desc'}}}

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
        expected = {'deleteAggregate': {
            'aggregate': {'id': 'QWdncmVnYXRlTm9kZTpOb25l'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected


class IpAddressTestCase(TestCase):
    def test_creating_new_ip_address(self):
        initialize_ip_address('19')
        query = '''
         mutation{
          newIpAddress(input: { address: "173.16.0.0/12", status: 3}) {
            ipAddress{
                id
                family
                address
                description
                status
            }
          }
        }
        '''
        expected = {'newIpAddress': {'ipAddress': {'id': 'SVBBZGRyZXNzTm9kZToz',
                                                   'family': 'A_4', 'address': '173.16.0.0/12', 'description': '', 'status': 'A_3'}}}

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
                    description
                    status
                  }
                }
              }
            }
        '''
        expected = {'ipAddress': {'edges': [{'node': {
            'id': 'SVBBZGRyZXNzTm9kZTox', 'family': 'A_4', 'address': '16.0.2.1/24', 'description': 'desc', 'status': 'A_1'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_ip_address(self):
        initialize_ip_address('151')

        query = '''
            mutation{
              updateIpAddress(input: { id:"SVBBZGRyZXNzTm9kZToz", description: "txt", status: 2}) {
                ipAddress{
                    id
                    family
                    address
                    description
                    status
                }
              }
            }
        '''
        expected = {'updateIpAddress': {'ipAddress': {'id': 'SVBBZGRyZXNzTm9kZToz',
                                                      'family': 'A_4', 'address': '173.16.0.0/12', 'description': 'txt', 'status': 'A_2'}}}

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
        expected = {'deleteIpAddress': {
            'ipAddress': {'id': 'SVBBZGRyZXNzTm9kZTpOb25l'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected


class PrefixTestCase(TestCase):
    def test_creating_new_prefix(self):
        initialize_vrf('159')
        initialize_vlan_role('159')

        query = '''
        mutation{
          newPrefix(input: { prefix: "173.16.0.0/12", description: "desc", vrf: "VlJGTm9kZToxNTk=", role: "Um9sZU5vZGU6MTU5", status: 1, isPool: false}) {
            prefix{
                id
                description
                family
                prefix
                vrf {
                  id
                }
                status
                role {
                  id
                }
                isPool
            }
          }
        }
        '''
        expected = {'newPrefix': {'prefix': {'id': 'UHJlZml4Tm9kZTox', 'description': 'desc', 'family': 'A_4', 'prefix': '173.16.0.0/12',
                                             'vrf': {'id': 'VlJGTm9kZToxNTk='}, 'status': 'A_1', 'role': {'id': 'Um9sZU5vZGU6MTU5'}, 'isPool': False}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_prefix(self):
        initialize_prefix('156')
        query = '''
        {
          prefixes(id: "UHJlZml4Tm9kZToxNTY=") {
            edges {
              node {
                id
                family
                prefix
                vrf {
                  id
                }
                status
                role {
                  id
                }
                isPool
                description
              }
            }
          }
        }
        '''
        expected = {'prefixes': {'edges': [{'node': {'id': 'UHJlZml4Tm9kZToxNTY=', 'family': 'A_4', 'prefix': '122.0.3.0/24', 'vrf': {
            'id': 'VlJGTm9kZToxNTY='}, 'status': 'A_1', 'role': {'id': 'Um9sZU5vZGU6MTU2'}, 'isPool': True, 'description': 'desc'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_prefix(self):
        initialize_prefix('155')

        query = '''
        mutation{
          updatePrefix(input: { id: "UHJlZml4Tm9kZToxNTU=", prefix: "173.16.0.0/24", description: "txt", status: 2, isPool: true}) {
            prefix{
            id
            description
            family
            prefix
            vrf {
              id
            }
            status
            role {
              id
            }
            isPool
            }
          }
        }
        '''

        expected = {'updatePrefix': {'prefix': {'id': 'UHJlZml4Tm9kZToxNTU=', 'description': 'txt', 'family': 'A_4',
                                                'prefix': '173.16.0.0/24', 'vrf': {'id': 'VlJGTm9kZToxNTU='}, 'status': 'A_2', 'role': {'id': 'Um9sZU5vZGU6MTU1'}, 'isPool': True}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_prefix(self):
        initialize_prefix('157')
        query = '''
        mutation{
          deletePrefix(input: {id: "UHJlZml4Tm9kZToxNTc="}) {
            prefix{
                id
            }
          }
        }
        '''
        expected = {'deletePrefix': {'prefix': {'id': 'UHJlZml4Tm9kZTpOb25l'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
