import sqlite3

def convert_image_into_binary(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
    return photo_image

def insert_image(image):
    image_database = sqlite3.connect("Image_data.db")
    data = image_database.cursor()
    insert_photo = convert_image_into_binary(image)
    data.execute("INSERT INTO Image Values(:image)", {'image': insert_photo})
    image_database.commit()
    image_database.close()

def create_database():
    image_database = sqlite3.connect("Image_data.db")
    data = image_database.cursor()
    data.execute("CREATE TABLE IF NOT EXISTS Image(Image BLOB)")
    image_database.commit()
    image_database.close()

# Prompt the user to enter the image directory
image = input("Enter the image directory: ")

create_database()
insert_image(image)
