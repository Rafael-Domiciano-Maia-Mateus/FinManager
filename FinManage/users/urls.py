from django.urls import path
from .views import *

urlpatterns = [
  path('', LoginView.as_view(), name='LoginView'),
  path('RegisterAccount/', RegisterView.as_view(), name='RegisterAccount'),
  path('logout/', LogoutView.as_view(), name='LogoutAccount'),
  path('account/', Account.as_view(), name='account')
]

