import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data  import initialize_circuit_type, initialize_circuit, initialize_provider, initialize_circuit_termination, initialize_site
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class ProviderTestCase(TestCase):
    def test_creating_new_provider(self):
        query = '''
        mutation {
          newProvider(input: {name: "Provider123", slug: "provider123", asn: 256, account: "account",
          portalUrl: "http://github.com/", nocContact:"noc", comments: "my comment"}) {
            provider {
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
        '''
        expected = {'newProvider':
                    {'provider': {'slug': 'provider123', 'name': 'Provider123',
                                  'asn': 256.0, 'account': 'account', 'portalUrl': 'http://github.com/',
                                  'nocContact': 'noc', 'comments': 'my comment'}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_provider(self):
        initialize_provider()
        query = '''
        {
          providers(id: "Q2lyY3VpdFR5cGVOb2RlOjExMQ==") {
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
        '''
        expected = {'providers':
                    {'edges': [{'node': {'id': 'UHJvdmlkZXJOb2RlOjExMQ==', 'slug': 'provider1',
                                         'name': 'Provider 1', 'asn': 256.0, 'account': '12345',
                                         'portalUrl': 'https://www.nine.ch', 'nocContact': 'noc_contact',
                                                      'comments': 'comments'}}]}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_provider(self):
        initialize_provider()
        query = '''
        mutation {
          updateProvider(input: {id:"UHJvdmlkZXJOb2RlOjExMQ==", name: "Provider1", slug: "provider1231",
          asn: 512, account: "account", portalUrl: "http://github.com/", nocContact:"noc", comments: "my comment"}) {
            provider {
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
        '''
        expected = {'updateProvider':
                    {'provider': {'id': 'UHJvdmlkZXJOb2RlOjExMQ==', 'slug': 'provider1231',
                                  'name': 'Provider1', 'asn': 512.0, 'account': 'account',
                                  'portalUrl': 'http://github.com/', 'nocContact': 'noc', 'comments': 'my comment'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_provider(self):
        initialize_provider()
        query = '''
        mutation {
          deleteProvider(input: {id:"UHJvdmlkZXJOb2RlOjExMQ=="}) {
            provider {
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
        '''
        expected = {'deleteProvider': {'provider': {'id': 'UHJvdmlkZXJOb2RlOk5vbmU=', 'slug': 'provider1',
                                                    'name': 'Provider 1', 'asn': 256.0, 'account': '12345',
                                                    'portalUrl': 'https://www.nine.ch', 'nocContact': 'noc_contact',
                                                    'comments': 'comments'}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
