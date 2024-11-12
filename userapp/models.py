from django.db import models
from adminapp.models import AdminModel,Rolemaster,TutoringSession

# Create your models here.

class SessionBooking(models.Model):
    user=models.ForeignKey(AdminModel,on_delete=models.CASCADE)
    sessions=models.ForeignKey(TutoringSession,on_delete=models.CASCADE)

    class Meta:
        db_table="sessionbooking"