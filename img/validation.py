import json
from ImageFormatValidator.ImageFormatValidator import ImageFormatValidator
from configs.configFormatValidator import configFormatValidator
from utils import list_all_files


class validation:
    def __init__(self,) -> None:
        pass
        
    def level0(self):
        self.path_image_folder = configFormatValidator.get("path_image_folder")
        self.path_image_list = configFormatValidator.get("path_image_list")
        self.max_size_mb = configFormatValidator.get("max_size_mb")
        self.allowed_formats = configFormatValidator.get("allowed_formats")
        self.min_size_mb = configFormatValidator.get("min_size_mb")
        self.expected_dimensions_list = configFormatValidator.get("expected_dimensions_list")
        self.expected_mode = configFormatValidator.get("expected_mode")
        self.pixel_range = configFormatValidator.get("pixel_range")

        self.list_path_images = list_all_files(self.path_image_folder)

        if not self.list_path_images:  # Handle case where there are no images
            return []

        with open(self.path_image_list, "r") as file:
            self.image_list = json.load(file)

        return ImageFormatValidator(
            self.list_path_images, 
            self.image_list, 
            self.max_size_mb, 
            self.allowed_formats,
            self.min_size_mb, 
            self.expected_dimensions_list,
            self.expected_mode,
            self.pixel_range
        )

        
model = validation()
model.level0()


from flask import Flask, render_template, jsonify
import json
from ImageFormatValidator.ImageFormatValidator import ImageFormatValidator
from configs.configFormatValidator import configFormatValidator
from utils import list_all_files

app = Flask(__name__)

@app.route('/')
def index():
    model = validation()
    validation_report = model.level0()
    print(validation_report)
    if not validation_report:  # Provide a default empty list to avoid NoneType error
        validation_report = []
    return render_template('index.html', validation_report=validation_report)


@app.route('/api/validate')
def validate_api():
    model = validation()
    validation_report = model.level0()
    return jsonify(validation_report)




if __name__ == '__main__':
    app.run(debug=True, port=5002)