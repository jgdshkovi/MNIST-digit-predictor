import os
from flask import *  

import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
model = tf.keras.models.load_model('my_mnist_cnn.h5 ')

app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("upload.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(os.path.join('uploads',f.filename))
        return render_template("success.html", name = f.filename)  


@app.route('/predict', methods = ['POST']) 
def predict():
    def d423d(arr):
        I,J,K = arr.shape
        ro = []
        for i in range(I):
            ri = []
            for j in range(J):
                ri.append( list(arr[i][j][:-1] ))
            ro.append(ri)
        
        return np.array(ro)

    def d32d1(img):
        img = img.resize((28,28))
        img = np.array(img)
        if len(img.shape)==3:
            if img.shape[2]==4:
                img = d423d(img)
        rgb_weights = [0.2989, 0.5870, 0.1140]
        grayscale_image = np.dot(img[...,:3], rgb_weights)
        grimg = np.array(grayscale_image)
        return grimg

    im = Image.open(os.path.join('uploads',f.filename))

    grimg = d32d1(im)
    grimg = grimg/255.0
    grimg = grimg.reshape(-1,28,28,1)

    prediction = model.predict(grimg)
    arr = []
    arr.append( [float(i) for i in str(prediction).replace('[','').replace(']','').split()] )

    #print(arr)
    #print(arr[0].index(max(arr[0])))
    res = str(arr[0].index(max(arr[0])))
    return render_template('res.html', name= res)

@app.errorhandler(Exception)          
def basic_error(e):
    res =   "an error occured: " + str(e)       
    return render_template('res.html', name= res)

if __name__ == '__main__':
    app.run(debug = True)  