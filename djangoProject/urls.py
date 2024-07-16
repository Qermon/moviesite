"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from djangoProject import settings
from film import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('moviesingle/', views.movie_single, name='movie_single'),
    path('moviegrid/', views.movie_grid, name='movie_grid'),
    path('movielist/', views.movie_list, name='movie_list'),
    path('celebritylist/', views.celebrity_list, name='celebrity_list'),
    path('celebritysingle/', views.celebrity_single, name='celebrity_single'),
    path('userprofile./', views.user_profile, name='user_profile'),
    path('bloglist/', views.blog_list, name='blog_list'),
    path('userfavoritegrid/', views.user_favorite_grid, name='user_favorite_grid'),
    path('userfavoritelist/', views.user_favorite_list, name='user_favorite_list'),
    path('userrate/', views.user_rate, name='user_rate'),
    path('landing/', views.landing, name='landing'),
    path('404/', views.er_404, name='404'),
    path('comingsoon/', views.coming_soon, name='comingsoon'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)