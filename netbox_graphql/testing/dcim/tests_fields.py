import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class FieldsTestCase(TestCase):
    def test_regions(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          regions {
            edges {
              node {
                id
                name
                slug
                parent {
                  name
                }
              }
            }
          }
        }
        '''))

    def test_sites(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          sites {
            edges {
              node {
                id
                name
                slug
                region {
                  name
                }
                tenant {
                  name
                }
                facility
                asn
                physicalAddress
                shippingAddress
                contactName
                contactPhone
                contactEmail
                comments
              }
            }
          }
        }
        '''))
