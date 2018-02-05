import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data  import initialize_circuit_type, initialize_circuit, initialize_provider, initialize_circuit_termination, initialize_site
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class CircuitTerminationTestCase(TestCase):
    def test_creating_new_circuit_termination(self):
        initialize_site('434')
        initialize_circuit('434')

        query = '''
        mutation {
          newCircuitTermination(input: {circuit: "Q2lyY3VpdE5vZGU6NDM0", portSpeed:128, termSide:"A", upstreamSpeed:128, site:"U2l0ZU5vZGU6NDM0", ppInfo:"ppInfo",xconnectId:"xconnectId" }) {
            circuitTermination {
              termSide
              portSpeed
              ppInfo
              upstreamSpeed
              xconnectId
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
        '''
        expected = {'newCircuitTermination': {
            'circuitTermination': {'termSide': 'A', 'portSpeed': 128,
                                   'ppInfo': 'ppInfo', 'upstreamSpeed': 128, 'xconnectId': 'xconnectId',
                                   'site': {'id': 'U2l0ZU5vZGU6NDM0', 'name': 'Site Name 434'},
                                   'circuit': {'id': 'Q2lyY3VpdE5vZGU6NDM0', 'cid': 'cid'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_circuit_termination(self):
        initialize_circuit_termination('789')
        query = '''
        {
          circuitTerminations(id:"Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3ODk=") {
            edges {
              node {
                termSide
                portSpeed
                ppInfo
                upstreamSpeed
                xconnectId
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
        '''
        expected = {'circuitTerminations': {'edges': [{'node': {'termSide': 'A', 'portSpeed': 256, 'ppInfo': 'pp_info', 'upstreamSpeed': 512, 'xconnectId': 'xconnect_id', 'site': {
            'id': 'U2l0ZU5vZGU6Nzg5', 'name': 'Site Name 789'}, 'circuit': {'id': 'Q2lyY3VpdE5vZGU6Nzg5', 'cid': 'cid'}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_circuit(self):
        initialize_circuit_termination('791')
        query = '''
        mutation {
          updateCircuitTermination(input: {id: "Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3ODk=", portSpeed:512, termSide:"Z", upstreamSpeed:512, ppInfo:"ppInfo123", xconnectId:"xconnectId123" }) {
            circuitTermination {
              id
              termSide
              portSpeed
              ppInfo
              upstreamSpeed
              xconnectId
            }
          }
        }
        '''
        expected = {'updateCircuitTermination': {'circuitTermination': {'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3ODk=',
                                                                        'termSide': 'Z', 'portSpeed': 512, 'ppInfo': 'ppInfo123', 'upstreamSpeed': 512, 'xconnectId': 'xconnectId123'}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_circuit_termination(self):
        initialize_circuit_termination('756')
        query = '''
        mutation {
          deleteCircuitTermination(input: {id: "Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3NTY=" }) {
            circuitTermination {
              id
              termSide
              portSpeed
              ppInfo
              upstreamSpeed
              xconnectId
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
        '''
        expected = {'deleteCircuitTermination': {'circuitTermination': {'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTpOb25l', 'termSide': 'A', 'portSpeed': 256, 'ppInfo': 'pp_info',
                                                                        'upstreamSpeed': 512, 'xconnectId': 'xconnect_id', 'site': {'id': 'U2l0ZU5vZGU6NzU2', 'name': 'Site Name 756'}, 'circuit': {'id': 'Q2lyY3VpdE5vZGU6NzU2', 'cid': 'cid'}}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
