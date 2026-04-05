from fastapi import Depends, HTTPException, status
from library.auth.dependencies import get_current_user
from library.access.permissions import Resource, Action, is_allowed
from library.db.users.models import User


def CheckAccess(resource: Resource, action: Action):
    """
    Dependency factory for route-level permission checks.

    Usage:
        @router.get("/", dependencies=[Depends(CheckAccess(Resource.Finance, Action.Read))])

    Or inline:
        async def my_route(current_user: User = Depends(CheckAccess(Resource.Finance, Action.Read))):
    """
    def _check(current_user: User = Depends(get_current_user)) -> User:
        if not is_allowed(current_user.role, resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' does not have {action} access to {resource}.",
            )
        return current_user
    # Give the inner function a unique name so FastAPI doesn't deduplicate it
    _check.__name__ = f"check_{resource}_{action}"
    return _check
