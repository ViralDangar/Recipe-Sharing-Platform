from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # def __str__(self):
    #     return self.name


class Recipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    preparation_steps = models.TextField()
    cooking_time = models.FloatField(default=0.0)
    serving_size = models.PositiveIntegerField(help_text='Number of servings')
    category = models.SmallIntegerField()

    # def __str__(self):
    #     return self.title


class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'Review by {self.user.username} for {self.recipe.title}'
