from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from.models import*
from datetime import datetime
from django.utils import timezone

class Validators():
    def users_valid(data):
   
        try:
            json_items = ["name","email","phonenumber","city","country","password","role"]
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
        
    def role_valid(data):
   
        try:
            json_items = ["role_name"]
            # Check for missing keys
            for key in json_items:
                if key not in data:
                    return {'data': f"{key} key is missing","status":False}
                
            for val in json_items:
                if val not in data:
                    return {'data': f"{val} value is required","status":False}
                
                for val in json_items:
                    if val == 'role_name':
                        role = data[val] 
                    if Rolemaster.objects.filter(role_name=role).exists():
                        return {'data': f"{role} - This username is already exit", 'status': False}

            return {'status': True}
                
        except Exception as e:
            return {'data': f'{e}' + " Internal Error", 'status': False}
        

    def admin_valid(data):
   
        try:
            json_items = ["name",'email','phonenumber',"city","country","password"]
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
        
    
 
    def session_valid(data, allowed_start_time=None, allowed_end_time=None):
        try:
            json_items = ["subject", "session_day", 'start_time', 'end_time']
            # Check for missing keys
            for key in json_items:
                if key not in data:
                    return {'data': f"{key} key is missing", "status": False}
            
            # Check for empty values
            for val in json_items:
                if not data.get(val):
                    return {'data': f"{val} value is required", "status": False}
            
            # Convert start_time and end_time to time objects
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            
            try:
                start_time_obj = datetime.strptime(start_time, "%H:%M").time()
                end_time_obj = datetime.strptime(end_time, "%H:%M").time()
            except ValueError:
                return {'data': 'Invalid time format. Use HH:MM.', 'status': False}

            # Time validation
            if allowed_start_time and allowed_end_time:
                allowed_start_time = datetime.strptime(allowed_start_time, "%H:%M").time()
                allowed_end_time = datetime.strptime(allowed_end_time, "%H:%M").time()
                if not (allowed_start_time <= start_time_obj < allowed_end_time and allowed_start_time < end_time_obj <= allowed_end_time):
                    return {'data': 'Booking time is not within allowed time slots.', 'status': False}

            # Date validation
            session_day_str = data.get('session_day')
            try:
                session_day = datetime.strptime(session_day_str, "%Y-%m-%d").date()
                if session_day <= timezone.now().date():
                    return {'data': 'The session day must be a future date.', 'status': False}
            except ValueError:
                return {'data': 'Invalid date format. Use YYYY-MM-DD.', 'status': False}
            
            # Check for overlapping sessions
            overlapping_sessions = TutoringSession.objects.filter(
                session_day=session_day,
                start_time__lt=end_time_obj,
                end_time__gt=start_time_obj
            )
            if overlapping_sessions.exists():
                session_time = f"{session_day_str} {start_time} - {end_time}"
                return {'data': f"{session_time} - this time slot is already booked", 'status': False}
            
            # Check if subject already exists
            subject = data.get('subject')
            if subject and TutoringSession.objects.filter(subject=subject).exists():
                return {'data': f"{subject} - this subject already exists", 'status': False}

            return {'status': True}
        
        except Exception as e:
            return {'data': f'{e} Internal Error', 'status': False}
