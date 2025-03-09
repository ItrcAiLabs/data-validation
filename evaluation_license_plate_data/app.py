from flask import Flask, render_template, request, jsonify
import json
import os
from werkzeug.utils import secure_filename
from evaluation_license_plate_data import evaluation_license_plate_data

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_json_file(file):
    try:
        return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"خطا در پردازش فایل JSON: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # دریافت داده‌های پایه
            xml_folder = request.form.get("xml_folder")
            image_folder = request.form.get("image_folder")
            threshold_days = int(request.form.get("threshold_days"))

            # پردازش محدوده ابعاد
            dimension_range = {
                "min_width": int(request.form.get("min_width")),
                "max_width": int(request.form.get("max_width")),
                "min_height": int(request.form.get("min_height")),
                "max_height": int(request.form.get("max_height"))
            }

            # پردازش اندازه فایل‌ها
            file_size_range = {
                "min_size": int(request.form.get("min_size")) * 1024,      # تبدیل کیلوبایت به بایت
                "max_size": int(request.form.get("max_size")) * 1024 * 1024  # تبدیل مگابایت به بایت
            }

            # دریافت متادیتاهای انتخابی
            required_metadata = request.form.getlist("metadata_fields[]")
            if len(required_metadata) < 3:
                return "حداقل ۳ مورد متادیتا باید انتخاب شود", 400

            # دریافت فرمت‌های مجاز
            allowed_file_types = request.form.getlist("allowed_formats[]")

            # پردازش فایل‌های آپلود شده
            accuracy_config = {}
            expected_counts = {}

            # پردازش فایل مپینگ XML به JSON
            if 'xml_config' in request.files:
                file = request.files['xml_config']
                if file.filename != '' and allowed_file(file.filename):
                    xml_config = parse_json_file(file.stream)
                    # انتظار داریم فایل JSON شامل کلید accuracy_required_fields باشد
                    if 'accuracy_required_fields' not in xml_config:
                        return "ساختار فایل مپینگ نامعتبر است", 400
                    accuracy_config = xml_config

            # پردازش فایل تعدادهای مورد انتظار
            if 'expected_counts' in request.files:
                file = request.files['expected_counts']
                if file.filename != '' and allowed_file(file.filename):
                    expected_counts = parse_json_file(file.stream)
                    if not all(k in expected_counts for k in ['CarColor', 'CarModel']):
                        return "فایل باید شامل کلیدهای CarColor و CarModel باشد", 400

            # آماده‌سازی پارامترهای نهایی
            params = {
                "xml_folder": xml_folder,
                "image_folder": image_folder,
                "threshold_days": threshold_days,
                "dimension_range": dimension_range,
                "file_size_range": file_size_range,
                "required_metadata": required_metadata,
                "allowed_file_types": allowed_file_types,
                "accuracy_required_fields": accuracy_config.get('accuracy_required_fields', {}),
                "expected_counts": expected_counts
            }

            # فراخوانی تابع اصلی ارزیابی
            report = evaluation_license_plate_data(**params)
            return render_template("result.html", report=report)

        except Exception as e:
            app.logger.error(f"خطا: {str(e)}")
            return render_template("error.html", error_message=str(e)), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
