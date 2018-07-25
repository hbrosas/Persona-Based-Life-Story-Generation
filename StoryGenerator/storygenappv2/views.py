# djangotemplates/example/views.py
from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from storygenappv2.storygen.driver import Driver
from storygenappv2.models import PersonalInformation
from datetime import date
from datetime import datetime

# from weasyprint import HTML
# from django.http import HttpResponse

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

context = {}

# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "index.html"
class LoadPageView(TemplateView):
    template_name = "loading.html"

class ProfilePageView(TemplateView):
    template_name = "profile-format.html"

def pdf(request):
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
    context = {'overview': overview, 'story': story,
               'profile': {'name': profile.name, 'birthday': birthday, 'numfriends': profile.numfriends,
                           'address': address}}

    template = get_template("profile-format.html")
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "personastory_%s.pdf" % ("12341231")
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    else:
        return HttpResponse("Error Rendering PDF", status=400)

    # html_template = get_template('profile-format.html')
    # template = html_template.render(context)
    # pdf_file = HTML(string=template).write_pdf()
    # response = HttpResponse(pdf_file, content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="persona-story.pdf"'
    #
    # return response

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



