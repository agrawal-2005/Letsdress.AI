from flask import Flask, request, render_template
import os
from PIL import Image
import requests
import io
import sqlite3
import smtplib
from dotenv import load_dotenv
load_dotenv()

# Use the new environment variable for the Stability AI key
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core" # Using Stable Image Core

app = Flask(__name__)

def save_database(image_path, text_data):
    """Saves the image path and its text description to the database."""
    def get_image_as_binary(filepath):
        with open(filepath, 'rb') as file:
            return file.read()

    db_path = "./database/Image_data.db"
    conn = None
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Image(Image BLOB, text_feature TEXT)")
        image_binary = get_image_as_binary(image_path)
        cursor.execute("INSERT INTO Image (Image, text_feature) VALUES (?, ?)", (image_binary, text_data))
        conn.commit()
        print(f"Successfully saved {image_path} to the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except IOError as e:
        print(f"File error: {e}")
    finally:
        if conn:
            conn.close()

def generate_image(prop):
    """Generates images using the Stable Image Core API with correct formatting."""
    try:
        for i in range(1, 9):
            user_input = f"{prop}, high quality photography"
            print(f"Generating image {i} with prompt: '{user_input}'")

            # --- *** KEY CORRECTIONS ARE HERE *** ---
            response = requests.post(
                API_URL,
                headers={
                    "authorization": f"Bearer {STABILITY_API_KEY}",
                    "accept": "image/*"  # We want the image bytes directly
                },
                # Use files to indicate a multipart/form-data request
                files={"none": ''},
                # Use data for form fields, not json
                data={
                    "prompt": user_input,
                    "output_format": "png",
                    # Optional: Add a style for better results
                    "style_preset": "photographic",
                },
                timeout=60
            )
            # --- *** END OF CORRECTIONS *** ---

            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content))
            image_path = f"./static/images/image{i}.png"
            image.save(image_path)
            print(f"Image saved as {image_path}")
            save_database(image_path, prop)
        
        return None # Success

    except requests.exceptions.HTTPError as e:
        error_details = "Unknown error"
        try:
            # Try to parse the JSON error response from Stability AI
            error_details = e.response.json()
        except ValueError:
            error_details = e.response.text

        print(f"API Error: {error_details}")
        # Provide a more user-friendly message
        message = f"API Error ({e.response.status_code}): Please check the server logs for details."
        if e.response.status_code == 401:
            message = "Authentication error: Please check your API key."
        return message
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please check the server logs."

@app.route('/')
def index():
    return render_template('opening.html')

@app.route('/read_more', methods=['GET', 'POST'])
def read_more_func():
    return render_template('index.html')

@app.route('/form_register', methods=['POST'])
def fetch():
    error_message = None
    if request.method == 'POST':
        req = request.form.get('search_bttn')
        if not req:
            error_message = "Please enter a description for the image."
        else:
            print(f"Received search request: {req}")
            error_message = generate_image(req)
            
    # Always render the template, passing an error message if one occurred
    return render_template('index.html', error=error_message)

@app.route('/form_send', methods=['POST'])
def send():
    try:
        send_user = request.form['send_name']
        send_gmail = request.form['send_email']
        send_mess = request.form['send_mess']
        
        send_from = os.getenv("GMAIL")
        recipient = os.getenv("GMAIL")
        password = os.getenv("GMAIL_PASSWORD")
        
        if not all([send_from, recipient, password]):
            return "Server email configuration is incomplete.", 500

        message = f"Subject: New Feedback from {send_user}\n\nEmail: {send_gmail}\nMessage: {send_mess}"
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(send_from, password)
            server.sendmail(send_from, recipient, message)
            
        return render_template('feedback.html')
    except Exception as e:
        print(f"Failed to send email: {e}")
        return "An error occurred while sending feedback.", 500

@app.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)