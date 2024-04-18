from django.db import models
from apps.cramschool_common.models import Category, City

# Create your models here.


class CategoryByInfo(models.Model):
    category_by_info_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    info = models.ForeignKey('Info', on_delete=models.CASCADE)


class Info(models.Model):
    info_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100)
    found_date = models.DateField()
    city = models.ForeignKey(
        City, on_delete=models.CASCADE)
