import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class CircuitTestCase(TestCase):
    def test_creating_new_circuit(self):
        circuit_type = CircuitType(
            id='123',
            name='Type 123',
            slug='type123'
        )
        circuit_type.save()

        provider = Provider(
            id='124',
            name='Provider 124',
            slug='provider124',
            asn='256',
            account='12345',
            portal_url='https://www.nine.ch',
            noc_contact='noc_contact',
            admin_contact='admin_contact',
            comments='comments',
            created='2015-01-15'
        )
        provider.save()

        query = '''
        mutation {
          newCircuit(input: {cid: "cid112", provider:"UHJvdmlkZXJOb2RlOjEyNA==", type:"Q2lyY3VpdFR5cGVOb2RlOjEyMw==",
          installDate:"2017-10-12", commitRate: 12, description:"desc", comments:"dsadsa" }) {
            circuit {
              cid
              provider {
                id
                name
              }
              type {
                id
                name
              }
              installDate
              commitRate
              description
              comments
            }
          }
        }
        '''
        expected = {'newCircuit': {'circuit': {'cid': 'cid112',
                                               'provider': {'id': 'UHJvdmlkZXJOb2RlOjEyNA==', 'name': 'Provider 124'},
                                               'type': {'id': 'Q2lyY3VpdFR5cGVOb2RlOjEyMw==', 'name': 'Type 123'},
                                               'installDate': '2017-10-12', 'commitRate': 12, 'description': 'desc',
                                               'comments': 'dsadsa'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_circuit(self):
        initialize_circuit('112')
        query = '''
        {
          circuits(id: "Q2lyY3VpdE5vZGU6MTEy") {
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
                installDate
                commitRate
                description
              }
            }
          }
        }
        '''
        expected = {'circuits': {'edges': [{'node': {'id': 'Q2lyY3VpdE5vZGU6MTEy', 'cid': 'cid',
                                                     'provider': {'id': 'UHJvdmlkZXJOb2RlOjExMg==',
                                                                  'name': 'Provider112'},
                                                     'type': {'id': 'Q2lyY3VpdFR5cGVOb2RlOjExMg==', 'name': 'Type112'},
                                                     'installDate': '2017-10-12', 'commitRate': 12,
                                                     'description': 'desc'}}]}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_circuit(self):
        initialize_circuit('117')
        query = '''
        mutation {
          updateCircuit(input: {id: "Q2lyY3VpdE5vZGU6MTEy", cid: "ci3d", installDate:"2017-11-12", commitRate: 12,
           description:"someting", comments:"dsadsa" }) {
            circuit {
                id
                cid
                installDate
                commitRate
                description
                comments
            }
          }
        }
        '''
        expected = {'updateCircuit': {
            'circuit': {'id': 'Q2lyY3VpdE5vZGU6MTEy', 'cid': 'ci3d', 'installDate': '2017-11-12', 'commitRate': 12,
                        'description': 'someting', 'comments': 'dsadsa'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_circuit(self):
        initialize_circuit('115')
        query = '''
        mutation {
          deleteCircuit(input: {id: "Q2lyY3VpdE5vZGU6MTE1"}) {
            circuit {
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
                installDate
                commitRate
                description
                comments
            }
          }
        }
        '''
        expected = {'deleteCircuit': {'circuit': {'id': 'Q2lyY3VpdE5vZGU6Tm9uZQ==', 'cid': 'cid',
                                                  'provider': {'id': 'UHJvdmlkZXJOb2RlOjExNQ==', 'name': 'Provider115'},
                                                  'type': {'id': 'Q2lyY3VpdFR5cGVOb2RlOjExNQ==', 'name': 'Type115'},
                                                  'installDate': '2017-10-12', 'commitRate': 12, 'description': 'desc',
                                                  'comments': 'comments'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
