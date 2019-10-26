from ariadne import ObjectType


mutation_error_type = ObjectType("MutationError")

mutation_error_type.set_alias("location", "loc")
mutation_error_type.set_alias("message", "msg")
