class FileWriter:

    def __init__(self, overview, userpreferences, userpref_story):
        self.overview = overview
        self.userpreferences = userpreferences
        self.userpref_story = userpref_story

    def save(self):
        """
        saves the story output in a text file
        """
        file = open("foodie_demo_results.txt", "w+")

        file.write(self.overview)
        if len(self.userpref_story) != 0:
            for u in range(len(self.userpreferences)):
                file.write(self.userpreferences[u] + "\n")
                file.write(self.userpref_story[u])

        file.close()
