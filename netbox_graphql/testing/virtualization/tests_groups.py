import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


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
        expected = {'newClusterGroup': {'clusterGroup': {
            'id': 'Q2x1c3Rlckdyb3VwTm9kZTox', 'name': 'clusterGroup1', 'slug': 'clustergroup1'}}}

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
        expected = {'clusterGroups': {'edges': [
            {'node': {'id': 'Q2x1c3Rlckdyb3VwTm9kZToy', 'name': 'Group 2', 'slug': 'group2'}}]}}

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
        expected = {'updateClusterGroup': {'clusterGroup': {
            'id': 'Q2x1c3Rlckdyb3VwTm9kZToz', 'name': 'clusterGroupA', 'slug': 'clustergroupA'}}}

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
        expected = {'deleteClusterGroup': {'clusterGroup': {
            'id': 'Q2x1c3Rlckdyb3VwTm9kZTpOb25l', 'name': 'Group 4', 'slug': 'group4'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
