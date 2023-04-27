from flask import Flask, render_template, Response
import json
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('C:\Firebase\serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://flask-app-b27bb-default-rtdb.firebaseio.com'
})

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/stream')
def stream():
    def event_stream():
        messages = []
        def callback(snapshot):
            messages.append(snapshot.val())
        messagesRef = db.reference('messages')
        messagesRef.order_by_key().limit_to_last(50).on('child_added', callback)
        while True:
            if messages:
                yield 'data: {}\n\n'.format(json.dumps(messages.pop()))
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)
