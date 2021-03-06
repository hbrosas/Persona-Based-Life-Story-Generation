from django.conf.urls import url, include # Add include to the imports here
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('clientapp.urls')), # tell django to read urls.py in example app
    url(r'^', include('testingapp.urls')) # tell django to read urls.py in example app
]
