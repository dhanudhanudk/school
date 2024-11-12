from django.shortcuts import render
from rest_framework.views import APIView,status
from django.http import JsonResponse,Http404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from userapp.validators import Validators
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions
from userapp.paginations import PageLimitPagination
import json,jwt
from.models import*
from userapp.serializers import *
from adminapp.serializers import SessionCreatedSerializers
from userapp.permissions import Isuser
# from django.db.models import Q
# from jwt import decode as decode_jwt, InvalidTokenError
# from rest_framework_simplejwt.exceptions import AuthenticationFailed

# user created views
class UserCreateViews(APIView):    
    permission_classes=[IsAdminUser,IsAuthenticated]
    
    def post(self,request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            validation =Validators.users_valid(data)
            if validation['status']==False:
                return JsonResponse(validation,status=status.HTTP_404_NOT_FOUND)
            if validation['status']==True:
                role=data.get('role')
                role_instance= Rolemaster.objects.get(id=role)
                role_id= role_instance.role_name
                if role_id != 'user':
                    return JsonResponse({"result":{"message":"user only allowed registration"},"status":False,"response":404})
                user=AdminModel.objects.create(
                        name=data.get('name'),
                        email=data.get('email'),
                        phonenumber=data.get('phonenumber'),
                        city=data.get('city'),
                        country=data.get('country'),
                        role=role_instance
                 )   
                password=data.get('password')
                user.set_password(password)
                if role_id=="user":
                    user.is_user=True
                if role_id=="admin":
                    user.is_admin=False
                    user.is_staff=False
                    return JsonResponse({"result":{"message": "role id 1 is admin only allowed user role","status":False,
                                                   "responsecode":404}})
                user.save()
                return JsonResponse({"result":{"data": {},"message": "user successfully created ","status":True,
                                               "responsecode":200}})  
            else:
                return JsonResponse({"result":{"message": "could not create user","status":False,"responsecode":404}})
        except Exception as e:
            return JsonResponse({"result":{
                "message":f"An unexpected missing and error:{str(e)}","status":False,"response":500}})
        
# user login views

class UsersLogin(APIView):

    permission_classes=[IsAdminUser]
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            validation = Validators.admin_login_valid(data)
            if validation["status"] == False:
                return JsonResponse(validation, status=status.HTTP_400_BAD_REQUEST)

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"result":{"message":"Email and password are required","status":False,"response":400}})

            try:
                user = AdminModel.objects.get(email=email)
            except AdminModel.DoesNotExist:
                return JsonResponse({"result":{"message":"user not found","status":False,"response":404}})



            password_check = check_password(password, user.password)
            if password_check:
                access_token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                access_token["is_user"] = user.is_user
                access_token['email'] = user.email
                access_token['name'] = user.name
                refresh_token['email'] = user.email
                refresh_token['name'] = user.name

                return JsonResponse({
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                    "result":{
                        "data": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                    },"message": "Login successfully","status":True,"responsecode":200}
                   
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"result":{
                        "data": {},"message": "could not login user","status":False,"responsecode":404}})
        except Exception as e:
            return JsonResponse({"result":{
                "message":f"An unexpected missing and error:{str(e)}","status":False,"response":500}})

class SessionBookingViews(APIView):
    permission_classes=[IsAuthenticated,Isuser]

    def post(self, request):

        try:
            token = request.headers['Authorization']
            if not token:
                return JsonResponse({"error": "Authorization token missing."}), 401
            # try:
            #     payload = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer', '').strip()
            #     decoded_token = AccessToken(payload)
            #     user = decoded_token.payload.get('is_user')
            #     if not user:
            #         return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            # except jwt.InvalidTokenError:
            #     raise AuthenticationFailed("Invalid token provided.")
            try:
                data = json.loads(request.body.decode('utf-8'))
                validation = Validators.session_booking(data)
                if not validation['status']:
                    return JsonResponse(validation, status=status.HTTP_400_BAD_REQUEST)

                user_id = data.get('user')
                sessions_id = data.get('sessions')

                if not user_id or not sessions_id:
                    return JsonResponse({"result":{"message":"User ID and session ID are required","status":False,"response":400}})
                try:
                    user_instance = AdminModel.objects.get(id=user_id)
                except AdminModel.DoesNotExist:
                    return JsonResponse({"result":{"message":"user not found","status":False,"response":404}})

                try:
                    session_instance = TutoringSession.objects.get(id=sessions_id)
                except TutoringSession.DoesNotExist:
                    return JsonResponse({"result":{"message":"session not found","status":False,"response":404}})
                # Create the session booking
                SessionBooking.objects.create(user=user_instance, sessions=session_instance)
                return JsonResponse({"result":{
                        "data": {},"message": "session successfully booking","status":True,"responsecode":200}})
            except Exception as e:
                return JsonResponse({"result":{
                "message":f"An unexpected missing and error:{str(e)}","status":False,"response":500}})
        except Exception as e:
            return JsonResponse({"result":{
            "message":f"An unexpected missing and error:{str(e)}","status":False,"response":500}})
        
class UnbookedSessionsListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated,Isuser]
    serializer_class = SessionCreatedSerializers
    pagination_class=PageLimitPagination
   

    def get_queryset(self):
        try:
            booked_session_ids = SessionBooking.objects.values_list('sessions', flat=True).distinct()
            return TutoringSession.objects.exclude(id__in=booked_session_ids)
        except Exception as e:
                return JsonResponse({"status": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)