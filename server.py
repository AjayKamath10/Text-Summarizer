from flask import Flask, render_template, request
import re
from backend import *
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

imageRegEx = re.compile(r"\.jpg$|\.jpeg$|\.png$")
urlRegEx = re.compile(r"^http")
pdfRegEx = re.compile(r'\.pdf')


@app.route('/text/')
def text():
    return render_template('text.html')

@app.route('/image/')
def image():
    return render_template('image.html')

@app.route('/pdf/')
def pdf():
    return render_template('pdf.html')

@app.route('/url/')
def url():
    return render_template('url.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/summarize', methods=['GET','POST'])
def my_form_post():
    if request.method == "POST":
        text = str(request.form['text1'])
    begin = time.time()
    inwords = 512
    inp = ""
    summary = ''
    if imageRegEx.search(text) != None:
        inp = "Image"
        inwords, summary = image_summary(text)
    elif urlRegEx.search(text) != None:
        inp = "URL"
        inwords, summary = url_output(text)
    elif pdfRegEx.search(text) != None:
        inp = "PDF"
        inwords, summary = pdf_summary(text)
    else:
        inp = "Text"
        inwords, summary = normal_text(text)
    outwords = len(summary.split())
    print("INP: ",inp)
    end = time.time()
    return render_template('summarized_text.html', result = summary, input_words = inwords, output_words = outwords, summarize_time = "{:.2f}".format(end- begin))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
