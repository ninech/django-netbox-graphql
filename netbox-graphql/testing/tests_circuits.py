import pytest
import json
from graphene.test import Client
from snapshottest import TestCase
from ..data import initialize_circuits
from ..schema import schema

pytestmark = pytest.mark.django_db

class FieldsTestCase(TestCase):
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

class CircuitTypeTestCase(TestCase):
    def test_creating_new_circuit_type(self):
        query = '''
        mutation {
          newCircuitType(input: {name: "Type", slug: "type"}) {
            circuitType {
              id
              name
              slug
            }
          }
        }
        '''
        expected = { 'newCircuitType':
            {'circuitType': {'id': 'Q2lyY3VpdFR5cGVOb2RlOjE=', 'name': 'Type', 'slug': 'type'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_circuit_type(self):
        initialize_circuits()
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
        initialize_circuits()
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
        initialize_circuits()
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
