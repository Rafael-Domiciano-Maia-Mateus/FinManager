from django.urls import path
from .views import *

urlpatterns = [
  path("", DashboardView.as_view(), name="dashboard"),
  path("add/", ExpenseCreateView.as_view(), name="add_expense"),
  path("manageCategories/", manageCategories.as_view(), name="manageCategories"),
]
