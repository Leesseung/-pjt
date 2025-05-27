from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    GET (읽기)는 모두 허용.
    PUT/PATCH/DELETE (수정·삭제)는 오직 본인만 허용.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
