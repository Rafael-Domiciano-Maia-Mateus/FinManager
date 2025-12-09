from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Expense

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
  template_name = "dashboard.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    expenses = Expense.objects.filter(user=self.request.user).order_by("-date")
    context["expenses"] = expenses

    labels = [exp.title for exp in expenses]
    values = [float(exp.amount) for exp in expenses]

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
  