from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView, TemplateView
from film.forms import RatingForm
from film.models import Movies, Actors, Rating, UserProfile
from django.shortcuts import render


class HomeView(ListView):
    """
    HomeView - це клас на основі перегляду, який відображає список фільмів на головній сторінці.
    Він обробляє пагінацію та дозволяє фільтрувати фільми за запитом пошуку.
    """
    model = Movies
    template_name = 'index.html'
    context_object_name = 'page_obj'
    paginate_by = 5

    def get_queryset(self):
        """
        Повертає відфільтрований набір фільмів на основі запиту пошуку в запиті.
        Якщо запит на пошук відсутній, фільми повертаються в випадковому порядку.
        """
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Movies.objects.filter(title__icontains=search_query)
        else:
            return Movies.objects.prefetch_related('movie_actors').order_by('?')


class ShowMovie(DetailView):
    """
    ShowMovie - це клас на основі перегляду, який відображає деталі одного фільму.
    Також включає форму для оцінки та всі фільми для відображення пов'язаного контенту.
    """
    model = Movies
    template_name = 'moviesingle.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """
        Додає додатковий контекст для шаблону, включаючи всі фільми та форму для оцінки.
        """
        context = super().get_context_data(**kwargs)
        context['movies'] = Movies.objects.all()
        context['form'] = RatingForm()
        return context


class ShowCelebrity(DetailView):
    """
    ShowCelebrity - це клас на основі перегляду, який відображає деталі одного актора.
    Також включає всіх акторів для відображення пов'язаного контенту.
    """
    model = Actors
    template_name = 'celebritysingle.html'
    context_object_name = 'actor'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """
        Додає додатковий контекст для шаблону, включаючи всіх акторів.
        """
        context = super().get_context_data(**kwargs)
        context['actors'] = Actors.objects.all()
        return context


def movie_list(request):
    """
    Відображає список фільмів з можливістю фільтрації за запитом пошуку, жанром,
    роком випуску та рейтингом. Результати пагінуються.
    """
    search_query = request.GET.get('search', '')
    genre_query = request.GET.get('genre', '')
    year_query = request.GET.get('year', '')
    rating_min = request.GET.get('rating_min', '')
    rating_max = request.GET.get('rating_max', '')
    query = Movies.objects.prefetch_related('movie_actors')

    if search_query:
        query = query.filter(title__icontains=search_query)

    if genre_query:
        query = query.filter(genre__icontains=genre_query)

    if year_query:
        query = query.filter(release_date=year_query)

    if rating_min:
        query = query.filter(rating__gte=float(rating_min))
    if rating_max:
        query = query.filter(rating__lte=float(rating_max))

    paginator = Paginator(query, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genres = ["Action", "Comedy", "Drama", "Thriller", "Romance", "Horror", "Sci-Fi", "Fantasy", "Prison"]
    context = {
        'page_obj': page_obj,
        'genres': genres,
    }

    return render(request, 'movielist.html', context)


def celebrity_list(request):
    """
    Відображає список акторів з можливістю фільтрації за запитом пошуку.
    Результати пагінуються.
    """
    search_query = request.GET.get('search', '')

    if search_query:
        actors = Actors.objects.filter(actor_names__icontains=search_query)
    else:
        actors = Actors.objects.all()

    paginator = Paginator(actors, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'celebritylist.html', context)


@login_required
def add_rating(request, title, id):
    """
    Додає рейтинг до фільму. Якщо форма є валідною, зберігається рейтинг,
    а також оновлюється середній рейтинг фільму.
    """
    movie = get_object_or_404(Movies, id=id, title=title)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.user = request.user
            rating.save()

            avg_rating = movie.ratings.aggregate(Avg('user_rate'))['user_rate__avg']
            if avg_rating is not None:
                movie.rating = avg_rating
                movie.save()

            return redirect('movie-detail', title=movie.title, id=movie.id)
    else:
        form = RatingForm()

    return render(request, 'moviesingle.html', {'movie': movie, 'form': form})


@login_required
def user_profile(request):
    return render(request, 'userprofile.html')


@login_required
def add_to_favorite(request, movie_id):
    """
    Додає фільм до списку улюблених фільмів користувача. Якщо фільм вже в списку,
    виводиться повідомлення про це.
    """
    movie = get_object_or_404(Movies, id=movie_id)
    user_profile = request.user.profile

    if movie in user_profile.favorite_movies.all():
        messages.info(request, f'{movie.title} додано')
    else:
        user_profile.favorite_movies.add(movie)
        messages.success(request, f'{movie.title} додано')

    return redirect('movie-detail', title=movie.title, id=movie.id)


@login_required
def add_actor_favorite(request, actor_id):
    """
    Додає актора до списку улюблених акторів користувача. Якщо актор вже в списку,
    виводиться повідомлення про це.
    """
    actor = get_object_or_404(Actors, id=actor_id)
    user_profile = request.user.profile

    if actor in user_profile.favorite_actors.all():
        messages.info(request, f'{actor.actor_names} is already in favorites.')
    else:
        user_profile.favorite_actors.add(actor)
        messages.info(request, f'{actor.actor_names} added to favorites.')

    slugified_actor_name = slugify(actor.actor_names)

    return redirect('actor-detail', actor_names=slugified_actor_name, id=actor_id)


@login_required
def user_favorite_movies(request):
    """
    Відображає список улюблених фільмів та акторів користувача.
    """
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_movies = user_profile.favorite_movies.all()
    favorite_actors = user_profile.favorite_actors.all()
    return render(request, 'userfavoritelist.html', {'favorite_movies': favorite_movies}, {'favorite_actors': favorite_actors})


@login_required
def change_avatar(request):
    """
    Змінює аватар користувача, якщо зображення було вибране.
    """
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        if avatar:
            profile = request.user.profile
            profile.avatar = avatar
            profile.save()
            messages.success(request, 'Avatar updated successfully!')
        else:
            messages.error(request, 'Please select an image.')
    return redirect('user_profile')


def movie_grid(request):
    return render(request, 'moviegrid.html')


def user_favorite_grid(request):
    return render(request, 'userfavoritegrid.html')


def user_favorite_list(request):
    return render(request, 'userfavoritelist.html')


@login_required
def user_rate(request):
    """
    Відображає список фільмів, які оцінив користувач.
    """
    rated_movies = Rating.objects.filter(user=request.user).select_related('movie')
    return render(request, 'userrate.html', {'rated_movies': rated_movies})


class Landing(TemplateView):
    template_name = 'landing.html'


class Error(TemplateView):
    template_name = '404.html'


class ComingSoon(TemplateView):
    template_name = 'comingsoon.html'


