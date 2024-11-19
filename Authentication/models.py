# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.utils import choices

class Farmer(AbstractUser):
    SUB_CHOICES = [
            ('Inactive', 'Inactive'),
            ('Demo','Demo'),
            ('Subscribed', 'Subscribed')
            ]


    full_name = models.CharField(max_length=255)
    county = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    farm_name = models.CharField(max_length=255)

    streak = models.IntegerField(default=0)
    subscription_status = models.CharField(max_length=100, choices=SUB_CHOICES, default='Demo')
#     date_of_subscription = 
    


    def __str__(self):
        return self.full_name

class Cow(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    breed_type = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    age = models.IntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='cows')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.farmer.farm_name}"


class Sensor(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='sensors')
    
    




