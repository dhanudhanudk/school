from rest_framework import serializers
from.models import*
from userapp.models import*

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=AdminModel
        fields="__all__"

class SessionBookingSerializers(serializers.ModelSerializer):
    class Meta:
        model=SessionBooking
        fields="__all__"