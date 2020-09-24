from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
	message="only users allowed"
	def has_object_permission(self,request,view,obj):
		if request.user == obj.user:
			return True
		else:
			return False

class IsAdmin(BasePermission):
	message="Only admins allowed"
	def has_object_permission(self,request,view,obj):
		if request.user == obj.event_organizer:
			return True
		else:
			return False
