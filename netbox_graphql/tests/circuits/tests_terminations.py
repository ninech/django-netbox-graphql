from string import Template

from graphene.test import Client
from django.test import TestCase

from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.circuit_factories import CircuitTerminationFactory, CircuitFactory
from netbox_graphql.tests.factories.dcim_factories import SiteFactory

from circuits.models import CircuitTermination


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.circuit = CircuitFactory()
        cls.site = SiteFactory()

        cls.query = Template('''
        mutation {
          newCircuitTermination(input: {circuit: "$circuitId", portSpeed: 128,
          termSide:"A", upstreamSpeed: 128, site:"$siteId" }) {
            circuitTermination {
              circuit {
                cid
              }
              portSpeed
              termSide
              upstreamSpeed
              site {
                name
              }
            }
          }
        }
        ''').substitute(circuitId=obj_to_global_id(cls.circuit),
                        siteId=obj_to_global_id(cls.site))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newCircuitTermination':
                    {'circuitTermination': {'circuit': {'cid': self.circuit.cid},
                                            'portSpeed': 128,
                                            'termSide': 'A',
                                            'upstreamSpeed': 128,
                                            'site': {'name': self.site.name}
                                            }
                     }}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = CircuitTermination.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(
            CircuitTermination.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTerminationFactory()
        cls.second = CircuitTerminationFactory(site=cls.first.site)
        cls.query = '''
        {
         circuitTerminations {
            edges {
                node {
                    id
                    site {
                        id
                    }
                    circuit {
                        id
                    }
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
        self.assertEquals(len(result.data['circuitTerminations']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTerminationFactory()
        cls.query = Template('''
        {
         circuitTerminations(id: "$id") {
            edges {
                node {
                    site {
                        name
                    }
                    circuit {
                        cid
                    }
                }
            }
         }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_single_provider_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_provider_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['circuitTerminations']['edges']), 1)

    def test_querying_single_provider_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'circuitTerminations':
                    {'edges': [
                        {'node': {'site': {'name': self.first.site.name},
                                  'circuit': {'cid': self.first.circuit.cid},
                                  }}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTerminationFactory()
        cls.query = Template('''
        mutation {
          updateCircuitTermination(input: {id: "$id", portSpeed: 512, termSide: "Z", upstreamSpeed: 512}) {
            circuitTermination {
              termSide
              portSpeed
              upstreamSpeed
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = CircuitTermination.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(CircuitTermination.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateCircuitTermination':
                    {'circuitTermination':
                        {'termSide': 'Z',
                         'portSpeed': 512,
                         'upstreamSpeed': 512}
                     }}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        circuit_termination = CircuitTermination.objects.get(id=self.first.id)
        self.assertEquals(circuit_termination.term_side, 'Z')
        self.assertEquals(circuit_termination.upstream_speed, 512)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTerminationFactory()
        cls.query = Template('''
        mutation {
          deleteCircuitTermination(input: {id: "$id" }) {
            circuitTermination {
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = CircuitTermination.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(
            CircuitTermination.objects.all().count(), oldCount - 1)
