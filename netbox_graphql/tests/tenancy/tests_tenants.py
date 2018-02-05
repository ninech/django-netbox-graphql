
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




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
        expected = {'newTenant': {'tenant': {'name': 'Tenant 1', 'slug': 'tenant-1',
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
