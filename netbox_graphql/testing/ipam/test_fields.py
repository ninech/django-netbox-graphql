import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import initialize_circuit_type, initialize_circuit, initialize_provider, initialize_circuit_termination, initialize_site
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class FieldsTestCase(TestCase):
    def test_vlan_roles(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          vlanRoles {
            edges {
              node {
                id
                slug
                name
                weight
              }
            }
          }
        }
        '''))

    def test_vlan_groups(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          vlanGroups {
            edges {
              node {
                id
                name
                slug
                site {
                  name
                }
              }
            }
          }
        }
        '''))

    def test_vlan(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        { vlans {
            edges {
              node {
                id
                name
                description
                vid
                site{
                  name
                }
                group{
                  name
                }
                tenant{
                  name
                }
                role{
                  name
                }
              }
            }
        }
        '''))

    def test_vrf(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          vrfs {
            edges {
              node {
                id
                name
                rd
                description
                enforceUnique
                tenant {
                  name
                }
              }
            }
          }
        }
        '''))

    def test_rir(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          rirs {
            edges {
              node {
                id
                name
                slug
                isPrivate
              }
            }
          }
        }
        '''))

    def test_aggregate(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          aggregates {
            edges {
              node {
                family
                prefix
                rir {
                  id
                  name
                }
                dateAdded
                description
              }
            }
          }
        }
        '''))

    def test_ip_address(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          ipAddress {
            edges {
              node {
                id
                family
                address
                vrf {
                  name
                }
                tenant {
                  name
                }
                interface {
                  name
                }
                natInside {
                  id
                }
                natOutside {
                  id
                }
                description
                status
              }
            }
          }
        }
        '''))

    def test_prefix(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          prefixes {
            edges {
              node {
                id
                family
                prefix
                site {
                  id
                }
                vrf {
                  id
                }
                tenant {
                  id
                }
                vlan {
                  id
                }
                status
                role {
                  id
                }
                isPool
                description
              }
            }
          }
        }
        '''))
