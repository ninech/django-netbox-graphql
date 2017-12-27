import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_cluster_type, initialize_cluster_group, initialize_cluster
from ..schema import schema
from virtualization.models import ClusterType
from ..helper_methods import print_result

pytestmark = pytest.mark.django_db

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
        expected = {'newClusterType': {'clusterType': {'id': 'Q2x1c3RlclR5cGVOb2RlOjE=', 'name': 'clusterType1', 'slug': 'clustertype1'}}}

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
        expected = {'clusterTypes': {'edges': [{'node': {'id': 'Q2x1c3RlclR5cGVOb2RlOjI=', 'name': 'Type 2', 'slug': 'type2'}}]}}

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
        expected = {'updateClusterType': {'clusterType': {'id': 'Q2x1c3RlclR5cGVOb2RlOjM=', 'name': 'clusterTypeA', 'slug': 'clustertypeA'}}}

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
        expected = {'deleteClusterType': {'clusterType': {'id': 'Q2x1c3RlclR5cGVOb2RlOk5vbmU=', 'name': 'Type 4', 'slug': 'type4'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

class ClusterGroupTestCase(TestCase):
    def test_creating_new_cluster_group(self):
        query = '''
        mutation{
          newClusterGroup(input: { name: "clusterGroup1", slug: "clustergroup1"}) {
            clusterGroup{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'newClusterGroup': {'clusterGroup': {'id': 'Q2x1c3Rlckdyb3VwTm9kZTox', 'name': 'clusterGroup1', 'slug': 'clustergroup1'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_cluster_group(self):
        initialize_cluster_group('2')
        query = '''
        {
          clusterGroups(id: "Q2x1c3Rlckdyb3VwTm9kZToy") {
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
        expected = {'clusterGroups': {'edges': [{'node': {'id': 'Q2x1c3Rlckdyb3VwTm9kZToy', 'name': 'Group 2', 'slug': 'group2'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_cluster_group(self):
        initialize_cluster_group('3')
        query = '''
        mutation{
          updateClusterGroup(input: { id: "Q2x1c3Rlckdyb3VwTm9kZToz", name: "clusterGroupA", slug: "clustergroupA"}) {
            clusterGroup{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'updateClusterGroup': {'clusterGroup': {'id': 'Q2x1c3Rlckdyb3VwTm9kZToz', 'name': 'clusterGroupA', 'slug': 'clustergroupA'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_cluster_group(self):
        initialize_cluster_group('4')
        query = '''
        mutation{
          deleteClusterGroup(input: { id: "Q2x1c3Rlckdyb3VwTm9kZTo0"}) {
            clusterGroup{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'deleteClusterGroup': {'clusterGroup': {'id': 'Q2x1c3Rlckdyb3VwTm9kZTpOb25l', 'name': 'Group 4', 'slug': 'group4'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

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
        expected = {'newCluster': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6MQ==', 'name': 'clusterA', 'type': {'id': 'Q2x1c3RlclR5cGVOb2RlOjEx'}}}}

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
        expected = {"clusters": {"edges": [{"node": {"id": "Q2x1c3Rlck5vZGU6MTI=", "name": "Cluster12", "type": {"id": "Q2x1c3RlclR5cGVOb2RlOjEy"}}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_cluster_group(self):
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
        expected = {'updateCluster': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6MTM=', 'name': 'clusterB', 'type': {'id': 'Q2x1c3RlclR5cGVOb2RlOjEz'}}}}

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
        expected = {'deleteCluster': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6Tm9uZQ==', 'name': 'Cluster14', 'type': {'id': 'Q2x1c3RlclR5cGVOb2RlOjE0'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
