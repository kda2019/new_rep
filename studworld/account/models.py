from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class UserPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    date = models.DateField(default=timezone.now, blank=True)
    body = models.TextField()

    def __str__(self):
        return 'Post for user {}'.format(self.user.username)

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_event = models.DateField(default=timezone.now)

    def __str__(self):
        return 'Event for user {}'.format(self.user.username)