from django.db import models


# Create your models here.
class CoolBeans(models.Model):
    """class for making wowzers table for database"""

    something = models.CharField(max_length=255, default="cool stuff bro")
