
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.tests.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination




class VirtualMachineTestCase(TestCase):
    def test_creating_new_vm(self):
        initialize_cluster('21')
        query = '''
            mutation{
              newVirtualMachine(input: { cluster:"Q2x1c3Rlck5vZGU6MjE=", name: "virtual machine", status: 1, vcpus: 12, memory:126, disk: 256, comments: "test" }) {
                virtualMachine{
                    cluster {
                      id
                    }
                    name
                    status
                    vcpus
                    memory
                    disk
                    comments
                }
              }
            }
            '''
        expected = {'newVirtualMachine': {'virtualMachine': {'cluster': {'id': 'Q2x1c3Rlck5vZGU6MjE='},
                                                             'name': 'virtual machine', 'status': 'A_1', 'vcpus': 12, 'memory': 126, 'disk': 256, 'comments': 'test'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_vm(self):
        initialize_virtual_machine('22')
        query = '''
        {
          virtualMachines(id: "VmlydHVhbE1hY2hpbmVOb2RlOjIy") {
            edges {
              node {
                id
                cluster {
                  id
                }
                name
                status
                vcpus
                memory
                disk
                comments
              }
            }
          }
        }
        '''
        expected = {'virtualMachines': {'edges': [{'node': {'id': 'VmlydHVhbE1hY2hpbmVOb2RlOjIy', 'cluster': {
            'id': 'Q2x1c3Rlck5vZGU6MjI='}, 'name': 'VM22', 'status': 'A_1', 'vcpus': 128, 'memory': 256, 'disk': 512, 'comments': 'txt'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_virtual_machine(self):
        initialize_virtual_machine('24')
        query = '''
        mutation{
          deleteVirtualMachine(input: { id: "VmlydHVhbE1hY2hpbmVOb2RlOjI0" }) {
            virtualMachine{
                id
                name
                status
            }
          }
        }
        '''
        expected = {'deleteVirtualMachine': {'virtualMachine': {
            'id': 'VmlydHVhbE1hY2hpbmVOb2RlOk5vbmU=', 'name': 'VM24', 'status': 'A_1'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
