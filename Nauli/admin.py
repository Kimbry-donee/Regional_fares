from django.contrib import admin
from .models import Region, Terminal, Route, Vehicle, Time


# Register your models here.
admin.site.register(Region)
admin.site.register(Terminal)

class RouteAdmin(admin.ModelAdmin):
 list_display = [
   'bus_name', 
   'dist_from', 
   'dist_to', 
   'price',
   'departure',
   'arrival',
   'stops'
   'via',
   ]
admin.site.register(Route)

admin.site.register(Vehicle)
admin.site.register(Time)
