from django.urls import path
from userapp.views import*

urlpatterns = [
    path('usercreate/',UserCreateViews.as_view()),
    path('userlogin/',UsersLogin.as_view()),
    path('sessionbooking/',SessionBookingViews.as_view()),
    path('unbookingsession/',UnbookedSessionsListView.as_view()),
]