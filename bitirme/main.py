
from flask import Flask, render_template, url_for
context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('landingPage.html', branding = False)

def main():
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(threaded=True, host='192.168.1.7', port=8080,ssl_context='adhoc')

if __name__=="__main__":
    main()
