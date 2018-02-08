import graphene
from .circuits_schema import CircuitsQuery, CircuitsMutations
from .tenancy_schema import TenancyQuery, TenancyMutations
from .dcim_schema import DcimQuery, DcimMutations
from .ipam_schema import IpamQuery, IpamMutations
from .virtualization_schema import VirtualizationQuery, VirtualizationMutations

# Root
class RootQuery(
      CircuitsQuery
    , TenancyQuery
    , DcimQuery
    , IpamQuery
    , VirtualizationQuery
    , graphene.ObjectType):
    pass

class RootMutation(
      CircuitsMutations
    , TenancyMutations
    , DcimMutations
    , IpamMutations
    , VirtualizationMutations
    , graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
