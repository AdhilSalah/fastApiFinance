from fastapi import APIRouter, Depends
from library.access.permissions import PermissionChecker, Resource, Action


def Access(resource: Resource, action: Action):
    """
    Decorator to attach permission metadata to a route handler.
    Used in conjunction with AccessRouter.
    """
    def decorator(func):
        # Store metadata on the function itself
        func._permission_info = (resource, action)
        return func
    return decorator


class AccessRouter(APIRouter):
    """
    A custom APIRouter that automatically injects PermissionChecker
    dependencies if a route handler is decorated with @Access.
    """
    def add_api_route(self, path: str, endpoint, **kwargs):
        if hasattr(endpoint, "_permission_info"):
            resource, action = endpoint._permission_info
            # Create a dependency and add it to the route's dependencies list
            permission_dependency = Depends(PermissionChecker(resource, action))
            
            # Ensure 'dependencies' key exists in kwargs
            if "dependencies" not in kwargs or kwargs["dependencies"] is None:
                kwargs["dependencies"] = []
            
            kwargs["dependencies"].append(permission_dependency)
            
        return super().add_api_route(path, endpoint, **kwargs)
