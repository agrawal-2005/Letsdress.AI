from flask import Flask, url_for, redirect, request, render_template, Response;
import os
import PIL
from PIL import Image
import requests
import io
import sqlite3
import smtplib
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

app = Flask(__name__)
def save_database(image, text_data):
    def convert_image_into_binary(filename):
        with open(filename, 'rb') as file:
            photo_image = file.read()
        return photo_image
    
    def insert_image(image):
        image_database = sqlite3.connect("./database/Image_data.db")
        data = image_database.cursor()
        insert_photo = convert_image_into_binary(image)
        data.execute("INSERT INTO Image (Image, text_feature) VALUES (:image, :text)", {'image': insert_photo, 'text': text_data})
        image_database.commit()
        image_database.close()

    def create_database():
        image_database = sqlite3.connect("./database/Image_data.db")
        data = image_database.cursor()
        data.execute("CREATE TABLE IF NOT EXISTS Image(Image BLOB, text_feature TEXT)")
        image_database.commit()
        image_database.close()
    
    try:
        create_database()
        insert_image(image)
    except Exception as e:
        return str(e)

# generate_image("male traditional")
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1
    return path

def generate_image(prop):
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        print(response.status_code)
        print(response.headers)
        print(response.content[:500])
        return response.content

    try:
        for i in range(1, 9):  # range(1, 9) was wrong. It doesn’t run 9
            user_input = f"{prop} outfit {i}"
            image_bytes = query({"inputs": user_input})
            image = Image.open(io.BytesIO(image_bytes))
            image_path = f"./static/images/image{i}.png"
            unique_path = uniquify(image_path)
            image.save(unique_path)
            print(f"Image saved as {unique_path}")
            save_database(unique_path, prop)
    except Exception as e:
        print(f"Error generating image: {e}")
        return str(e)

@app.route('/')
def index():
    return render_template('opening.html')

@app.route('/read_more', methods=['GET', 'POST'])
def read_more_func():
    return render_template('index.html')

@app.route('/form_register', methods=['POST'])
def fetch():
    if request.method == 'POST':
        try:
            req = request.form.get('search_bttn')
            if not req:
                return "Error: No prompt provided", 400
            print(req)
            generate_image(req)
            return render_template('index.html')
        except Exception as e:
            return str(e)

@app.route('/form_send', methods=['GET', 'POST'])
def send():
    send_user=request.form['send_name']
    send_gmail=request.form['send_email']
    send_mess=request.form['send_mess']
    print(send_user, send_gmail, send_mess)
    send = os.getenv("GMAIL")
    rec = os.getenv("GMAIL")
    pas = os.getenv("GMAIL_PASSWORD")
    message = f"Subject: {send_gmail}\n\nMR/MRS {send_user} messaged you: {send_mess}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send, pas)
    server.sendmail(send, rec, message)
    return render_template('feedback.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)