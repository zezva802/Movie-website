from django.contrib import admin
from .models import Movie, Genre, Review, Profile

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Profile)
# Register your models here.
