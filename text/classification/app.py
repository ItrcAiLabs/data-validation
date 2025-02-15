
from classification import classification
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json

from currentness.currentness import currentness
from completeness.completeness import completeness
from consistency.consistency import consistency
from accuracy.accuracy import accuracy

app = Flask(__name__)

@app.template_filter('get_color_class')
def get_color_class(value):
    """
    بر اساس مقدار عددی (مثلاً accuracy یا ratio)، کلاس رنگی مناسب را برمی‌گرداند.
    """
    try:
        val = float(value)
    except:
        # اگر نتوانستیم مقدار را به float تبدیل کنیم، بدون رنگ برگردانیم.
        return ''
    
    # شرط‌بندی برای رنگ‌ها
    if val >= 0.8:
        return 'good'       # سبز
    elif val >= 0.5:
        return 'average'    # زرد
    else:
        return 'poor'       # قرمز
    
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # بررسی فایل آپلود شده
        if 'file' not in request.files:
            return "فایل آپلود نشده است.", 400

        file = request.files['file']
        if file.filename == '':
            return "هیچ فایلی انتخاب نشده است.", 400

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return "خطا در خواندن فایل CSV: " + str(e), 400

        config = {}

        # تنظیمات currentness
        if request.form.get('enable_currentness'):
            config["currentness"] = {
                "text_column": request.form.get('currentness_text_column', 'text'),
                "context": request.form.get('currentness_context', 'Political'),
                "timestamp_col": request.form.get('currentness_timestamp_col', 'timestamp'),
                "threshold_days": int(request.form.get('currentness_threshold_days', 600))
            }
        else:
            config["currentness"] = None

        # تنظیمات completeness
        if request.form.get('enable_completeness'):
            try:
                expected_occurrences = json.loads(request.form.get('completeness_expected_occurrences', '{}'))
            except:
                expected_occurrences = {}
            config["completeness"] = {
                "label_column": request.form.get('completeness_label_column', 'label'),
                "expected_occurrences": expected_occurrences
            }
        else:
            config["completeness"] = None

        # تنظیمات consistency
        if request.form.get('enable_consistency'):
            config["consistency"] = {
                "text_column": request.form.get('consistency_text_column', 'text'),
                "label_column": request.form.get('consistency_label_column', 'label'),
                "date_column": request.form.get('consistency_date_column', 'date'),
                "similarity_threshold": float(request.form.get('consistency_similarity_threshold', 0.95))
            }
        else:
            config["consistency"] = None

        # تنظیمات accuracy
        if request.form.get('enable_accuracy'):
            required_columns = request.form.get('accuracy_required_columns', '')
            required_columns = [col.strip() for col in required_columns.split(',') if col.strip()]

            # دریافت عملیات پاکسازی انتخاب‌شده (چک‌باکس‌ها)
            sequence_of_operations = request.form.getlist('clean_ops')
            # دریافت وظیفه معنایی (رادیو)
            semantic_task = request.form.get('semantic_task', '')

            try:
                mapping_label = json.loads(request.form.get('accuracy_mapping_label', '{}'))
            except:
                mapping_label = {}

            config["accuracy"] = {
                "required_columns": required_columns,
                "required_size": int(request.form.get('accuracy_required_size', 0)),
                "text_column": request.form.get('accuracy_text_column', 'text'),
                "date_column": request.form.get('accuracy_date_column', 'date'),
                "min_length": int(request.form.get('accuracy_min_length', 0)),
                "max_length": int(request.form.get('accuracy_max_length', 0)),
                "start_date": request.form.get('accuracy_start_date', ''),
                "end_date": request.form.get('accuracy_end_date', ''),
                "sequence_of_operations": sequence_of_operations,
                "mapping_label": mapping_label,
                "semantic_task": semantic_task,
                "semantic_model_name": request.form.get('accuracy_semantic_model_name', '')
            }
        else:
            config["accuracy"] = None

        report_json = classification(df, config)
        # تبدیل دوباره به دیکشنری پایتون برای نمایش (و پردازش) در قالب
        report = json.loads(report_json)
        return render_template('report.html', report=report)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)