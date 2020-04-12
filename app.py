import os
from flask import Flask, render_template, flash, request, redirect, url_for, Response
app = Flask(__name__)
UPLOAD_FOLDER='./static/assets'

class Spot: #clasa ce detaliaza un loc de parcare, deocamdata are un singur camp care semnifica daca locul este ocupat sau nu
    def __init__(self,taken):
        self.taken=taken

@app.route('/') #ruta folosita pentru interfata web
def hello():
    spot=Spot(False)
    path=os.path.join(UPLOAD_FOLDER,'image.jpg')
    print(path)
    return render_template('base.html',spot=spot,image_path=path) #returneaza un template ce se schimba in fuctie de locul de parcare si imaginea primita


@app.route('/image',methods=['GET','POST']) #ruta folosita pentru upload de imagine
def addImage():
    if(request.method=='POST'):
        if 'file' not in request.files:
            return Response("File not present in the request",400)
    file=request.files['file'] 
    path=os.path.join(UPLOAD_FOLDER,'image.jpg')
    file.save(path) #salvam imaginea pe disk
    print(path)
    return "success"

if __name__ == '__main__':
    app.run()