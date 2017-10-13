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
from ipam.models import IPAddress, VLANGroup, Role, VLAN
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

# Queries
class IpamQuery(AbstractType):
    ip_address = DjangoFilterConnectionField(IPAddressNode)
    vlan_roles = DjangoFilterConnectionField(RoleNode)
    vlan_groups = DjangoFilterConnectionField(VLANGroupNode)

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

class IpamMutations(AbstractType):
    # Roles
    new_vlan_role = NewRole.Field()
    update_vlan_role = UpdateRole.Field()
    delete_vlan_role = DeleteRole.Field()
    # VLAN Group
    new_vlan_group = NewVLANGroup.Field()
    update_vlan_group = UpdateVLANGroup.Field()
    delete_vlan_group = DeleteVLANGroup.Field()
