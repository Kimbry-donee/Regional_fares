from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser



# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Region(models.Model):
  regional_name = models.CharField(max_length=15, unique=True)
  
  class Meta:
    ordering = ['regional_name']
    
  def save(self, *args, **kwargs):
    self.regional_name = self.regional_name.upper()
    super().save(*args, **kwargs)
    
  def __str__(self):
        return self.regional_name
  
  
class Terminal(models.Model):
  terminal_name = models.CharField(max_length=15)
  created_time = models.DateTimeField(
    auto_now_add=True, 
    blank=True,
    null=True,
  )
  region = models.OneToOneField(Region, on_delete=models.CASCADE)

  class Meta:
    ordering = ['-created_time']
    
  def save(self, *args, **kwargs):
    self.terminal_name = self.terminal_name.capitalize()
    super().save(*args, **kwargs)
    
  def __str__(self):
    return f"{self.terminal_name},{self.region.regional_name}"
  

class Vehicle(models.Model):
  CLASSES_CHOICES = [
        ('Odinary', 'Odinary'),
        ('Semi-luxury', 'Semi-luxury'),
        ('Luxury', 'Luxury'),
    ]
  bus_name = models.CharField(max_length=100)
  bus_class = models.CharField(max_length=15, choices=CLASSES_CHOICES, default='Semi-luxury')
  image_1 = models.CharField(max_length=500, blank=True, null=True)
  image_2= models.CharField(max_length=500, blank=True, null=True)

  def __str__(self):
    return self.bus_name

  
  
class Route(models.Model):
  #images = models.ArrayField(models.ImageField(upload_to='images/'), blank=True, null=True)
  dist_from = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='from_region')
  dist_to = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='to_region')
  distance = models.FloatField()
  via = models.CharField(max_length=15, blank=True, null=True)
  stops = models.ManyToManyField(Terminal, blank=False)
  
  def __str__(self):
    return f"Kutoka {self.dist_from} mpaka {self.dist_to}"


class Time(models.Model):
  route = models.ForeignKey(Route, on_delete=models.CASCADE)
  bus = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
  price = models.IntegerField()
  departure_time = models.TimeField()
  arrival_time = models.TimeField()
    
  def __str__(self):
    return f"Departure for {self.bus.bus_name} is {self.departure_time} from {self.route.dist_from} and arrive at {self.arrival_time}to {self.route.dist_to}"