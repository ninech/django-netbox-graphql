from string import Template

from graphene.test import Client
from django.test import TestCase

from netbox_graphql.schema import schema
from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.circuit_factories import CircuitFactory, ProviderFactory, CircuitTypeFactory

from circuits.models import Circuit


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.provider = ProviderFactory()
        cls.circuit_type = CircuitTypeFactory()
        cls.circuit = CircuitFactory.build()
        cls.query = Template('''
        mutation {
          newCircuit(input: {cid: "$cid", provider:"$providerId", type:"$typeId",
          installDate:"2017-10-12", commitRate: 12, description:"desc", comments:"Awesome Comment!" }) {
            circuit {
              cid
              provider {
                name
              }
              type {
                name
              }
              installDate
              commitRate
              description
              comments
            }
          }
        }
        ''').substitute(cid=cls.circuit.cid,
                        providerId=obj_to_global_id(cls.provider),
                        typeId=obj_to_global_id(cls.circuit_type))

    def test_creating_provider_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_provider_returns_data(self):
        expected = {'newCircuit': {'circuit': {'cid': self.circuit.cid,
                                               'provider': {'name': self.provider.name},
                                               'type': {'name': self.circuit_type.name},
                                               'installDate': '2017-10-12',
                                               'commitRate': 12,
                                               'description': 'desc',
                                               'comments': 'Awesome Comment!'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_provider_creates_it(self):
        oldCount = Circuit.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Circuit.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitFactory()
        cls.second = CircuitFactory(provider=cls.first.provider,
                                    type=cls.first.type)
        cls.query = '''
        query {circuits {
            edges {
                node {
                    id
                    cid
                    provider {
                        id
                    }
                    type {
                        id
                    }
                }
            }
        }}
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['circuits']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitFactory()
        cls.second = CircuitFactory(provider=cls.first.provider,
                                    type=cls.first.type)
        cls.query = Template('''
        {
            circuits(id: "$id") {
                edges {
                    node {
                        cid
                        provider {
                            name
                        }
                        type {
                            name
                        }
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
        self.assertEquals(len(result.data['circuits']['edges']), 1)

    def test_querying_single_provider_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'circuits':
                    {'edges': [
                        {'node': {'cid': self.second.cid,
                                  'provider': {'name': self.second.provider.name},
                                  'type': {'name': self.second.type.name},
                                  }}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitFactory()
        cls.query = Template('''
        mutation {
          updateCircuit(input:{id: "$id", cid: "117", comments: "New Awesome Comment!" }) {
            circuit {
                cid
                comments
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Circuit.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Circuit.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateCircuit':
                    {'circuit': {'cid': '117', 'comments': 'New Awesome Comment!'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        circuit = Circuit.objects.get(id=self.first.id)
        self.assertEquals(circuit.cid, '117')
        self.assertEquals(circuit.comments, 'New Awesome Comment!')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = CircuitFactory()
        cls.query = Template('''
        mutation {
          deleteCircuit(input: {id: "$id"}) {
            circuit {
               id
               cid
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Circuit.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Circuit.objects.all().count(), oldCount - 1)
