from .categorycreate import category_create_mutation
from .categorydelete import category_delete_mutation
from .categorymove import category_move_mutation
from .editcategory import category_update_mutation
from .login import login_mutation
from .settingsupdate import settings_update_mutation
from .usercreate import user_create_mutation
from .userdelete import user_delete_mutation
from .userupdate import user_update_mutation

mutations = [
    category_create_mutation,
    category_delete_mutation,
    category_move_mutation,
    category_update_mutation,
    login_mutation,
    settings_update_mutation,
    user_create_mutation,
    user_delete_mutation,
    user_update_mutation,
]
