from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from.models import*
class Validators():
    def users_valid_put(data):
   
        try:
            json_items = ["id","role_id",]
            # Check for missing keys
            for key in json_items:
                if key not in data:
                    return {'data': f"{key} key is missing","status":False}
                
            for val in json_items:
                if val not in data:
                    return {'data': f"{val} value is required","status":False}
            
            return {'status': True}
                
        except Exception as e:
            return {'data': f'{e}' + " Internal Error", 'status': False}
        
    def users_valid(data):
   
        try:
            json_items = ["name","email","phonenumber","city","country","password",]
            # Check for missing keys
            for key in json_items:
                if key not in data:
                    return {'data': f"{key} key is missing","status":False}
                
            for val in json_items:
                if val not in data:
                    return {'data': f"{val} value is required","status":False}
                
            
            return {'status': True}
                
        except Exception as e:
            return {'data': f'{e}' + " Internal Error", 'status': False}
    def admin_login_valid(data):
        try:
            json_items = ['email','password']
            # Check for missing keys
            for key in json_items:
                if key not in data:
                    return {'data': f"{key} key is missing","status":False}
                
            for val in json_items:
                if val not in data:
                    return {'data': f"{val} value is required","status":False}

            return {'status': True}
                
        except Exception as e:
            return {'data': f'{e}' + " Internal Error", 'status': False}
        
    def session_booking(data):
        try:
            json_items = ['user','sessions']
            # Check for missing keys
            for key in json_items:
                if key not in data:
                    return {'data': f"{key} key is missing","status":False}
                
            for val in json_items:
                if val not in data:
                    return {'data': f"{val} value is required","status":False}
             #filter unique user 
            sessions= data.get('sessions')
            if sessions :
                if SessionBooking.objects.filter(sessions=sessions).exists():
                    return {'data': f"{sessions}-Session already booking ", 'status': False}
                

            return {'status': True}
                
        except Exception as e:
            return {'data': f'{e}' + " Internal Error", 'status': False}