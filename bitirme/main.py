
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('landingPage.html', branding = False)

def main():
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run()

if __name__=="__main__":
    main(host='127.0.0.1', port=8080, debug=True)
