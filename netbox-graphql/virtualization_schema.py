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
from virtualization.models import ClusterType, ClusterGroup, Cluster, VirtualMachine
from tenancy.models import Tenant

# Nodes
class ClusterTypeNode(DjangoObjectType):
    class Meta:
        model = ClusterType
        interfaces = (Node, )
        filter_fields = {
            'id': ['exact'],
            'name': string_types,
            'slug': ['exact'],
        }

# Queries
class VirtualizationQuery(AbstractType):
    cluster_types = DjangoFilterConnectionField(ClusterTypeNode)

# Mutations
class NewClusterType(ClientIDMutation):
    cluster_type = Field(ClusterTypeNode)
    class Input:
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterType()

        fields = [ 'name', 'slug' ]
        return NewClusterType(cluster_type=set_and_save(fields, input, temp))

class UpdateClusterType(ClientIDMutation):
    cluster_type = Field(ClusterTypeNode)
    class Input:
        id = String()
        name = String()
        slug = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterType.objects.get(pk=from_global_id(input.get('id'))[1])

        fields = [ 'name', 'slug' ]
        return UpdateClusterType(cluster_type=set_and_save(fields, input, temp))

class DeleteClusterType(ClientIDMutation):
    cluster_type = Field(ClusterTypeNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = ClusterType.objects.get(pk=from_global_id(input.get('id'))[1])
        temp.delete()
        return DeleteClusterType(cluster_type=temp)


class VirtualizationMutations(AbstractType):
    # Cluster Type
    new_cluster_type = NewClusterType.Field()
    update_cluster_type = UpdateClusterType.Field()
    delete_cluster_type = DeleteClusterType.Field()
