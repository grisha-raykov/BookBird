"""
URL configuration for BookBird project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

from apps.core import views
from apps.core.views import IndexView


urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path("admin/", admin.site.urls),
    path(
        "authors/",
        include("apps.authors.urls"),
    ),
    path(
        "publications/",
        include("apps.publications.urls"),
    ),
    path(
        "titles/",
        include("apps.titles.urls"),
    ),  # Keep titles URLs for detail views
    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),
    path(
        "lists/",
        include("apps.lists.urls"),
    ),
    path(
        "friends/",
        include("apps.friends.urls"),
    ),
    path(
        "search/",
        views.GlobalSearchView.as_view(),
        name="search",
    ),
    path(
        "reviews/",
        include("apps.reviews.urls"),
    ),
    path(
        "groups/",
        include("apps.groups.urls"),
    ),
    path(
        "awards/",
        include("apps.awards.urls"),
    ),
]
