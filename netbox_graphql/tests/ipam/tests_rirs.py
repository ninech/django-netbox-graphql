from string import Template

from graphene.test import Client
from django.test import TestCase

from ipam.models import RIR

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import RIRFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = '''
            mutation{
                newRir(input: { name: "New Name",  slug: "rir", isPrivate: true }) {
                    rir{
                        name
                        slug
                        isPrivate
                    }
                }
            }
            '''

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newRir':
                    {'rir': {'name': 'New Name',
                             'slug': 'rir',
                             'isPrivate': True}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = RIR.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(RIR.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RIRFactory()
        cls.second = RIRFactory()
        cls.query = '''
        {
          rirs {
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
        self.assertEquals(len(result.data['rirs']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RIRFactory()
        cls.second = RIRFactory()
        cls.query = Template('''
        {
          rirs(id: "$id") {
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
        self.assertEquals(len(result.data['rirs']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'rirs':
                    {'edges': [
                        {'node': {'name': self.first.name,
                                  'slug': self.first.slug, }}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RIRFactory()
        cls.query = Template('''
        mutation{
          updateRir(input: { id:"$id", name: "New Name", slug: "nsl1" }) {
            rir{
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
        oldCount = RIR.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(RIR.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateRir':
                    {'rir': {'name': 'New Name',
                             'slug': 'nsl1'}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        rir = RIR.objects.get(id=self.first.id)
        self.assertEquals(rir.name, 'New Name')
        self.assertEquals(rir.slug, 'nsl1')


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RIRFactory()
        cls.query = Template('''
        mutation{
          deleteRir(input: { id:"$id" }) {
            rir{
                id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = RIR.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(RIR.objects.all().count(), oldCount - 1)
