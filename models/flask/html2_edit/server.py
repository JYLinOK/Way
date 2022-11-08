from flask import Flask, redirect, url_for, request, render_template
from gevent import pywsgi


app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name
    

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      print(1)
      user = request.form['nm']
      return redirect(url_for('success', name = user))
   else:
      print(2)
      user = request.args.get('nm')
      return redirect(url_for('success', name = user))


if __name__ == '__main__':
    app.run(port=6666)

    # WSGI Sever
    # server = pywsgi.WSGIServer(('0.0.0.0', 6666), app)
    # server.serve_forever()
