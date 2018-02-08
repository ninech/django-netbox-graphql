from graphql_relay.node.node import from_global_id, to_global_id


def obj_to_global_id(obj):
    return to_global_id(type(obj).__name__, obj.id)
