import load_libs
from bs4 import BeautifulSoup
from urllib2 import urlopen


class DumpITWorld(object):
    
    def __init__(self, url):
        self.url = url
        self.response = self.get_all_articles()
        self.itworld = "http://www.itworld.com"
    
    def get_all_articles(self):
        html = urlopen(self.url).read()
        soup = BeautifulSoup(html, "lxml")
        return soup
    
    def create_request(self, url):
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        return soup
    
    def get_title_articles(self):
        titles = []
        list_with_articles = self.response.find_all('ul', {"class": "tp-list" })
        for article in list_with_articles:
            for title in article.find_all('h3', {"class": "title"}):
                titles.append(title.text)

        return titles
    
    def get_link_articles(self):
        links_articles = []
        list_with_articles = self.response.find_all('ul', {"class": "tp-list" })
        for article in list_with_articles:
            for title in article.find_all('h3', {"class": "title"}):
                for link_article in title.find_all('a', href=True):
                    links_articles.append(link_article['href'])
        
        return links_articles
    
    def get_content_articles(self, articles_links, num_articles):
        title_articles = []
        articles_info = []
        articles_data = {"title_articles": title_articles, "articles_info": articles_info}
        for counter, article_link in enumerate(articles_links):
            
            if counter == num_articles:
                break
            
            response = self.create_request(self.itworld+article_link)
            title = response.find_all('h1', {"id": "article-title"})
            page_counter = response.find_all('div', {"class": "links"})
            
            if page_counter:
                continue
            
            title_articles.append(title[0])
            article_info = response.find_all('div', {"id": "article-content"})
            articles_info.append(article_info[0])
            
        return articles_data
    
    def get_clean_articles(self, num_articles=None):
        articles_data = self.get_content_articles(self.get_link_articles(), num_articles)
        clean_articles = {'articles_info': articles_data['articles_info']}
        
        clean_articles['title_articles'] = articles_data['title_articles']
        merge_title_info = zip(clean_articles['title_articles'], clean_articles['articles_info'])
        return merge_title_info

