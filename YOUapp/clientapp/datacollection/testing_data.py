from django.http import JsonResponse
import json
import MySQLdb

'''
Attached on index.html if collecting testing data.
'''

def store_testing_data(request):
    print('STORE TESTING DATA')

    personalInfo = request.POST.get('personalInfo', None)
    ''' DEPRACATED: education = request.POST.get('education', None)
    work = request.POST.get('work', None) '''
    posts = request.POST.get('posts', None)
    likes = request.POST.get('likes', None)
    events = request.POST.get('events', None)
    print("NYAAAAAARUUUUUUUUT", events)

    personalInfoDict = json.loads(personalInfo)
    ''' DEPRACATED:
    try:
        educationArray = json.loads(education)
    except:
        educationArray = None

    try:
        workArray = json.loads(work)
    except:
        workArray = None
    '''

    postsArray = json.loads(posts)[0]
    likesArray = json.loads(likes)[0]

    if(events != '[]'):
        eventsArray = json.loads(events)[0]         # IN THE CASE OF NO EVENTS

    print('personalInfo: ', personalInfoDict['id'])
    print('Total Posts: ', len(postsArray))
    print('Total Likes: ', len(likesArray))
    if (events != '[]'):
        print('Total Events: ', len(eventsArray))   # IN THE CASE OF NO EVENTS


    targetDB = 'thesis_testing_db'
    conn = setTargetDB(targetDB)                    #change accordingly
    tableName = personalInfoDict['name'].replace(" ", "")
    createTables(conn, targetDB, tableName)

    print('CREATED TABLES...')
    store_profile(personalInfoDict, conn)
    # if(educationArray != None):
    #     store_education(educationArray, conn)
    # if(workArray != None):
    #     store_work(workArray, conn)
    store_testing_posts(postsArray, conn, tableName)
    store_testing_likes(likesArray, conn, tableName)
    if (events != '[]'):
        store_testing_events(eventsArray, conn, tableName)      # IN THE CASE OF NO EVENTS
    print('STORED FB DATA TO DB...')

    # dummy data
    data = {
        'success': '123'
    }

    return JsonResponse(data)

def setTargetDB(targetDB):
    '''
    Configure variable db based on persona of the person.
    1 db per person.

    DB: testingdb_sportsfan,
        testingdb_fangirl,
        testingdb_gamer,
        testingdb_foodie,
        testingdb_melancholic,
    '''

    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db=targetDB, use_unicode=True,
                           charset="utf8mb4")

    return conn


def createTables(conn, targetDB, tableName):
    cursor = conn.cursor()

    sql = "CREATE TABLE " + targetDB + "." + tableName + "_posts"
    sql += ''' 
            (
                id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                fbid VARCHAR(50) NOT NULL,
                post LONGTEXT NOT NULL,
                updated_time LONGTEXT NOT NULL,
                label VARCHAR(50)
            );
    '''

    sql += "CREATE TABLE " + targetDB + "." + tableName + "_likes"
    sql += '''
            (
                id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                fbid VARCHAR(50) NOT NULL,
                liked_page LONGTEXT NOT NULL,
                category LONGTEXT NOT NULL,
                label VARCHAR(50)
            );   
    '''

    sql += "CREATE TABLE " + targetDB + "." + tableName + "_events"
    sql += '''
            (
                id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                fbid VARCHAR(50) NOT NULL,
                event LONGTEXT NOT NULL,
                label VARCHAR(50) 
            );
    '''
    cursor.execute(sql)

def store_profile(personalInfo, conn):

    fbid = personalInfo['id']
    name = personalInfo['name']
    try:
        gender = personalInfo['gender']
    except:
        gender = None

    try:
        birthday = personalInfo['birthday']
    except:
        birthday = None

    try:
        address = personalInfo['address']
    except:
        address = None

    try:
        location = personalInfo['location']
    except:
        location = None

    try:
        hometown = personalInfo['hometown']
    except:
        hometown = None

    try:
        about = personalInfo['about']
    except:
        about = None

    try:
        friends = personalInfo['friends']
    except:
        friends = None

    cursor = conn.cursor()
    cursor.execute(
        ("INSERT INTO profile VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"),
        (fbid, name, gender, birthday, address, location, hometown, about, int(friends))
    )

    conn.commit()
    print('Profile successfuly stored in DB!')


def store_education(educations, conn):
    for education in educations:
        fbid = education['id']
        try:
            organization = education['school']['name']
        except:
            organization = None

        try:
            type = education['type']
        except:
            type = None

        try:
            yearended = education['year']['name']           #year started cannot be extracted
        except:
            yearended = None

        try:
            courseorposition = ''
            for index, concentration in enumerate(education[concentration]):
                courseorposition += concentration['name']

                if(index != len(education[concentration]) - 1):
                    courseorposition += ' ,'                #separate by commas
        except:
            courseorposition = None

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO work_and_education(fbid, organization, type, yearended, courseorposition) VALUES(%s,%s,%s,%s,%s)"),
            (fbid, organization, type, yearended, courseorposition)
        )
        conn.commit()

    print('Education successfully stored in DB!')

def store_work(works, conn):
    for work in works:
        fbid = work['id']
        try:
            organization = work['employer']['name']
        except:
            organization = None

        type = 'Work'                           #pre-defined

        try:
            yearstarted = work['start_date']
        except:
            yearstarted = None

        try:
            yearended = work['end_date']
        except:
            yearended = None

        try:
            courseorposition = work['position']['name']
        except:
            courseorposition = None

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO work_and_education(fbid, organization, type, yearstarted, yearended, courseorposition) VALUES(%s,%s,%s,%s,%s,%s)"),
            (fbid, organization, type, yearstarted, yearended, courseorposition)
        )
        conn.commit()

    print('Work successfully stored in DB!')

def store_testing_posts(posts, conn, tableName):
    for post in posts:
        fbid = post['id']

        try:
            story = post['story']
        except:
            story = ''

        try:
            description = post['description']
        except:
            description = ''

        try:
            message = post['message']
        except:
            message = ''

        text_post = ''
        space = '. '

        if(story != ''): #e.g. Danica updated her... Danica is at... Danica shared... Danica added...
            text_post += story

        if (description != ''):
            text_post += " The post says " + description + space

        if (message != '' and (description != '' or story!='')):
            text_post += "He says " + message + space
        elif (message != ''):
            text_post += message

        updated_time = post['updated_time']

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO " + tableName + "_posts(fbid, post, updated_time) VALUES(%s,%s,%s)"),
            (fbid, text_post, updated_time)
        )
        conn.commit()

        #p = TrainingPosts(fbid=fbid, post=text_post, updated_time=updated_time)
        #p.save()

    print('Text-based posts successfully stored in DB')

def store_testing_likes(likes, conn, tableName):
    for like in likes:
        fbid = like['id']

        try:
            name = like['name']
        except:
            name = ''

        try:
            category = like['category']
        except:
            category = ''

        try:
            about = like['about']
        except:
            about = ''

        try:
            description = like['description']
        except:
            description = ''

        he_likes = 'He likes '
        space = '. '

        liked_page = he_likes + name + space + about + space + description

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO " + tableName + "_likes(fbid, category, liked_page) VALUES(%s,%s,%s)"),
            (fbid, category, liked_page)
        )
        conn.commit()

    print('Liked pages successfully stored in DB')

        #l = TrainingLikes(fbid=fbid, category=category, liked_page=liked_page)
        #l.save()

def store_testing_events(events, conn, tableName):
    for event in events:
        fbid = event['id']

        try:
            name = event['name']
        except:
            name = ''

        try:
            description = event['description']
        except:
            description = ''

        try:
            rsvp_status = event['rsvp_status']
        except:
            rsvp_status = ''

        he_rsvp = 'He is ' + rsvp_status + ' in '        #in or at? -- attending, unsure, interested
        space = '. '

        #e.g. He is attending in Empowher. Empowher is blablabla.

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO " + tableName + "_events(fbid, event) VALUES(%s,%s)"),
            (fbid, he_rsvp + name + space + description)
        )
        conn.commit()

    print('Events successfully stored in DB')
        #e = TrainingEvents(fbid=fbid, event=he_rsvp + name + space + description)
        #e.save()