from .change_settings import change_settings_mutation
from .login import login_mutation


admin_mutations = [
    change_settings_mutation,
    login_mutation,
]
