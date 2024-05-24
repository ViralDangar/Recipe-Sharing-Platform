"""
URL configuration for receipeApp project.

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
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from RecipeApplication.views import recipe_detail, delete_recipe, update_recipe, create_recipe, login_page, register_page, logout_page, show_details

urlpatterns = [
    path("admin/", admin.site.urls),
    path("recipe_detail/", recipe_detail, name='recipe_detail'),
    path("delete_recipe/<id>/", delete_recipe, name='delete_recipe'),
    path("update_recipe/<id>/", update_recipe, name='update_recipe'),
    path("show_details/<id>/", show_details, name='show_details'),
    path("create_recipe/", create_recipe, name='create_recipe'),
    path("login/", login_page, name='login_page'),
    path("register/", register_page, name='register_page'),
    path("logout/", logout_page, name='logout_page'),
    # Redirect empty path to login page
    path('', lambda request: redirect('login_page')),

]
