from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    """
    Extensão do modelo padrão de usuário do Django.

    Esta classe adiciona ao usuário:
    - Um número de telefone único.
    - Formatação automática do número ao salvar.

    A formatação suporta:
      - Celular (11 dígitos): (XX)XXXXX-XXXX
      - Telefone fixo (10 dígitos): (XX)XXXX-XXXX

    Se o número informado não tiver 10 ou 11 dígitos,
    um ValueError será lançado.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_numbers = models.CharField(max_length=14, unique=True, help_text="Número de telefone formatado automaticamente.")

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para padronizar o número de telefone
        antes de salvar no banco de dados.

        - Remove qualquer caractere não numérico
        - Formata conforme o tamanho (10 ou 11 dígitos)
        - Lança erro caso o número seja inválido
        """
        
        phone = ''.join(filter(str.isdigit, self.phone_numbers))
        self.phone_numbers = (
            f"({phone[:2]}){phone[2:7]}-{phone[7:]}" if len(phone) == 11 else
            f"({phone[:2]}){phone[2:6]}-{phone[6:]}" if len(phone) == 10 else
            (_ for _ in ()).throw(ValueError("Número de telefone inválido"))
        )

        super().save(*args, **kwargs)

    def __str__(self):
        """Retorna uma string amigável para o admin e debug."""
        return f"{self.user.username} - {self.phone_numbers}"
