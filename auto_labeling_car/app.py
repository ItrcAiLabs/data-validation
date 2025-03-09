from flask import Blueprint, render_template, request, jsonify
from threading import Thread, Lock
import time
import os
from .automatic_labeling import Labeling




bp_dir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(bp_dir, 'templates')
static_folder = os.path.join(bp_dir, 'static')

automatic_labeling_app = Blueprint(
    'automatic_labeling_app',
    __name__,
    template_folder=template_folder,
    static_folder=static_folder,
    static_url_path='/auto_labeling_car/static'
)

# Point template_folder one level up to use the project’s templates
# automatic_labeling_app = Blueprint('automatic_labeling_app', __name__, template_folder='./templates')

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

@automatic_labeling_app.route('/progress')
def get_progress():
    with progress_lock:
        return jsonify(progress)

@automatic_labeling_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source_dir = request.form['source_dir']
        output_dir = request.form['output_dir']
        
        if not os.path.isdir(source_dir):
            return render_template('index.html', error="Invalid image directory!")
        
        thread = Thread(target=process_images, args=(source_dir, output_dir))
        thread.start()
        
        return render_template('processing.html')
    
    return render_template('index.html')