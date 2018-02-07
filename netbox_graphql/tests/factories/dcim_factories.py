import factory
from . import tenant_factories, virtualization_factories
from dcim.models import Region, Site, Interface, DeviceRole, Platform


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Region %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'r%i' % o.id)


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Site %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 's%i' % o.id)
    region = factory.SubFactory(RegionFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    facility = "DC"
    asn = 10.0
    physical_address = "Planet Nano"
    shipping_address = "Skywalker Corp."
    contact_name = "Luke Skywalker"
    contact_phone = "+00"
    contact_email = "luke@skywalkerink.com"
    comments = "Awesome Comment!"


class InterfaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Interface

    id = factory.Sequence(lambda n: n)
    # device =
    # virtual_machine = # http://factoryboy.readthedocs.io/en/latest/reference.html#circular-imports
    # lag =
    name = factory.LazyAttribute(lambda o: 'Interface %i' % o.id)
    # mac_address =
    # mtu =
    # mtu =
    description = "I'm an awesome interface!"


class DeviceRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeviceRole

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'DeviceRole %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'dr%i' % o.id)
    vm_role = False


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Platform

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Platform %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'p%i' % o.id)
    napalm_driver = 'ABCX13'
    # rpc_client =
