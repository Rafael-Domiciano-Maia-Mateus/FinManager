from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Lower
from django.utils import timezone
from dashboard.models import Expense

# Create your views here.
class Homepage(LoginRequiredMixin, View):
  template_name = "homepage.html"

  def get(self, request):
    now = timezone.now()

    total_month = (
      Expense.objects.filter(
        user=request.user,
        date__year=now.year,
        date__month=now.month,
      ).aggregate(total=Sum('amount'))['total'] or 0
    )

    last_expense = (
      Expense.objects.filter(user=request.user).order_by('-created_at').first()
    )

    categories_count = (
      Expense.objects
      .filter(user=request.user, category__isnull=False)
      .exclude(category='')
      .annotate(category_lower=Lower('category'))
      .values('category_lower')
      .distinct()
      .count()
    )

    context = {
      'total_month': total_month,
      'last_expense': last_expense,
      'categories_count': categories_count
    }

    return render(request, self.template_name, context)
