import graphene
from graphene import AbstractType, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field

from dcim.models import Device, Interface, Site
from dcim.fields import ASNField, MACAddressField

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

# Queries
class DcimQuery(AbstractType):
    devices = DjangoFilterConnectionField(DeviceNode)
    interfaces = DjangoFilterConnectionField(InterfaceNode)
    sites = DjangoFilterConnectionField(SiteNode)
