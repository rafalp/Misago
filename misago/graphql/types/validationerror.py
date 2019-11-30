from ariadne import ObjectType


validation_error_type = ObjectType("ValidationError")

validation_error_type.set_alias("location", "loc")
validation_error_type.set_alias("message", "msg")
