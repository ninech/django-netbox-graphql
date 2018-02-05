import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import initialize_circuit_type, initialize_circuit, initialize_provider, initialize_circuit_termination, initialize_site
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class VRFTestCase(TestCase):
    def test_creating_new_vrf(self):
        initialize_vrf('1091')
        query = '''
        mutation{
          newVrf(input: { tenant: "VGVuYW50Tm9kZToxMDkx",  name: "vrf", rd: "rd", enforceUnique: true, description: "desc" }) {
            vrf{
                id
                name
                rd
                description
                enforceUnique
                tenant {
                name
              }
            }
          }
        }
        '''
        expected = {'newVrf': {'vrf': {'id': 'VlJGTm9kZTox', 'name': 'vrf', 'rd': 'rd',
                                       'description': 'desc', 'enforceUnique': True, 'tenant': {'name': 'Tenant 1091'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_vrf(self):
        initialize_vrf('1092')
        query = '''
        {
          vrfs(id: "VGVuYW50Tm9kZToxMDky") {
            edges {
              node {
                id
                name
                rd
                description
                enforceUnique
                tenant {
                  name
                }
              }
            }
          }
        }
        '''
        expected = {'vrfs': {'edges': [{'node': {'id': 'VlJGTm9kZToxMDky', 'name': 'vrf1092', 'rd': 'rd1092',
                                                 'description': 'description', 'enforceUnique': True, 'tenant': {'name': 'Tenant 1092'}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_vrf(self):
        initialize_vrf('2099')
        query = '''
        mutation{
          updateVrf(input: { id: "VlJGTm9kZToyMDk5", name: "vrfUpdate", rd: "rdUpdate", description: "desc" }) {
            vrf{
                id
                name
                rd
                description
                enforceUnique
            }
          }
        }
        '''
        expected = {'updateVrf': {'vrf': {'id': 'VlJGTm9kZToyMDk5', 'name': 'vrfUpdate',
                                          'rd': 'rdUpdate', 'description': 'desc', 'enforceUnique': True}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_vrf(self):
        initialize_vrf('1094')
        query = '''
        mutation{
          deleteVrf(input: { id: "VlJGTm9kZToxMDk0" }) {
            vrf{
               name
            }
          }
        }
        '''
        expected = {'deleteVrf': {'vrf': {'name': 'vrf1094'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
