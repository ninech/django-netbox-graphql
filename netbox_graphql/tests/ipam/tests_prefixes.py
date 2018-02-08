from string import Template
import netaddr

from graphene.test import Client
from django.test import TestCase

from ipam.models import Prefix

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import PrefixFactory, VRFFactory, RoleFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vrf = VRFFactory()
        cls.role = RoleFactory()
        cls.query = Template('''
            mutation{
              newPrefix(input: { prefix: "173.16.0.0/12", vrf: "$vrfId", 
                                 role: "$roleId", status: 2, isPool: false}) {
                prefix{
                    prefix
                    status
                    isPool
                    vrf {
                      name
                    }
                    role {
                      name
                    }
                }
              }
            }
            ''').substitute(roleId=obj_to_global_id(cls.role),
                            vrfId=obj_to_global_id(cls.vrf))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newPrefix':
                    {'prefix': {'prefix': '173.16.0.0/12',
                                'status': "A_2",
                                'isPool': False,
                                'vrf': {'name': self.vrf.name},
                                'role': {'name': self.role.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Prefix.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Prefix.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = PrefixFactory()
        cls.second = PrefixFactory()
        cls.query = '''
        {
          prefixes {
            edges {
              node {
                id
              }
            }
          }
        }
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['prefixes']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = PrefixFactory()
        cls.second = PrefixFactory()
        cls.query = Template('''
        {
          prefixes(id: "$id") {
            edges {
              node {
                prefix
                role {
                  name
                }
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['prefixes']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'prefixes':
                    {'edges': [
                        {'node': {'prefix': str(self.first.prefix.cidr),
                                  'role': {'name': self.first.role.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = PrefixFactory()
        cls.query = Template('''
        mutation{
          updatePrefix(input: { id: "$id", prefix: "173.16.0.0/24", isPool: true}) {
            prefix{
                prefix
                isPool
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Prefix.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Prefix.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updatePrefix':
                    {'prefix': {'prefix': '173.16.0.0/24',
                                'isPool': True}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        prefix = Prefix.objects.get(id=self.first.id)
        self.assertEquals(prefix.prefix, netaddr.IPNetwork('173.16.0.0/24'))
        self.assertEquals(prefix.is_pool, True)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = PrefixFactory()
        cls.query = Template('''
        mutation{
          deletePrefix(input: {id: "$id"}) {
            prefix{
                id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Prefix.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Prefix.objects.all().count(), oldCount - 1)
