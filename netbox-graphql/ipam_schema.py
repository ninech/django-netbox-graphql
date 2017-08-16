import graphene
from graphene import AbstractType, Node
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from ipam.models import IPAddress
from ipam.fields import IPNetworkField, IPAddressField

@convert_django_field.register(IPNetworkField)
def iPNetworkFieldConvert(field, registry=None):
    return graphene.String()

@convert_django_field.register(IPAddressField)
def iPAddressFieldConvert(field, registry=None):
    return graphene.String()

# Nodes
class IPAddressNode(DjangoObjectType):
    class Meta:
        model = IPAddress
        interfaces = (Node, )

# Queries
class IpamQuery(AbstractType):
    ip_address = DjangoFilterConnectionField(IPAddressNode)
