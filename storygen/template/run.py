from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def loadhtml(overview, userpref_dict):
    return render_template('profile.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)
