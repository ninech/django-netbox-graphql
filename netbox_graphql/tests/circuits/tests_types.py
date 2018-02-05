
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




class CircuitTypeTestCase(TestCase):
    def test_creating_new_circuit_type(self):
        query = '''
        mutation {
          newCircuitType(input: {name: "Type", slug: "type"}) {
            circuitType {
              name
              slug
            }
          }
        }
        '''
        expected = {'newCircuitType':
                    {'circuitType': {'name': 'Type', 'slug': 'type'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_circuit_type(self):
        initialize_circuit_type()
        query = '''
        {
          circuitTypes(id: "Q2lyY3VpdFR5cGVOb2RlOjExMQ==") {
            edges {
              node {
                id
                name
                slug
              }
            }
          }
        }
        '''
        expected = {'circuitTypes': {
            'edges': [{'node': {'id': 'Q2lyY3VpdFR5cGVOb2RlOjExMQ==', 'name': 'Type 1', 'slug': 'type1'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_circuit_type(self):
        initialize_circuit_type()
        query = '''
        mutation {
          updateCircuitType(input: {id:"Q2lyY3VpdFR5cGVOb2RlOjExMQ==", name: "TypeX", slug: "typex"}) {
            circuitType {
             id
              name
              slug
            }
          }
        }
        '''
        expected = {'updateCircuitType':
                    {'circuitType': {'id': 'Q2lyY3VpdFR5cGVOb2RlOjExMQ==', 'name': 'TypeX', 'slug': 'typex'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_circuit_type(self):
        initialize_circuit_type()
        query = '''
        mutation {
          deleteCircuitType(input: {id:"Q2lyY3VpdFR5cGVOb2RlOjExMQ=="}) {
            circuitType {
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'deleteCircuitType':
                    {'circuitType': {'id': 'Q2lyY3VpdFR5cGVOb2RlOk5vbmU=', 'name': 'Type 1', 'slug': 'type1'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
