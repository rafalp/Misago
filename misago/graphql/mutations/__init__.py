from .editpost import edit_post_mutation
from .login import login_mutation
from .postreply import post_reply_mutation
from .postthread import post_thread_mutation
from .register import register_mutation


mutations = [
    edit_post_mutation,
    login_mutation,
    post_reply_mutation,
    post_thread_mutation,
    register_mutation,
]
