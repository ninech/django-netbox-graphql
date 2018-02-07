from string import Template

from graphene.test import Client
from django.test import TestCase

from virtualization.models import ClusterGroup

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.virtualization_factories import ClusterGroupFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
            mutation{
              newClusterGroup(input: { name: "New Name", slug: "nsl1"}) {
                clusterGroup{
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
        expected = {'newClusterGroup':
                    {'clusterGroup': {'name': 'New Name', 'slug': 'nsl1'}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = ClusterGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(ClusterGroup.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterGroupFactory()
        cls.second = ClusterGroupFactory()
        cls.query = '''
        {
          clusterGroups {
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
        self.assertEquals(len(result.data['clusterGroups']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterGroupFactory()
        cls.second = ClusterGroupFactory()
        cls.query = Template('''
        {
          clusterGroups(id: "$id") {
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
        self.assertEquals(len(result.data['clusterGroups']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'clusterGroups':
                    {'edges': [
                        {'node': {'name': self.first.name}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterGroupFactory()
        cls.query = Template('''
        mutation{
          updateClusterGroup(input: { id: "$id", name: "New Name", slug: "nsl1"}) {
            clusterGroup {
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
        oldCount = ClusterGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(ClusterGroup.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateClusterGroup':
                    {'clusterGroup': {'name': 'New Name', 'slug': 'nsl1'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        circuit_type = ClusterGroup.objects.get(id=self.first.id)
        self.assertEquals(circuit_type.name, 'New Name')
        self.assertEquals(circuit_type.slug, 'nsl1')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = ClusterGroupFactory()
        cls.query = Template('''
        mutation{
          deleteClusterGroup(input: { id: "$id"}) {
            clusterGroup{
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = ClusterGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(ClusterGroup.objects.all().count(), oldCount - 1)
