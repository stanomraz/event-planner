from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Event, Location, Tag, Registration
from .forms import EventForm, LocationForm, TagForm, SignUpForm


def is_organizer(user):
    return user.is_staff


# HOME
def home(request):
    events = Event.objects.all().order_by('date')[:6]
    return render(request, 'events/home.html', {'events': events})


# EVENT VIEWS
# --- FILIP: CRUD pre Event ---
def event_list(request):
    events = Event.objects.all().order_by('date')

    # Filtrovanie
    # --- FILIP: Filtrovanie eventov podľa dátumu, mesta, tagu, organizátora ---
    date = request.GET.get('date')
    city = request.GET.get('city')
    tag = request.GET.get('tag')
    organizer = request.GET.get('organizer')

    if date:
        events = events.filter(date=date)
    if city:
        events = events.filter(location__city__icontains=city)
    if tag:
        events = events.filter(tags__name__icontains=tag)
    if organizer:
        events = events.filter(organizer__username__icontains=organizer)

    tags = Tag.objects.all()
    return render(request, 'events/event_list.html', {'events': events, 'tags': tags})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event, status='confirmed').exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'spots_left': event.spots_left(),
    })


@login_required
@user_passes_test(is_organizer)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()
            messages.success(request, 'Event vytvorený!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Nový event'})


@login_required
@user_passes_test(is_organizer)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event upravený!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Upraviť event'})


@login_required
@user_passes_test(is_organizer)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event vymazaný!')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'object': event, 'type': 'event'})


# LOCATION VIEWS
@login_required
@user_passes_test(is_organizer)
# --- FILIP: CRUD pre Location ---
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'events/location_list.html', {'locations': locations})


@login_required
@user_passes_test(is_organizer)
def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Miesto vytvorené!')
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Nové miesto'})


@login_required
@user_passes_test(is_organizer)
def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Miesto upravené!')
            return redirect('location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Upraviť miesto'})


@login_required
@user_passes_test(is_organizer)
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Miesto vymazané!')
        return redirect('location_list')
    return render(request, 'events/event_confirm_delete.html', {'object': location, 'type': 'miesto'})


# TAG VIEWS
@login_required
@user_passes_test(is_organizer)
# --- FILIP: CRUD pre Tag ---
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'events/tag_list.html', {'tags': tags})


@login_required
@user_passes_test(is_organizer)
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag vytvorený!')
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Nový tag'})


@login_required
@user_passes_test(is_organizer)
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag upravený!')
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Upraviť tag'})


@login_required
@user_passes_test(is_organizer)
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag vymazaný!')
        return redirect('tag_list')
    return render(request, 'events/event_confirm_delete.html', {'object': tag, 'type': 'tag'})


# REGISTRATION VIEWS
@login_required
# --- ALEX: Registrácia používateľa na event ---
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.spots_left() <= 0:
        messages.error(request, 'Event je plný!')
        return redirect('event_detail', pk=pk)
    registration, created = Registration.objects.get_or_create(user=request.user, event=event)
    if not created and registration.status == 'confirmed':
        messages.warning(request, 'Už si registrovaný!')
    else:
        registration.status = 'confirmed'
        registration.save()
        messages.success(request, 'Úspešne si sa zaregistroval!')
    return redirect('event_detail', pk=pk)


@login_required
# --- ALEX: Odhlásenie používateľa z eventu ---
def event_unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = Registration.objects.filter(user=request.user, event=event).first()
    if registration:
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, 'Odhlásenie úspešné!')
    return redirect('event_detail', pk=pk)


@login_required
@user_passes_test(is_organizer)
def event_participants(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = Registration.objects.filter(event=event, status='confirmed')
    return render(request, 'events/event_participants.html', {'event': event, 'registrations': registrations})


# AUTH VIEWS

# --- ALEX: Login / Logout funkcionalita ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Zlé meno alebo heslo!')
    return render(request, 'events/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'events/signup.html', {'form': form})