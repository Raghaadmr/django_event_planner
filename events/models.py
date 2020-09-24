from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Event(models.Model):
    event_organizer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=120)
    description = models.TextField()
    seats=models.PositiveIntegerField()
    date = models.DateTimeField(null= True, blank = True)
    location = models.CharField(max_length=120, null= True, blank = True)
    price = models.FloatField(null= True, blank = True)
    pic = models.ImageField(null=True, blank=True)
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})
    def __str__(self):
        return self.name

@property
def pic_url(self):
    if self.pic and hasattr(self.pic, 'url'):
        return self.pic.url
class TicketsHolder(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    tickets = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(1),
                                       MaxValueValidator(20)])
    event=models.ForeignKey(Event,on_delete=models.DO_NOTHING)
    def __str__(self):
        return "%s-%s"%(self.user,self.event)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#
#     def get_full_name(self):
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
