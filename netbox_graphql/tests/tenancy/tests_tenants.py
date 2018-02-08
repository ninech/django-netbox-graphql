from string import Template

from graphene.test import Client
from django.test import TestCase

from tenancy.models import Tenant

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.tenant_factories import TenantFactory, TenantGroupFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = TenantGroupFactory()
        cls.query = Template('''
            mutation {
              newTenant(input: {name: "New Tenant", slug: "t1", group: "$groupId", description: "desc", comments: "comments"}) {
                tenant {
                    name
                    group {
                        name
                    }
                }
              }
            }
            ''').substitute(groupId=obj_to_global_id(cls.group))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newTenant':
                    {'tenant': {'name': 'New Tenant',
                                'group': {'name': self.group.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Tenant.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Tenant.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantFactory()
        cls.second = TenantFactory(group=cls.first.group)
        cls.third = TenantFactory()
        cls.query = Template('''
        {
            tenants{
                edges {
                    node {
                        name
                        group {
                            name
                        }
                    }
                }
            }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_types_returns_three_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['tenants']['edges']), 3)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantFactory()
        cls.second = TenantFactory(group=cls.first.group)
        cls.query = Template('''
        {
            tenants(id: "$id") {
                edges {
                    node {
                        name
                        group {
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
        self.assertEquals(len(result.data['tenants']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'tenants':
                    {'edges': [
                        {'node': {'name': self.first.name,
                                  'group': {'name': self.first.group.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantFactory()
        cls.group = TenantGroupFactory()
        cls.query = Template('''
        mutation {
          updateTenant(input: {id: "$id", name: "New Name", slug: "nsl1", group: "$groupId"}) {
            tenant {
              name
              slug
              group {
                name
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first), groupId=obj_to_global_id(cls.group))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Tenant.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Tenant.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateTenant':
                    {'tenant': {'name': 'New Name',
                                'slug': 'nsl1',
                                'group': {'name': self.group.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        tenant = Tenant.objects.get(id=self.first.id)
        self.assertEquals(tenant.name, 'New Name')
        self.assertEquals(tenant.slug, 'nsl1')
        self.assertEquals(tenant.group, self.group)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = TenantFactory()
        cls.query = Template('''
        mutation {
          deleteTenant(input: {id: "$id"}) {
            tenant {
              name
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Tenant.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Tenant.objects.all().count(), oldCount - 1)
