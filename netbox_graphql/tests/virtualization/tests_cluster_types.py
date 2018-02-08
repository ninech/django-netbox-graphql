from string import Template

from graphene.test import Client
from django.test import TestCase

from virtualization.models import ClusterType

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.virtualization_factories import ClusterTypeFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
            mutation{
                newClusterType(input: { name: "Cluster Name", slug: "cl1"}) {
                    clusterType {
                        name
                        slug
                    }
                }
            }
            '''

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newClusterType':
                    {'clusterType': {'name': 'Cluster Name', 'slug': 'cl1'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = ClusterType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(ClusterType.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterTypeFactory()
        cls.second = ClusterTypeFactory()
        cls.query = '''
        {
          clusterTypes {
            edges {
              node {
                id
              }
            }
          }
        }
        '''

    def test_querying_all_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_all_returns_two_results(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['clusterTypes']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterTypeFactory()
        cls.query = Template('''
        {
          clusterTypes(id: "$id") {
            edges {
              node {
                name
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['clusterTypes']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'clusterTypes':
                    {'edges': [
                        {'node': {'name': self.first.name}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterTypeFactory()
        cls.query = Template('''
        mutation {
          updateClusterType(input: { id: "$id", name: "New Name", slug: "nsl1"}) {
            clusterType {
              name
              slug
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = ClusterType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(ClusterType.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateClusterType':
                    {'clusterType': {'name': 'New Name', 'slug': 'nsl1'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        cluster_type_factory = ClusterType.objects.get(id=self.first.id)
        self.assertEquals(cluster_type_factory.name, 'New Name')
        self.assertEquals(cluster_type_factory.slug, 'nsl1')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterTypeFactory()
        cls.query = Template('''
        mutation{
          deleteClusterType(input: { id: "$id"}) {
            clusterType{
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = ClusterType.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(ClusterType.objects.all().count(), oldCount - 1)
