from ariadne import ObjectType

from ....threads.models import Thread

thread_edge_type = ObjectType("ThreadEdge")
thread_edge_type.set_alias("cursor", "last_post_id")


@thread_edge_type.field("node")
def resolve_edge_node(obj: Thread, *_):
    return obj
