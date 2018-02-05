import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_tenant_group, initialize_tenant
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
        expected = {'deleteTenantGroup': {'tenantGroup': {'id': 'VGVuYW50R3JvdXBOb2RlOk5vbmU=', 'name': 'Tenant Group12', 'slug': 'tenant-group-12'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

class TenantTestCase(TestCase):
    def test_creating_new_tenant(self):
        initialize_tenant_group('11')
        query = '''
        mutation {
            newTenant(input: {name: "Tenant 1", slug: "tenant-1", group: "VGVuYW50R3JvdXBOb2RlOjEx=", description: "desc", comments: "comments"}) {
            tenant {
            name
            slug
            group {
              name
            }
            description
            comments
            }
          }
        }
        '''
        expected = {'newTenant': {'tenant': { 'name': 'Tenant 1', 'slug': 'tenant-1',
                                             'group': {'name': 'Tenant Group11'}, 'description': 'desc',
                                             'comments': 'comments'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_provider(self):
        initialize_tenant('12')
        query = '''
        {
          tenants(id: "VGVuYW50Tm9kZToxMg=="){
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
        '''
        expected = {'tenants': {'edges': [{'node': {'id': 'VGVuYW50Tm9kZToxMg==', 'name': 'Tenant 12',
                                                    'slug': 'tenant-12', 'group': {'id': 'VGVuYW50R3JvdXBOb2RlOjEy'},
                                                    'description': 'desc', 'comments': 'comment'}}]}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
    #
    def test_update_provider(self):
        initialize_tenant('14')
        query = '''
        mutation {
          updateTenant(input: {id: "VGVuYW50Tm9kZTox", name: "Tenant A", slug: "tenant-A", group: "VGVuYW50R3JvdXBOb2RlOjE=", description: "descA", comments: "commentsA"}) {
            tenant {
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
        '''
        expected = {'updateTenant': {'tenant': {'id': 'VGVuYW50Tm9kZTox', 'name': 'Tenant A', 'slug': 'tenant-A',
                                                'group': {'id': 'VGVuYW50R3JvdXBOb2RlOjE='}, 'description': 'descA',
                                                'comments': 'commentsA'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_tenant(self):
        initialize_tenant('13')
        query = '''
        mutation {
          deleteTenant(input: {id: "VGVuYW50Tm9kZToxMg=="}) {
            tenant {
              name
              slug
              group {
                name
              }
              description
              comments
            }
          }
        }
        '''
        expected = {'deleteTenant': {
            'tenant': {'name': 'Tenant 12', 'slug': 'tenant-12', 'group': {'name': 'Tenant Group12'},
                       'description': 'desc', 'comments': 'comment'}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
