from flask import Flask, render_template

from auto_labeling_car.app import automatic_labeling_app  
# from evaluation_text_classification_data.app import evaluation_text_classification_data_app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(automatic_labeling_app, url_prefix='/auto_labeling_car')   

if __name__ == '__main__':
    app.run(debug=True, port=5001)
