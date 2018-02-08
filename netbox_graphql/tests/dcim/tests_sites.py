from string import Template

from graphene.test import Client
from django.test import TestCase

from dcim.models import Site

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.dcim_factories import SiteFactory, RegionFactory
from netbox_graphql.tests.factories.tenant_factories import TenantFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = RegionFactory()
        cls.tenant = TenantFactory()
        cls.query = Template('''
            mutation{
                newSite(input: { name:"New Name", slug: "nsl1", region:"$regionId", tenant: "$tenantId"}) {
                    site {
                        name
                        slug
                        region {
                            name
                        }
                        tenant {
                            name
                        }                   
                    }
                }
            }
            ''').substitute(regionId=obj_to_global_id(cls.region),
                            tenantId=obj_to_global_id(cls.tenant))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newSite':
                    {'site': {'name': 'New Name',
                              'slug': "nsl1",
                              'region': {'name': self.region.name},
                              'tenant': {'name': self.tenant.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = Site.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Site.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = SiteFactory()
        cls.second = SiteFactory()
        cls.query = '''
        {
          sites {
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
        self.assertEquals(len(result.data['sites']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = SiteFactory()
        cls.second = SiteFactory()
        cls.query = Template('''
        {
          sites(id: "$id") {
            edges {
              node {
                name
                region {
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
        self.assertEquals(len(result.data['sites']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'sites':
                    {'edges': [
                        {'node': {'name': self.first.name,
                                  'region': {'name': self.first.region.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = SiteFactory()
        cls.tenant = TenantFactory()
        cls.query = Template('''
        mutation{
          updateSite(input: { id: "$id" name:"New Name", tenant: "$tenantId"}) {
            site {
                name
                tenant {
                    name
                }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first),
                        tenantId=obj_to_global_id(cls.tenant))

    def test_updating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_updating_doesnt_change_count(self):
        oldCount = Site.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Site.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateSite':
                    {'site': {'name': 'New Name',
                              'tenant': {'name': self.tenant.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        site = Site.objects.get(id=self.first.id)
        self.assertEquals(site.name, 'New Name')
        self.assertEquals(site.tenant.name, self.tenant.name)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = SiteFactory()
        cls.query = Template('''
        mutation{
         deleteSite(input: { id:"$id" }) {
            site {
                id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = Site.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(Site.objects.all().count(), oldCount - 1)
