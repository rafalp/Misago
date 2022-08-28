from typing import List


def add_permission(permissions: List[str], permission: str):
    if permission not in permissions:
        permissions.append(permission)
