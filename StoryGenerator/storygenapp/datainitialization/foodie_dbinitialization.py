# import csv, json
# from storygenapp.models import AssertionTypes, Assertions, PersonalInformation, WorkAndEducation
# from storygenapp.storygen.JSONHandler.JSONReader import JSONReader
# from storygenapp.storygen.models.AssertionModel import AssertionModel
#
#
# def populate_db():
#     populate_profile()
#     populate_workandeducation()
#     populate_assertions_types()
#     populate_assertions()
#
#
# def populate_profile():
#     with open('storygenapp\\data\\foodie\\foodie_profile.csv', newline='') as csvfile:
#         readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
#         if PersonalInformation.objects.count() != 0:
#             PersonalInformation.objects.all().delete()
#         for row in readcsv:
#             PersonalInformation.objects.create(fbid=row[0], name=row[1], gender=row[2],
#                                                birthday=row[3], address=row[4], location=row[5],
#                                                hometown=row[6], about=row[7], numfriends=row[8])
#
#
# def populate_workandeducation():
#     with open('storygenapp\\data\\foodie\\foodie_work_and_education.csv', newline='') as csvfile:
#         readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
#         if WorkAndEducation.objects.count() != 0:
#             WorkAndEducation.objects.all().delete()
#         for row in readcsv:
#             WorkAndEducation.objects.create(fbid=row[1], organization=row[2], type=row[3],
#                                             yearstarted=row[4], yearended=row[5], courseorposition=row[6])
#
#
# def populate_assertions_types():
#     with open('storygenapp\\data\\foodie\\foodie_assertions_types.csv', newline='') as csvfile:
#         readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
#         if AssertionTypes.objects.count() != 0:
#             AssertionTypes.objects.all().delete()
#         for row in readcsv:
#             user_pref = row[1]
#             type = row[2]
#             parameter = row[3]
#
#             AssertionTypes.objects.create(user_pref=user_pref, assertion_type=type, parameter=parameter)
#
#
# def populate_assertions():
#     assertions = JSONReader.readjson(self=JSONReader, filename="assertions_foodie_3.txt")
#     for a in assertions['assertions']:
#         assertion_type = a['type']
#         type_id = AssertionModel.getAssertionTypeID(self=AssertionModel, assertion_type=assertion_type)
#         user_pref = a['persona']
#         parameters = a['values']
#         param_json = json.dumps(parameters)
#         Assertions.objects.create(user_pref=user_pref, assertion_type=type_id, parameters=param_json)
#
#     # print("LENGTH", len(assertions))
#     # with open('SampleAssertions.csv', newline='') as csvfile:
#     #     readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')
#     #     if Assertions.objects.count() != 0:
#     #         Assertions.objects.all().delete()
#     #     for row in readcsv:
#     #         user_pref = row[1]
#     #         assertion_type = row[2]
#     #         parameters = row[3]
#     #
#     #         Assertions.objects.create(user_pref=user_pref, assertion_type=assertion_type, parameters=parameters)
#
