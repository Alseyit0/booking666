from rest_framework import permissions


class CheckUSerCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'simpleUser':
            return False
        return True

class CheckReviewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'simpleUser':
            return True
        return False


class CheckHotelOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class CheckRoomsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.hotel_room.owner == request.user


class CheckReviewEDIT(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user_name



class CheckOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user