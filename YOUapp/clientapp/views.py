# djangotemplates/example/views.py
from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView

# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "index.html"

class LoadPageView(TemplateView):
    template_name = "loading.html"

class Module1PageView(TemplateView):
    template_name = "module1_loading.html"

class ProfilePageView(TemplateView):
    template_name = "profile.html"
