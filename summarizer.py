#import statements

from tkinter import * #gui
from transformers import pipeline  #transformers
import cv2  #image loading comp vision
import pytesseract # ocr
from pdf2image import convert_from_path #pdf 2 image
from pytesseract import image_to_string 
from bs4 import BeautifulSoup #web scraping
import requests #web scraping
import os #files 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import unidecode 
import re 
import time  
from autocorrect import Speller  
import string 
print("All imports ok")


#main


#data cleaning

def clean_data_before(text):
    # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
    Formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com').replace("    "," ")
    # Removing all the occurrences of links that starts with https
    Formatted_text = re.sub(r'http\S+', '', text)
    # Remove all the occurrences of text that ends with .com
    Formatted_text = re.sub(r"\ [A-Za-z]*\.com", " ", Formatted_text)
     # Remove accented characters from text using unidecode.
    # Unidecode() - It takes unicode data & tries to represent it to ASCII characters. 
    Formatted_text = unidecode.unidecode(Formatted_text)
    Formatted_text = Formatted_text.lower()
    #spell = Speller(lang='en')
    #Formatted_text = spell(Formatted_text)
    Formatted_Text = re.sub(r"[^a-zA-Z0-9:$-,%.?!]+", ' ', Formatted_text) 
    return Formatted_text

#capitalize after summarization
def clean_data_after(text):
    #capitalize
    s=""
    for i in text.split("."):
        s+=i.capitalize()+"."
    return(s)



min_val = 100 #get from settings


#normal summarization    
def normal_text(article):
##    print("Print normal text")
##    article = '''The potato is a starchy food, a tuber of the plant Solanum tuberosum and is a root vegetable native to the Americas. The plant is a perennial in the nightshade family Solanaceae.[2]
##
##Wild potato species can be found from the southern United States to southern Chile.[3] The potato was originally believed to have been domesticated by Native Americans independently in multiple locations,[4] but later genetic studies traced a single origin, in the area of present-day southern Peru and extreme northwestern Bolivia. Potatoes were domesticated there approximately 7,000–10,000 years ago, from a species in the Solanum brevicaule complex.[5][6][7] In the Andes region of South America, where the species is indigenous, some close relatives of the potato are cultivated.
##
##Potatoes were introduced to Europe from the Americas by the Spanish in the second half of the 16th century. Today they are a staple food in many parts of the world and an integral part of much of the world's food supply. As of 2014, potatoes were the world's fourth-largest food crop after maize (corn), wheat, and rice.[8] Following millennia of selective breeding, there are now over 5,000 different types of potatoes.[6] Over 99% of potatoes presently cultivated worldwide descend from varieties that originated in the lowlands of south-central Chile.[9] The importance of the potato as a food source and culinary ingredient varies by region and is still changing. It remains an essential crop in Europe, especially Northern and Eastern Europe, where per capita production is still the highest in the world, while the most rapid expansion in production since 2000 has occurred in southern and eastern Asia, with China and India leading the world in overall production as of 2018.
##
##Like the tomato, the potato is a nightshade in the genus Solanum, and the vegetative and fruiting parts of the potato contain the toxin solanine which is dangerous for human consumption. Normal potato tubers that have been grown and stored properly produce glycoalkaloids in amounts small enough to be negligible to human health, but, if green sections of the plant (namely sprouts and skins) are exposed to light, the tuber can accumulate a high enough concentration of glycoalkaloids to affect human health.[10] The discovery of acrylamides in starchy foods in 2002 led to international health concerns, but subsequent high-quality evidence showed acrylamide is not likely to cause cancer in humans.[11][12] '''

    summary = Text_sum(article)
    print("Summary\n", summary)
    return summary
    
#normal_text()

#functions for general summarization    
def Text_sum(article):
    if min_val >= 100:
        min_value = min_val
    else:
        min_value = 100
    article = clean_data_before(article)
    summarizer1 = pipeline("summarization",model="t5-small")
    #article=article[:512]
    summary_text = summarizer1(article,do_sample=False,min_length=min_val)[0]['summary_text']
    summary_text = clean_data_after(summary_text)
    return(summary_text)


def img_to_sum(image):
    img = cv2.imread(image)
    text = pytesseract.image_to_string(img)
    k=Text_sum(text)
    return(k)

#image summary
def image_summary():
    img = r"C:\Users\kamat\Downloads\tomato_handwriting.png"
    summary = img_to_sum(img)
    print("Image summarized: ", summary)

image_summary()


    

    
    
#convert pdf to images and extract data using tesseract

def convert_pdf_to_img(pdf_file):
    pop = r"C:\poppler-0.68.0_x86\poppler-0.68.0\bin"
    return convert_from_path(pdf_file,poppler_path=pop)





def convert_image_to_text(file):
    text = image_to_string(file)
    return text

def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
    return final_text

def pdf_sum_pre(path_to_pdf):    
    text = get_text_from_any_pdf(path_to_pdf)
    text = text.replace("-\n", "")
    l=[]
    for i in text.split():
        l.append(i)
    article=""
    for i in l:
        article += i+" "
    return(article)

#pdf to summary function
def pdf_to_sum(path_to_pdf):
    text = pdf_sum_pre(path_to_pdf)
    k = Text_sum(text)
    return(k)    
        
#summary of pdf
def pdf_summary():
    pdf = r"C:\Users\kamat\Downloads\tomato_handwriting.pdf"
    summary = pdf_to_sum(pdf)
    print("PDF Summarized\n", summary)
    
#pdf_summary()
    
#url summarization    

    
#output the summary from url
def url_output():
    url = "https://en.wikipedia.org/wiki/Potato"
    #print(url)
    summary = url_to_sum(url)
    print("URL Summarized\n",summary)
    


#url_output()

#url to summary
def url_to_sum(URL):
    text = url_convert(URL)
    k = Text_sum(text[:512])
    return(k)

#web scrape url and obtain text
def url_convert(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['h1', 'p'])
    text = [result.text for result in results]
    ARTICLE = ' '.join(text)
    return(ARTICLE)    
    
    


    
