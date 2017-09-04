from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

def initialize_circuits():

    circuit_type = CircuitType(
        id = '111',
        name = 'Type 1',
        slug = 'type1'
    )
    circuit_type.save()

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
