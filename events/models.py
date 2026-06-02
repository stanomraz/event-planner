from django.db import models
from django.contrib.auth.models import User

# --- FILIP: Location model ---
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.city}"

# --- FILIP: Tag model ---
class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# --- FILIP: Event model so vzťahmi na Location, User a Tag ---
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    capacity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    # --- ALEX: Kontrola kapacity udalosti ---
    def spots_left(self):
        registered = self.registrations.filter(status='confirmed').count()
        return self.capacity - registered

# --- ALEX: Registration model (M:N vzťah medzi User a Event) ---
class Registration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    date_registered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"