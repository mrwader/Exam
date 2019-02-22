from django.shortcuts import render, redirect
from .models import User, Trip
import bcrypt
from django.contrib import messages
import datetime


def index(request):
    return render(request, "exam_app/index.html")


def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        fname_from_form = request.POST['first_name']
        lname_from_form = request.POST['last_name']
        email_from_form = request.POST['email']
        password_from_form = request.POST['password']

        pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt())

        user = User.objects.create(
            first_name=fname_from_form, last_name=lname_from_form, email=email_from_form, password=pw_hash)

        if 'user' in request.session:
            request.session['user'] = user.email
        else:
            request.session['user'] = user.email
        return redirect("/dashboard")


def login(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        email_from_form = request.POST['email']
        password_from_form = request.POST['password']
        user = User.objects.get(email=email_from_form)
        print(user)
        if bcrypt.checkpw(password_from_form.encode(), user.password.encode()):
            if 'user' in request.session:
                request.session['user'] = user.email
            else:
                request.session['user'] = user.email
            return redirect("/dashboard")
        return redirect("/")

def logout(request):
    del request.session['user']
    return redirect("/")   

def dashboard(request):
    if 'user' not in request.session:
        return redirect("/")

    user = User.objects.get(email = request.session['user'])
    ordered= user.user_trips.all().order_by('-created_at')
    exclude = Trip.objects.exclude(users = user)

    context={
        "user": User.objects.get(email=request.session['user']),
        "trips": ordered,
        # "other_trips": Trip.objects.exclude(user=user)
        "other_trips": exclude
    }
    return render(request, "exam_app/dashboard.html", context)

def new_trip(request):
    if 'user' not in request.session:
        return redirect("/")
    context={
        "user": User.objects.get(email=request.session['user']),
    }
    return render(request, "exam_app/new_trip.html", context)

def create_trip(request):
    if 'user' not in request.session:
        return redirect("/")
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trips/new")
    else:

        user = User.objects.get(email = request.session['user'])
        destination_form = request.POST['destination']
        start_date_form = request.POST['start_date']
        end_date_form = request.POST['end_date']
        plan_form = request.POST['plan']
        trip = Trip.objects.create(destination = destination_form, start_date = start_date_form, end_date = end_date_form, plan = plan_form,user=user)
        user.user_trips.add(trip)
        return redirect ("/dashboard")

def edit_trip(request, id):
    if 'user' not in request.session:
        return redirect("/")
    
    trip = Trip.objects.get(id=id)
    if trip.user.email != request.session['user']:
        
        return redirect("/dashboard")
    context = {
        "trip": trip,
        "user": User.objects.get(email=request.session['user']),
    }

    return render(request, "exam_app/edit_trip.html", context)

def update_trip(request):
    if 'user' not in request.session:
        return redirect("/")

    trip_id = request.POST['trip_id']
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trips/edit/{trip_id}")
    else:
        trip = Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.updated_at = datetime.datetime.now()
        trip.save()
        return redirect("/dashboard")

def delete_trip(request, id):
    if 'user' not in request.session:
        return redirect("/")
    
    trip = Trip.objects.get(id=id)
    if trip.user.email != request.session['user']:
        return redirect("/dashboard")
    else:
        trip.delete()
        return redirect("/dashboard")

def view_trip (request, id):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        "trip": Trip.objects.get(id=id),
        "user": User.objects.get(email=request.session['user']),
    }

    return render(request, "exam_app/view_trip.html", context)

def join_trip(request,id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(email=request.session['user'])
    trip.users.add(user)
    print(trip)
    return redirect("/dashboard")

def cancel_trip(request,id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(email=request.session['user'])
    trip.users.remove(user)
    print(trip)
    return redirect("/dashboard")



