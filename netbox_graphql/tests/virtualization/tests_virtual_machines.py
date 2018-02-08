from string import Template

from graphene.test import Client
from django.test import TestCase

from virtualization.models import VirtualMachine

from netbox_graphql.schema import schema

from netbox_graphql.tests.utils import obj_to_global_id
from netbox_graphql.tests.factories.virtualization_factories import VirtualMachineFactory, ClusterFactory
from netbox_graphql.tests.factories.tenant_factories import TenantFactory
from netbox_graphql.tests.factories.dcim_factories import PlatformFactory
from netbox_graphql.tests.factories.ipam_factories import IPAddressFactory


class CreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cluster = ClusterFactory()
        cls.tenant = TenantFactory()
        cls.platform = PlatformFactory()
        cls.ipv4 = IPAddressFactory(family=4)
        cls.query = Template('''
            mutation{
              newVirtualMachine(input: { cluster: "$clusterId", tenant: "$tenantId", 
                                         platform: "$platformId", primaryIp4: "$ipv4Id",
                                         name: "New Name", status: 1, vcpus: 12, 
                                         memory:126, disk: 256 }) {
                virtualMachine {
                    name
                    cluster {
                      name
                    }
                    tenant {
                      name
                    }
                    platform {
                      name
                    }
                }
              }
            }
            ''').substitute(clusterId=obj_to_global_id(cls.cluster),
                            tenantId=obj_to_global_id(cls.tenant),
                            platformId=obj_to_global_id(cls.platform),
                            ipv4Id=obj_to_global_id(cls.ipv4))

    def test_creating_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_creating_returns_data(self):
        expected = {'newVirtualMachine':
                    {'virtualMachine': {'name': 'New Name',
                                        'cluster': {'name': self.cluster.name},
                                        'tenant': {'name': self.tenant.name},
                                        'platform': {'name': self.platform.name}, }}}

        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_creating_creates_it(self):
        oldCount = VirtualMachine.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VirtualMachine.objects.all().count(), oldCount + 1)


class QueryMultipleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VirtualMachineFactory()
        cls.second = VirtualMachineFactory()
        cls.query = '''
        {
          virtualMachines {
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
        self.assertEquals(len(result.data['virtualMachines']['edges']), 2)


class QuerySingleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VirtualMachineFactory()
        cls.query = Template('''
        {
          virtualMachines(id: "$id") {
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
        self.assertEquals(len(result.data['virtualMachines']['edges']), 1)

    def test_querying_single_returns_expected_result(self):
        result = schema.execute(self.query)
        expected = {'virtualMachines':
                    {'edges': [
                        {'node': {'name': self.first.name}}
                    ]}
                    }
        self.assertEquals(result.data, expected)


class UpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VirtualMachineFactory()
        cls.tenant = TenantFactory()
        cls.query = Template('''
        mutation {
          updateVirtualMachine(input: {id:"$id", tenant: "$tenantId", name: "New Name"}) {
            virtualMachine {
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
        oldCount = VirtualMachine.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VirtualMachine.objects.all().count(), oldCount)

    def test_updating_returns_updated_data(self):
        expected = {'updateVirtualMachine':
                    {'virtualMachine': {'name': 'New Name',
                                        'tenant': {'name': self.tenant.name}}}}
        result = schema.execute(self.query)
        self.assertEquals(result.data, expected)

    def test_updating_alters_data(self):
        schema.execute(self.query)
        virtual_machine = VirtualMachine.objects.get(id=self.first.id)
        self.assertEquals(virtual_machine.name, 'New Name')
        self.assertEquals(virtual_machine.tenant.name, self.tenant.name)


class DeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = VirtualMachineFactory()
        cls.query = Template('''
        mutation{
          deleteVirtualMachine(input: { id: "$id" }) {
            virtualMachine{
                id
            }
          }
        }
        ''').substitute(id=obj_to_global_id(cls.first))

    def test_deleting_returns_no_error(self):
        result = schema.execute(self.query)
        assert not result.errors

    def test_deleting_removes_a_type(self):
        oldCount = VirtualMachine.objects.all().count()
        schema.execute(self.query)
        self.assertEquals(VirtualMachine.objects.all().count(), oldCount - 1)
