# djangotemplates/example/views.py
from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from storygenapp.storygen.driver import Driver
from storygenapp.models import PersonalInformation
from datetime import date
from datetime import datetime

# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "index.html"

class LoadPageView(TemplateView):
    template_name = "loading.html"

class ProfilePageView(TemplateView):
    template_name = "profile.html"

def profile(request):
    Driver.init(Driver)
    overview = Driver.overview
    userpreferences = Driver.userpreferences
    userpref_story = Driver.userpref_story
    story = []
    for i in range(len(userpreferences)):
        elem = [userpreferences[i], userpref_story[i]]
        story.append(elem)

    profile = PersonalInformation.objects.get(id=1)

    birthdayformat = datetime.strptime(profile.birthday, '%m/%d/%Y').date()
    birthday = birthdayformat.strftime("%B %d %Y")
    address = ''
    if profile.address is not None and profile.address != '':
        print("ADDRESS")
        address = profile.address
    elif profile.address == '' and profile.hometown is not None and profile.hometown != '':
        print("HOMETOWN")
        address = profile.hometown
    else:
        print("LOCATION")
        if profile.location is not None and profile.location != '':
            address = profile.location

    print(story)
    context = {'overview':overview, 'story':story,
               'profile':{'name': profile.name, 'birthday':birthday, 'numfriends':profile.numfriends,
                          'address':address}}

    return render(request, 'profile-format.html', context)



