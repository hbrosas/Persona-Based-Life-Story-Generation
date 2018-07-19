from django.http import JsonResponse
from clientapp.module1 import PersonaIdentification

def identify_persona(request):
    print("IM HERE IN IDENTIFYING PERSONA!!!!!!!!")
    user = request.POST.get('targetDB', None).replace(" ", "")
    print('TARGETDB:', user)

    persona_identification = PersonaIdentification.PersonaIdentification(user)
    persona_identification.run();
    personas = persona_identification.identifyPersona();

    # dummy data
    data = {
        'success': '123'
    }

    return JsonResponse(personas)