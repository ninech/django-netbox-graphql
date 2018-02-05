
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




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
        expected = {'newTenantGroup':
                    {'tenantGroup': {'name': 'TenantGroupA', 'slug': 'tenant-group-A'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_tenant_group(self):
        initialize_tenant_group('11')
        query = '''
        {
          tenantGroups(id: "VGVuYW50R3JvdXBOb2RlOjEx") {
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

    def test_update_tenant_group(self):
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

    def test_delete_tenant_group(self):
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
        expected = {'deleteTenantGroup': {'tenantGroup': {
            'id': 'VGVuYW50R3JvdXBOb2RlOk5vbmU=', 'name': 'Tenant Group12', 'slug': 'tenant-group-12'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
