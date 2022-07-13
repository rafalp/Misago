from ..loaders import Loader, batch_load_function
from .get import get_users_by_id, get_users_groups_by_id
from .models import User, UserGroup

batch_load_users = batch_load_function(get_users_by_id)
batch_load_users_groups = batch_load_function(get_users_groups_by_id)


class UsersLoader(Loader[User]):
    context_key = "_users_loader"

    def get_batch_load_function(self):
        return batch_load_users


users_loader = UsersLoader()


class UsersGroupsLoader(Loader[UserGroup]):
    context_key = "_users_groups_loader"

    def get_batch_load_function(self):
        return batch_load_users_groups


users_groups_loader = UsersGroupsLoader()
