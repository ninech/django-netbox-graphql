import factory
import datetime

import netaddr

from . import tenant_factories, dcim_factories
from ipam.models import VRF, RIR, Aggregate, Role, IPAddress, VLANGroup, VLAN, Prefix
from ipam.fields import IPAddressField


class VRFFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VRF

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'VRF %i' % o.id)
    rd = factory.LazyAttribute(lambda o: 'rd%i' % o.id)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    enforce_unique = True
    description = "This is a VRF!"


class RIRFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RIR

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'RIR %i' % o.id)
    rd = factory.LazyAttribute(lambda o: 'rir%i' % o.id)
    is_private = False


class AggreagateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aggregate

    # family =
    # prefix =
    rir = factory.SubFactory(RIRFactory)
    date_added = datetime.date(2008, 1, 1)
    description = "I'm an Aggregate!"


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Role %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'r%i' % o.id)
    weight = 1000


class IPAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IPAddress

    family = 4
    address = netaddr.IPAddress('127.0.0.1')
    vrf = factory.SubFactory(VRFFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    # status =
    role = 1
    # interface =
    # nat_inside =
    description = "I'm an IPAddress!"


class VLANGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VLANGroup

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'VLANGroup %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'vg%i' % o.id)
    site = factory.SubFactory(dcim_factories.SiteFactory)


class VLANFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VLAN

    id = factory.Sequence(lambda n: n)
    site = factory.SubFactory(dcim_factories.SiteFactory)
    group = factory.SubFactory(VLANGroupFactory)
    vid = 1
    name = factory.LazyAttribute(lambda o: 'VLAN %i' % o.id)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    # status =
    role = factory.SubFactory(RoleFactory)
    description = "I'm a VLAN!"


class PrefixFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Prefix

    # family =
    # prefix =
    site = factory.SubFactory(dcim_factories.SiteFactory)
    vrf = factory.SubFactory(VRFFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    # vlan =
    # status =
    role = factory.SubFactory(RoleFactory)
    is_pool = False
    description = "I'm a Prefix!"
