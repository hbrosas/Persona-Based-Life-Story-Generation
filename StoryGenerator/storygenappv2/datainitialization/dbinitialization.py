import csv, json
from storygenappv2.models import AssertionTypes, Assertions, PersonalInformation
from storygenappv2.storygen.JSONHandler.JSONReader import JSONReader
from storygenappv2.storygen.models.AssertionModel import AssertionModel


def populate_db(self):
    # populate_profile(self)
    # populate_workandeducation(self)
    populate_assertions_types(self)
    populate_assertions(self)


# def populate_profile(self):
#     with open('storygenappv2\\data\\Sean Bravo\\profile.csv', newline='') as csvfile:
#         readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
#         if PersonalInformation.objects.count() != 0:
#             PersonalInformation.objects.all().delete()
#         for row in readcsv:
#             PersonalInformation.objects.create(fbid=row[0], name=row[1], gender=row[2],
#                                                birthday=row[3], address=row[4], location=row[5],
#                                                hometown=row[6], about=row[7], numfriends=row[8])


# def populate_workandeducation():
#     with open('storygenappv2\\data\\fangirl\\fangirl_work_and_education.csv', newline='') as csvfile:
#         readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
#         if WorkAndEducation.objects.count() != 0:
#             WorkAndEducation.objects.all().delete()
#         for row in readcsv:
#             WorkAndEducation.objects.create(fbid=row[1], organization=row[2], type=row[3],
#                                             yearstarted=row[4], yearended=row[5], courseorposition=row[6])


def populate_assertions_types(self):
    with open('storygenappv2\\data\\Assertion_Types.csv', newline='') as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        if AssertionTypes.objects.count() != 0:
            AssertionTypes.objects.all().delete()
        for row in readcsv:
            user_pref = row[1]
            type = row[2]
            parameter = row[3]

            AssertionTypes.objects.create(user_pref=user_pref, assertion_type=type, parameter=parameter)


def populate_assertions(self):
    assertions = JSONReader.readjson(self=JSONReader, filename="storygenappv2\\data\\Sean Bravo\\assertions_sean_bravo.txt")
    for a in assertions['assertions']:
        try:
            assertion_type = a['type']
        except:
            assertion_type = a['TYPE']
        if assertion_type.lower() == 'likes':
            user_pref = 'Likes'
        elif assertion_type.lower() == 'events':
            user_pref = 'Events'
        else:
            user_pref = a['persona']

        type_id = AssertionModel.getAssertionTypeID(self=AssertionModel, assertion_type=assertion_type, user_pref=user_pref)

        try:
            parameters = a['values']
        except:
            parameters = a['VALUES']
        param_json = json.dumps(parameters)
        Assertions.objects.create(user_pref=user_pref, assertion_type=type_id, parameters=param_json)