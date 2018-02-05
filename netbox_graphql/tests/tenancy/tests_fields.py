
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




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
