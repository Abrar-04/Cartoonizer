from flask import * 
from flask import url_for
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

picture = os.path.join('static', 'pics')

def start():
    app = Flask(__name__)  

app.config['UPLOAD_FOLDER'] = picture 

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  


@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        img_dir=f.filename

    def img_read(img_dir):
        img=cv2.imread(img_dir,cv2.IMREAD_UNCHANGED)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        return img
    img=img_read(img_dir)

    def cartoon_filter(img):
        numDownSamples = 2 
        numBilateralFilters = 5  

        img_color = img
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)

        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)


        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)


        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)

        img_edge = cv2.adaptiveThreshold(img_blur, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        return cv2.bitwise_and(img_color, img_edge)

    cartoon=cartoon_filter(img)
    cartoon=cv2.cvtColor(cartoon,cv2.COLOR_BGR2RGB)

    cv2.imwrite('static/pics/final.jpg', cartoon)

    return render_template("success.html", name = 'final',user_image = 'final.jpg')



if __name__ == '__main__':  
    app.run(debug = True)  
