from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class Rolemaster(models.Model):
    role_name=models.CharField(max_length=20,null=True)
    class Meta:
        db_table="rolemaster"

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,name,email,city,country,password,**extra_fields):
        if not email:
            raise ValueError(('The Email field must be set')) 
        email = self.normalize_email(email)
        user = self.model(name=name,
                          email=email,city=city
                         ,country=country,password=password,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name,email,city,country,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name,email,city,country,password, **extra_fields)

class AdminModel(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=50,null=True)
    email=models.EmailField(max_length=64,unique=True,)
    phonenumber=models.CharField(max_length=100,blank=False)
    city=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100)
    password=models.CharField(max_length=100,null=True)
    role=models.ForeignKey(Rolemaster,on_delete=models.CASCADE,null=True)
    is_admin=models.BooleanField(default=False)
    is_user=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phonenumber','city','country','password']
    

    class Meta:
        db_table="tutoradmin"


class TutoringSession(models.Model):
    subject=models.CharField(max_length=100,null=True)
    start_time=models.TimeField(null=True)
    end_time=models.TimeField(null=True)
    session_day=models.DateField()
    class Meta:
        db_table="tutoringsession"
