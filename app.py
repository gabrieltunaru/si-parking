import os
from flask import Flask, render_template, flash, request, redirect, url_for, Response
app = Flask(__name__)
UPLOAD_FOLDER='./static/assets'

class Spot:
    def __init__(self,taken):
        self.taken=taken

@app.route('/')
def hello():
    spot=Spot(False)
    path=os.path.join(UPLOAD_FOLDER,'image.jpg')
    print(path)
    return render_template('base.html',spot=spot,image_path=path)


@app.route('/image',methods=['GET','POST'])
def addImage():
    if(request.method=='POST'):
        if 'file' not in request.files:
            return Response("File not present in the request",400)
    file=request.files['file']
    path=os.path.join(UPLOAD_FOLDER,'image.jpg')
    file.save(path)
    print(path)
    return "success"

if __name__ == '__main__':
    app.run()