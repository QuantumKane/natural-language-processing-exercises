# Necessary imports

import requests
import bs4
import os
import pandas as pd

def get_blog_articles(urls, cached=False):
    '''
    This function takes in a url and returns a dictionary. 
    '''
    # initialize an empty dictionary
    dict = []
    
    for url in urls:
        headers = {'User-Agent': 'Codeup Data Science'} 
        response = requests.get(url, headers=headers)
        # 
        soup = bs4.BeautifulSoup(response.text)
        website = soup.find('div', class_='jupiterx-post-content')
        
        # creates empty dictionary
        website_dict = {'title':[], 'content':[]}
        # adds title to dictionary
        website_dict['title'] = soup.title.string
        # adds content to dictionary
        website_dict['content'] = website.text
        
        # adds this dict to the url list
        dict.append(website_dict)
        
    # make it a dataframe
    dict = pd.DataFrame(dict)
    
    return dict