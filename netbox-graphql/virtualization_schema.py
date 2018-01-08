import graphene
from graphene import AbstractType, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene import AbstractType, Field, Node, ClientIDMutation, AbstractType
from graphene import ID, Boolean, Float, Int, List, String
from graphql_relay.node.node import from_global_id

from .custom_filter_fields import date_types, string_types, number_types
from .helper_methods import not_none, set_and_save
from virtualization.models import ClusterType, ClusterGroup, Cluster, VirtualMachine
from tenancy.models import Tenant
from dcim.models import Site, Interface, Platform, DeviceRole
from ipam.models import IPAddress

# Nodes
class ClusterTypeNode(DjangoObjectType):
    class Meta:
        model = ClusterType
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class ClusterGroupNode(DjangoObjectType):
    class Meta:
        model = ClusterGroup
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class ClusterNode(DjangoObjectType):
    class Meta:
        model = Cluster
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
        }

class VirtualMachineNode(DjangoObjectType):
    class Meta:
        model = VirtualMachine
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
        }

# Queries
class VirtualizationQuery(AbstractType):
    cluster_types = DjangoFilterConnectionField(ClusterTypeNode)
    cluster_groups = DjangoFilterConnectionField(ClusterGroupNode)
    clusters = DjangoFilterConnectionField(ClusterNode)
    virtual_machines = DjangoFilterConnectionField(VirtualMachineNode)

# Mutations
class NewClusterType(ClientIDMutation):
    cluster_type = Field(ClusterTypeNode)
    class Input:
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterType()

        fields = [ 'name', 'slug' ]
        return NewClusterType(cluster_type=set_and_save(fields, input, temp))

class UpdateClusterType(ClientIDMutation):
    cluster_type = Field(ClusterTypeNode)
    class Input:
        id = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterType.objects.get(pk=from_global_id(input.get('id'))[1])

        fields = [ 'name', 'slug' ]
        return UpdateClusterType(cluster_type=set_and_save(fields, input, temp))

class DeleteClusterType(ClientIDMutation):
    cluster_type = Field(ClusterTypeNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterType.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteClusterType(cluster_type=temp)

# Cluster Group
class NewClusterGroup(ClientIDMutation):
    cluster_group = Field(ClusterGroupNode)
    class Input:
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterGroup()

        fields = [ 'name', 'slug' ]
        return NewClusterGroup(cluster_group=set_and_save(fields, input, temp))

class UpdateClusterGroup(ClientIDMutation):
    cluster_group = Field(ClusterGroupNode)
    class Input:
        id = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterGroup.objects.get(pk=from_global_id(input.get('id'))[1])

        fields = [ 'name', 'slug' ]
        return UpdateClusterGroup(cluster_group=set_and_save(fields, input, temp))

class DeleteClusterGroup(ClientIDMutation):
    cluster_group = Field(ClusterGroupNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterGroup.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteClusterGroup(cluster_group=temp)

### Cluster

class NewCluster(ClientIDMutation):
    cluster = Field(ClusterNode)
    class Input:
        name = String(default_value=None)
        type = String(default_value=None)
        group = String(default_value=None)
        site = String(default_value=None)
        comments = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        type = input.get('type')
        group = input.get('group')
        site = input.get('site')

        temp = Cluster()

        if not_none(type):
            temp.type = ClusterType.objects.get(pk=from_global_id(type)[1])

        if not_none(group):
            temp.group = ClusterGroup.objects.get(pk=from_global_id(group)[1])

        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])

        fields = ['name', 'comments']
        return NewCluster(cluster=set_and_save(fields, input, temp))

class UpdateCluster(ClientIDMutation):
    cluster = Field(ClusterNode)
    class Input:
        id = String()
        name = String(default_value=None)
        type = String(default_value=None)
        group = String(default_value=None)
        site = String(default_value=None)
        comments = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Cluster.objects.get(pk=from_global_id(input.get('id'))[1])

        type = input.get('type')
        group = input.get('group')
        site = input.get('site')

        if not_none(type):
            temp.type = ClusterType.objects.get(pk=from_global_id(type)[1])

        if not_none(group):
            temp.group = ClusterGroup.objects.get(pk=from_global_id(group)[1])

        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])

        fields = ['name', 'comments']

        return UpdateCluster(cluster=set_and_save(fields, input, temp))

class DeleteCluster(ClientIDMutation):
    cluster = Field(ClusterNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Cluster.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteCluster(cluster=temp)

### Virtual machine

class NewVirtualMachine(ClientIDMutation):
    virtual_machine = Field(VirtualMachineNode)
    class Input:
        cluster = String(default_value=None)
        tenant = String(default_value=None)
        platform = String(default_value=None)
        name = String(default_value=None)
        status = Int(default_value=None)
        role = String(default_value=None)
        primary_ip4 = String(default_value=None)
        primary_ip6 = String(default_value=None)
        vcpus = Int(default_value=None)
        memory = Int(default_value=None)
        disk = Int(default_value=None)
        comments = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        cluster = input.get('cluster')
        tenant = input.get('tenant')
        platform = input.get('platform')
        role = input.get('role')
        primary_ip4 = input.get('primary_ip4')
        primary_ip6 = input.get('primary_ip6')

        temp = VirtualMachine()

        if not_none(cluster):
            temp.cluster = Cluster.objects.get(pk=from_global_id(cluster)[1])

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        if not_none(platform):
            temp.platform = Platform.objects.get(pk=from_global_id(platform)[1])

        if not_none(role):
            temp.role = DeviceRole.objects.get(pk=from_global_id(role)[1])

        if not_none(primary_ip4):
            temp.primary_ip4 = IPAddress.objects.get(pk=from_global_id(primary_ip4)[1])

        if not_none(primary_ip6):
            temp.primary_ip6 = IPAddress.objects.get(pk=from_global_id(primary_ip6)[1])

        fields = ['name', 'status', 'vcpus', 'memory', 'disk', 'comments']
        return NewVirtualMachine(virtual_machine=set_and_save(fields, input, temp))

class UpdateVirtualMachine(ClientIDMutation):
    virtual_machine = Field(VirtualMachineNode)
    class Input:
        id = String()
        cluster = String(default_value=None)
        tenant = String(default_value=None)
        platform = String(default_value=None)
        name = String(default_value=None)
        status = Int(default_value=None)
        role = String(default_value=None)
        primary_ip4 = String(default_value=None)
        primary_ip6 = String(default_value=None)
        vcpus = Int(default_value=None)
        memory = Int(default_value=None)
        disk = Int(default_value=None)
        comments = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VirtualMachine.objects.get(pk=from_global_id(input.get('id'))[1])

        cluster = input.get('cluster')
        tenant = input.get('tenant')
        platform = input.get('platform')
        role = input.get('role')
        primary_ip4 = input.get('primary_ip4')
        primary_ip6 = input.get('primary_ip6')

        if not_none(cluster):
            temp.cluster = Cluster.objects.get(pk=from_global_id(cluster)[1])

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        if not_none(platform):
            temp.platform = Platform.objects.get(pk=from_global_id(platform)[1])

        if not_none(role):
            temp.role = DeviceRole.objects.get(pk=from_global_id(role)[1])

        if not_none(primary_ip4):
            temp.primary_ip4 = IPAddress.objects.get(pk=from_global_id(primary_ip4)[1])

        if not_none(primary_ip6):
            temp.primary_ip6 = IPAddress.objects.get(pk=from_global_id(primary_ip6)[1])

        fields = ['name', 'status', 'vcpus', 'memory', 'disk', 'comments']

        return UpdateVirtualMachine(virtual_machine=set_and_save(fields, input, temp))

class DeleteVirtualMachine(ClientIDMutation):
    virtual_machine = Field(VirtualMachineNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VirtualMachine.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteVirtualMachine(virtual_machine=temp)

class VirtualizationMutations(AbstractType):
    # Cluster Type
    new_cluster_type = NewClusterType.Field()
    update_cluster_type = UpdateClusterType.Field()
    delete_cluster_type = DeleteClusterType.Field()
    # Cluster Group
    new_cluster_group = NewClusterGroup.Field()
    update_cluster_group = UpdateClusterGroup.Field()
    delete_cluster_group = DeleteClusterGroup.Field()
    # Cluster
    new_cluster = NewCluster.Field()
    update_cluster = UpdateCluster.Field()
    delete_cluster = DeleteCluster.Field()
    # Virtual Machine
    new_virtual_machine = NewVirtualMachine.Field()
    update_virtual_machine = UpdateVirtualMachine.Field()
    delete_virtual_machine = DeleteVirtualMachine.Field()
