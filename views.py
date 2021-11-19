from django.shortcuts import render, redirect
from django.urls import reverse  # Redirecting Users after password change
from django.contrib.auth import update_session_auth_hash  # Used to change password
from django.contrib.auth import login, authenticate  # Django login
from django.contrib.auth.forms import PasswordChangeForm  # Django Password change form
from .forms import SignUpForm, EventCreationForm
from django.views.decorators.http import require_POST
from .models import Event, Shared_Event
import datetime
from datetime import date, time, timedelta
from django.db import models
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        date_val = datetime.datetime.today()
        date_plus = date_val + timedelta(hours=1)
        date_minus = date_val - timedelta(hours=0)
        # Query for Events within 1 hour of current time
        exc = Shared_Event.objects.filter(user=request.user)
        count = Event.objects.filter(user=request.user).filter(date_time__gte=date_minus,
                                                               date_time__lte=date_plus).exclude(id__in=exc).filter(
            complete=False).count()
        primarycount = Shared_Event.objects.filter(user=request.user).filter(date_time__gte=date_minus,
                                                                             date_time__lte=date_plus).filter(
            complete=False).count()
        secondarycount = Shared_Event.objects.filter(secondary_user=request.user).filter(date_time__gte=date_minus,
                                                                                         date_time__lte=date_plus).filter(
            complete2=False).count()

        maincount=count+primarycount+secondarycount

        context = {
            "count": maincount,
        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


# signup using google authenticate or via backend
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def EventCreate(request):
    form = EventCreationForm()
    context = {'form': form}
    return render(request, 'EventCreate.html', context)


# collects data from the form rendered via 'EventCreate' view
@require_POST
def AddEvent(request):
    print(User.username)
    print(request.POST['Name'])
    print(request.POST['Location'])
    New_Event = Event(user=request.user, Name=request.POST['Name'], Location=request.POST['Location'],
                      date_time=request.POST['DateTime'])

    New_Event.save()
    return redirect('home')


# Shows Events for the particular user only
def SeeEvent(request):
    # Shared_Event uses multiple inheritance and so instance also appears in Event. The 2 following queries ensure only
    # events exclusive to Events is shown
    exc = Shared_Event.objects.filter(user=request.user)
    UserEvents = Event.objects.filter(user=request.user).filter(date_time__range=(date.today(), '2999-01-01')). \
        exclude(id__in=exc).order_by('date_time')
    # Gets all instances where current user is the one who invited others
    UserPrimaryEvents = Shared_Event.objects.filter(user=request.user).filter(
        date_time__range=(date.today(), '2999-01-01')).order_by('date_time')
    PrimaryCount = Shared_Event.objects.filter(user=request.user).filter(
        date_time__range=(date.today(), '2999-01-01')).count()
    # Gets all instances where current user is the one who is invited
    UserSecondaryEvents = Shared_Event.objects.filter(secondary_user=request.user).filter(
        date_time__range=(date.today(), '2999-01-01')).order_by('date_time')
    SecondaryCount = Shared_Event.objects.filter(secondary_user=request.user).filter(
        date_time__range=(date.today(), '2999-01-01')).count()

    context = {
        "UserEvents": UserEvents,
        "UserPrimary": UserPrimaryEvents,
        "UserSecondary": UserSecondaryEvents,
        "PrimaryCount": PrimaryCount,
        "SecondaryCount": SecondaryCount
    }
    return render(request, 'SeeCurrentEvents.html', context)


# Allows user to mark incomplete events as completed
def complete(request, Event_id):
    Completed = Event.objects.get(pk=Event_id)
    Completed.complete = True
    Completed.save()

    return redirect('SeeEvent')


# Allows user to mark complete events as incomplete
def incomplete(request, Event_id):
    inCompleted = Event.objects.get(pk=Event_id)
    inCompleted.complete = False
    inCompleted.save()

    return redirect('SeeEvent')


# Allows user to edit events
def Edit(request, Event_id):
    Prime_Event = Event.objects.get(pk=Event_id)

    context = {
        "Prime_Event": Prime_Event
    }

    return render(request, 'Edit_Event.html', context)


# Saves the edit into database
def Save_Edit(request, Event_id):
    New_Event = Event.objects.get(pk=Event_id)
    New_Event.Name = request.POST['Name']
    New_Event.Location = request.POST['Location']
    New_Event.date_time = request.POST['DateTime']
    New_Event.save()

    return redirect('SeeEvent')


# Deletes completed events of particular user
def DeleteEvent(request):
    Event.objects.filter(user=request.user).filter(complete=True).delete()

    return redirect('SeeEvent')


# Deletes all events of particular user
def DeleteAllEvent(request):
    Event.objects.filter(user=request.user).delete()

    return redirect('SeeEvent')


# Generating Notification
def notification(request):
    date_val = datetime.datetime.today()
    date_plus = date_val + timedelta(hours=1)
    date_minus = date_val - timedelta(hours=0)
    # Query for Events within 1 hour of current time
    exc = Shared_Event.objects.filter(user=request.user)
    order_list = Event.objects.filter(user=request.user).filter(date_time__gte=date_minus,
                                                                date_time__lte=date_plus).exclude(id__in=exc).filter(complete=False)

    count = Event.objects.filter(user=request.user).filter(date_time__gte=date_minus,
                                                           date_time__lte=date_plus).exclude(id__in=exc).filter(complete=False).count()

    order_list2=Shared_Event.objects.filter(user=request.user).filter(date_time__gte=date_minus,
                                                                date_time__lte=date_plus).filter(complete=False)

    primarycount=Shared_Event.objects.filter(user=request.user).filter(date_time__gte=date_minus,
                                                                date_time__lte=date_plus).filter(complete=False).count()

    order_list3=Shared_Event.objects.filter(secondary_user=request.user).filter(date_time__gte=date_minus,
                                                           date_time__lte=date_plus).filter(complete2=False)

    secondarycount=Shared_Event.objects.filter(secondary_user=request.user).filter(date_time__gte=date_minus,
                                                           date_time__lte=date_plus).filter(complete2=False).count()



    context = {
        "count": count,
        "order_list": order_list,
        'primarycount': primarycount,
        'order_list2': order_list2,
        'secondarycount': secondarycount,
        'order_list3': order_list3
    }

    return render(request, 'notification.html', context)


def account(request):
    return render(request, 'account.html')


# Password is changed by using in built django password change feature
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('home'))  # After password is changed instead of logging out redirects back to home
        else:
            return redirect(reverse('changepassword'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'changepassword.html', args)


# Creates shared Event
def CreateSharedEvent(request):
    secondary = User.objects.exclude(id=request.user.id)
    context = {
        'secondary_user': secondary
    }
    return render(request, 'SharedEventCreate.html', context)


@require_POST
def addshared(request):
    sharedevent = Shared_Event(user=request.user, Name=request.POST['Name'], Location=request.POST['Location'],
                               date_time=request.POST['DateTime'],
                               secondary_user=User.objects.get(id=request.POST['user2']))
    sharedevent.save()
    return redirect('home')


# Allows Editing of Shared Events only
def Editshared(request, Shared_Event_id):
    Prime_Event = Shared_Event.objects.get(pk=Shared_Event_id)
    secondary = User.objects.exclude(id=request.user.id)

    context = {
        "Prime_Event": Prime_Event,
        'secondary_user': secondary
    }

    return render(request, 'Edit_Shared_Event.html', context)


# Saves the Edit
def Save_Shared_Edit(request, Event_id):
    New_Event = Shared_Event.objects.get(pk=Event_id)
    New_Event.Name = request.POST['Name']
    New_Event.Location = request.POST['Location']
    New_Event.date_time = request.POST['DateTime']
    New_Event.secondary_user = User.objects.get(id=request.POST['user2'])
    New_Event.save()

    return redirect('SeeEvent')


# Allows users to commplete events they created
def shcomplete1(request, Shared_Event_id):
    Completed = Shared_Event.objects.get(pk=Shared_Event_id)
    Completed.complete = True
    Completed.save()

    return redirect('SeeEvent')


# Allows users to incommplete events they created
def shincomplete1(request, Shared_Event_id):
    inCompleted = Shared_Event.objects.get(pk=Shared_Event_id)
    inCompleted.complete = False
    inCompleted.save()

    return redirect('SeeEvent')


# Allows users to commplete events they were invited to
def shcomplete2(request, Shared_Event_id):
    Completed = Shared_Event.objects.get(pk=Shared_Event_id)
    Completed.complete2 = True
    Completed.save()

    return redirect('SeeEvent')


# Allows users to incommplete events they were invited to
def shincomplete2(request, Shared_Event_id):
    inCompleted = Shared_Event.objects.get(pk=Shared_Event_id)
    inCompleted.complete2 = False
    inCompleted.save()

    return redirect('SeeEvent')


# Allows users to delete specific events from Shared_Events
def deleteshared(request, Shared_Event_id):
    Shared_Event.objects.get(pk=Shared_Event_id).delete()

    return redirect('SeeEvent')


# Allows users to delete a single specific Event
def singledelete(request, Event_id):
    Event.objects.get(pk=Event_id).delete()

    return redirect('SeeEvent')


# Allows users to delete a single specific Shared_Event
def DeleteSharedEvent(request):
    Shared_Event.objects.filter(user=request.user).filter(complete=True).filter(complete2=True).delete()

    return redirect('SeeEvent')


# Deletes all Shared_Events of particular user
def DeleteSharedAllEvent(request):
    Shared_Event.objects.filter(user=request.user).delete()

    return redirect('SeeEvent')


def EventHistory(request):
    # Shared_Event uses multiple inheritance and so instance also appears in Event. The 2 following queries ensure only
    # events exclusive to Events is shown
    exc = Shared_Event.objects.filter(user=request.user)
    UserEvents = Event.objects.filter(user=request.user).filter(date_time__range=('2018-01-01', date.today())). \
        exclude(id__in=exc).order_by('date_time')
    # Gets all instances where current user is the one who invited others
    UserPrimaryEvents = Shared_Event.objects.filter(user=request.user).filter(
        date_time__range=('2018-01-01', date.today())).order_by('date_time')
    PrimaryCount = Shared_Event.objects.filter(user=request.user).filter(
        date_time__range=('2018-01-01', '2999-01-01')).count()
    # Gets all instances where current user is the one who is invited
    UserSecondaryEvents = Shared_Event.objects.filter(secondary_user=request.user).filter(
        date_time__range=('2018-01-01', date.today())).order_by('date_time')
    SecondaryCount = Shared_Event.objects.filter(secondary_user=request.user).filter(
        date_time__range=('2018-01-01', date.today())).count()

    context = {
        "UserEvents": UserEvents,
        "UserPrimary": UserPrimaryEvents,
        "UserSecondary": UserSecondaryEvents,
        "PrimaryCount": PrimaryCount,
        "SecondaryCount": SecondaryCount
    }
    return render(request, 'EventHistory.html', context)
