import os
from flask import Flask, render_template, flash, request, redirect, url_for, Response
import PIL
from PIL import Image
import sys
import io
from ml import check_photo
from datetime import datetime
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
app = Flask(__name__)
UPLOAD_FOLDER = './static/assets'
UPLOAD_FOLDER_SAVE = './flaskr/static/assets'


class Spot:  # clasa ce detaliaza un loc de parcare, deocamdata are un singur camp care semnifica daca locul este ocupat sau nu
    def __init__(self, taken):
        self.taken = taken

    def set_taken(self, taken):
        self.taken = taken


spot = Spot(False)


@app.route('/')  # ruta folosita pentru interfata web
def hello():
    path = os.path.join(UPLOAD_FOLDER, 'image.jpg')
    print(path)
    # returneaza un template ce se schimba in fuctie de locul de parcare si imaginea primita
    return render_template('base.html', spot=spot, image_path=path)


# ruta folosita pentru upload de imagine
@app.route('/image', methods=['GET', 'POST'])
def addImage():
    if(request.method == 'POST'):
        if 'file' not in request.files:
            return Response("File not present in the request", 400)
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, 'image.jpg')
    file.save(path)  # salvam imaginea pe disk
    print(path)
    return "success"

# ruta folosita pentru upload de imagine
@app.route('/imageBMP', methods=['GET', 'POST'])
def addjpgImage():
    try:
        file = request.data
        image = Image.open(io.BytesIO(file))
        path = os.path.join(UPLOAD_FOLDER_SAVE, 'image.jpg')
        image.save(path)  # salvam imaginea pe disk
        spot.imageTime = datetime.now()
        print(spot.imageTime)
        check_photo()
        return "success"
    except Exception as err:
        f = open("./logs.txt", "a")
        f.write(str(datetime.now()) + ": " + str(err)+ "\n")
        f.close()
        print(str(err))
        return str(err), 500


@app.route('/distance', methods=['GET', 'POST'])
def setDistance():
    data = request.get_json()
    print("request data: %s" % data)
    try:
        distance1 = data['distance1']
        spot.distance1 = distance1
        print("distance1: %s" % distance1)
        distance2 = data['distance2']
        spot.distance2 = distance2
        print("distance2: %s" % distance2)
        spot.distanceTime = datetime.now()
        if(distance1 < 100 and distance2 < 100):
            spot.set_taken(True)
        else:
            spot.set_taken(False)
        return "success"
    except:
        response = "Invalid JSON format: " + str(data)
        return response, 400


if __name__ == '__main__':
    app.run()
