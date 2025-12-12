from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import Users

class LoginView(View):
  template_name = "login.html"
  
  def get(self, request):
    if request.user.is_authenticated:
      return redirect('homepage')
    return render(request, self.template_name)
  
  def post(self, request):
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    
    if not email or not password:
      messages.error(request, 'Fill in all the fields.')
      return redirect('LoginView')

    try:
      user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
      messages.error(request, 'Invalid email or password.')
      return redirect('LoginView')
    
    user = authenticate(request, username=user_obj.username, password=password)
    
    if user is None:
      messages.error(request, 'Invalid email or password.')
      return redirect('LoginView')
    
    if not user.is_active:
      messages.error(request, 'Account deactivated.')
      return redirect('LoginView')
    
    login(request, user)
    return redirect('homepage')


class RegisterView(View):
  template_name = "registerAccount.html"
  
  def get(self, request):
    if request.user.is_authenticated:
      return redirect('homepage')
    return render(request, self.template_name)
  
  def post(self, request):
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    password = request.POST.get('password', '').strip()
    confirmPassword = request.POST.get('confirm_password', '').strip()
    
    if not all([username, email, phone, password, confirmPassword]):
      messages.error(request, 'Fill in all the fields.')
      return redirect('RegisterAccount')
    
    if password != confirmPassword:
      messages.error(request, 'The passwords do not match.')
      return redirect('RegisterAccount')
    
    if User.objects.filter(email=email).exists():
      messages.error(request, 'Email is already in use.')
      return redirect('RegisterAccount')
    
    try:
      user = User.objects.create_user(username=username, email=email, password=password)
      Users.objects.create(user=user, phone_numbers=phone)
      messages.success(request, 'Account created successfully! Please login.')
      return redirect('LoginView')
    
    except IntegrityError:
      messages.error(request, 'Phone number already registered.')
      return redirect('RegisterAccount')

    except ValueError as e:
      messages.error(request, str(e))
      return redirect('RegisterAccount')
    
    except Exception:
      messages.error(request, 'Unexpected error.')
      return redirect('RegisterAccount')


class LogoutView(View):
  def get(self, request):
    logout(request)
    return redirect('LoginView')


class Account(LoginRequiredMixin, View):
  template_name = "account.html"

  def get(self, request):
    conta = Users.objects.get(user=request.user)
    context = {
      'conta': conta
    }
    return render(request, self.template_name, context)
    