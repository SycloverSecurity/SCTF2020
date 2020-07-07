from django.contrib.auth.models import AbstractUser
from django.db import models


class Token(models.Model):
    Token = models.CharField(max_length=64,null=True)
