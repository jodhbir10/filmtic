from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length = 50, null=True, blank=True)

class Review(models.Model):
    movie_title = models.CharField(max_length=100)
    rating = models.IntegerField()
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie_title} - {self.rating}/5 by {self.user.username}"
