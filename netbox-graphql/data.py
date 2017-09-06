from circuits.models import CircuitType, Circuit, Provider, CircuitTermination
from dcim.models import Site, Interface

def initialize_circuit_type():

    circuit_type = CircuitType(
        id = '111',
        name = 'Type 1',
        slug = 'type1'
    )
    circuit_type.save()
    return  circuit_type

def initialize_provider():
    provider = Provider(
        id = '111',
        name = 'Provider 1',
        slug = 'provider1',
        asn = '256',
        account = '12345',
        portal_url = 'https://www.nine.ch',
        noc_contact = 'noc_contact',
        admin_contact = 'admin_contact',
        comments = 'comments',
        created = '2015-01-15'
    )
    provider.save()
    return provider

def initialize_circuit(id):
    circuit_type = CircuitType(
        id = id,
        name = 'Type' + id,
        slug = 'type' + id
    )
    circuit_type.save()

    provider = Provider(
        id = id,
        name = 'Provider'+id,
        slug = 'provider'+id,
        asn = '256',
        account = '12345',
        portal_url = 'https://www.nine.ch',
        noc_contact = 'noc_contact',
        admin_contact = 'admin_contact',
        comments = 'comments',
        created = '2015-01-15'
    )
    provider.save()

    circuit = Circuit(
        id = id,
        cid = 'cid',
        provider = provider,
        type = circuit_type,
        install_date = '2017-10-12',
        commit_rate = 12,
        description = 'desc',
        comments = 'comments'
    )
    circuit.save()
    return circuit
