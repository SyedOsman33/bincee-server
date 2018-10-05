from django.db import models

# Create your models here.
from django.db.models import PROTECT


class BinceeType(models.Model):
    name = models.CharField(null=False, max_length=50)
    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)





class BinceeEntities(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(BinceeType, on_delete=PROTECT)
    # customer = models.ForeignKey(Customer, on_delete=PROTECT)


    #TODO ADD COLUMNS GENERICALLY
