from flask import Flask, render_template, request, jsonify
from threading import Thread, Lock
import time
import os
from automatic_labeling import Labeling

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

progress = {
    "processing": False,
    "total": 0,
    "processed": 0,
    "start_time": None
}
progress_lock = Lock()

def process_images(source_dir, output_dir):
    global progress
    try:
        labeling = Labeling(source_dir, output_dir)
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
        images = [f for f in os.listdir(source_dir) if any(f.lower().endswith(ext) for ext in image_extensions)]
        
        with progress_lock:
            progress["total"] = len(images)
            progress["processed"] = 0
            progress["processing"] = True
            progress["start_time"] = time.time()

        for i, file in enumerate(images):
            img_path = os.path.join(source_dir, file)
            labeling.extract_info(img_path)
            labeling.save_xml(file)
            
            with progress_lock:
                progress["processed"] = i + 1

        with progress_lock:
            progress["processing"] = False

    except Exception as e:
        with progress_lock:
            progress["processing"] = False
        raise e

@app.route('/progress')
def get_progress():
    with progress_lock:
        return jsonify(progress)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source_dir = request.form['source_dir']
        output_dir = request.form['output_dir']
        
        if not os.path.isdir(source_dir):
            return render_template('index.html', error="مسیر پوشه تصاویر نامعتبر است!")
        
        thread = Thread(target=process_images, args=(source_dir, output_dir))
        thread.start()
        
        return render_template('processing.html')
    
    return render_template('index.html')


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)