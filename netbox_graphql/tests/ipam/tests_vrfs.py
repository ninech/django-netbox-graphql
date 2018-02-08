from string import Template

from graphene.test import Client
from django.test import TestCase

from ipam.models import VRF

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import VRFFactory
from netbox_graphql.tests.factories.tenant_factories import TenantFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = TenantFactory()
        cls.query = Template('''
            mutation{
                newVrf(input: { tenant: "$tenantId",  name: "New Name", rd: "rd", enforceUnique: true }) {
                    vrf {
                        name
                        rd
                        enforceUnique
                        tenant {
                            name
                        }
                    }
                }
            }
            ''').substitute(tenantId=obj_to_global_id(cls.tenant))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newVrf':
                    {'vrf': {'name': 'New Name',
                             'rd': 'rd',
                             'enforceUnique': True,
                             'tenant': {'name': self.tenant.name}}}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = VRF.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VRF.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VRFFactory()
        cls.second = VRFFactory()
        cls.query = '''
        {
          vrfs {
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
        self.assertEquals(len(result.data['vrfs']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VRFFactory()
        cls.second = VRFFactory()
        cls.query = Template('''
        {
          vrfs(id: "$id") {
            edges {
              node {
                name
                rd
                enforceUnique
                tenant {
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
        self.assertEquals(len(result.data['vrfs']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'vrfs':
                    {'edges': [
                        {'node': {'name': self.first.name,
                                  'rd': self.first.rd,
                                  'enforceUnique': True,
                                  'tenant': {'name': self.first.tenant.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VRFFactory()
        cls.tenant = TenantFactory()
        cls.query = Template('''
         mutation{
          updateVrf(input: { id: "$id", name: "New Name", rd: "upd", tenant: "$tenantId" }) {
            vrf {
                name
                rd
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
        oldCount = VRF.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VRF.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateVrf': {'vrf': {'name': 'New Name',
                                          'rd': 'upd',
                                          'tenant': {'name': self.tenant.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        vrf = VRF.objects.get(id=self.first.id)
        self.assertEquals(vrf.name, 'New Name')
        self.assertEquals(vrf.rd, 'upd')
        self.assertEquals(vrf.tenant.name, self.tenant.name)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VRFFactory()
        cls.query = Template('''
        mutation{
          deleteVrf(input: { id: "$id" }) {
            vrf {
               id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = VRF.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VRF.objects.all().count(), oldCount - 1)
