import factory

from . import dcim_factories, tenant_factories, ipam_factories
from virtualization.models import ClusterType, ClusterGroup, Cluster, VirtualMachine


class ClusterTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClusterType

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'ClusterType %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'ct%i' % o.id)


class ClusterGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClusterGroup

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'ClusterGroup %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'cg%i' % o.id)


class ClusterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cluster

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Cluster %i' % o.id)
    type = factory.SubFactory(ClusterTypeFactory)
    group = factory.SubFactory(ClusterGroupFactory)
    site = factory.SubFactory(dcim_factories.SiteFactory)
    comments = "This is a cluster comment!"


class VirtualMachineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VirtualMachine

    id = factory.Sequence(lambda n: n)
    cluster = factory.SubFactory(ClusterFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
    platform = factory.SubFactory(dcim_factories.PlatformFactory)
    name = factory.LazyAttribute(lambda o: 'VM %i' % o.id)
    # status =
    role = factory.SubFactory(dcim_factories.DeviceRoleFactory, vm_role=True)
    primary_ip4 = factory.SubFactory(ipam_factories.IPAddressFactory)
    primary_ip6 = factory.SubFactory(ipam_factories.IPAddressFactory)
    vcpus = 4
    memory = 4096
    disk = 40
    comments = "I'm a VM comment!"
