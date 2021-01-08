import os

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session

from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "APP_SECRET_KEY"

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="967323801663-l27svq4heurlacnt0p4679nnd8oc92ji.apps.googleusercontent.com",
    client_secret="0-2EE8CfSUro5wURZEFUa64d",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for upload in request.files.getlist("file"):
        print(upload)
        filename = upload.filename
        destination = "/".join([target, filename])
        print(destination)
        upload.save(destination)
    return render_template("amb.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)



@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['email'] = user_info['email']
     # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

if __name__ == "__main__":
    app.run(port=4555, debug=True)
