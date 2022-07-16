from ..database import ObjectMapper
from ..tables import categories_permissions, user_groups_permissions

categories_permissions_query = ObjectMapper(categories_permissions)
permissions_query = ObjectMapper(user_groups_permissions)
