import graphene
from .circuits_schema import CircuitsQuery, CircuitsMutations
from .tenancy_schema import TenancyQuery, TenancyMutations
from .dcim_schema import DcimQuery, DcimMutations
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
      CircuitsMutations
    , TenancyMutations
    , DcimMutations
    , graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
