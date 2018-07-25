"""StoryGenerator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import url
from storygenapp import views as views
from storygenappv2 import views as views2
from storygenapp.datainitialization import dbinitialization, foodie_dbinitialization
from storygenappv2.datainitialization import dbinitialization as dbinitializationv2, \
    foodie_dbinitialization as foodie_dbinitializationv2, fangirl_dbinitialization as fangirl_dbinitializationv2, \
    sportsfanatic_dbinitialization as sportsfan_dbinitializationv2, gamer_dbinitialization as gamer_dbinitializationv2
from storygenappv2.datainitialization import categories_dbinitialization
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', views2.HomePageView.as_view(), name='home'), # Notice the URL has been named
    # url(r'^$', csrf_exempt(dbinitializationv2.populate_db()), name='load_data'),
    # url(r'^$', csrf_exempt(foodie_dbinitializationv2.populate_db()), name='load_data'),
    # url(r'^$', csrf_exempt(categories_dbinitialization.populate_categories()), name='load_data'),
    # url(r'^loading/$', views.LoadPageView.as_view(), name='loading'),
    url(r'^profile/$', views2.profile, name='profile'),
    url(r'^savestory/$', views2.pdf, name='pdf'),
]