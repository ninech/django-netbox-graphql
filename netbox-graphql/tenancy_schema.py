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
    tenants = DjangoFilterConnectionField(TenantNode)

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

class NewTenant(ClientIDMutation):
    tenant = Field(TenantNode)
    class Input:
        name = String()
        slug = String()
        group = String(default_value=None)
        description = String(default_value=None)
        comments = String(default_value=None)
        custom_field_values = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        fields = [ 'name', 'slug', 'description', 'comments', 'custom_field_values' ]
        group = input.get('group')

        temp = Tenant()

        if not_none(group):
            temp.group = TenantGroup.objects.get(pk=from_global_id(group)[1])

        return NewTenant(tenant=set_and_save(fields, input, temp))

class UpdateTenant(ClientIDMutation):
    tenant = Field(TenantNode)
    class Input:
        id = String(default_value=None)
        name = String(default_value=None)
        slug = String(default_value=None)
        group = String(default_value=None)
        description = String(default_value=None)
        comments = String(default_value=None)
        custom_field_values = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        group = input.get('group')

        temp = Tenant.objects.get(pk=from_global_id(input.get('id'))[1])

        if not_none(group):
            temp.group = TenantGroup.objects.get(pk=from_global_id(group)[1])

        fields = [ 'name', 'slug', 'description', 'comments', 'custom_field_values' ]
        return UpdateTenant(tenant=set_and_save(fields, input, temp))

class DeleteTenant(ClientIDMutation):
    tenant = Field(TenantNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Tenant.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteTenant(tenant=temp)

class TenancyMutations(AbstractType):
    # Tenant Group
    new_tenant_group = NewTenantGroup.Field()
    update_tenant_group = UpdateTenantGroup.Field()
    delete_tenant_group = DeleteTenantGroup.Field()
    # Tenant
    new_tenant = NewTenant.Field()
    update_tenant = UpdateTenant.Field()
    delete_tenant = DeleteTenant.Field()
