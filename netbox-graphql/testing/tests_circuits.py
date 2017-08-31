from graphene.test import Client
from snapshottest import TestCase
from ..schema import schema


class QueriesTestCase(TestCase):
    def test_providers(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          providers {
            edges {
              node {
                id
                slug
                name
                asn
                account
                portalUrl
                nocContact
                comments
              }
            }
          }
        }
        '''))

    def test_circuit_types(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          circuitTypes {
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

    def test_circuits(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          circuits {
            edges {
              node {
                id
                cid
                provider {
                  id
                  name
                }
                type {
                  id
                  name
                }
                tenant {
                  id
                  name
                }
                installDate
                commitRate
                description
              }
            }
          }
        }
        '''))

    def test_circuit_terminations(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          circuitTerminations {
            edges {
              node {
                id
                termSide
                portSpeed
                ppInfo
                upstreamSpeed
                xconnectId
                interface {
                  id
                  name
                }
                site {
                  id
                  name
                }
                circuit {
                  id
                  cid
                }
              }
            }
          }
        }
        '''))
