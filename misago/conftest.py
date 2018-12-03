from misago.acl import ACL_CACHE
from misago.conf import SETTINGS_CACHE
from misago.users.constants import BANS_CACHE

def cache_versions():
    return {
        ACL_CACHE: "abcdefgh",
        BANS_CACHE: "abcdefgh",
        SETTINGS_CACHE: "abcdefgh",
    }