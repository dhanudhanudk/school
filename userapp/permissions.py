from django.http import HttpResponse,JsonResponse,Http404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class Isuser(BasePermission):
    def token_permission(self,request,view):
        if request.user.is_authenticated and getattr(request.user,"is_user",False):
            return True
        return JsonResponse("User only Access","not_allowed",False)