from .changesettings import change_settings_mutation
from .createcategory import create_category_mutation
from .deletecategory import delete_category_mutation
from .editcategory import edit_category_mutation
from .login import login_mutation
from .movecategory import move_category_mutation
from .usercreate import user_create_mutation
from .userdelete import user_delete_mutation
from .userupdate import user_update_mutation

mutations = [
    change_settings_mutation,
    create_category_mutation,
    delete_category_mutation,
    edit_category_mutation,
    login_mutation,
    move_category_mutation,
    user_create_mutation,
    user_delete_mutation,
    user_update_mutation,
]
