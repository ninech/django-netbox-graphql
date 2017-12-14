import graphene
from graphene import AbstractType, Node
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene import AbstractType, Field, Node, ClientIDMutation, AbstractType
from graphene import ID, Boolean, Float, Int, List, String
from graphql_relay.node.node import from_global_id
from .custom_filter_fields import date_types, string_types, number_types
from .helper_methods import not_none, set_and_save
from ipam.models import IPAddress, VLANGroup, Role, VLAN, VRF, RIR, Aggregate
from tenancy.models import Tenant
from ipam.fields import IPNetworkField, IPAddressField
from dcim.models import Site

@convert_django_field.register(IPNetworkField)
def iPNetworkFieldConvert(field, registry=None):
    return graphene.String()

@convert_django_field.register(IPAddressField)
def iPAddressFieldConvert(field, registry=None):
    return graphene.String()

# Nodes
class IPAddressNode(DjangoObjectType):
    class Meta:
        model = IPAddress
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact']
        }

class RoleNode(DjangoObjectType):
    class Meta:
        model = Role
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class VLANGroupNode(DjangoObjectType):
    class Meta:
        model = VLANGroup
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class VLANNode(DjangoObjectType):
    class Meta:
        model = VLAN
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
        }

class VRFNode(DjangoObjectType):
    class Meta:
        model = VRF
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
        }

class RIRNode(DjangoObjectType):
    class Meta:
        model = RIR
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class AggregateNode(DjangoObjectType):
    class Meta:
        model = Aggregate
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
        }

# Queries
class IpamQuery(AbstractType):
    ip_address = DjangoFilterConnectionField(IPAddressNode)
    vlan_roles = DjangoFilterConnectionField(RoleNode)
    vlan_groups = DjangoFilterConnectionField(VLANGroupNode)
    vlans = DjangoFilterConnectionField(VLANNode)
    vrfs = DjangoFilterConnectionField(VRFNode)
    rirs = DjangoFilterConnectionField(RIRNode)
    aggregates = DjangoFilterConnectionField(AggregateNode)

# Mutations
class NewRole(ClientIDMutation):
    vlan_role = Field(RoleNode)
    class Input:
        slug = String()
        name = String(default_value=None)
        weight = Int(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Role()
        fields = ['name', 'slug', 'weight']
        return NewRole(vlan_role=set_and_save(fields, input, temp))

class UpdateRole(ClientIDMutation):
    vlan_role = Field(RoleNode)
    class Input:
        id = String()
        slug = String(default_value=None)
        name = String(default_value=None)
        weight = Int(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Role.objects.get(pk=from_global_id(input.get('id'))[1])
        fields = [ 'name', 'slug', 'weight' ]
        return UpdateRole(vlan_role=set_and_save(fields, input, temp))

class DeleteRole(ClientIDMutation):
    vlan_role = Field(RoleNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Role.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteRole(vlan_role=temp)

class NewVLANGroup(ClientIDMutation):
    vlan_group = Field(VLANGroupNode)
    class Input:
        name = String(default_value=None)
        slug = String(default_value=None)
        site = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        site = input.get('site')

        temp = VLANGroup()

        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])

        fields = [ 'name', 'slug' ]
        return NewVLANGroup(vlan_group=set_and_save(fields, input, temp))

class UpdateVLANGroup(ClientIDMutation):
    vlan_group = Field(VLANGroupNode)
    class Input:
        id = String()
        name = String(default_value=None)
        slug = String(default_value=None)
        site = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VLANGroup.objects.get(pk=from_global_id(input.get('id'))[1])

        site = input.get('site')

        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])

        fields = [ 'name', 'slug' ]
        return UpdateVLANGroup(vlan_group=set_and_save(fields, input, temp))

class DeleteVLANGroup(ClientIDMutation):
    vlan_group = Field(VLANGroupNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VLANGroup.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteVLANGroup(vlan_group=temp)

class NewVLAN(ClientIDMutation):
    vlan = Field(VLANNode)
    class Input:
        site = String(default_value=None)
        group = String(default_value=None)
        vid = Int(default_value=None)
        name = String(default_value=None)
        tenant = String(default_value=None)
        status = Int(default_value=None)
        role = String(default_value=None)
        description = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        site = input.get('site')
        group = input.get('group')
        tenant = input.get('tenant')
        role = input.get('role')

        temp = VLAN()

        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])

        if not_none(group):
            temp.group = VLANGroup.objects.get(pk=from_global_id(group)[1])

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        if not_none(role):
            temp.role = Role.objects.get(pk=from_global_id(role)[1])

        fields = [ 'name', 'vid', 'name', 'description' ]
        return NewVLAN(vlan=set_and_save(fields, input, temp))

class UpdateVLAN(ClientIDMutation):
    vlan = Field(VLANNode)
    class Input:
        id = String()
        site = String(default_value=None)
        group = String(default_value=None)
        vid = Int(default_value=None)
        name = String(default_value=None)
        tenant = String(default_value=None)
        status = Int(default_value=None)
        role = String(default_value=None)
        description = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VLAN.objects.get(pk=from_global_id(input.get('id'))[1])

        site = input.get('site')
        group = input.get('group')
        tenant = input.get('tenant')
        role = input.get('role')

        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])

        if not_none(group):
            temp.group = VLANGroup.objects.get(pk=from_global_id(group)[1])

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        if not_none(role):
            temp.role = Role.objects.get(pk=from_global_id(role)[1])

        fields = [ 'name', 'vid', 'name', 'description' ]
        return UpdateVLAN(vlan=set_and_save(fields, input, temp))

class DeleteVLAN(ClientIDMutation):
    vlan = Field(VLANNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VLAN.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteVLAN(vlan=temp)

# VRF
class NewVRF(ClientIDMutation):
    vrf = Field(VRFNode)
    class Input:
        name = String(default_value=None)
        rd = String(default_value=None)
        tenant = String(default_value=None)
        enforce_unique = Boolean(default_value=None)
        description = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        tenant = input.get('tenant')

        temp = VRF()

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        fields = ['name', 'rd', 'enforce_unique', 'description']
        return NewVRF(vrf=set_and_save(fields, input, temp))

class UpdateVRF(ClientIDMutation):
    vrf = Field(VRFNode)
    class Input:
        id = String()
        name = String(default_value=None)
        rd = String(default_value=None)
        tenant = String(default_value=None)
        enforce_unique = Boolean(default_value=None)
        description = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VRF.objects.get(pk=from_global_id(input.get('id'))[1])

        tenant = input.get('tenant')

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        fields = ['name', 'rd', 'enforce_unique', 'description']
        return UpdateVRF(vrf=set_and_save(fields, input, temp))

class DeleteVRF(ClientIDMutation):
    vrf = Field(VRFNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = VRF.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteVRF(vrf=temp)

# RIR
class NewRIR(ClientIDMutation):
    rir = Field(RIRNode)
    class Input:
        name = String(default_value=None)
        slug = String(default_value=None)
        is_private = Boolean(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):

        temp = RIR()

        fields = ['name', 'slug', 'is_private']
        return NewRIR(rir=set_and_save(fields, input, temp))

class UpdateRIR(ClientIDMutation):
    rir = Field(RIRNode)
    class Input:
        id = String()
        name = String(default_value=None)
        slug = String(default_value=None)
        is_private = Boolean(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = RIR.objects.get(pk=from_global_id(input.get('id'))[1])

        fields = ['name', 'slug', 'is_private']
        return UpdateRIR(rir=set_and_save(fields, input, temp))

class DeleteRIR(ClientIDMutation):
    rir = Field(RIRNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = RIR.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteRIR(rir=temp)

# Aggregate
class NewAggregate(ClientIDMutation):
    aggregate = Field(AggregateNode)
    class Input:
        family = Int(default_value=None)
        prefix = String(default_value=None)
        rir = String(default_value=None)
        date_added = String(default_value=None)
        description = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        rir = input.get('rir')

        temp = Aggregate()

        if not_none(rir):
            temp.rir = RIR.objects.get(pk=from_global_id(rir)[1])

        fields = ['family', 'prefix', 'date_added', 'description']
        return NewAggregate(aggregate=set_and_save(fields, input, temp))

class UpdateAggregate(ClientIDMutation):
    aggregate = Field(AggregateNode)
    class Input:
        id = String()
        family = Int(default_value=None)
        prefix = String(default_value=None)
        rir = String(default_value=None)
        date_added = String(default_value=None)
        description = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        rir = input.get('rir')
        temp = Aggregate.objects.get(pk=from_global_id(input.get('id'))[1])

        if not_none(rir):
            temp.rir = RIR.objects.get(pk=from_global_id(rir)[1])

        fields = ['family', 'prefix', 'date_added', 'description']

        return UpdateAggregate(aggregate=set_and_save(fields, input, temp))

class DeleteAggregate(ClientIDMutation):
    aggregate = Field(AggregateNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Aggregate.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteAggregate(aggregate=temp)

class IpamMutations(AbstractType):
    # Roles
    new_vlan_role = NewRole.Field()
    update_vlan_role = UpdateRole.Field()
    delete_vlan_role = DeleteRole.Field()
    # VLAN Group
    new_vlan_group = NewVLANGroup.Field()
    update_vlan_group = UpdateVLANGroup.Field()
    delete_vlan_group = DeleteVLANGroup.Field()
    # VLAN
    new_vlan = NewVLAN.Field()
    update_vlan = UpdateVLAN.Field()
    delete_vlan = DeleteVLAN.Field()
    # VRF
    new_vrf = NewVRF.Field()
    update_vrf = UpdateVRF.Field()
    delete_vrf = DeleteVRF.Field()
    # RIR
    new_rir = NewRIR.Field()
    update_rir = UpdateRIR.Field()
    delete_rir = DeleteRIR.Field()
    # Aggregate
    new_aggregate = NewAggregate.Field()
    update_aggregate = UpdateAggregate.Field()
    delete_aggregate = DeleteAggregate.Field()
