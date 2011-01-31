from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import EmailMessage

from geopy import geocoders

from django.http import *
from django.core.urlresolvers import reverse

from thebus.web.forms import *
from thebus.web.models import *
from thebus.web.search import *

from thebus.ots.models import *

# Home View
def home(request, template):
    
    form = SearchForm()
    
    return render_to_response(template, {
        'form': form,
    }, context_instance=RequestContext(request))


# Search View
def search(request, template):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        
        if form.is_valid():
            query = form.cleaned_data['query']
            
            if query.isdigit():
                try:
                    stop = Stop.objects.get(code=query)
                    found_stops = [stop,]
                    
                    return HttpResponseRedirect(stop.get_absolute_url())
                    
                except Stop.DoesNotExist, e:
                    pass
                    
            stop_query = get_query(query, ['code', 'name',])
            found_stops = Stop.objects.filter(stop_query).order_by('code')[:20]
            
            # If only one stop is found, just redirect to it.
            if len(found_stops) == 1:
                return HttpResponseRedirect(found_stops[0].get_absolute_url())
            
            return_value = {
                'form': form,
                'query': query,
                'stops': found_stops
            }
        else:
            return_value = {
                'form': form
            }
            
    else:
        form = SearchForm()
        
        return_value = {
            'form': form
        }
    
    return render_to_response(template, return_value, context_instance=RequestContext(request))

def search_by_location(request, template, latitude, longitude):
    if latitude and longitude:
        latitude = float(latitude)
        longitude = float(longitude)
        
        g = geocoders.Google()
        
        location_string = g.reverse((latitude, longitude))
        
        stops = Stop.objects.near(latitude, longitude, 0.3);
        
        response = { 'stops': stops, 'form': SearchForm(), 'location_string': location_string }
    
    else:
        response = { 'form': SearchForm() }

    return render_to_response(template, response, context_instance=RequestContext(request))


def stop_detail(request, template, stop_id):
    stop = get_object_or_404(Stop, code=stop_id)

    return render_to_response(template, {
        'stop': stop,
        'routes': stop.get_routes,
        'times': stop.get_times,
        'form': SearchForm()
    }, context_instance=RequestContext(request))
    
def route_detail(request, template, route_short_name):
    route = get_object_or_404(Route, short_name=route_short_name)
    
    trips = Trip.objects.filter(route=route)
    
    return render_to_response(template, {
        'route': route,
        'trips': trips,
        'form': SearchForm()
    }, context_instance=RequestContext(request))

def bus_detail(request, template, bus_number):
    bus = get_object_or_404(Bus, number=bus_number)
    
    return render_to_response(template, {
        'bus': bus,
        'form': SearchForm()
    }, context_instance=RequestContext(request))

def updates(request, template):
    updates = Update.objects.all().order_by('-published')
    
    return render_to_response(template, {
        'updates': updates,
        'form': SearchForm()
    }, context_instance=RequestContext(request))
    
def update_detail(request, template, update_slug):
    update = get_object_or_404(Update, slug=update_slug)
    
    return render_to_response(template, {
        'update': update,
        'form': SearchForm()
    }, context_instance=RequestContext(request))
    
def feedback(request, template):
    feedback_success = False
    data = request.GET.copy()

    if 'success' in data:
        feedback_success = True
    
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        
        if feedback_form.is_valid():
            feedback_payload = {
                'message': feedback_form.cleaned_data['message'],
                'email': feedback_form.cleaned_data['email'],
                'client_info': request.META,
            }
            
            sender = 'TheBus.ws <no-reply@thebus.ws>'
            subject = 'New TheBus.ws Feedback'
            content = render_to_string('emails/feedback.txt', { 'payload' : feedback_payload, })
            recipients = ['michael@whalesalad.com']
            
            message = EmailMessage(subject=subject, body=content, from_email=sender, to=recipients, headers = { 'Reply-To': feedback_payload['email'] })
            message.content_subtype = "html"
            message.send()
            
            return HttpResponseRedirect('/feedback/?success')
            
    else:
        feedback_form = FeedbackForm()
        
    # A feedback page... has a form to submit comments
    return render_to_response(template, {
        'feedback_form': feedback_form,
        'form': SearchForm(),
        'feedback_success': feedback_success
    }, context_instance=RequestContext(request))
    
