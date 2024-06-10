from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('moviepage/<str:pk>', views.movie_page, name="movie-page"),
    path('add-review/<str:movie_id>/', views.add_review, name='add-review'),
    path('delete-review/<str:review_id>/', views.delete_review, name='delete-review'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_page, name='register'),
    path('profile/<str:pk>', views.profile_page,name='profile-page'),
    path('toggle-favorite/<str:pk>', views.toggle_favorite,name='toggle-favorite'),
    path('toggle-watchlist/<str:pk>', views.toggle_watchlist,name='toggle-watchlist'),
    path('delete-review-profile/<str:review_id>/', views.delete_review_profile, name='delete-review-profile'),
    path('update-user', views.update_user, name="update-user")

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
