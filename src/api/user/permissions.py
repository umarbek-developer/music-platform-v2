from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS



class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        action = None 
        if request.method == "GET":
            action = "view"
        elif request.method == "POST":
            action == "add"
        elif request.method == "PUT" or request.method == "PATCH":
            action == "change"
        elif request.method == "DELETE":
            action = "delete"
        user = request.user  
        return request.user.has_perm((f"{view.app_label}.{view}_{view.app_model}"))
