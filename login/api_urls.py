# login/urls.py
from django.urls import path
from .views import SignupView, LoginView,index

urlpatterns = [
    #  path('', view=index, name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
