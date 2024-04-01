from django.db import models
from cramschool_common.models import City

# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

class Info(models.Model):
    info_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100)
    found_date = models.DateField()
    city = models.ForeignKey(
    City, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
