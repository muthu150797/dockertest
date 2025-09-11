from flask import Flask
import face_recognition
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask inside Docker on Render!"

@app.route('/GetfaceRecogV')
def GetfaceRecogV():
    return "face recognition version is "+face_recognition.__version__

@app.route('/getme')
def sayhi():
    return "HIIIII"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
