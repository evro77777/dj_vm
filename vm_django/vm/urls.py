from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginUser.as_view(), name='home'),
    path('form/', addquery, name='form'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',logout_user,name='logout'),

]
