from django.urls import path
from .views import *

urlpatterns = [
  path('homepage/', Homepage.as_view(), name="homepage"),
]