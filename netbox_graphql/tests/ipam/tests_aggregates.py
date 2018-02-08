from string import Template
import datetime
import netaddr

from graphene.test import Client
from django.test import TestCase

from ipam.models import Aggregate

from netbox_graphql.schema import schema

from netbox_graphql.tests.data import *
from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import AggreagateFactory, RIRFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rir = RIRFactory()
        cls.query = Template('''
            mutation {
                newAggregate(input: { family: 4, rir: "$rirId", prefix: "192.0.0.0/12" }) {
                    aggregate{
                        family
                        prefix
                        rir {
                            name
                        }
                    }
                }
            }
            ''').substitute(rirId=obj_to_global_id(cls.rir))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newAggregate':
                    {'aggregate': {'family': 'A_4',
                                   'prefix': '192.0.0.0/12',
                                   'rir': {'name': self.rir.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Aggregate.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Aggregate.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = AggreagateFactory()
        cls.second = AggreagateFactory()
        cls.query = '''
        {
          aggregates {
            edges {
              node {
                id
              }
            }
          }
        }
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['aggregates']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = AggreagateFactory()
        cls.second = AggreagateFactory()
        cls.query = Template('''
        {
        aggregates(id: "$id") {
            edges {
                node {
                    family
                    prefix
                    rir {
                        name
                    }
                }
            }
        }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['aggregates']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'aggregates':
                    {'edges': [
                        {'node':  {'family': 'A_4',
                                   'prefix': str(self.first.prefix),
                                   'rir': {'name': self.first.rir.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = AggreagateFactory()
        cls.query = Template('''
        mutation{
          updateAggregate(input: { id: "$id", dateAdded: "2017-01-01", prefix: "54.0.0.0/8"}) {
            aggregate{
                prefix
                dateAdded
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Aggregate.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Aggregate.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateAggregate':
                    {'aggregate': {'prefix': '54.0.0.0/8',
                                   'dateAdded': '2017-01-01'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        aggregate = Aggregate.objects.get(id=self.first.id)
        self.assertEquals(aggregate.prefix, netaddr.IPNetwork('54.0.0.0/8'))
        self.assertEquals(aggregate.date_added, datetime.date(2017, 1, 1))


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = AggreagateFactory()
        cls.query = Template('''
        mutation{
          deleteAggregate(input: { id: "$id"}) {
            aggregate{
                id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Aggregate.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Aggregate.objects.all().count(), oldCount - 1)
