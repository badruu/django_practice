from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


    # This solves the error EITHER PROVIDE A URL OR DEFINE A GET_ABSOLUTE_URL METHOD IN MODELS.
    # THIS HELPS DJANGO FIND THE URL OF A MODEL object
    # To get the url for a particlar route, we need to use the reverse function.
    #Difference btn redirect & reverse:
    #  redirect will actually redirect you to a
    # specific route but reverse will simply
    # return the full URL to that route as a
    # check out SUCCESS URL
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})