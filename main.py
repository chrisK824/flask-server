from app import app
import os
import eventlet
from eventlet import wsgi

if __name__ == '__main__':
    # app.secret_key = os.urandom(1)
    # wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    app.run(debug=True)
