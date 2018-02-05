import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class ClusterTestCase(TestCase):
    def test_creating_new_cluster(self):
        initialize_cluster_type('11')
        query = '''
        mutation{
          newCluster(input: { name: "clusterA", type: "Q2x1c3RlclR5cGVOb2RlOjEx"}) {
            cluster{
              id
              name
              type {
                id
              }
            }
          }
        }
        '''
        expected = {'newCluster': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6MQ==',
                                               'name': 'clusterA', 'type': {'id': 'Q2x1c3RlclR5cGVOb2RlOjEx'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_cluster(self):
        initialize_cluster('12')
        query = '''
        {
          clusters(id: "Q2x1c3Rlck5vZGU6MTI=") {
            edges {
              node {
                id
                name
                type {
                  id
                }
              }
            }
          }
        }
        '''
        expected = {"clusters": {"edges": [{"node": {
            "id": "Q2x1c3Rlck5vZGU6MTI=", "name": "Cluster12", "type": {"id": "Q2x1c3RlclR5cGVOb2RlOjEy"}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_cluster(self):
        initialize_cluster('13')
        query = '''
        mutation{
          updateCluster(input: { id:"Q2x1c3Rlck5vZGU6MTM=", name: "clusterB", type: "Q2x1c3RlclR5cGVOb2RlOjEz"}) {
            cluster{
              id
              name
              type {
                id
              }
            }
          }
        }
        '''
        expected = {'updateCluster': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6MTM=',
                                                  'name': 'clusterB', 'type': {'id': 'Q2x1c3RlclR5cGVOb2RlOjEz'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_cluster(self):
        initialize_cluster('14')
        query = '''
        mutation{
          deleteCluster(input: { id:"Q2x1c3Rlck5vZGU6MTQ="}) {
            cluster{
              id
              name
              type {
                id
              }
            }
          }
        }
        '''
        expected = {'deleteCluster': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6Tm9uZQ==',
                                                  'name': 'Cluster14', 'type': {'id': 'Q2x1c3RlclR5cGVOb2RlOjE0'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected


def print_virtual_machine(id):
    initialize_virtual_machine(id)
    query = '''
    {
      virtualMachines {
        edges {
          node {
            id
            cluster {
              id
            }
            tenant {
              id
            }
            platform {
              id
            }
            name
            status
            role {
              id
            }
            primaryIp4 {
              id
            }
            primaryIp6 {
              id
            }
            vcpus
            memory
            disk
            comments
          }
        }
      }
    }
    '''

    result = schema.execute(query)
    print_result(result)
