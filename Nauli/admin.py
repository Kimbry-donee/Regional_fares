from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Region, Terminal, Route, Vehicle, Time, CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Define the display fields for the user model in the admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
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
