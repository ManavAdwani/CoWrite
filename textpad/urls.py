from django.urls import path
from .views import *

urlpatterns = [
    path('textpad',view=textpad,name='textpad'),
]
