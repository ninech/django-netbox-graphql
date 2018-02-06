import factory
from . import tenant_factories
from dcim.models import Region, Site, Interface


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
    # virtual_machine =
    # lag =
    name = factory.LazyAttribute(lambda o: 'Interface %i' % o.id)
    # mac_address =
    # mtu =
    # mtu =
    description = "I'm an awesome interface!"
