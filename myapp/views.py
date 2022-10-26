from django.shortcuts import render, HttpResponse, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import requests
from .models import *

# Create your views here.
def index(request):
  return render(request, 'index.html')


def register(request):
  if request.method == "POST":
    errors = User.objects.validation(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else:
      new_id = User.objects.register(request.POST)
      request.session['user_id'] = new_id
      return redirect('/dashboard')

def login(request):
  if request.method == "POST":
    valid = User.objects.loginvalidation(request.POST)
    if valid:
      user_info = User.objects.get(email=request.POST['login_username'])
      request.session['user_id'] = user_info.id
      return redirect('/dashboard')
    else:
      messages.add_message(request, messages.INFO, "Invalid Username or Password")
      return redirect('/')

def dashboard(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else: 
    context = {
      "user_info": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'dashboard.html', context)

def edit(request):
  context = {
    "user_info": User.objects.get(id=request.session['user_id'])
  }
  return render(request, 'edit.html', context)

def getcity(request):
  if request.method == "POST":
    context = {}
    destination = request.POST['code']
    radius = int(request.POST['radius'])*1.609344

    gmaps = requests.request("GET", f'https://maps.googleapis.com/maps/api/geocode/json?address={destination}&key=AIzaSyCM_kVQIQbZI2CsmTNGhkcPI5sVioQmrdE')
    jsonGmaps = gmaps.json()
    lat = jsonGmaps['results'][0]['geometry']['location']['lat']
    lng = jsonGmaps['results'][0]['geometry']['location']['lng']
    
    url = "https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/by-radius"

    
    querystring = {"radius":radius,"lng":lng,"lat":lat}

    headers = {
        'x-rapidapi-host': "cometari-airportsfinder-v1.p.rapidapi.com",
        'x-rapidapi-key': "aef226d282msh249d9c623d1a1c2p1331b4jsnaceddd0934ee"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonResponse = response.json()
    print(jsonResponse)
    airportsList = []
    for i in range(len(jsonResponse)):
      airportsList.append(jsonResponse[i])

    print(airportsList)
    context["result_location_source"] = jsonGmaps['results'][0]['formatted_address']
    context["all_airports"] = airportsList
    context["destination"] = destination
    

  return render(request, 'result.html', context)


def upload(request):
  if request.method == "POST":
    pic = request.FILES['picture']
    fs = FileSystemStorage()
    user_pic = fs.save(pic.name, pic)
    url = fs.url(user_pic)
    context = {
      "url": url
    }

    adminUser = User.objects.get(id=2)
    adminUser.pic = user_pic
  return render(request, 'upload.html', context)

def process_edit(request):
  pass

def logout(request):
  del request.session['user_id']
  return redirect('/')