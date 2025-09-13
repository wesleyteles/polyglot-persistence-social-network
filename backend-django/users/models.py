from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """Modelo de usuário customizado"""
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True)
    foto_perfil = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    # O username, password, first_name, last_name já vêm do AbstractUser