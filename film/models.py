from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    release_date = models.TextField(null=True)
    image = models.URLField()
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0)
    rating2 = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
