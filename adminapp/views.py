from django.shortcuts import render
from rest_framework.views import APIView, status
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from adminapp.validators import Validators
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics
from django.contrib.auth import authenticate
from adminapp.paginations import PageLimitPagination
from django.db.models import Q
from .models import *
from userapp.models import SessionBooking
from userapp.serializers import SessionBookingSerializers
from .serializers import *
import pandas as pd
import os,csv, json
from pathlib import Path
# from rest_framework.generics import ListAPIView, get_object_or_404
# from django.core.files.storage import default_storage


class RoleMasterViews(APIView):  # Role master created api. 
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            validation = Validators.role_valid(data)
            if validation['status'] == False:
                return JsonResponse(validation, status=status.HTTP_404_NOT_FOUND)
            if validation['status'] == True:
                Rolemaster.objects.create(**data)
                return JsonResponse({"result": {"data": {}, "message": "Role successfully created ", "status": True,
                                                "responsecode": 200}})
            else:
                return JsonResponse({"result": {"message": "could not create role ", "status": False,
                                                "responsecode": 404}})
        except Exception as e:
            return JsonResponse({"result": {
                "message": f"An unexpected missing and error:{str(e)}", "status": False, "response": 500}})


class AdminCreateViews(APIView):  # admin created api.
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            validation = Validators.users_valid(data)
            if validation['status'] == False:
                return JsonResponse(validation, status=status.HTTP_404_NOT_FOUND)
            if validation['status'] == True:
                role=data.get('role')
                role_instance= Rolemaster.objects.get(id=role)
                role_id= role_instance.role_name
                if role_id != 'admin':
                    return JsonResponse({"result":{"message":"admin only allowed registration"},"status":False,
                                         "response":404})
                user = AdminModel.objects.create(
                    name=data.get('name'),
                    email=data.get('email'),
                    phonenumber=data.get('phonenumber'),
                    city=data.get('city'),
                    country=data.get('country'),
                    role=role_instance
                )

                password = data.get('password')
                user.set_password(password)
                if role_id == "user":
                    user.is_user = False
                if role_id == "admin":
                    user.is_admin = True
                    user.is_staff = True

                user.save()
                return JsonResponse({"result": {"data": {}, "message": "admin successfully created ",
                                                 "status": True, "responsecode": 200}})
            else:
                return JsonResponse({"result": {"message": "admin not upload data", "status": False,
                                                "responsecode": 404}})
        except Exception as e:
            return JsonResponse({"result": {
                "message": f"An unexpected missing and error:{str(e)}", "status": False, "response": 500}})


class AdminLogin(APIView): # admin login api
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            validation = Validators.admin_login_valid(data)
            if validation["status"] == False:
                return JsonResponse(validation, status=status.HTTP_400_BAD_REQUEST)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"result": {"message": "email and password not required", "status": False,
                                                "responsecode": 404}})
            user = authenticate(email=email, password=password)
            if user is None:
                return JsonResponse({"result": {"message": "Invalid email or password", "status": False,
                                                "responsecode": 404}})
            if user:
                access_token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                access_token['is_staff'] = user.is_staff
                access_token['email'] = user.email
                access_token['email'] = user.name
                refresh_token['email'] = user.email
                refresh_token['name'] = user.name

                return JsonResponse({"result": {"access_token": str(access_token), "refresh_token": str(refresh_token),
                                    "data": {
                                        "id": user.id,
                                        "email": user.email,
                                        "name": user.name, },
                                     "message": "admin login successfully","status": True, "responsecode": 200}})
            else:
                return JsonResponse({"result": {"message": "could not admin login", "status": False,"responsecode": 404}})
        except Exception as e:
            return JsonResponse({"result": {"message": f"An unexpected missing and error:{str(e)}", 
                                            "status": False, "response": 500}})


class SessionCreateViews(APIView):  # tutoring session create.
    permission_classes=[IsAdminUser]
    def post(self,request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            validation =Validators.session_valid(data)
            if validation['status']==False:
                return JsonResponse(validation,status=status.HTTP_404_NOT_FOUND)
            if validation['status']==True:
                TutoringSession.objects.create(**data)
                return JsonResponse({"result":{ "data": {},"message": "session successfully created ","status":True,
                                               "responsecode":200}})  
            else:
              return JsonResponse({"result":{"message": "session not upload data","status":False,"responsecode":404}}) 
        except Exception as e:
           return JsonResponse({"result":{"message":f"An unexpected missing and error:{str(e)}","status":False,"response":500}})

class userList(generics.ListAPIView):  # user list of api.
    serializer_class = UserListSerializers
    permission_classes=[IsAdminUser,IsAuthenticated]
    pagination_class = PageLimitPagination

    def get_queryset(self):

        queryset = AdminModel.objects.filter(is_user=True)
        try:
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(Q(name__icontains=search))
                return queryset
            else:
                return AdminModel.objects.filter(is_user=True)
        except Exception as e:
            return JsonResponse({"result": {
                "message": f"An unexpected missing and error:{str(e)}", "status": False, "response": 500}})


class SessionList(generics.ListAPIView): #session list of api.
    serializer_class = SessionCreatedSerializers
    permission_classes = [IsAdminUser, IsAuthenticated]
    pagination_class = PageLimitPagination

    def get_queryset(self):
        queryset = TutoringSession.objects.all()
        try:
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(Q(subject__icontains=search) | Q(session_day__icontains=search))
                return queryset
            else:
                return TutoringSession.objects.all()
        except Exception as e:
            return JsonResponse({"result": {
                "message": f"An unexpected missing and error:{str(e)}", "status": False, "response": 500}})

class BookingList(generics.ListAPIView): #session booking list of api.
    serializer_class=SessionBookingSerializers
    permission_classes=[IsAuthenticated,IsAdminUser]
    def get_queryset(self):
        queryset=SessionBooking.objects.all()
        try:
            search=self.request.query_params.get('search',None)
            if search:
                # session_id = TutoringSession.objects.get(subject=subject)
                queryset = queryset.filter(Q(sessions__subject__icontains=search)|Q(user__name__icontains=search)
                                           |Q(sessions__session_day__icontains=search))
                return queryset
            else:
                return SessionBooking.objects.all()
        except Exception as e:
          return JsonResponse({"status": f"An unexpected error occurred: {str(e)}"}) 


class ConvertToJsonView(APIView):
    permission_classes = [AllowAny]
    serializer_class = FileSerializers

    def post(self, request):
        file_upload = request.FILES.get("file")

        if not file_upload:
            return JsonResponse({"status": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract file name and extension
        _, file_extension = os.path.splitext(file_upload.name)
        file_extension = file_extension.lower()  # Convert the extension to lowercase

        if file_extension not in ['.csv', '.xls', '.xlsx']:
            return JsonResponse({"status": "Unsupported file type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        try:
            if file_extension == '.csv':
                df = pd.read_csv(file_upload)
            else:
                df = pd.read_excel(file_upload)

            data_dict = {}
            for _, row in df.iterrows():
                school_name = row.get('School Name')
                grades = ["KG 1", "KG 2", "GRADE 1", "GRADE 3", "GRADE 4","GRADE 5", "GRADE 6", "GRADE 7", "GRADE 8",
                           "GRADE 9", "GRADE 10","GRADE 11", "GRADE 12"]
                
                if school_name not in data_dict:
                    data_dict[school_name] = []

                for grade in grades:
                    fees = row.get(grade)
                    if not pd.isna(fees):
                        try:
                            data_dict[school_name].append({"fees": fees,"grade": grade})
                        except ValueError:
                            return JsonResponse({"result":{ "message": f"Invalid fee value for {grade} in school {school_name}",
                                                           "status":False,"responsecode":404}})  
            filtered_dict = {school: entries for school, entries in data_dict.items() if entries}
            data_dict.clear()
            data_dict.update(filtered_dict)

            json_data = json.dumps(filtered_dict,indent=4)
            path = Path(__file__).resolve().parent.parent    # path name
            file_path=(os.path.join(path, "sample.txt"))
            with open(file_path, 'w') as json_file:
                json_file.write(json_data)

            return JsonResponse({"result":{ "message": "file successfully convert to json.","status":True,
                                           "responsecode":200}})  
        except Exception as e:
            return JsonResponse({"result": {"message": f"An unexpected error occurred: {str(e)}","status": False,
                                            "response": 500}})

class JsonConvertTxt(APIView): # file convert json to pdf.
        permission_classes=[AllowAny]
        serializer_class = FileSerializers

        def post(self, request):
            try:
                file_upload = request.FILES.get("file")
                if not file_upload:
                    return JsonResponse({"status": "File not found"}, status=status.HTTP_404_NOT_FOUND)
                
                try:
                    json_data = json.load(file_upload)
                except json.JSONDecodeError:
                    return HttpResponse("Invalid JSON", status=400)
                
                school_data = []
                for school_name,details in json_data.items():
                    school_data.append(f"School Name: {school_name} has following grades and fees")
                    for details in json_data[school_name]:
                        grade = details["grade"]
                        fee = details["fees"]
                        school_data.append(f"{grade}fees is {fee}")

                json_data = json.dumps(school_data,indent=5)
                path = Path(__file__).resolve().parent.parent  #path name 
                file_path=(os.path.join(path, "school_data.txt"))

                with open(file_path, 'w') as json_file:
                    json_file.write(json_data)
                    return JsonResponse({"result":{ "message": "file successfully convert to pdf.","status":True,
                                                           "responsecode":200}})
            except Exception as e:
                return JsonResponse({"result": {"message": f"An unexpected error occurred: {str(e)}","status": False,
                                                "response": 500}})


