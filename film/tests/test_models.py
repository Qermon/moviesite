from django.contrib.auth.models import User
from django.test import TestCase

from film.models import Movies, Actors, MovieActor, UserProfile


class MoviesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Створення тестових даних для перевірки моделей.
        Створюються актори, фільм, зв'язок між акторами та фільмом,
        а також користувач та його профіль з улюбленими фільмами і акторами.
        """
        actor1 = Actors.objects.create(actor_names='Fred Hechinger')
        actor2 = Actors.objects.create(actor_names='Russell Crowe')
        movie = Movies.objects.create(
            title='Kraven the Hunter',
            description='A movie about Kraven the Hunter, a Marvel character.',
            release_date=2024,
            image='https://www.imdb.com/title/tt8790086/mediaviewer/rm797010177/?ref_=tt_ov_i',
            rating=0,
            rating2='8.5/10',
            directors='J.C. Chandor',
            writers='Art Marcum, Matt Holloway',
            duration='2h 7min',
            genre='Action, Adventure'
        )

        MovieActor.objects.create(movie=movie, actor=actor1, role='Chameleon')
        MovieActor.objects.create(movie=movie, actor=actor2, role='Nikolai Kravinoff')
        user = User.objects.create_user(username='usertest', password='testpassword')
        profile = UserProfile.objects.create(user=user)
        profile.favorite_movies.add(movie)
        profile.favorite_actors.add(actor1, actor2)

    def test_movie_has_actors(self):
        """
        Тестуємо, чи має фільм акторів.
        Перевіряємо, чи два актори пов'язані з фільмом.
        """
        movie = Movies.objects.get(title='Kraven the Hunter')
        actors = movie.movie_actors.all()
        self.assertEqual(actors.count(), 2)
        self.assertIn('Fred Hechinger', [actor.actor_names for actor in actors])
        self.assertIn('Russell Crowe', [actor.actor_names for actor in actors])

    def test_actor_movies(self):
        """
        Тестуємо, чи актор пов'язаний з фільмами.
        Перевіряємо, чи актор з'являється лише у цьому фільмі.
        """
        actor = Actors.objects.get(actor_names='Fred Hechinger')
        movies = actor.movies.all()
        self.assertEqual(movies.count(), 1)
        self.assertEqual(movies[0].title, 'Kraven the Hunter')

    def test_role(self):
        """
        Тестуємо роль актора у фільмі.
        Перевіряємо правильність акторської ролі в конкретному фільмі.
        """
        movie_actor = MovieActor.objects.get(role='Chameleon')
        self.assertEqual(movie_actor.actor.actor_names, 'Fred Hechinger')
        self.assertEqual(movie_actor.movie.title, 'Kraven the Hunter')

    def test_favorite_movies(self):
        """
        Тестуємо, чи користувач має улюблені фільми.
        Перевіряємо, чи фільм є улюбленим у профілі користувача.
        """
        user = User.objects.get(username='usertest')
        profile = user.profile
        favorite_movies = profile.favorite_movies.all()
        self.assertEqual(favorite_movies.count(), 1)
        self.assertEqual(favorite_movies[0].title, 'Kraven the Hunter')

    def test_favorite_actors(self):
        """
        Тестуємо, чи користувач має улюблених акторів.
        Перевіряємо, чи обидва актори є улюбленими для користувача.
        """
        user = User.objects.get(username='usertest')
        profile = user.profile
        favorite_actors = profile.favorite_actors.all()
        self.assertEqual(favorite_actors.count(), 2)
        self.assertIn('Fred Hechinger', [actor.actor_names for actor in favorite_actors])
        self.assertIn('Russell Crowe', [actor.actor_names for actor in favorite_actors])

    def test_title_label(self):
        """
        Тестуємо, чи правильна мітка для поля 'title' (назва фільму).
        Перевіряємо, чи мітка для цього поля вірна.
        """
        movie = Movies.objects.get(id=1)
        field_label = movie._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'name')

    def test_title_max_length(self):
        """
        Тестуємо, чи правильно встановлена максимальна довжина для поля 'title'.
        Перевіряємо, чи максимальна довжина назви фільму не перевищує 255 символів.
        """
        movie = Movies.objects.get(id=1)
        max_length = movie._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_release_date_nullable(self):
        """
        Тестуємо, чи може поле 'release_date' бути порожнім.
        Перевіряємо, чи це поле може бути пустим.
        """
        movie = Movies.objects.get(id=1)
        nullable = movie._meta.get_field('release_date').null
        self.assertTrue(nullable)

    def test_image_field_blank(self):
        """
        Тестуємо, чи може поле 'image' бути пустим.
        Перевіряємо, чи це поле може бути залишене порожнім.
        """
        movie = Movies.objects.get(id=1)
        blank = movie._meta.get_field('image').blank
        self.assertTrue(blank)

    def test_default_rating(self):
        """
        Тестуємо, чи правильно встановлено за замовчуванням значення рейтингу.
        Перевіряємо, чи рейтинг за замовчуванням дорівнює 0.
        """
        movie = Movies.objects.get(id=1)
        self.assertEqual(movie.rating, 0)

    def test_directors_field(self):
        """
        Тестуємо, чи правильно встановлене поле 'directors' (режисери).
        Перевіряємо, чи вказано правильне ім'я режисера.
        """
        movie = Movies.objects.get(id=1)
        self.assertEqual(movie.directors, 'J.C. Chandor')

    def test_object_name_is_title(self):
        """
        Тестуємо, чи коректно працює метод __str__ у моделі 'Movies'.
        Перевіряємо, чи виводиться назва фільму.
        """
        movie = Movies.objects.get(id=1)
        self.assertEqual(str(movie), 'Kraven the Hunter')

    def test_ordering(self):
        """
        Тестуємо, чи правильно визначено порядок сортування для фільмів.
        Перевіряємо, чи є в метаданих параметр сортування.
        """
        self.assertIn('?', Movies._meta.ordering)

    def test_genre_blank(self):
        """
        Тестуємо, чи може поле 'genre' бути порожнім.
        Перевіряємо, чи це поле може бути порожнім.
        """
        movie = Movies.objects.get(id=1)
        field_blank = movie._meta.get_field('genre').blank
        self.assertTrue(field_blank)

    def test_duration_field_nullable(self):
        """
        Тестуємо, чи може поле 'duration' бути порожнім.
        Перевіряємо, чи це поле може бути пустим.
        """
        movie = Movies.objects.get(id=1)
        nullable = movie._meta.get_field('duration').null
        self.assertTrue(nullable)

    def test_verbose_name_plural(self):
        """
        Тестуємо, чи правильно визначено множину для моделі 'Movies'.
        Перевіряємо, чи правильно встановлено значення verbose_name_plural.
        """
        verbose_name_plural = Movies._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Films')

