import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_circuit_type, initialize_circuit, initialize_provider, initialize_circuit_termination, initialize_site
from ..schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

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
              name
              slug
            }
          }
        }
        '''
        expected = { 'newCircuitType':
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
                        {'provider': { 'slug': 'provider123', 'name': 'Provider123',
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

class CircuitTestCase(TestCase):
    def test_creating_new_circuit(self):
        circuit_type = CircuitType(
            id = '123',
            name = 'Type 123',
            slug = 'type123'
        )
        circuit_type.save()

        provider = Provider(
            id = '124',
            name = 'Provider 124',
            slug = 'provider124',
            asn = '256',
            account = '12345',
            portal_url = 'https://www.nine.ch',
            noc_contact = 'noc_contact',
            admin_contact = 'admin_contact',
            comments = 'comments',
            created = '2015-01-15'
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
        expected = {'circuitTerminations': {'edges': [{'node': {'termSide': 'A', 'portSpeed': 256, 'ppInfo': 'pp_info', 'upstreamSpeed': 512, 'xconnectId': 'xconnect_id', 'site': {'id': 'U2l0ZU5vZGU6Nzg5', 'name': 'Site Name 789'}, 'circuit': {'id': 'Q2lyY3VpdE5vZGU6Nzg5', 'cid': 'cid'}}}]}}

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
        expected = {'updateCircuitTermination': {'circuitTermination': {'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3ODk=', 'termSide': 'Z', 'portSpeed': 512, 'ppInfo': 'ppInfo123', 'upstreamSpeed': 512, 'xconnectId': 'xconnectId123'}}}
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
        expected = {'deleteCircuitTermination': {'circuitTermination': {'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTpOb25l', 'termSide': 'A', 'portSpeed': 256, 'ppInfo': 'pp_info', 'upstreamSpeed': 512, 'xconnectId': 'xconnect_id', 'site': {'id': 'U2l0ZU5vZGU6NzU2', 'name': 'Site Name 756'}, 'circuit': {'id': 'Q2lyY3VpdE5vZGU6NzU2', 'cid': 'cid'}}}}
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
