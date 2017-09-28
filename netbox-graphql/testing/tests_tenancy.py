import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_tenant_group
from ..schema import schema
from tenancy.models import Tenant, TenantGroup

pytestmark = pytest.mark.django_db

class FieldsTestCase(TestCase):
    def test_tenant_groups(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          tenantGroups {
            edges {
              node {
                id
                name
                slug
              }
            }
          }
        }
        '''))

    def test_tenants(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          tenants {
            edges {
              node {
                id
                name
                slug
                group {
                  id
                }
                description
                comments
              }
            }
          }
        }
        '''))

class TenantGroupTestCase(TestCase):
    def test_creating_new_tenant_group(self):
        query = '''
        mutation{
          newTenantGroup(input: {name: "TenantGroupA", slug: "tenant-group-A"}) {
            tenantGroup{
              name
              slug
            }
          }
        }
        '''
        expected = { 'newTenantGroup':
                         {'tenantGroup': {'name': 'TenantGroupA', 'slug': 'tenant-group-A'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_tenant_group(self):
        initialize_tenant_group('11')
        query = '''
        {
          tenantGroups {
            edges {
              node {
                id
                name
                slug
              }
            }
          }
        }
        '''
        expected = {'tenantGroups': {
            'edges': [{'node': {'id': 'VGVuYW50R3JvdXBOb2RlOjEx', 'name': 'Tenant Group11', 'slug': 'tenant-group-11'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_circuit_type(self):
        initialize_tenant_group('11')
        query = '''
        mutation {
          updateTenantGroup(input: {id:"VGVuYW50R3JvdXBOb2RlOjEx", name: "Tenant GroupX", slug: "tenant-group-x"}) {
            tenantGroup {
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'updateTenantGroup':
                        {'tenantGroup': {'id': 'VGVuYW50R3JvdXBOb2RlOjEx', 'name': 'Tenant GroupX', 'slug': 'tenant-group-x'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_circuit_type(self):
        initialize_tenant_group('12')
        query = '''
        mutation {
          deleteTenantGroup(input: {id:"VGVuYW50R3JvdXBOb2RlOjEy"}) {
            tenantGroup {
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'deleteTenantGroup': {'tenantGroup': {'id': 'VGVuYW50R3JvdXBOb2RlOk5vbmU=', 'name': 'Tenant Group12', 'slug': 'tenant-group-12'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
