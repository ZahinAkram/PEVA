from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Classes
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    Location = models.CharField(max_length=250)
    Name = models.CharField(max_length=250)
    complete = models.BooleanField(default=False)
    # Time = models.TimeField(blank=True, null=True)
    # Date = models.DateField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=datetime.today())

    def __str__(self):
        return '%s %s %s %s ' % (self.user, self.Location, self.Name, self.complete, )


class Shared_Event(Event):
    secondary_user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete2 = models.BooleanField(default=False)

    class Meta:
        ordering = []





