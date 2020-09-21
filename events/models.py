from django.db import models
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Event(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField()
    seats=models.PositiveIntegerField()
	event_organizer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(null= True, blank = True)
    location = models.CharField( null= True, blank = True)
    price = models.FloatField(null= True, blank = True)
    
	def get_absolute_url(self):
		return reverse('event-detail', kwargs={'event_id': self.id})

class TicketsHolder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
	seats = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(20)])
    event=models.ForeignKey(Event,on_delete=models.CASCADE)


class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
