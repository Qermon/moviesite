from django.shortcuts import render

from film.models import Movie


# Create your views here.
def home(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})


def movie_single(request):
    return render(request, 'moviesingle.html')


def movie_grid(request):
    return render(request, 'moviegrid.html')

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movielist.html', {'movies': movies})

def celebrity_list(request):

    return render(request, 'celebritylist.html')

def user_profile(request):
    return render(request, 'userprofile.html')

def blog_list(request):
    return render(request, 'bloglist.html')

def celebrity_single(request):
    return render(request, 'celebritysingle.html')

def user_favorite_grid(request):
    return render(request, 'userfavoritegrid.html')

def user_favorite_list(request):
    return render(request, 'userfavoritelist.html')

def user_rate(request):
    return render(request, 'userrate.html')

def landing(request):
    return render(request, 'landing.html')

def er_404(request):
    return render(request, '404.html')

def coming_soon(request):
    return render(request, 'comingsoon.html')