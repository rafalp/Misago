from .avatarupload import avatar_upload_mutation
from .login import login_mutation
from .postcreate import post_create_mutation
from .postdelete import post_delete_mutation
from .postsbulkdelete import posts_bulk_delete_mutation
from .postupdate import post_update_mutation
from .sitesetup import site_setup_mutation
from .threadclose import thread_close_mutation
from .threadcreate import thread_create_mutation
from .threaddelete import thread_delete_mutation
from .threadmove import thread_move_mutation
from .threadopen import thread_open_mutation
from .threadsbulkdelete import threads_bulk_delete_mutation
from .threadsbulkmove import threads_bulk_move_mutation
from .threadsisclosedbulkupdate import threads_is_closed_bulk_update_mutation
from .threadrename import thread_rename_mutation
from .usercreate import user_create_mutation

mutations = [
    avatar_upload_mutation,
    login_mutation,
    post_create_mutation,
    post_delete_mutation,
    post_update_mutation,
    posts_bulk_delete_mutation,
    site_setup_mutation,
    thread_close_mutation,
    thread_create_mutation,
    thread_delete_mutation,
    thread_move_mutation,
    thread_open_mutation,
    thread_rename_mutation,
    threads_bulk_delete_mutation,
    threads_bulk_move_mutation,
    threads_is_closed_bulk_update_mutation,
    user_create_mutation,
]
