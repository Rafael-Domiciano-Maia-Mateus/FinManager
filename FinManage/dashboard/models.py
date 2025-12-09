from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=150)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  category = models.CharField(max_length=50, blank=True, null=True)
  date = models.DateField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now_add=True) 

  def __str__(self):
    return f"{self.title} - R${self.amount}"

