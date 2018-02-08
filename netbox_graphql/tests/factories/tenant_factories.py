import factory
from tenancy.models import Tenant, TenantGroup


class TenantGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TenantGroup

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Tenant Group %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 'tg%i' % o.id)


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: 'Tenant %i' % o.id)
    slug = factory.LazyAttribute(lambda o: 't%i' % o.id)
    group = factory.SubFactory(TenantGroupFactory)
    description = "Tenant description!!"
    comments = "Tenant comment!!"
