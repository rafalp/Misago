"""
ACL Exceptions thrown by Misago actions
"""

class ACLErrror(Exception):
    pass


class ACLError403(ACLErrror):
    pass


class ACLError404(ACLErrror):
    pass