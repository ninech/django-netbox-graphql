
from string import Template
import netaddr

from graphene.test import Client
from django.test import TestCase

from ipam.models import IPAddress

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import IPAddressFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
        mutation{
          newIpAddress(input: { address: "173.16.0.0", status: 3}) {
            ipAddress{
                family
                address
                status
            }
          }
        }
        '''

    def test_creating_circuit_type_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_circuit_type_returns_data(self):
        expected = {'newIpAddress':
                    {'ipAddress': {'family': 'A_4',
                                   'address': '173.16.0.0/32',
                                   'status': 'A_3'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_circut_type_creates_it(self):
        oldCount = IPAddress.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(IPAddress.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = IPAddressFactory()
        cls.second = IPAddressFactory()
        cls.query = '''
        { ipAddress {
            edges {
                node {
                    id
                }
            }
        }}
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['ipAddress']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = IPAddressFactory()
        cls.second = IPAddressFactory()

        cls.query = Template('''
        { ipAddress(id: "$id") {
            edges {
                node {
                    address
                }
            }
        }}
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['ipAddress']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'ipAddress':
                    {'edges': [
                        {'node': {'address': str(
                            netaddr.IPNetwork(self.first.address))}}
                    ]}
                    }
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = IPAddressFactory()
        cls.query = Template('''
        mutation{
            updateIpAddress(input: { id:"$id", address: "192.168.1.1"}) {
                ipAddress{
                    address
                }
            }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = IPAddress.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(IPAddress.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateIpAddress':
                    {'ipAddress': {'address': str(netaddr.IPNetwork('192.168.1.1'))}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        ip_address = IPAddress.objects.get(id=self.first.id)
        self.assertEquals(ip_address.address, netaddr.IPNetwork('192.168.1.1'))


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = IPAddressFactory()
        cls.query = Template('''
        mutation {
          deleteIpAddress(input: { id:"$id"}) {
            ipAddress{
                id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = IPAddress.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(IPAddress.objects.all().count(), oldCount - 1)
