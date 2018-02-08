from string import Template

from graphene.test import Client
from django.test import TestCase

from dcim.models import Region

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.dcim_factories import RegionFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.parent = RegionFactory()
        cls.query = Template('''
            mutation{
                newRegion(input: { parent:"$parentId", name: "New Name", slug: "nsl1"}) {
                    region{
                        name
                        slug
                        parent{
                            name
                        }
                    }
                }
            }
            ''').substitute(parentId=obj_to_global_id(cls.parent))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newRegion':
                    {'region': {'name': 'New Name',
                                'slug': "nsl1",
                                'parent': {'name': self.parent.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Region.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Region.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RegionFactory()
        cls.second = RegionFactory()
        cls.query = '''
        {
          regions {
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
        self.assertEquals(len(result.data['regions']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RegionFactory()
        cls.second = RegionFactory()
        cls.query = Template('''
        {
          regions(id: "$id") {
            edges {
              node {
                name
                slug
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
        self.assertEquals(len(result.data['regions']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'regions':
                    {'edges': [
                        {'node': {'name': self.first.name,
                                  'slug': self.first.slug}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RegionFactory()
        cls.parent = RegionFactory()
        cls.query = Template('''
        mutation{
          updateRegion(input: { id:"$id", parent:"$parentId", slug: "nsl1"}) {
            region{
              slug
              parent{
                name
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first),
                        parentId=obj_to_global_id(cls.parent))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Region.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Region.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateRegion':
                    {'region': {'slug': 'nsl1',
                                'parent': {'name': self.parent.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        region = Region.objects.get(id=self.first.id)
        self.assertEquals(region.slug, 'nsl1')
        self.assertEquals(region.parent.name, self.parent.name)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RegionFactory()
        cls.query = Template('''
        mutation{
          deleteRegion(input: { id:"$id"}) {
            region{
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Region.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Region.objects.all().count(), oldCount - 1)
