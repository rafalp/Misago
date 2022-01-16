from .avatarupload import avatar_upload_mutation
from .closethread import close_thread_mutation
from .closethreads import close_threads_mutation
from .deletethread import delete_thread_mutation
from .deletethreadpost import delete_thread_post_mutation
from .deletethreadposts import delete_thread_posts_mutation
from .deletethreads import delete_threads_mutation
from .editthreadtitle import edit_thread_title_mutation
from .login import login_mutation
from .movethread import move_thread_mutation
from .movethreads import move_threads_mutation
from .postcreate import post_create_mutation
from .postupdate import post_update_mutation
from .register import register_mutation
from .sitesetup import site_setup_mutation
from .threadcreate import thread_create_mutation

mutations = [
    avatar_upload_mutation,
    close_thread_mutation,
    close_threads_mutation,
    delete_thread_mutation,
    delete_thread_posts_mutation,
    delete_thread_post_mutation,
    delete_threads_mutation,
    edit_thread_title_mutation,
    login_mutation,
    move_thread_mutation,
    move_threads_mutation,
    post_create_mutation,
    post_update_mutation,
    register_mutation,
    site_setup_mutation,
    thread_create_mutation,
]
