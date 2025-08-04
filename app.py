from flask import Flask,url_for,redirect,request,render_template,Response;
import os
import PIL
from PIL import Image
import requests
import io
import sqlite3
import smtplib
API_TOKEN = "REMOVED"
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
app = Flask(__name__)

def generate_image(prop):
    def generate(user_input):
        def uniquify(path):
            filename, extension = os.path.splitext(path)
            counter = 1
            while os.path.exists(path):
                path = filename + " (" + str(counter) + ")" + extension
                counter += 1
            return path

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.content

        image_bytes = query({"inputs": user_input})
        image = PIL.Image.open(io.BytesIO(image_bytes))
        image_path = "image" + str(i) + ".jpg"
        image.save("./static/images/" + image_path)
        print(f"Image saved as {image_path}")

    for i in range(1,9):
           generate(str(prop)+ "outfit" + str(i))


@app.route('/')
def index():
    return render_template('opening.html')
@app.route('/read_more', methods=['GET', 'POST'])
def read_more_func():
    return render_template('index.html')
@app.route('/form_register', methods=['POST', 'GET'])
def fetch():
    try:
        req = request.form['search_bttn']
        print(req)
        generate_image(req)
        return render_template('index2.html')
    except Exception as e:
        return str(e)
@app.route('/form_send',methods=['POST','GET'])
def Send():
    send_user=request.form['send_name']
    send_gmail=request.form['send_email']
    send_mess=request.form['send_mess']
    print(send_user,send_gmail,send_mess)
    send = "project.feedback.02@gmail.com"
    rec = "project.feedback.02@gmail.com"
    pas = "yzay obwk fisz kpcj"
    message = f"Subject: {send_gmail}\n\nMR/MRS {send_user} messaged you: {send_mess}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send, pas)
    server.sendmail(send, rec, message)
    return render_template('feedback.html')
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    return render_template('feedback.html')
@app.route('/startup', methods=['GET', 'POST'])
def startup():
    return render_template('opening.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
