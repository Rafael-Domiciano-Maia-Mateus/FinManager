from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models.functions import Lower
from .models import Expense

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
  template_name = "dashboard.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    expenses = Expense.objects.filter(user=self.request.user).order_by("-date")

    context["expenses"] = expenses

    category_data = expenses.values('category').annotate(total_amount=Sum('amount'))

    labels = [item['category'] for item in category_data]
    values = [float(item['total_amount']) for item in category_data]

    context["labels"] = labels
    context["values"] = values
    return context
  

class ExpenseCreateView(LoginRequiredMixin, CreateView):
  model = Expense
  fields = ["title", "amount", "category"]
  template_name = "add_expense.html"
  success_url = reverse_lazy("dashboard")

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  

class manageCategories(LoginRequiredMixin, View):
  template_name = "manageCategories.html"

  def get(self, request):
    expenses_by_category = (
      Expense.objects
      .filter(user=request.user)
      .annotate(category_lower=Lower('category'))
      .values('category_lower')
      .annotate(total=Sum('amount'))
      .order_by('category_lower')
    )
    
    context = {
      'expenses_by_category': expenses_by_category
    }
    
    return render(request, self.template_name, context)
  