import graphene
from graphene import AbstractType, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene import AbstractType, Field, Node, ClientIDMutation, AbstractType
from graphene import ID, Boolean, Float, Int, List, String
from graphql_relay.node.node import from_global_id

from .custom_filter_fields import date_types, string_types, number_types
from .helper_methods import not_none, set_and_save
from dcim.models import Device, Interface, Site, Region, Platform, DeviceRole
from dcim.fields import ASNField, MACAddressField
from tenancy.models import Tenant

# Convert special field
@convert_django_field.register(MACAddressField)
def MACAddressFieldConvert(field, registry=None):
    return graphene.String()

@convert_django_field.register(ASNField)
def ASNFieldConvert(field, registry=None):
    return graphene.Float()

# Nodes
class DeviceNode(DjangoObjectType):
    class Meta:
        model = Device
        interfaces = (Node, )

class InterfaceNode(DjangoObjectType):
    class Meta:
        model = Interface
        interfaces = (Node, )

class SiteNode(DjangoObjectType):
    class Meta:
        model = Site
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class DeviceRoleNode(DjangoObjectType):
    class Meta:
        model = DeviceRole
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

class PlatformNode(DjangoObjectType):
    class Meta:
        model = Platform
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }
# Queries
class DcimQuery(AbstractType):
    devices = DjangoFilterConnectionField(DeviceNode)
    interfaces = DjangoFilterConnectionField(InterfaceNode)
    sites = DjangoFilterConnectionField(SiteNode)
    regions = DjangoFilterConnectionField(RegionNode)

# Mutations
class NewRegion(ClientIDMutation):
    region = Field(RegionNode)
    class Input:
        parent = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        parent = input.get('parent')

        temp = Region()

        if not_none(parent):
            temp.parent = Region.objects.get(pk=from_global_id(parent)[1])

        fields = [ 'name', 'slug' ]
        return NewRegion(region=set_and_save(fields, input, temp))

class UpdateRegion(ClientIDMutation):
    region = Field(RegionNode)
    class Input:
        id = String()
        parent = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Region.objects.get(pk=from_global_id(input.get('id'))[1])

        parent = input.get('parent')

        if not_none(parent):
            temp.parent = Region.objects.get(pk=from_global_id(parent)[1])

        fields = [ 'name', 'slug' ]
        return UpdateRegion(region=set_and_save(fields, input, temp))

class DeleteRegion(ClientIDMutation):
    region = Field(RegionNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Region.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteRegion(region=temp)

# Site
class NewSite(ClientIDMutation):
    site = Field(SiteNode)
    class Input:
        name = String()
        slug = String()
        region = String(default_value=None)
        tenant = String(default_value=None)
        facility = String(default_value=None)
        asn = Float(default_value=None)
        physical_address = String(default_value=None)
        shipping_address = String(default_value=None)
        contact_name = String(default_value=None)
        contact_phone = String(default_value=None)
        contact_email = String(default_value=None)
        comments = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        region = input.get('region')
        tenant = input.get('tenant')

        temp = Site()

        if not_none(region):
            temp.region = Region.objects.get(pk=from_global_id(region)[1])

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        fields = [ 'name', 'slug', 'facility', 'asn', 'physical_address', 'shipping_address', 'contact_name', 'contact_phone', 'contact_email', 'comments' ]
        return NewSite(site=set_and_save(fields, input, temp))

class UpdateSite(ClientIDMutation):
    site = Field(SiteNode)
    class Input:
        id = String()
        name = String()
        slug = String()
        region = String(default_value=None)
        tenant = String(default_value=None)
        facility = String(default_value=None)
        asn = Float(default_value=None)
        physical_address = String(default_value=None)
        shipping_address = String(default_value=None)
        contact_name = String(default_value=None)
        contact_phone = String(default_value=None)
        contact_email = String(default_value=None)
        comments = String(default_value=None)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Site.objects.get(pk=from_global_id(input.get('id'))[1])

        region = input.get('region')
        tenant = input.get('tenant')

        if not_none(region):
            temp.region = Region.objects.get(pk=from_global_id(region)[1])

        if not_none(tenant):
            temp.tenant = Tenant.objects.get(pk=from_global_id(tenant)[1])

        fields = [ 'name', 'slug', 'facility', 'asn', 'physical_address', 'shipping_address', 'contact_name', 'contact_phone', 'contact_email', 'comments' ]

        return UpdateSite(site=set_and_save(fields, input, temp))

class DeleteSite(ClientIDMutation):
    site = Field(SiteNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Site.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteSite(site=temp)

class DcimMutations(AbstractType):
    # Region
    new_region = NewRegion.Field()
    update_region = UpdateRegion.Field()
    delete_region = DeleteRegion.Field()
    # Site
    new_site = NewSite.Field()
    update_site = UpdateSite.Field()
    delete_site = DeleteSite.Field()
