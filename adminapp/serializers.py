from rest_framework import serializers
from.models import*
from userapp.models import SessionBooking
from userapp.serializers import SessionBookingSerializers

class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model=Rolemaster
        fields="__all__"
        
class AdminCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=AdminModel
        fields="__all__"

class CreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=AdminModel
        fields="__all__"

class SessionCreatedSerializers(serializers.ModelSerializer):
    class Meta:
        model=TutoringSession
        fields="__all__"

class UserListSerializers(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    
    class Meta:
        model=SessionBooking
        fields=["id","name","email"]
    def get_id(self, obj):
        return obj.id
    def get_name(self, obj):
        return obj.name
    def get_email(self, obj):
        return obj.email
    
class SessionBookingSerializers(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    subject=serializers.SerializerMethodField()
    start_time=serializers.SerializerMethodField()
    end_time=serializers.SerializerMethodField()
    session_day=serializers.SerializerMethodField()
    
    class Meta:
        model=SessionBooking
        fields=["id","name","email","subject","start_time","end_time","session_day"]
    def get_id(self, obj):
        return obj.user.id
    def get_name(self, obj):
        return obj.user.name
    def get_email(self, obj):
        return obj.user.email
    def get_subject(self, obj):
        return obj.sessions.subject
    def get_start_time(self, obj):
        return obj.sessions.start_time
    def get_end_time(self, obj):
        return obj.sessions.end_time
    def get_session_day(self, obj):
        return obj.sessions.session_day
    
class FileSerializers(serializers.ModelSerializer):
    file=serializers.FileField()

