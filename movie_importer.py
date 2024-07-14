import requests
from bs4 import BeautifulSoup
import re

class ReviewFetcher:
    
    def __init__(self,username) -> None:
        self.username = username
        self.pageNum = 1
        

    def clean_text(self,text):
        return re.sub(r'\s+', ' ', text).strip()
    
    def get_watched_movies_for_page(self,page):

        if page > 1:
            url = f"https://letterboxd.com/{self.username}/films/diary/page/{page}/"
        else:
            url = f"https://letterboxd.com/{self.username}/films/diary/"
        print(url)

        try:
            response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        except requests.exceptions.Timeout:
            print(f"Request timed out for page {page}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        
        movies = []
        for entry in soup.find_all('tr', class_='diary-entry-row'):
            movie_title = self.clean_text(entry.find('h3').get_text(strip=True))
            review_tag = entry.find('a', class_='edit-review-button')
            review = ""
            if review_tag and 'data-review-text' in review_tag.attrs:
                review = review_tag['data-review-text'].strip()
            movies.append({'title': movie_title, 'review': review})
        return movies

    def get_all_movies(self):
        all_pages = {}
        while True:
            responseMovie = self.get_watched_movies_for_page(self.pageNum)
        
            if not responseMovie:
                break
            all_pages[self.pageNum] = responseMovie
            self.pageNum += 1

        return all_pages






    