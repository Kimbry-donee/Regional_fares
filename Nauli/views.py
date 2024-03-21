from django.shortcuts import render
from django.db.models import Q
from .models import Time
from django.utils.safestring import mark_safe


def searchFare(request):
  start_region = request.GET.get('first_region', '')
  stop_region = request.GET.get('second_region', '')
  # Determine if the user inputted the regions in direct or inverse order
  direct_order = start_region < stop_region
  # Create Q objects for both direct and inverse queries
  inverse_query = Q(route__dist_from__regional_name__icontains=stop_region) & Q(route__dist_to__regional_name__icontains=start_region)
  direct_query = Q(route__dist_from__regional_name__icontains=start_region) & Q(route__dist_to__regional_name__icontains=stop_region)
  
  # Combine the queries with OR to get results for either direct or inverse inputs
  query = direct_query | inverse_query
  
  # Perform the query
  results = Time.objects.filter(query)
  if not results:
      message = mark_safe(f"Hakuna magari yanayopatikana kutoka <strong>{start_region}</strong> hadi <strong>{stop_region}</strong>")
      return render(request, 'nauli/home.html', {'message': message})
  context = {
    'results': results, 
    'direct_order': direct_order,
  }
  return render(request, 'nauli/home.html', context)

