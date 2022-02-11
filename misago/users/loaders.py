from ..loaders import Loader, batch_load_function
from .get import get_users_by_id
from .models import User

batch_load_users = batch_load_function(get_users_by_id)


class UsersLoader(Loader[User]):
    context_key = "_users_loader"

    def get_batch_load_function(self):
        return batch_load_users


users_loader = UsersLoader()
