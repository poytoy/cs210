import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

from config import LINK_LIST_PATH

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t",error_bad_lines=False)
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()
    print(start_page,downloaded_url_list)
    # WRITE YOUR CODE HERE
    #########################################
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)
    rootURL="https://mirex.gob.do/en/noticias/page/" #add page
    for pid in range(start_page,57):
        pageURL='{}{}'.format(rootURL,pid)
        print(pageURL)
        
        resp=requests.get(pageURL)
        #print(resp.text)
        soup=bs(resp.text,'lxml')
        #print(soup)
        
        for item in soup.find_all("article",{"class":"elementor-post"}):
            
        # Save the collected url in the variable "collected_url"
            collected_url = item.find('div').find('a')['href']
            
            collected_url=collected_url.replace("https://mirex.gob.do/noticias/page/","https://mirex.gob.do/en/noticias/page/")
            # Save the page that the url is taken from in the variable "page"
            page = pid

        # The following code block saves the collected url and page
        # Save the collected urls one by one so that if an error occurs
        # you do not have to start all over again
            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, page)
        #########################################


if __name__ == "__main__":
    download_links_from_index()
