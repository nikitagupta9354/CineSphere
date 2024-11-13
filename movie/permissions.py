from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsAdminModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
                return True
        if request.user.is_authenticated:
            if request.method!='DELETE':
                return request.user.role in ['Admin','Moderator']
            return request.user.role=='Admin'
        return False
    
class IsReviewOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            if request.method!='PUT':
                return obj.user==request.user or request.user.role in ['Admin','Moderator']
            return obj.user==request.user
        return False