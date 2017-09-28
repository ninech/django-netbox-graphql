from circuits.models import CircuitType, Circuit, Provider, CircuitTermination
from dcim.models import Site, Interface
from tenancy.models import Tenant, TenantGroup

# circuits
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

def initialize_site(id):
    site = Site(
        id = id,
        name = 'Site Name ' + id,
        slug = 'site-name ' + id
    )
    site.save()
    return site

def initialize_circuit_termination(id):
    circuit = initialize_circuit(id)
    site = initialize_site(id)

    circuit_termination = CircuitTermination(
        id = id,
        circuit = circuit,
        term_side = 'A',
        site = site,
        port_speed = 256,
        upstream_speed = 512,
        xconnect_id = 'xconnect_id',
        pp_info = 'pp_info'
    )
    circuit_termination.save()
    return circuit_termination

# tenancy

def initialize_tenant_group(id):
    tenancy_group = TenantGroup(
        id = id,
        name = 'Tenant Group' + id,
        slug = 'tenant-group-' + id
    )
    tenancy_group.save()
    return  tenancy_group
