from flask import Flask,render_template,request
from nltk_summarizer import nltk_summarizer
from spacy_summarizer import text_summarizer
import time
import spacy 
from bs4 import BeautifulSoup
from urllib.request import urlopen
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

def readingtime(mytxt):
    total_words = len([token.text for token in nlp(mytxt)])
    estimated_time = total_words/200.0
    return estimated_time

def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page,"lxml")
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse',methods=['GET','POST'])
def analyse():
    start = time.time()
    if request.method == 'POST':
        # summarization_nltk
        rawtxt = request.form['raw-text']
        final_readingtime = readingtime(rawtxt)
        final_sumarization_nltk = nltk_summarizer(rawtxt)
        final_summarizetime_nltk = readingtime(final_sumarization_nltk)
        # summarization_nltk
        final_sumarization_spacy = text_summarizer(rawtxt)
        final_summarizetime_spacy = readingtime(final_sumarization_spacy)
        #finalize time
        end = time.time()
        final_time = start - end
    return render_template('index.html',final_sumarize_nltk = final_sumarization_nltk,f_time_nltk = final_summarizetime_nltk,
                          final_sumarize_spacy = final_sumarization_spacy,f_time_spacy = final_summarizetime_spacy)

@app.route('/analyse_url',methods=['GET','POST'])
def analyse_url():
    start = time.time()
    if request.method == 'POST':
        # summarization
        rawurl = request.form['raw-url']
        rawtxt = get_text(rawurl)
        final_readingtime = readingtime(rawtxt)
        final_sumarization_nltk = nltk_summarizer(rawtxt)
        final_summarizetime_nltk = readingtime(final_sumarization_nltk)
        # summarization_nltk
        final_sumarization_spacy = text_summarizer(rawtxt)
        final_summarizetime_spacy = readingtime(final_sumarization_spacy)
        #finalize time
        end = time.time()
        final_time = start - end
    return render_template('index.html',final_sumarize_nltk = final_sumarization_nltk,f_time_nltk = final_summarizetime_nltk,
                          final_sumarize_spacy = final_sumarization_spacy,f_time_spacy = final_summarizetime_spacy)

@app.route('/compare_summary')
def compare_summary():
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)
