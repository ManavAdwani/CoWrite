# login/urls.py
from django.urls import path
from .views import *

urlpatterns = [
     path('', view=index, name='index'),
     path('login',view=loginpage,name='loginpage'),
      path('signup',view=signuppage,name='signuppage'),
    # path('sig', LoginView.as_view(), name='login'),
]
