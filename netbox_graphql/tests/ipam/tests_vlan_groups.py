from string import Template

from graphene.test import Client
from django.test import TestCase

from ipam.models import VLANGroup

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import VLANGroupFactory
from netbox_graphql.tests.factories.dcim_factories import SiteFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.site = SiteFactory()
        cls.query = Template('''
            mutation{
                newVlanGroup(input: { name: "VLANname", slug: "v1", site: "$siteId"}) {
                    vlanGroup{
                        name
                        slug
                        site {
                            name
                        }
                    }
                }
            }
            ''').substitute(siteId=obj_to_global_id(cls.site))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newVlanGroup':
                    {'vlanGroup': {'name': 'VLANname',
                                   'slug': 'v1',
                                   'site': {'name': self.site.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = VLANGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VLANGroup.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANGroupFactory()
        cls.second = VLANGroupFactory()
        cls.query = '''
        {
          vlanGroups {
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
        self.assertEquals(len(result.data['vlanGroups']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANGroupFactory()
        cls.second = VLANGroupFactory()
        cls.query = Template('''
        {
          vlanGroups(id: "$id") {
            edges {
              node {
                name
                slug
                site {
                  name
                }
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
        self.assertEquals(len(result.data['vlanGroups']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'vlanGroups':
                    {'edges': [
                        {'node': {'name': self.first.name,
                                  'slug': self.first.slug,
                                  'site': {'name': self.first.site.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANGroupFactory()
        cls.site = SiteFactory()
        cls.query = Template('''
        mutation{
          updateVlanGroup(input: { id:"$id", name: "New Name", slug: "nsl1", site: "$siteId"}) {
            vlanGroup{
              name
              slug
              site {
                name
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first),
                        siteId=obj_to_global_id(cls.site))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = VLANGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VLANGroup.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateVlanGroup':
                    {'vlanGroup': {'name': 'New Name',
                                   'slug': 'nsl1',
                                   'site': {'name': self.site.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        vlan_group = VLANGroup.objects.get(id=self.first.id)
        self.assertEquals(vlan_group.name, 'New Name')
        self.assertEquals(vlan_group.slug, 'nsl1')
        self.assertEquals(vlan_group.site.name, self.site.name)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANGroupFactory()
        cls.query = Template('''
        mutation{
          deleteVlanGroup(input: { id:"$id"}) {
            vlanGroup{
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = VLANGroup.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VLANGroup.objects.all().count(), oldCount - 1)
