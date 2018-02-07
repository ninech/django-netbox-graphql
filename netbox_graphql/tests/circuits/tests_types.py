from string import Template

from graphene.test import Client
from django.test import TestCase

from circuits.models import CircuitType

from netbox_graphql.schema import schema

from netbox_graphql.tests.data import *
from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.circuit_factories import CircuitTypeFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
        mutation {
          newCircuitType(input: {name: "Typename", slug: "typeslug"}) {
            circuitType {
              name
              slug
            }
          }
        }
        '''

    def test_creating_circuit_type_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_circuit_type_returns_data(self):
        expected = {'newCircuitType':
                    {'circuitType': {'name': 'Typename', 'slug': 'typeslug'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_circut_type_creates_it(self):
        oldCount = CircuitType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(CircuitType.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTypeFactory()
        cls.second = CircuitTypeFactory()
        cls.query = '''
        query {circuitTypes {
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
        self.assertEquals(len(result.data['circuitTypes']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTypeFactory()
        cls.second = CircuitTypeFactory()

        cls.query = Template('''
        {
          circuitTypes(id: "$id") {
            edges {
              node {
                name
                slug
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
        self.assertEquals(len(result.data['circuitTypes']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'circuitTypes':
                    {'edges': [
                        {'node': {'name': self.first.name, 'slug': self.first.slug}}
                    ]}
                    }
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTypeFactory()
        cls.query = Template('''
        mutation {
          updateCircuitType(input: {id:"$id", name: "New Name", slug: "nsl1"}) {
            circuitType {
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
        oldCount = CircuitType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(CircuitType.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateCircuitType':
                    {'circuitType': {'name': 'New Name', 'slug': 'nsl1'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        circuit_type = CircuitType.objects.get(id=self.first.id)
        self.assertEquals(circuit_type.name, 'New Name')
        self.assertEquals(circuit_type.slug, 'nsl1')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitTypeFactory()
        cls.query = Template('''
        mutation {
          deleteCircuitType(input: {id:"$id"}) {
            circuitType {
              name
              slug
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = CircuitType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(CircuitType.objects.all().count(), oldCount - 1)
