from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_numbers = models.CharField(max_length=14, unique=True, help_text="Número de telefone formatado automaticamente.")

  def save(self, *args, **kwargs):
    phone = ''.join(filter(str.isdigit, self.phone_numbers))
    self.phone_numbers = (
      f"({phone[:2]}){phone[2:7]}-{phone[7:]}" if len(phone) == 11 else
      f"({phone[:2]}){phone[2:6]}-{phone[6:]}" if len(phone) == 10 else
      (_ for _ in ()).throw(ValueError("Número de telefone inválido"))
    )

    super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.user.username} - {self.phone_numbers}"