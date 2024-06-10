from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.CharField(max_length=4)
    genre = models.ManyToManyField(Genre)
    director = models.CharField(max_length=255)
    duration = models.IntegerField()  # Duration in minutes
    image = models.URLField(default='https://spotlightonline.co/wp-content/uploads/2017/03/cinema_projector.jpg')
    image_small = models.URLField(default='https://spotlightonline.co/wp-content/uploads/2017/03/cinema_projector.jpg')
    link = models.URLField()  # Link to the movie

    def __str__(self):
        return self.title




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/',default='profile_pictures/img.png', null=True, blank=True)
    favorite_movies = models.ManyToManyField(Movie, blank=True, related_name='favorited_by')
    watchlist=models.ManyToManyField(Movie,blank=True,related_name='wished_by')

    def __str__(self):
        return f'{self.user.username} Profile'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.review_text}"
