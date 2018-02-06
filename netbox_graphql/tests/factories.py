import factory

from circuits.models import CircuitType, Circuit, Provider, CircuitTermination
from dcim.models import Device, Interface, Site, Region, Platform, DeviceRole
from ipam.models import IPAddress, VLANGroup, Role, VLAN, VRF, RIR, Aggregate, IPAddress, Prefix
from tenancy.models import Tenant, TenantGroup


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Provider

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Factory %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'f%i' % o.id)
    asn = 29691.0
    account = '12345'
    portal_url = 'https://nine.ch'
    noc_contact = 'noc@postmaster.com'
    admin_contact = 'admin@postmaster.com'
    comments = 'Awesome Comment!'


class CircuitTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CircuitType

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Type %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'ct%i' % o.id)
