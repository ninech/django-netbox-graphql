from string import Template

from graphene.test import Client
from django.test import TestCase

from ipam.models import Role

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import RoleFactory
from netbox_graphql.tests.factories.dcim_factories import SiteFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
        mutation{
          newVlanRole(input: { name: "New Name", slug: "nsl1", weight: 1001}) {
            vlanRole{
              name
              slug
              weight
            }
          }
        }
        '''

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newVlanRole':
                    {'vlanRole': {'name': 'New Name',
                                  'slug': 'nsl1',
                                  'weight': 1001}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Role.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Role.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RoleFactory()
        cls.second = RoleFactory()
        cls.query = '''
        {
          vlanRoles {
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
        self.assertEquals(len(result.data['vlanRoles']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RoleFactory()
        cls.second = RoleFactory()
        cls.query = Template('''
        {
          vlanRoles(id: "$id") {
            edges {
              node {
                name
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.second))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['vlanRoles']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'vlanRoles':
                    {'edges': [
                        {'node': {'name': self.second.name}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RoleFactory()
        cls.query = Template('''
        mutation{
          updateVlanRole(input: {id: "$id", name: "New Name", slug: "nsl1", weight: 1}) {
            vlanRole {
              name
              slug
              weight
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Role.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Role.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateVlanRole':
                    {'vlanRole': {'name': 'New Name',
                                  'slug': 'nsl1',
                                  'weight': 1}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        role = Role.objects.get(id=self.first.id)
        self.assertEquals(role.name, 'New Name')
        self.assertEquals(role.slug, 'nsl1')
        self.assertEquals(role.weight, 1)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RoleFactory()
        cls.query = Template('''
        mutation{
          deleteVlanRole(input: {id: "$id"}) {
            vlanRole{
              id
              name
              slug
              weight
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Role.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Role.objects.all().count(), oldCount - 1)
