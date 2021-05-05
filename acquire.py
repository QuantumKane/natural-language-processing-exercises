# Necessary imports

import requests
import bs4
import os
import pandas as pd

def get_blog_articles(urls, cached=False):
    '''
    This function takes in a url, does a little BeautifulSoup action, 
    creates an empty dictionary and returns that dictionary. 
    '''
    # initialize an empty dictionary
    dict = []
    
    for url in urls:
        headers = {'User-Agent': 'Codeup Data Science'} 
        response = requests.get(url, headers=headers)
        # BeautifulSoup
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



def get_news_articles(cache=False):
    '''
    This function uses a default cache == False to give the option of 
    returning a dataframe of inshorts topics and info by reading a csv file or
    of doing a fresh scrape of inshort pages with topics business, sports, technology,
    and entertainment and writing the returned df to a csv file.
    '''
    # default to read in a csv instead of scrape for df
    if cache == False:
        df = pd.read_csv('articles.csv', index_col=0)
        
    # cache == True completes a fresh scrape for df    
    else:
    
        # Set base_url and headers that will be used in get request

        base_url = 'https://inshorts.com/en/read/'
        headers = {'User-Agent': 'Codeup Data Science'}
        
        # List of topics to scrape
        topics = ['business', 'sports', 'technology', 'entertainment']

        # Create an empty list, articles, to hold our dictionaries
        articles = []

        for topic in topics:

            # Get a response object from the main inshorts page
            response = requests.get(base_url + topic, headers=headers)

            # Create soup object using response from inshort
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

            # Scrape a ResultSet of all the news cards on the page
            cards = soup.find_all('div', class_='news-card')

            # Loop through each news card on the page and get what we want
            for card in cards:
                title = card.find('span', itemprop='headline' ).text
                author = card.find('span', class_='author').text
                content = card.find('div', itemprop='articleBody').text

                # Create a dictionary, article, for each news card
                article = ({'topic': topic, 
                            'title': title, 
                            'author': author, 
                            'content': content})

                # Add the dictionary, article, to our list of dictionaries, articles.
                articles.append(article)
            
        # return it as a DataFrame
        df = pd.DataFrame(articles)
        
        # write df to csv for future use
        df.to_csv('articles.csv')
    
    return df