from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene import AbstractType, Field, Node, ClientIDMutation, AbstractType
from graphql_relay.node.node import from_global_id
from graphene import ID, Boolean, Float, Int, List, String

from circuits.models import CircuitType, Circuit, Provider, CircuitTermination
from dcim.models import Site, Interface
from tenancy.models import Tenant
from .custom_filter_fields import date_types, string_types, number_types
from .helper_methods import not_none, set_and_save

# Nodes


class ProviderNode(DjangoObjectType):
    asn = Float()
    custom_field_values = String()

    class Meta:
        model = Provider
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
            'asn': number_types,
        }


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


class CircuitTypeNode(DjangoObjectType):
    class Meta:
        model = CircuitType
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': string_types,
        }


class CircuitTerminationNode(DjangoObjectType):
    class Meta:
        model = CircuitTermination
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'term_side': string_types,
        }

# Queries


class CircuitsQuery(AbstractType):
    providers = DjangoFilterConnectionField(ProviderNode)

    circuit_types = DjangoFilterConnectionField(CircuitTypeNode)

    circuit = Node.Field(CircuitNode)
    circuits = DjangoFilterConnectionField(CircuitNode)

    circuit_terminations = DjangoFilterConnectionField(CircuitTerminationNode)

# Mutations


class NewCircuitType(ClientIDMutation):
    circuit_type = Field(CircuitTypeNode)

    class Input:
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        fields = ['name', 'slug']
        return NewCircuitType(circuit_type=set_and_save(fields, input, CircuitType()))


class UpdateCircuitType(ClientIDMutation):
    circuit_type = Field(CircuitTypeNode)

    class Input:
        id = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = CircuitType.objects.get(pk=from_global_id(input.get('id'))[1])
        fields = ['name', 'slug']
        return UpdateCircuitType(circuit_type=set_and_save(fields, input, temp))


class DeleteCircuitType(ClientIDMutation):
    circuit_type = Field(CircuitTypeNode)

    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = CircuitType.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteCircuitType(circuit_type=temp)


class NewProvider(ClientIDMutation):
    provider = Field(ProviderNode)

    class Input:
        name = String()
        slug = String()
        asn = Float()
        account = String(default_value=None)
        portal_url = String(default_value=None)
        noc_contact = String(default_value=None)
        admin_contact = String(default_value=None)
        comments = String(default_value=None)
        custom_field_values = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        fields = ['name', 'slug', 'asn', 'account', 'portal_url', 'noc_contact',
                  'admin_contact', 'comments', 'custom_field_values']
        return NewProvider(provider=set_and_save(fields, input, Provider()))


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
        fields = ['name', 'slug', 'asn', 'account', 'portal_url', 'noc_contact',
                  'admin_contact', 'comments', 'custom_field_values']
        return UpdateProvider(provider=set_and_save(fields, input, temp))


class DeleteProvider(ClientIDMutation):
    provider = Field(ProviderNode)

    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Provider.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteProvider(provider=temp)


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
        provider = input.get('provider')
        type = input.get('type')
        tenant = input.get('tenant')

        temp = Circuit()

        if not_none(provider):
            temp.provider = Provider.objects.get(
                pk=from_global_id(provider)[1])
        if not_none(type):
            temp.type = CircuitType.objects.get(pk=from_global_id(type)[1])
        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        fields = ['cid', 'install_date', 'commit_rate',
                  'description', 'comments', 'custom_field_values']
        return NewCircuit(circuit=set_and_save(fields, input, temp))


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
        provider = input.get('provider')
        type = input.get('type')
        tenant = input.get('tenant')

        temp = Circuit.objects.get(pk=from_global_id(input.get('id'))[1])

        if not_none(provider):
            temp.provider = Provider.objects.get(
                pk=from_global_id(provider)[1])
        if not_none(type):
            temp.type = CircuitType.objects.get(pk=from_global_id(type)[1])
        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        fields = ['cid', 'install_date', 'commit_rate',
                  'description', 'comments', 'custom_field_values']
        return UpdateCircuit(circuit=set_and_save(fields, input, temp))


class DeleteCircuit(ClientIDMutation):
    circuit = Field(CircuitNode)

    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Circuit.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteCircuit(circuit=temp)


class NewCircuitTermination(ClientIDMutation):
    circuit_termination = Field(CircuitTerminationNode)

    class Input:
        circuit = String(default_value=None)
        term_side = String(default_value=None)
        site = String(default_value=None)
        interface = String(default_value=None)
        port_speed = Int(default_value=None)
        upstream_speed = Int(default_value=None)
        xconnect_id = String(default_value=None)
        pp_info = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        circuit = input.get('circuit')
        site = input.get('site')
        interface = input.get('interface')

        temp = CircuitTermination()

        if not_none(circuit):
            temp.circuit = Circuit.objects.get(pk=from_global_id(circuit)[1])
        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])
        if not_none(interface):
            temp.interface = Interface.objects.get(
                pk=from_global_id(interface)[1])

        fields = ['term_side', 'port_speed',
                  'upstream_speed', 'xconnect_id', 'pp_info']
        return NewCircuitTermination(circuit_termination=set_and_save(fields, input, temp))


class UpdateCircuitTermination(ClientIDMutation):
    circuit_termination = Field(CircuitTerminationNode)

    class Input:
        id = String(default_value=None)
        circuit = String(default_value=None)
        term_side = String(default_value=None)
        site = String(default_value=None)
        interface = String(default_value=None)
        port_speed = Int(default_value=None)
        upstream_speed = Int(default_value=None)
        xconnect_id = String(default_value=None)
        pp_info = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        circuit = input.get('circuit')
        site = input.get('site')
        interface = input.get('interface')

        temp = CircuitTermination.objects.get(
            pk=from_global_id(input.get('id'))[1])

        if not_none(circuit):
            temp.circuit = Circuit.objects.get(pk=from_global_id(circuit)[1])
        if not_none(site):
            temp.site = Site.objects.get(pk=from_global_id(site)[1])
        if not_none(interface):
            temp.interface = Interface.objects.get(
                pk=from_global_id(interface)[1])

        fields = ['term_side', 'port_speed',
                  'upstream_speed', 'xconnect_id', 'pp_info']
        return UpdateCircuitTermination(circuit_termination=set_and_save(fields, input, temp))


class DeleteCircuitTermination(ClientIDMutation):
    circuit_termination = Field(CircuitTerminationNode)

    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = CircuitTermination.objects.get(
            pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteCircuitTermination(circuit_termination=temp)


class CircuitsMutations(AbstractType):
    # Circuit
    new_circuit = NewCircuit.Field()
    update_circuit = UpdateCircuit.Field()
    delete_circuit = DeleteCircuit.Field()
    # Provider
    new_provider = NewProvider.Field()
    update_provider = UpdateProvider.Field()
    delete_provider = DeleteProvider.Field()
    # CircuitType
    new_circuit_type = NewCircuitType.Field()
    update_circuit_type = UpdateCircuitType.Field()
    delete_circuit_type = DeleteCircuitType.Field()
    # CircuitTermination
    new_circuit_termination = NewCircuitTermination.Field()
    update_circuit_termination = UpdateCircuitTermination.Field()
    delete_circuit_termination = DeleteCircuitTermination.Field()
