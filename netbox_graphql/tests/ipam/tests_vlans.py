from string import Template

from graphene.test import Client
from django.test import TestCase

from ipam.models import VLAN

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.ipam_factories import VLANFactory, RoleFactory
from netbox_graphql.tests.factories.tenant_factories import TenantFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = TenantFactory()
        cls.role = RoleFactory()
        cls.query = Template('''
            mutation{
                newVlan(input: { tenant: "$tenantId", role: "$roleId", vid: 2, name: "New Vlan"}) {
                    vlan{
                        name
                        vid
                        tenant{
                            name
                        }
                        role{
                            name
                        }
                    }
                }
            }
            ''').substitute(tenantId=obj_to_global_id(cls.tenant),
                            roleId=obj_to_global_id(cls.role))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newVlan':
                    {'vlan': {'name': 'New Vlan',
                              'vid': 2,
                              'tenant': {'name': self.tenant.name},
                              'role': {'name': self.role.name}
                              }}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = VLAN.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VLAN.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANFactory()
        cls.second = VLANFactory()
        cls.query = '''
        {
          vlans {
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
        self.assertEquals(len(result.data['vlans']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANFactory()
        cls.second = VLANFactory()
        cls.query = Template('''
        {
          vlans(id: "$id") {
            edges {
              node {
                name
                vid
                tenant {
                  name
                }
                role {
                  name
                }
              }
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.second))

    def test_querying_single_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_querying_single_returns_result(self):
        result = schema.execute(self.query)
        self.assertEquals(len(result.data['vlans']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'vlans':
                    {'edges': [
                        {'node': {'name': self.second.name,
                                  'vid': self.second.vid,
                                  'tenant': {'name': self.second.tenant.name},
                                  'role': {'name': self.second.role.name}}}
                    ]}}
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANFactory()
        cls.tenant = TenantFactory()
        cls.query = Template('''
        mutation{
          updateVlan(input: { id: "$id", vid: 10, name: "New Name", tenant: "$tenantId"}) {
            vlan{
              name
              vid
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
        oldCount = VLAN.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VLAN.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateVlan':
                    {'vlan': {'name': 'New Name',
                              'vid': 10,
                              'tenant': {'name': self.tenant.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        vlan = VLAN.objects.get(id=self.first.id)
        self.assertEquals(vlan.name, 'New Name')
        self.assertEquals(vlan.vid, 10)
        self.assertEquals(vlan.tenant.name, self.tenant.name)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VLANFactory()
        cls.query = Template('''
        mutation{
          deleteVlan(input: { id:"$id"}) {
            vlan{
              id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = VLAN.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VLAN.objects.all().count(), oldCount - 1)
