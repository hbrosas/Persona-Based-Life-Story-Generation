import pandas as pd
import MySQLdb
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
import pickle
import operator
from clientapp.module1 import Normalizer

class PersonaIdentification:
    def __init__(self, user):
        self.user = user
        self.targetDB = 'thesis_testing_db'
        self.dir = 'clientapp/module1/'
        self.bestmodel = self.dir + 'pac_ngrams2_model.pkl'
        self.vectorizer = self.dir + 'tfidf_vectorizer_12.pkl'
        self.test_posts = ''
        self.test_likes = ''
        self.test_events = ''
        self.labels = ['No Label', 'The Fangirl/Fanboy', 'The Foodie', 'The Gamer', 'The Melancholic', 'The Sports Fanatic']
        self.personas = {}

    def setTargetDB(self):
        '''
        Directs to the the db of the testing users.
        '''

        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db=self.targetDB, use_unicode=True,
                               charset="utf8mb4")

        return conn

    def create_persona_table(self, conn):
        cursor = conn.cursor()
        sql = "CREATE TABLE " + self.targetDB + "." + self.user + "_personas"
        sql += ''' 
                (
                    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                    label VARCHAR(50) NOT NULL,
                    score DOUBLE NOT NULL,
                    percentage DOUBLE NOT NULL
                );
        '''

        cursor.execute(sql)

    def load_data(self):
        conn = self.setTargetDB()
        cursor_posts = conn.cursor()
        cursor_likes = conn.cursor()
        cursor_events = conn.cursor()

        cursor_posts.execute("""
                        SELECT post
                        FROM """ + self.user + """_posts;
                        """)

        self.test_posts = ([i[0] for i in cursor_posts.fetchall()])
        cursor_likes.execute("""
                        SELECT liked_page
                        FROM """ + self.user + """_likes;
                        """)
        self.test_likes = [i[0] for i in cursor_likes.fetchall()]
        cursor_events.execute("""
                        SELECT event
                        FROM """ + self.user + """_events;
                        """)

        self.test_events = [i[0] for i in cursor_events.fetchall()]
        # print(len(self.test_texts))
        # print(self.test_texts)

    def preprocess(self, train_texts):
        normalizer = Normalizer.Normalizer()
        return normalizer.clean_text(train_texts)

    def machine_learning(self, model_filename, test_texts):
        vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(self.vectorizer, "rb")))

        model = joblib.load(model_filename).predict(vectorizer.fit_transform(test_texts))
        model_predictions = model
        return model_predictions

    def str_join(*args):
        return ''.join(map(str, args))

    def append_labels(self, conn, table, num_labels):

        for i, num_label in enumerate(num_labels):
            cursor = conn.cursor()
            print('Num_Label', num_label)
            cursor.execute('''
                    UPDATE %s 
                    SET label = '%s'
                    WHERE id = %s;
                ''' % (table, self.labels[num_label], i+1))
            conn.commit()

    def store_personas(self, conn, personas):
        for key, value in personas.items():
            totalsum = sum(personas.values())
            cursor = conn.cursor()

            percentage = (value/totalsum) * 100

            self.personas[key] = percentage
            cursor.execute(
                (
                "INSERT INTO " + self.user + "_personas (label, score, percentage) VALUES(%s, %s, %s)"),
                (key, value, percentage)
            )

            conn.commit()

    def get_actual_labels(self,  filename):
        test_actual_labels = []
        dataset = pd.read_excel(filename, sheet_name="Posts")
        test_actual_labels.extend(dataset['label'].apply(self.labels.index).tolist())
        dataset = pd.read_excel(filename, sheet_name="Likes")
        test_actual_labels.extend(dataset['label'].apply(self.labels.index).tolist())
        dataset = pd.read_excel(filename, sheet_name="Events")
        test_actual_labels.extend(dataset['label'].apply(self.labels.index).tolist())

        return test_actual_labels

    def evaluate(self, actual_labels,predicted_labels):
        print(classification_report(actual_labels,predicted_labels))

        print("Accuracy Rate:", accuracy_score(actual_labels, predicted_labels))

    def identifyPersona(self):
        conn = self.setTargetDB()
        self.create_persona_table(conn)
        cursor_posts = conn.cursor()
        cursor_likes = conn.cursor()
        cursor_events = conn.cursor()

        cursor_posts.execute("""
                        SELECT label, COUNT(*) AS num 
                        FROM """ + self.user +"""_posts
                        GROUP BY label
                        ORDER BY num DESC        
                        """)
        cursor_likes.execute("""
                        SELECT label, COUNT(*) AS num 
                        FROM """ + self.user +"""_likes
                        GROUP BY label
                        ORDER BY num DESC        
                        """)
        cursor_events.execute("""
                        SELECT label, COUNT(*) AS num 
                        FROM """ + self.user +"""_events
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

        # Convert to percentages
        total = sum(final_persona.values())
        for key, value in final_persona.items():
            final_persona[key] = (value/total)*100

        # Print out all personas found
        print('FINAL PERSONAS:')
        print(final_persona)
        self.store_personas(conn, final_persona)

        # Final Persona
        # print(max(final_persona.items(), key=operator.itemgetter(1))[0])
        print('Online Persona:', self.identify_online_persona(final_persona))
        return self.personas

    def identify_online_persona(self, final_persona):
        online_persona = ''
        max_percentage = 0
        for key, value in final_persona.items():
            if value > max_percentage and key != 'No Label':
                max_percentage = value
                online_persona = key

        return online_persona

    def run(self):
        test_predicted_labels = []
        testing_dataset_filename = "Testing Dataset/(FANGIRL) Testing.xlsx"

        '''
        1.) Get the posts, likes and events of the user in the DB.
            Initializes the test_posts, test_likes, test_events.
            Creates a persona table
        '''
        self.load_data()
        conn = self.setTargetDB()
        print('Model: ', self.bestmodel)

        '''
        2.) Pre-process and feed it into the best model to get predicted
        '''

        self.test_posts = self.preprocess(self.test_posts)
        predictions = self.machine_learning(self.bestmodel, self.test_posts)
        # print('Predictions:', predictions)
        self.append_labels(conn, self.user + '_posts', predictions)
        test_predicted_labels.extend(predictions)

        # print('LIKED PAGES:', len(self.test_likes))
        self.test_likes = self.preprocess(self.test_likes)
        predictions = self.machine_learning(self.bestmodel, self.test_likes)
        # print('Predictions:', predictions)
        self.append_labels(conn, self.user + '_likes', predictions)
        test_predicted_labels.extend(predictions)

        if(len(self.test_events) != 0): #IN CASE WHEN THERE ARE NO EVENTS
            print('EVENTS:', len(self.test_events))
            self.test_events = self.preprocess(self.test_events)
            predictions = self.machine_learning(self.bestmodel, self.test_events)
            # print('Predictions:', predictions)
            self.append_labels(conn, self.user + '_events', predictions)
            test_predicted_labels.extend(predictions)

        print('Test texts: ', len(test_predicted_labels))
        #self.evaluate(self.get_actual_labels(testing_dataset_filename), test_predicted_labels)











