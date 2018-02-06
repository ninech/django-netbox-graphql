import factory
import datetime

from . import tenant_factories, dcim_factories
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Provider

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Provider %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'p%i' % o.id)
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


class CircuitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Circuit

    id = factory.Sequence(lambda n: n)
    cid = factory.LazyAttribute(lambda o: 'cid%i' % o.id)
    provider = factory.SubFactory(ProviderFactory)
    type = factory.SubFactory(CircuitTypeFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    install_date = datetime.date(2008, 1, 1)
    commit_rate = 1024
    description = "I'm an awesome circuit!"
    comments = "This is an awesome comment :)"


class CircuitTerminationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CircuitTermination

    id = factory.Sequence(lambda n: n)
    circuit = factory.SubFactory(CircuitFactory)
    term_side = 'A'
    site = factory.SubFactory(dcim_factories.SiteFactory)
    interface = factory.SubFactory(dcim_factories.InterfaceFactory)
    port_speed = 128
    upstream_speed = 64
    xconnect_id = 1
    pp_info = "Patchy, patchy"
