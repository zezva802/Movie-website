from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Profile, Genre
from .forms import ReviewForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q


# Create your views here.
def home(request):
    q = request.GET.get('q', '')
    selected_genres = request.GET.getlist('genres')

    movies = Movie.objects.all()

    if q:
        movies = movies.filter(Q(title__icontains=q))

    if selected_genres:
        movies = movies.filter(genre__name__in=selected_genres)

    genres = Genre.objects.all()

    context = {
        "movies": movies,
        "genres": genres,
        "selected_genres": selected_genres,
        "q": q,
    }
    return render(request, 'base/home.html', context)


def movie_page(request, pk):
    movie = Movie.objects.get(id=pk)
    reviews = movie.review_set.all().order_by('-created_at')
    user_review = None
    form = None

    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(user=request.user, movie=movie)
            form = ReviewForm(instance=user_review)
        except Review.DoesNotExist:
            form = ReviewForm()

    if request.user.is_authenticated:
        if movie in request.user.profile.favorite_movies.all():
            movie.is_favorite = True
        else:
            movie.is_favorite = False
        if movie in request.user.profile.watchlist.all():
            movie.in_watchlist = True
        else:
            movie.in_watchlist = False
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'base/movie_page.html', context)


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['review_text']
            rating = form.cleaned_data['rating']
            review, created = Review.objects.get_or_create(user=request.user, movie=movie, defaults={'rating': rating})

            if not created:
                review.review_text = text
                review.rating = rating
                review.save()
            else:
                form = ReviewForm(request.POST, instance=review)
                form.save()

            reviews = movie.review_set.all().order_by('-created_at')
            return render(request, 'base/reviews.html', {'reviews': reviews, 'movie': movie, 'form': ReviewForm()})
        else:
            return JsonResponse({"error": form.errors}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return JsonResponse({"error": "არ გაქვს უფლება წაშალო"}, status=403)

    if request.method == 'POST':
        movie = review.movie
        review.delete()
        reviews = movie.review_set.all().order_by('-created_at')
        return render(request, 'base/reviews.html', {'reviews': reviews, 'movie': movie, 'form': ReviewForm()})

    return JsonResponse({"error": "Invalid request"}, status=400)


def login_page(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "ანგარიშის სახელი არ მოიძებნა")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "არასწორი პაროლი")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def register_page(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile_picture = form.cleaned_data.get('profile_picture')

            profile = Profile.objects.create(user=user)

            if profile_picture:
                profile.profile_picture = profile_picture
                profile.save()

            login(request, user)
            messages.success(request, f'ანგარიში შექმნილია')
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def profile_page(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    list = []

    profile = Profile.objects.get(id=pk)
    reviews = Review.objects.filter(user=profile.user)
    favorites = profile.favorite_movies.all()
    watchlist = profile.watchlist.all()
    print(q)
    if q == "favorites":

        list = favorites
    elif q == "watchlist":
        list = watchlist
    elif q == "reviews":
        list = reviews
        print(list)

    context = {"favorites": favorites, "reviews": reviews, "profile": profile, "watchlist": watchlist, "list": list}
    return render(request, 'base/profile.html', context)


@login_required()
def toggle_favorite(request, pk):
    movie = Movie.objects.get(id=pk)
    if movie in request.user.profile.favorite_movies.all():
        request.user.profile.favorite_movies.remove(movie)
    else:
        request.user.profile.favorite_movies.add(movie)

    return redirect('movie-page', pk=pk)


@login_required()
def toggle_watchlist(request, pk):
    movie = Movie.objects.get(id=pk)
    if movie in request.user.profile.watchlist.all():
        request.user.profile.watchlist.remove(movie)
    else:
        request.user.profile.watchlist.add(movie)
    return redirect('movie-page', pk=pk)


@login_required
def delete_review_profile(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return JsonResponse({"error": "არ გაქვს უფლება წაშალო"}, status=403)

    if request.method == 'POST':
        profile = review.user
        review.delete()
        reviews = profile.review_set.all().order_by('-created_at')
        return render(request, 'base/profile_reviews.html', {'reviews': reviews, 'profile': profile})

    return JsonResponse({"error": "Invalid request"}, status=400)
