import operator
import pymysql

class PersonaIdentification:

    def identifyPersona(self, targetDB):
        conn = self.setTargetDB(targetDB)
        cursor_posts = conn.cursor()
        cursor_likes = conn.cursor()
        cursor_events = conn.cursor()

        cursor_posts.execute("""
                        SELECT label, COUNT(*) AS num 
                        FROM testingposts
                        WHERE label NOT LIKE 'No Label'
                        GROUP BY label
                        ORDER BY num DESC        
                        """)
        cursor_likes.execute("""
                        SELECT label, COUNT(*) AS num 
                        FROM testinglikes
                        WHERE label NOT LIKE 'No Label'
                        GROUP BY label
                        ORDER BY num DESC        
                        """)
        cursor_events.execute("""
                        SELECT label, COUNT(*) AS num 
                        FROM testingevents
                        WHERE label NOT LIKE 'No Label'
                        GROUP BY label
                        ORDER BY num DESC        
                        """)

        posts = dict(cursor_posts.fetchall())
        print(posts)

        likes = dict(cursor_likes.fetchall())
        print(likes)

        events = dict(cursor_events.fetchall())
        print(events)

        posts_persona = {}
        likes_events_persona = {}
        final_persona = {}

        for key, value in posts.items():
            posts_persona[key] = value * .7

        print('---------')
        print(posts_persona)

        for key, value in likes.items():
            try:
                v = value + events[key]
            except:
                v = value # dummy

            likes_events_persona[key] = v * 0.3

        for key, value in events.items():
            try:
                likes_events_persona[key]
            except:
                likes_events_persona[key] = value * 0.3

        print(likes_events_persona)


        # Combine Scores of Posts & Liked Pages and Events
        for key, value in posts_persona.items():
            try:
                final_persona[key] = value + likes_events_persona[key]
            except:
                final_persona[key] = value

        for key, value in likes_events_persona.items():
            try:
                final_persona[key]
            except:
                final_persona[key] = value


        # Print out all personas found
        print(final_persona)

        # Final Persona
        print(max(final_persona.items(), key=operator.itemgetter(1))[0])

    def setTargetDB(self, targetDB):
        '''
    Configure variable db based on persona of the person.
    1 db per person.

    DB: testingdb_sportsfan,
        testingdb_fangirl,
        testingdb_gamer,
        testingdb_foodie,
        testingdb_melancholic,
    '''

        conn = pymysql.connect(host="localhost", user="root", passwd="root", db=targetDB, use_unicode=True,
                           charset="utf8mb4")

        return conn

if __name__ == '__main__':
    PersonaIdentification().identifyPersona("testingdb_foodie")
