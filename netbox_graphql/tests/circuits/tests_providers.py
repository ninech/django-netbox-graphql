
from string import Template

from graphene.test import Client
from django.test import TestCase

from netbox_graphql.tests.data import *
from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.circuit_factories import ProviderFactory

from netbox_graphql.schema import schema

from graphql_relay.node.node import from_global_id, to_global_id

from circuits.models import Provider


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
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

    def test_creating_provider_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_provider_returns_data(self):
        expected = {'newProvider':
                    {'provider': {'slug': 'provider123', 'name': 'Provider123',
                                  'asn': 256.0, 'account': 'account', 'portalUrl': 'http://github.com/',
                                  'nocContact': 'noc', 'comments': 'my comment'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_provider_creates_it(self):
        oldCount = Provider.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Provider.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ProviderFactory()
        cls.second = ProviderFactory()
        cls.query = '''
        query {providers {
            edges {
                node {
                id
                name
                slug
                }
            }
        }}
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['providers']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ProviderFactory()
        cls.second = ProviderFactory()

        cls.query = Template('''
        {
          providers(id: "$id") {
            edges {
              node {
                name
                slug
                asn
                account
                portalUrl
                nocContact
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.second))

    def test_querying_single_provider_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_provider_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['providers']['edges']), 1)

    def test_querying_single_provider_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'providers':
                    {'edges': [
                        {'node': {'name': self.second.name,
                                  'slug': self.second.slug,
                                  'asn': self.second.asn,
                                  'account': self.second.account,
                                  'portalUrl': self.second.portal_url,
                                  'nocContact': self.second.noc_contact,
                                  }}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ProviderFactory()
        cls.query = Template('''
        mutation {
          updateProvider(input: {id:"$id", name: "New Name", slug: "psl1", 
          portalUrl: "http://github.com/", comments: "my comment"}) {
            provider {
              name
              slug
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Provider.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Provider.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateProvider':
                    {'provider': {'name': 'New Name', 'slug': 'psl1'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        provider = Provider.objects.get(id=self.first.id)
        self.assertEquals(provider.name, 'New Name')
        self.assertEquals(provider.slug, 'psl1')
        self.assertEquals(provider.portal_url, 'http://github.com/')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ProviderFactory()
        cls.query = Template('''
        mutation {
          deleteProvider(input: {id:"$id"}) {
            provider {
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Provider.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Provider.objects.all().count(), oldCount - 1)
