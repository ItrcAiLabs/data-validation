from flask import Flask, render_template, request, jsonify
import json
from werkzeug.utils import secure_filename
from evaluation_license_plate_data import evaluation_license_plate_data

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # حداکثر حجم ۲ مگابایت

ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_json_file(file):
    try:
        data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("فرمت JSON نامعتبر")
        return data
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

            # پردازش محدوده ابعاد تصویر
            dimension_range = {
                "min_width": int(request.form.get("min_width")),
                "max_width": int(request.form.get("max_width")),
                "min_height": int(request.form.get("min_height")),
                "max_height": int(request.form.get("max_height"))
            }

            # پردازش محدوده اندازه فایل
            file_size_range = {
                "min_size": int(request.form.get("min_size")) * 1024,      # تبدیل کیلوبایت به بایت
                "max_size": int(request.form.get("max_size")) * 1024 * 1024  # تبدیل مگابایت به بایت
            }

            # دریافت متادیتاهای انتخابی
            required_metadata = request.form.getlist("metadata_fields[]")
            if len(required_metadata) < 3:
                return "حداقل ۳ مورد متادیتا باید انتخاب شود", 400

            # دریافت فرمت‌های مجاز تصویر
            allowed_file_types = request.form.getlist("allowed_formats[]")

            # پردازش فایل‌های آپلود شده

            # فایل پیکربندی XML (فایل مپینگ)
            xml_file = request.files.get("xml_config")
            print("--------", xml_file)
            if not xml_file or xml_file.filename == "":
                return "فایل پیکربندی XML الزامی است", 400
            if not allowed_file(xml_file.filename):
                return f"فرمت فایل {xml_file.filename} نامعتبر است", 400

            # مقداردهی اولیه به متغیر xml_data برای جلوگیری از خطای دسترسی به متغیر تعریف‌نشده
            xml_data = None
            try:
                xml_data = parse_json_file(xml_file.stream)
            except Exception as e:
                return f"خطا در پردازش فایل {xml_file.filename}: {str(e)}", 400

            if not xml_data or "config" not in xml_data:
                return "ساختار فایل مپینگ نامعتبر است", 400

            # فایل تعدادهای مورد انتظار
            expected_counts_file = request.files.get("expected_counts")
            if not expected_counts_file or expected_counts_file.filename == "":
                return "فایل تعدادهای مورد انتظار الزامی است", 400
            if not allowed_file(expected_counts_file.filename):
                return f"فرمت فایل {expected_counts_file.filename} نامعتبر است", 400

            try:
                expected_counts = parse_json_file(expected_counts_file.stream)
            except Exception as e:
                return f"خطا در پردازش فایل {expected_counts_file.filename}: {str(e)}", 400

            if not all(k in expected_counts for k in ['CarColor', 'CarModel']):
                return "فایل تعدادهای مورد انتظار باید شامل کلیدهای CarColor و CarModel باشد", 400

            # پردازش داده‌های موجود در فایل پیکربندی (xml_data)
            mapping = xml_data.get("config")
            features = list(mapping.values())
            completeness_field_xpaths = {key: mapping[key] for key in mapping if key in {"CarModel", "CarColor"}}
            accuracy_required_fields = {key: mapping[key] for key in mapping if key in {
                "registration_prefix", "series_letter", "registration_number", "province_code",
                "car_model", "car_color", "license_plate_coordinates", "car_coordinates"
            }}
            xpaths_syntactic = {key: mapping[key] for key in mapping if key in {
                "registration_prefix", "series_letter", "registration_number", "province_code"
            }}
            currentness_field_xpaths = {key: mapping[key] for key in mapping if key in {"CarModel", "CarColor"}}

            report = evaluation_license_plate_data(
                xml_folder,
                image_folder,
                threshold_days,
                features,
                expected_counts,
                completeness_field_xpaths,
                required_metadata,
                accuracy_required_fields,
                allowed_file_types,
                dimension_range,
                file_size_range,
                xpaths_syntactic,
                currentness_field_xpaths
            )


            field_translations = {
                    "registration_prefix": "پیشوند ثبت پلاک",
                    "series_letter": "حرف سری پلاک",
                    "registration_number": "شماره ثبت پلاک",
                    "province_code": "کد استان پلاک",
                    "car_model": "مدل خودرو",
                    "car_color": "رنگ خودرو",
                    "license_plate_coordinates": "مختصات پلاک خودرو",
                    "car_coordinates": "مختصات خودرو",
                    "car_coordinates_X": "مختصات X خودرو",
                    "car_coordinates_Y": "مختصات Y خودرو",
                    "car_coordinates_Width": "عرض خودرو",
                    "car_coordinates_Height": "ارتفاع خودرو"
                    
                }
            
            if isinstance(report, str):
                try:
                    report = json.loads(report)  #
                except json.JSONDecodeError:
                    return render_template("error.html", error_message=report), 500
            return render_template("result.html", report=report, field_translations=field_translations)



        except Exception as e:
            app.logger.error(f"خطا: {str(e)}")
            return render_template("error.html", error_message=str(e)), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)
