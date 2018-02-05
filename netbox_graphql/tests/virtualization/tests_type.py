
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




class ClusterTypeTestCase(TestCase):
    def test_creating_new_cluster_type(self):
        query = '''
        mutation{
          newClusterType(input: { name: "clusterType1", slug: "clustertype1"}) {
            clusterType{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'newClusterType': {'clusterType': {
            'id': 'Q2x1c3RlclR5cGVOb2RlOjE=', 'name': 'clusterType1', 'slug': 'clustertype1'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_cluster_type(self):
        initialize_cluster_type('2')
        query = '''
        {
          clusterTypes(id: "Q2x1c3RlclR5cGVOb2RlOjI=") {
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
        expected = {'clusterTypes': {'edges': [
            {'node': {'id': 'Q2x1c3RlclR5cGVOb2RlOjI=', 'name': 'Type 2', 'slug': 'type2'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_cluster_type(self):
        initialize_cluster_type('3')
        query = '''
        mutation{
          updateClusterType(input: { id: "Q2x1c3RlclR5cGVOb2RlOjM=", name: "clusterTypeA", slug: "clustertypeA"}) {
            clusterType{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'updateClusterType': {'clusterType': {
            'id': 'Q2x1c3RlclR5cGVOb2RlOjM=', 'name': 'clusterTypeA', 'slug': 'clustertypeA'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_cluster_type(self):
        initialize_cluster_type('4')
        query = '''
        mutation{
          deleteClusterType(input: { id: "Q2x1c3RlclR5cGVOb2RlOjQ="}) {
            clusterType{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'deleteClusterType': {'clusterType': {
            'id': 'Q2x1c3RlclR5cGVOb2RlOk5vbmU=', 'name': 'Type 4', 'slug': 'type4'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
