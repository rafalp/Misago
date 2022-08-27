from ..database.models import mapper_registry
from ..tables import categories_permissions, moderators, user_groups_permissions

categories_permissions_query = mapper_registry.query_table(categories_permissions)
permissions_query = mapper_registry.query_table(user_groups_permissions)
moderators_query = mapper_registry.query_table(moderators)
