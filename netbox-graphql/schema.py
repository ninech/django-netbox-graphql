import graphene
from .circuits_schema import CircuitsQuery, CircuitTypeMutation, ProviderMutation, CircuitMutation
from .tenancy_schema import TenancyQuery
from .dcim_schema import DcimQuery
from .ipam_schema import IpamQuery

# Root
class RootQuery(
      CircuitsQuery
    , TenancyQuery
    , DcimQuery
    , IpamQuery
    , graphene.ObjectType):
    pass


class RootMutation(
      CircuitTypeMutation
    , ProviderMutation
    , CircuitMutation
    , graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
