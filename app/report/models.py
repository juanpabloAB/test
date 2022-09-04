from django.db import models

# Create your models here.
class Transactions(models.Model):
    date = models.DateTimeField()
    amount = models.IntegerField()
    report = models.UUIDField()
    report_id=models.IntegerField()