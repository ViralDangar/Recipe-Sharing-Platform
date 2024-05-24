from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.


@login_required(login_url="/login/")
def recipe_detail(request):
    searchData = ''
    searchCategory = -1
    if request.method == "POST":
        data = request.POST
        searchData = request.POST
        searchCategory = data.get('category')

        # return redirect('/recipe_detail/')
    queryset = Recipe.objects.all().order_by('-id')
    querysetReview = Review.objects.all().order_by('-created_at')
    # recipe = get_object_or_404(Recipe, id=1)
    # reviews = Review.objects.filter(recipe=recipe).order_by('-created_at')
    # total_reviews = reviews.count()

    from django.db.models import Q

    if searchData:
        search_query = Q(title__icontains=searchData['search']) | Q(
            ingredients__icontains=searchData['search'])
        queryset = queryset.filter(search_query)

    if searchCategory != -1:
        queryset = queryset.filter(category__icontains=searchCategory)

    for r in queryset:
        recipe = get_object_or_404(Recipe, id=r.id)
        reviews = Review.objects.filter(recipe=recipe).order_by('-created_at')
        sum_ratings = reviews.aggregate(Sum('rating'))['rating__sum']

        if (sum_ratings is not None):
            r.avg = round((sum_ratings/reviews.count()), 1)

    for q in queryset:
        if (q.category) == 1:
            q.category = 'Starters'
        if (q.category) == 2:
            q.category = 'Main Course'
        if (q.category == 3):
            q.category = 'Dessert'

    context = {'recipes': queryset}
    return render(request, 'recipe_detail.html', context)


@login_required(login_url="/login/")
def create_recipe(request):
    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        ingredients = data.get('ingredients')
        preparation_steps = data.get('preparation_steps')
        cooking_time = data.get('cooking_time')
        serving_size = data.get('serving_size')
        category = data.get('category')
        user = request.user

        Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            preparation_steps=preparation_steps,
            cooking_time=cooking_time,
            serving_size=serving_size,
            category=category,
            user=user
        )
        return redirect('/recipe_detail/')
    return render(request, 'add_recipe.html')


@login_required(login_url="/login/")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipe_detail/')


@login_required(login_url="/login/")
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    print('category', queryset.category)

    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        ingredients = data.get('ingredients')
        preparation_steps = data.get('preparation_steps')
        cooking_time = data.get('cooking_time')
        serving_size = data.get('serving_size')
        category = data.get('category')
        user = request.user

        queryset.title = title
        queryset.description = description
        queryset.ingredients = ingredients
        queryset.preparation_steps = preparation_steps
        queryset.cooking_time = cooking_time
        queryset.serving_size = serving_size
        queryset.category = category
        queryset.user = user

        queryset.save()
        return redirect('/recipe_detail/')
    context = {'recipe': queryset}
    return render(request, 'update_recipe.html', context)


@login_required(login_url="/login/")
def show_details(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "POST":
        data = request.POST
        rating = data.get('rating')
        comment = data.get('comment')
        user = request.user

        Review.objects.create(
            user=user,
            recipe=recipe,
            comment=comment,
            rating=rating
        )
    querysetReview = Review.objects.all().order_by('-created_at')
    queryset = Recipe.objects.get(id=id)
    context = {'recipe': queryset, 'reviews': querysetReview}
    return render(request, 'show_details.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipe_detail/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')

        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        print(user)
        user.save()
        messages.info(request, "Account created successfully!")
        return redirect('/register/')
    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')
