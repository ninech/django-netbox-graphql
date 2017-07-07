from graphene import AbstractType
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from circuits.models import CircuitType, Circuit, Provider
from filter_fields import date_types, string_types, number_types

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
        temp = CircuitType(
            name = input.get('name') ,
            slug = input.get('slug') ,
        )
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
        circuit_type = CircuitType.objects.get(pk=from_global_id(input.get('id'))[1])
        circuit_type.name=input.get('name')
        circuit_type.slug=input.get('slug')
        circuit_type.full_clean()
        circuit_type.save()
        return UpdateCircuitType(circuit_type=circuit_type)

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
        account = String()
        portal_url = String()
        noc_contact = String()
        admin_contact = String()
        comments = String()
        custom_field_values = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Provider(
            name = input.get('name') ,
            slug = input.get('slug') ,
            asn = input.get('asn') ,
            account = input.get('account') ,
            portal_url = input.get('portal_url') ,
            noc_contact = input.get('noc_contact') ,
            admin_contact = input.get('admin_contact') ,
            comments = input.get('comments') ,
            custom_field_values = input.get('custom_field_values'),
        )
        temp.full_clean()
        temp.save()
        return NewProvider(provider=temp)

class UpdateProvider(ClientIDMutation):
    provider = Field(ProviderNode)
    class Input:
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
        provider = Provider.objects.get(pk=from_global_id(input.get('id'))[1])
        provider.name = input.get('name')
        provider.slug = input.get('slug')
        provider.asn = input.get('asn')
        provider.account = input.get('account')
        provider.portal_url = input.get('portal_url')
        provider.noc_contact = input.get('noc_contact')
        provider.admin_contact = input.get('admin_contact')
        provider.comments = input.get('comments')
        provider.custom_field_values = input.get('custom_field_values')
        provider.full_clean()
        provider.save()
        return UpdateProvider(provider=provider)

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
