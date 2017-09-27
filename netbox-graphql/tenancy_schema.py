from graphene import AbstractType, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene import ID, Boolean, Float, Int, List, String
from graphene import AbstractType, Field, Node, ClientIDMutation, AbstractType
from graphql_relay.node.node import from_global_id

from .custom_filter_fields import date_types, string_types, number_types
from tenancy.models import Tenant, TenantGroup
from .helper_methods import not_none, set_and_save

# Nodes
class TenantGroupNode(DjangoObjectType):
    class Meta:
        model = TenantGroup
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': string_types,
        }


class TenantNode(DjangoObjectType):
    class Meta:
        model = Tenant
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'description': string_types,
            'comments': string_types,
        }

# Queries
class TenancyQuery(AbstractType):
    tenant_groups = DjangoFilterConnectionField(TenantGroupNode)
    tenants = DjangoFilterConnectionField(TenantGroupNode)

# Mutations
class NewTenantGroup(ClientIDMutation):
    tenant_group = Field(TenantGroupNode)
    class Input:
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        fields = [ 'name', 'slug' ]
        return NewTenantGroup(tenant_group=set_and_save(fields, input, TenantGroup()))

class UpdateTenantGroup(ClientIDMutation):
    tenant_group = Field(TenantGroupNode)
    class Input:
        id = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = TenantGroup.objects.get(pk=from_global_id(input.get('id'))[1])
        fields = [ 'name', 'slug' ]
        return UpdateTenantGroup(tenant_group=set_and_save(fields, input, temp))

class DeleteTenantGroup(ClientIDMutation):
    tenant_group = Field(TenantGroupNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = TenantGroup.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteTenantGroup(tenant_group=temp)

class TenancyMutations(AbstractType):
    # Tenant Group
    new_tenant_group = NewTenantGroup.Field()
    update_tenant_group = UpdateTenantGroup.Field()
    delete_tenant_group = DeleteTenantGroup.Field()
