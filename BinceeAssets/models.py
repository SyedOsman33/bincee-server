from django.db import models

# Create your models here.
from django.db.models import PROTECT
from BMS import settings

class BinceeType(models.Model):
    name = models.CharField(null=False, max_length=50)
    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)


class BinceeEntities(models.Model):
    #TODO Qasmi add generic and specific fields for All Bincee Assets
    name = models.CharField(max_length=250) #FULL NAME
    type = models.ForeignKey(BinceeType, on_delete=PROTECT)
    description = models.CharField(blank=True, null=True, max_length=1000)
    dob = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='static/media/',blank=True, null=True)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    # customer = models.ForeignKey(Customer, on_delete=PROTECT)


class RealTimeLocationData(models.Model):
    #TODO Qasmi use this model for location data.
    bince_entity = models.ForeignKey(BinceeEntities, related_name='location_data_entity_id')
    timestamp = models.DateTimeField(null=False, db_index=True)
    #Fixed location or realtime moving objects.
    latitude = models.DecimalField(decimal_places=10, null=True, blank=True,max_digits=20)
    longitude = models.DecimalField(decimal_places=10, null=True, blank=True,max_digits=20)
