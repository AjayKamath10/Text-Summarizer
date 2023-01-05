from flask import Flask, render_template, request
import re

imageRegEx = re.compile(r"\.jpg$|\.jpeg$|\.png$")
urlRegEx = re.compile(r"^http")
pdfRegEx = re.compile(r'\.pdf')





app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/text/')
def text():
    return render_template('text.html')

@app.route('/image/')
def text():
    return render_template('image.html')

@app.route('/summarize', methods=['GET','POST'])
def my_form_post():
    if request.method == "POST":
        text = request.form['text1']
    inp = ""
    if imageRegEx.search(text).group() != None:
        inp = "Image"
    elif urlRegEx.search(text).group() != None:
        inp = "URL"
    elif pdfRegEx.search(text).group() != None:
        inp = "PDF"
    else:
        inp = "Text"
    print("INP: ",inp)
    
    return render_template('summarized_text.html', result = text.upper())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
