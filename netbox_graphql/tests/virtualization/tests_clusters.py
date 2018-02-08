from string import Template

from graphene.test import Client
from django.test import TestCase

from virtualization.models import Cluster

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.virtualization_factories import ClusterFactory, ClusterTypeFactory, ClusterGroupFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.type = ClusterTypeFactory()
        cls.group = ClusterGroupFactory()
        cls.query = Template('''
            mutation{
              newCluster(input: { name: "New Cluster", type: "$typeId", group: "$groupId"}) {
                cluster{
                  name
                  type {
                    name
                  }
                }
              }
            }
            ''').substitute(typeId=obj_to_global_id(cls.type),
                            groupId=obj_to_global_id(cls.group))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newCluster':
                    {'cluster': {'name': 'New Cluster',
                                 'type': {'name': self.type.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Cluster.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Cluster.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterFactory()
        cls.second = ClusterFactory(type=cls.first.type)
        cls.third = ClusterFactory()
        cls.query = Template('''
        {
          clusters {
            edges {
              node {
                id
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_types_returns_three_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['clusters']['edges']), 3)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterFactory()
        cls.second = ClusterFactory(type=cls.first.type)
        cls.third = ClusterFactory()
        cls.query = Template('''
        {
          clusters(id: "$id") {
            edges {
              node {
                name
                type {
                    name
                }
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.third))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['clusters']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'clusters':
                    {'edges': [
                        {'node': {'name': self.third.name,
                                  'type': {'name': self.third.type.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterFactory()
        cls.type = ClusterTypeFactory()
        cls.query = Template('''
        mutation{
          updateCluster(input: { id:"$id", name: "New Name", type: "$typeId"}) {
            cluster{
              name
              type {
                name
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first), typeId=obj_to_global_id(cls.type))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Cluster.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Cluster.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateCluster':
                    {'cluster': {'name': 'New Name',
                                 'type': {'name': self.type.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        cluster = Cluster.objects.get(id=self.first.id)
        self.assertEquals(cluster.name, 'New Name')
        self.assertEquals(cluster.type, self.type)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterFactory()
        cls.query = Template('''
        mutation {
          deleteCluster(input: {id: "$id"}) {
            cluster {
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Cluster.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Cluster.objects.all().count(), oldCount - 1)
