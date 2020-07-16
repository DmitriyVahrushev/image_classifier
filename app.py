import os

from flask import Flask, render_template, request, redirect, flash

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            #No file part
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('result.html', class_name = "no file has been sent!")
        if not allowed_file(file.filename):
            #Not allowed file extension
            return redirect(request.url)
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        class_name = format_class_name(class_name)
        return render_template('result.html', class_id=class_id,
                               class_name=class_name)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
