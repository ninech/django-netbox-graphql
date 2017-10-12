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

# Queries
class IpamQuery(AbstractType):
    ip_address = DjangoFilterConnectionField(IPAddressNode)
    vlan_roles = DjangoFilterConnectionField(RoleNode)

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

class IpamMutations(AbstractType):
    # Roles
    new_vlan_role = NewRole.Field()
    update_vlan_role = UpdateRole.Field()
    delete_vlan_role = DeleteRole.Field()
