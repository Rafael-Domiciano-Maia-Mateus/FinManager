from django.urls import path
from .views import DashboardView, ExpenseCreateView

urlpatterns = [
  path("", DashboardView.as_view(), name="dashboard"),
  path("add/", ExpenseCreateView.as_view(), name="add_expense"),
]
