
from flask import Flask, render_template, Response
from main import generate_video




app = Flask(__name__)


@app.route("/")  ## --> decorator
def index():
    return render_template("home.html")

@app.route("/about")  ## --> decorator
def about():
    return render_template("about.html")

@app.route("/pro")  ## --> decorator
def project():
    return render_template("project.html")

@app.route("/work")  ## --> decorator
def work():
    return render_template("workflow.html")

@app.route("/cam")  ## --> decorator
def cam():
    return render_template("camera.html")

@app.route("/video")  ## --> decorator
def video():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/info")  ## --> decorator
def info():
    return render_template("contact.html")

    

## to run your app
if __name__ =="__main__":
    app.run(debug=True)