from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe
from .models import Time
from django.http import JsonResponse
from Regional_fares import settings
from .forms import EmailForm
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import logging
import hashlib


logger = logging.getLogger(__name__)
mailchimp = Client()
mailchimp.set_config({
  'api_key': settings.MAILCHIMP_API_KEY,
  'server': settings.MAILCHIMP_REGION,
})


def mailchimp_ping_view(request):
    response = mailchimp.ping.get()
    return JsonResponse(response)


def subscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                form_email_hash = hashlib.md5(form_email.encode('utf-8').lower()).hexdigest()
                member_info = {
                    'email_address': form_email,
                    'status': 'subscribed',
                    'merge_fields': {
                      'FNAME': 'Elliot',
                      'LNAME': 'Alderson',
                    }
                }
                # response = client.lists.set_list_member("list_id", "subscriber_hash", {"email_address": "Tommie_Balistreri81@gmail.com", "status_if_new": "unsubscribed"})
                # response = client.lists.add_list_member("list_id", {"email_address": "Addie71@hotmail.com", "status": "unsubscribed"})
                response = mailchimp.lists.set_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_info,
                )
                logger.info(f'API call successful: {response}')
                return redirect('Nauli:subscribe-success')

            except ApiClientError as error:
                logger.error(f'An exception occurred: {error.text}')
                return redirect('Nauli:subscribe-fail')
              

    return render(request, 'nauli/subscribe.html', {
        'form': EmailForm(),
    })

def subscribe_success_view(request):
    return render(request, 'nauli/message.html', {
        'title': 'Successfully subscribed',
        'message': 'Yay, you have been successfully subscribed to our mailing list.',
    })


def subscribe_fail_view(request):
    return render(request, 'nauli/message.html', {
        'title': 'Failed to subscribe',
        'message': 'Oops, something went wrong.',
    })


def unsubscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                form_email_hash = hashlib.md5(form_email.encode('utf-8').lower()).hexdigest()
                member_update = {
                    'status': 'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_update,
                )
                logger.info(f'API call successful: {response}')
                return redirect('Nauli:unsubscribe-success')

            except ApiClientError as error:
                logger.error(f'An exception occurred: {error.text}')
                return redirect('Nauli:unsubscribe-fail')

    return render(request, 'nauli/unsubscribe.html', {
        'form': EmailForm(),
    })

def unsubscribe_success_view(request):
    return render(request, 'nauli/message.html', {
        'title': 'Successfully unsubscribed',
        'message': 'You have been successfully unsubscribed from our mailing list.',
    })


def unsubscribe_fail_view(request):
    return render(request, 'nauli/message.html', {
        'title': 'Failed to unsubscribe',
        'message': 'Oops, something went wrong.',
    })

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


