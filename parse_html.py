import os, sys, glob, re
import json
from pprint import pprint
from time import sleep
from unidecode import unidecode

import backoff
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import googletrans
from config import RAW_HTML_DIR, PARSED_HTML_PATH
from googletrans import Translator

# Encoding for writing the parsed data to JSONS file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def extract_content_from_page(file_path):
    """
    This function should take as an input the path to one html file
    and return a dictionary "parsed_data" having the following information:

    parsed_data = {
        "date": Date of the news on the html page
        "title": Title of the news on the html page
        "content": The text content of the html page
        }

    This function is used in the parse_html_pages() function.
    You do not need to modify anything in that function.
    """
    parsed_data = {}

    # WRITE YOUR CODE HERE
    ##################################
    
  
            
    soup=bs(open(file_path,'r').read(),'lxml')
    
    #extract them dates
    #manually translating months becouse I want to make sure.
    rep={"enero":"january","febrero":"february","marzo":"march","abril":"april","mayo":"may","junio":"june","julio":"july","agosto":"august","septiembre":"september","octubre":"october","noviembre":"november","diciembre":"december"}
    rep=dict((re.escape(k),v) for k,v in rep.items())
    pattern=re.compile("|".join(rep.keys()))
    
    parsed_data['date']=pattern.sub(lambda m: rep[re.escape(m.group(0))],(soup.find('li',{'itemprop':'datePublished'}).find('span',{'class':'elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date'}).text).strip())
    translator=Translator()
    #extract the title
    txt2=(soup.find('h1',{'class':'elementor-heading-title'}).text).strip()
    txt2=unidecode(txt2)
    result=translator.translate(txt2,src='es',dest='en')
    parsed_data['title']=result.text
    #parsed_data['content']=soup.find('div',{'class':'elementor-element elementor-element-702eb468 elementor-widget elementor-widget-theme-post-content'}).text
    txt3=(soup.find('div',{'class':'elementor-element elementor-element-702eb468 elementor-widget elementor-widget-theme-post-content'}).text).strip()
    txt3=unidecode(txt3)
    ##here since translate function gives error after 5000 chars. we divide the text into chunks of 4500 and translate them. and then we unite them.
    myList=[]
    results=""
    k=0
    limit=len(txt3)/4500
    if(len(txt3)<4500):
        myList.append(txt3)
    while(k<limit):
        myList.append(txt3[k*4500:(k+1)*4500])
        k=k+1
    if(k==limit):
        myList.append(txt3[k*4500:])
    
    for i in range(len(myList)):
        result2=translator.translate(myList[i], src='es',dest='en')
        results+=result2.text
        
    #results.replace('\"',"")
    #results.replace("\n"," ")
    parsed_data['content']=results
    ##################################

    return parsed_data


def parse_html_pages():
    # Load the parsed pages
    parsed_id_list = []
    if os.path.exists(PARSED_HTML_PATH):
        with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
            # Saving the parsed ids to avoid reparsing them
            for line in f:
                data = json.loads(line.strip())
                id_str = data["id"]
                parsed_id_list.append(id_str)
    else:
        with open(PARSED_HTML_PATH, "w", encoding=ENCODING) as f:
            pass

    # Iterating through html files
    for file_name in os.listdir(RAW_HTML_DIR):
        page_id = file_name[:-5]

        # Skip if already parsed
        if page_id in parsed_id_list:
            continue

        # Read the html file and extract the required information

        # Path to the html file
        file_path = os.path.join(RAW_HTML_DIR, file_name)

        try:
            parsed_data = extract_content_from_page(file_path)
            parsed_data["id"] = page_id
            print(f"Parsed page {page_id}")

            # Saving the parsed data
            with open(PARSED_HTML_PATH, "a", encoding=ENCODING) as f:
                f.write("{}\n".format(json.dumps(parsed_data)))

        except Exception as e:
            print(f"Failed to parse page {page_id}: {e}")
        
if __name__ == "__main__":
    parse_html_pages()
