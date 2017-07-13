from graphene import AbstractType
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from circuits.models import CircuitType, Circuit, Provider
from tenancy.models import Tenant
from filter_fields import date_types, string_types, number_types
from helper_methods import not_none

from graphene import AbstractType
from graphene import Field
from graphene import Node
from graphene import ClientIDMutation
from graphql_relay.node.node import from_global_id
from graphene import ID, Boolean, Float, Int, List, String

# Nodes
class ProviderNode(DjangoObjectType):
    asn = Float()
    custom_field_values = String()
    class Meta:
        model = Provider
        interfaces = (Node, )
        filter_fields = {
            'name': string_types,
            'slug': ['exact'],
            'asn' : number_types,
        }
        # filter_order_by = ('id')

class CircuitNode(DjangoObjectType):
    custom_field_values = String()
    class Meta:
        model = Circuit
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'cid': string_types,
            'commit_rate': number_types,
            'install_date': date_types,
            'description': string_types,
            'comments': string_types,
        }
        # filter_order_by = ('id', 'cid')

class CircuitTypeNode(DjangoObjectType):
    class Meta:
        model = CircuitType
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': string_types,
        }
        # filter_order_by = ('slug')

# Queries
class CircuitsQuery(AbstractType):
    providers = DjangoFilterConnectionField(ProviderNode)
    circuit_types = DjangoFilterConnectionField(CircuitTypeNode)
    circuit = Node.Field(CircuitNode)
    circuits = DjangoFilterConnectionField(CircuitNode)

# Mutations

class NewCircuitType(ClientIDMutation):
    circuit_type = Field(CircuitTypeNode)
    class Input:
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = CircuitType()
        temp.name = input.get('name')
        temp.slug = input.get('slug')
        temp.full_clean()
        temp.save()
        return NewCircuitType(circuit_type=temp)

class UpdateCircuitType(ClientIDMutation):
    circuit_type = Field(CircuitTypeNode)
    class Input:
        id = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = CircuitType.objects.get(pk=from_global_id(input.get('id'))[1])

        name = input.get('name')
        slug = input.get('slug')

        if not_none(name):
            temp.name = name
        if not_none(slug):
            temp.slug = slug
        temp.full_clean()
        temp.save()
        return UpdateCircuitType(circuit_type=temp)

class DeleteCircuitType(ClientIDMutation):
    circuit_type = Field(CircuitTypeNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        circuit_type = CircuitType.objects.get(pk=from_global_id(input.get('id'))[1])
        circuit_type.delete()
        return DeleteCircuitType(circuit_type=circuit_type)

class CircuitTypeMutation(AbstractType):
    new_circuit_type = NewCircuitType.Field()
    update_circuit_type = UpdateCircuitType.Field()
    delete_circuit_type = DeleteCircuitType.Field()

class NewProvider(ClientIDMutation):
    provider = Field(ProviderNode)
    class Input:
        name = String()
        slug = String()
        asn = Float()
        account = String(default_value="")
        portal_url = String(default_value="")
        noc_contact = String(default_value="")
        admin_contact = String(default_value="")
        comments = String(default_value="")
        custom_field_values = String(default_value="")

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Provider()
        temp.name = input.get('name')
        temp.slug = input.get('slug')
        temp.asn = input.get('asn')
        temp.account = input.get('account')
        temp.portal_url = input.get('portal_url')
        temp.noc_contact = input.get('noc_contact')
        temp.admin_contact = input.get('admin_contact')
        temp.comments = input.get('comments')
        temp.custom_field_values = input.get('custom_field_values')
        temp.full_clean()
        temp.save()
        return NewProvider(provider=temp)

class UpdateProvider(ClientIDMutation):
    provider = Field(ProviderNode)
    class Input:
        id = String()
        name = String()
        slug = String()
        asn = Float()
        account = String()
        portal_url = String()
        noc_contact = String()
        admin_contact = String()
        comments = String()
        custom_field_values = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Provider.objects.get(pk=from_global_id(input.get('id'))[1])

        name = input.get('name')
        slug = input.get('slug')
        asn = input.get('asn')
        account = input.get('account')
        portal_url = input.get('portal_url')
        noc_contact = input.get('noc_contact')
        admin_contact = input.get('admin_contact')
        comments = input.get('comments')
        custom_field_values = input.get('custom_field_values')

        if not_none(name):
            temp.name = name
        if not_none(slug):
            temp.slug = slug
        if not_none(asn):
            temp.asn = asn
        if not_none(account):
            temp.account = account
        if not_none(portal_url):
            temp.portal_url = portal_url
        if not_none(noc_contact):
            temp.noc_contact = noc_contact
        if not_none(admin_contact):
            temp.admin_contact = admin_contact
        if not_none(comments):
            temp.comments = comments
        if not_none(custom_field_values):
            temp.custom_field_values = custom_field_values
        temp.full_clean()
        temp.save()
        return UpdateProvider(provider=temp)

class DeleteProvider(ClientIDMutation):
    provider = Field(ProviderNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        provider = Provider.objects.get(pk=from_global_id(input.get('id'))[1])
        provider.delete()
        return DeleteProvider(provider=provider)

class ProviderMutation(AbstractType):
    new_provider = NewProvider.Field()
    update_provider = UpdateProvider.Field()
    delete_provider = DeleteProvider.Field()

class NewCircuit(ClientIDMutation):
    circuit = Field(CircuitNode)
    class Input:
        cid = String(default_value=None)
        provider = String(default_value=None)
        type = String(default_value=None)
        tenant = String(default_value=None)
        install_date = String(default_value=None)
        commit_rate = Int(default_value=None)
        description = String(default_value=None)
        comments = String(default_value=None)
        custom_field_values = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        cid = input.get('cid')
        provider = input.get('provider')
        type = input.get('type')
        tenant = input.get('tenant')
        install_date = input.get('install_date')
        commit_rate = input.get('commit_rate')
        description = input.get('description')
        comments = input.get('comments')
        custom_field_values =input.get('custom_field_values')

        temp = Circuit()

        if not_none(cid):
            temp.cid = cid
        if not_none(provider):
            temp.provider = Provider.objects.get(pk=from_global_id(input.get('provider'))[1])
        if not_none(type):
            temp.type = CircuitType.objects.get(pk=from_global_id(input.get('type'))[1])
        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(input.get('tenant'))[1])
        if not_none(install_date):
            temp.install_date = install_date
        if not_none(commit_rate):
            temp.commit_rate = commit_rate
        if not_none(description):
            temp.description = description
        if not_none(comments):
            temp.comments = comments
        if not_none(custom_field_values):
            temp.custom_field_values = custom_field_values
        temp.full_clean()
        temp.save()
        return NewCircuit(circuit=temp)

class UpdateCircuit(ClientIDMutation):
    circuit = Field(CircuitNode)
    class Input:
        id = String(default_value=None)
        cid = String(default_value=None)
        provider = String(default_value=None)
        type = String(default_value=None)
        tenant = String(default_value=None)
        install_date = String(default_value=None)
        commit_rate = Int(default_value=None)
        description = String(default_value=None)
        comments = String(default_value=None)
        custom_field_values = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        cid = input.get('cid')
        provider = input.get('provider')
        type = input.get('type')
        tenant = input.get('tenant')
        install_date = input.get('install_date')
        commit_rate = input.get('commit_rate')
        description = input.get('description')
        comments = input.get('comments')
        custom_field_values =input.get('custom_field_values')

        temp = Circuit.objects.get(pk=from_global_id(input.get('id'))[1])

        if not_none(cid):
            temp.cid = cid
        if not_none(provider):
            temp.provider = Provider.objects.get(pk=from_global_id(input.get('provider'))[1])
        if not_none(type):
            temp.type = CircuitType.objects.get(pk=from_global_id(input.get('type'))[1])
        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(input.get('tenant'))[1])
        if not_none(install_date):
            temp.install_date = install_date
        if not_none(commit_rate):
            temp.commit_rate = commit_rate
        if not_none(description):
            temp.description = description
        if not_none(comments):
            temp.comments = comments
        if not_none(custom_field_values):
            temp.custom_field_values = custom_field_values
        temp.full_clean()
        temp.save()
        return UpdateCircuit(circuit=temp)

class DeleteCircuit(ClientIDMutation):
    circuit = Field(CircuitNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        circuit = Circuit.objects.get(pk=from_global_id(input.get('id'))[1])
        circuit.delete()
        return DeleteCircuit(circuit=circuit)

class CircuitMutation(AbstractType):
    new_circuit = NewCircuit.Field()
    update_circuit = UpdateCircuit.Field()
    delete_circuit = DeleteCircuit.Field()