from circuits.models import CircuitType, Circuit, Provider, CircuitTermination
from dcim.models import Site, Interface, Region
from tenancy.models import Tenant, TenantGroup
from ipam.models import Role, VLANGroup, VLAN, VRF, RIR

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
    region = initialize_region(id)
    tenant = initialize_tenant(id)

    site = Site(
        id = id,
        name = 'Site Name ' + id,
        slug = 'site-name ' + id,
        region = region,
        tenant = tenant,
        facility = 'fac',
        asn = 12,
        physical_address = 'A1',
        shipping_address = 'A2',
        contact_name = 'Name',
        contact_phone = '123',
        contact_email = 'a@gmail.com',
        comments = 'comment'
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
    tenant_group = TenantGroup(
        id = id,
        name = 'Tenant Group' + id,
        slug = 'tenant-group-' + id
    )
    tenant_group.save()
    return  tenant_group

def initialize_tenant(id):
    tenant_goup = initialize_tenant_group(id)
    tenant = Tenant(
        id = id,
        name = 'Tenant ' + id,
        slug = 'tenant-' + id,
        group = tenant_goup,
        description = 'desc',
        comments = 'comment'
    )
    tenant.save()
    return tenant

# dcim

def initialize_region(id):
    region = Region(
        id = id,
        name = 'Region' + id,
        slug = 'region-' + id
    )
    region.save()
    return region

# ipam

def initialize_vlan_role(id):
    vlan_role = Role(
        id = id,
        name = 'VlanRole' + id,
        slug = 'vlanrole-' + id,
        weight = 1000
    )
    vlan_role.save()
    return vlan_role

def initialize_vlan_group(id):
    site = initialize_site(id)
    vlan_group = VLANGroup(
        id = id,
        name = 'VlanGroup' + id,
        slug = 'vlangroup-' + id,
        site = site
    )
    vlan_group.save()
    return vlan_group

def initialize_vlan(id):
    tenant = initialize_tenant(id)
    role = initialize_vlan_role(id)

    vlan = VLAN(
        id = id,
        vid = 2,
        name = 'vlan' + id,
        status = 1,
        description = 'desc',
        tenant = tenant,
        role = role,
    )
    vlan.save()
    return vlan

def initialize_vrf(id):
    tenant = initialize_tenant(id)

    vrf = VRF(
        id = id,
        name = 'vrf' + id,
        rd = 'rd' + id,
        tenant = tenant,
        enforce_unique = True,
        description = 'description'
    )
    vrf.save()
    return vrf
