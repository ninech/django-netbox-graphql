import graphene
from .circuits_schema import CircuitsQuery, CircuitTypeMutation, ProviderMutation, CircuitMutation, CircuitTerminationMutation
from .tenancy_schema import TenancyQuery, TenantGroupMutation
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
    #circuits
      CircuitTypeMutation
    , ProviderMutation
    , CircuitMutation
    , CircuitTerminationMutation
    # tenancy
    , TenantGroupMutation
    , graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
