from django.urls import path
from adminapp.views import*

urlpatterns = [
    path('rolecreate/',RoleMasterViews.as_view()),
    path('admincreate/',AdminCreateViews.as_view()),
    path('adminlogin/',AdminLogin.as_view()),
    path('sessioncreate/',SessionCreateViews.as_view()),
    path('userlist/',userList.as_view()),
    path('sessionlist/',SessionList.as_view()),
    path('bookingList/',BookingList.as_view()),

    path('filetojson/',ConvertToJsonView.as_view()),
    path('jsontotxt/',JsonConvertTxt.as_view()),
    path('pdftrans/',PdfTranslateView.as_view()),
  

  
]