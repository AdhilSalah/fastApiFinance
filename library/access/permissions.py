from enum import Enum
from fastapi import Depends, HTTPException, status
from library.access.roles import Role
from library.auth.dependencies import get_current_user
from library.db.users.models import User


class Resource(str, Enum):
    Dashboard = "Dashboard"
    Finance = "Finance"
    User = "User"
    Insights = "Insights"


class Action(str, Enum):
    Read = "Read"
    Create = "Create"
    Update = "Update"
    Delete = "Delete"


# Permission matrix: role → set of (Resource, Action) tuples allowed
PERMISSIONS: dict[Role, set[tuple[Resource, Action]]] = {
    Role.viewer: {
        (Resource.Dashboard, Action.Read),
    },
    Role.analyst: {
        (Resource.Dashboard, Action.Read),
        (Resource.Finance, Action.Read),
        (Resource.Insights, Action.Read),
        (Resource.User,Action.Read)
    },
    Role.admin: {
        # Dashboard
        (Resource.Dashboard, Action.Read),
        # Finance — full CRUD
        (Resource.Finance, Action.Read),
        (Resource.Finance, Action.Create),
        (Resource.Finance, Action.Update),
        (Resource.Finance, Action.Delete),
        # Users — full CRUD
        (Resource.User, Action.Read),
        (Resource.User, Action.Create),
        (Resource.User, Action.Update),
        (Resource.User, Action.Delete),
        # Insights
        (Resource.Insights, Action.Read),
    },
}


def is_allowed(role: Role, resource: Resource, action: Action) -> bool:
    return (resource, action) in PERMISSIONS.get(role, set())


class PermissionChecker:
    def __init__(self, resource: Resource, action: Action):
        self.resource = resource
        self.action = action

    def __call__(self, user: User = Depends(get_current_user)):
        if not is_allowed(user.role, self.resource, self.action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user
