from django.db import models

# Create your models here.
class Emergency_Room(models.Model):
    hospital_name = models.CharField(max_length=250, blank=True, default="") #dutyName
    address = models.CharField(max_length=250, blank=True, default="") #dutyAddr
    phone = models.CharField(max_length=250, blank=True, default="") #hv1
    bed_number = models.IntegerField(default=0) #HVS01
    bed_number_now = models.IntegerField(default=0) #hvec
    distance_km = models.IntegerField(default=30) #
    # description = models.TextField(blank=True, default="") #
    
    
    def __str__(self):
        return self.hospital_name