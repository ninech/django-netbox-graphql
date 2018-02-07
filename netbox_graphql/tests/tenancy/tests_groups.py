from string import Template

from graphene.test import Client
from django.test import TestCase

from tenancy.models import TenantGroup

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.tenant_factories import TenantGroupFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
            mutation{
            newTenantGroup(input: {name: "Groupname", slug: "groupslug"}) {
                tenantGroup{
                name
                slug
                }
            }
            }
            '''

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newTenantGroup':
                    {'tenantGroup': {'name': 'Groupname', 'slug': 'groupslug'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = TenantGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(TenantGroup.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantGroupFactory()
        cls.second = TenantGroupFactory()
        cls.query = '''
        {tenantGroups {
            edges {
                node {
                    name
                    slug
                }
            }
        }}
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['tenantGroups']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantGroupFactory()
        cls.second = TenantGroupFactory()
        cls.query = Template('''
        {tenantGroups(id: "$id") {
            edges {
                node {
                    name
                    slug
                }
            }
        }}
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['tenantGroups']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'tenantGroups':
                    {'edges': [
                        {'node': {'name': self.first.name, 'slug': self.first.slug}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantGroupFactory()
        cls.query = Template('''
        mutation {
          updateTenantGroup(input: {id:"$id", name: "New Name", slug: "nsl1"}) {
            tenantGroup {
              name
              slug
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = CircuitType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(CircuitType.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateTenantGroup':
                    {'tenantGroup': {'name': 'New Name', 'slug': 'nsl1'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        tenant_group = TenantGroup.objects.get(id=self.first.id)
        self.assertEquals(tenant_group.name, 'New Name')
        self.assertEquals(tenant_group.slug, 'nsl1')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantGroupFactory()
        cls.query = Template('''
        mutation {
          deleteTenantGroup(input: {id:"$id"}) {
            tenantGroup {
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = TenantGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(TenantGroup.objects.all().count(), oldCount - 1)
