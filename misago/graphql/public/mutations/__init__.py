from .avatarupload import avatar_upload_mutation
from .closethread import close_thread_mutation
from .closethreads import close_threads_mutation
from .deletethread import delete_thread_mutation
from .deletethreadpost import delete_thread_post_mutation
from .deletethreadposts import delete_thread_posts_mutation
from .deletethreads import delete_threads_mutation
from .editpost import edit_post_mutation
from .editthreadtitle import edit_thread_title_mutation
from .login import login_mutation
from .movethread import move_thread_mutation
from .movethreads import move_threads_mutation
from .postreply import post_reply_mutation
from .postthread import post_thread_mutation
from .register import register_mutation
from .setupsite import setup_site_mutation

mutations = [
    avatar_upload_mutation,
    close_thread_mutation,
    close_threads_mutation,
    delete_thread_mutation,
    delete_thread_posts_mutation,
    delete_thread_post_mutation,
    delete_threads_mutation,
    edit_post_mutation,
    edit_thread_title_mutation,
    login_mutation,
    move_thread_mutation,
    move_threads_mutation,
    post_reply_mutation,
    post_thread_mutation,
    register_mutation,
    setup_site_mutation,
]
