import load_libs
from bs4 import BeautifulSoup
from urllib2 import urlopen
from dump_article.social_utils import SocialUtilsNew


class DumpITWorld(object):
    
    def __init__(self, url):
        self.url = url
        self.response = self.get_all_articles()
        self.itworld = lambda link: "http://www.itworld.com"+link
    
    def get_all_articles(self):
        """
        Get all articles and return response
        """
        html = urlopen(self.url).read()
        soup = BeautifulSoup(html, "lxml")
        return soup
    
    def create_request(self, url):
        """
        Get currrent request(article) and return response
        """
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        return soup
    
    def get_title_articles(self, num_titles=None):
        """
        Get titles only
        """
        titles = []
        list_with_articles = self.response.find_all('ul', {"class": "tp-list" })
        for counter, article in enumerate(list_with_articles):
            if num_titles == counter:
                break 
            for title in article.find_all('h3', {"class": "title"}):
                titles.append(title.text)

        return titles
    
    def get_link_articles(self):
        """
        Get link from current request
        get link from all titles
        """
        links_articles = []
        list_with_articles = self.response.find_all('ul', {"class": "tp-list" })
        for article in list_with_articles:
            for title in article.find_all('h3', {"class": "title"}):
                for link_article in title.find_all('a', href=True):
                    links_articles.append(link_article['href'])
        
        return links_articles
    
    def get_content_articles(self, articles_links, num_articles):
        """
        Get content from current articles
        """
        title_articles = []
        articles_info = []
        articles_data = {"title_articles": title_articles, "articles_info": articles_info}
        for counter, article_link in enumerate(articles_links):
            
            if counter == num_articles:
                break
            response = self.create_request(self.itworld(article_link))
            title = response.find_all('h1', {"id": "article-title"})
            page_counter = response.find_all('div', {"class": "links"})
            article_info = response.find_all('div', {"id": "article-content"})

            if page_counter:
                article_info[0].append(self.__get_continue_article(page_counter))
            
            title_articles.append(title[0])
            articles_info.append(article_info[0])
            
        return articles_data
    
    def __get_continue_article(self, div_links):
        """
        Get content from other pages on current article
        """
        link = div_links[0].find_all('li', {'class': 'pager-next'})
        next_link = link
        if not next_link:
            return ""
        link = link[0].find_all('a', href=True)
        
        response = self.create_request(self.itworld(link[0]['href']))
        content = ""
        
        article_info = response.find_all('div', {"id": "article-content"})
        page_counter = response.find_all('div', {'class': 'links'})
        
        if page_counter:
            content = self.__get_continue_article(page_counter)
        
        if content:
            article_info[0].append(content)
        
        return article_info[0]
    
    def get_clean_articles(self, num_articles=None):
        """
        Get clean article and merge content and title
        """
        articles_data = self.get_content_articles(self.get_link_articles(), num_articles)
        clean_articles = {'articles_info': articles_data['articles_info']}
        
        clean_articles['title_articles'] = articles_data['title_articles']
        merge_title_info = zip(clean_articles['title_articles'], clean_articles['articles_info'])
        return merge_title_info
    
    def get_popular_articles_titles(self, num_titles=None, reverse=False):
        """
        Get Popular titles compared fasebook likes
        """
        list_with_articles = self.response.find_all('ul', {"class": "tp-list" })
        titles = []
        fb_likes = []
        for counter, article in enumerate(list_with_articles):
            if num_titles == counter:
                break 
            for title in article.find_all('h3', {"class": "title"}):
                for title_link in title.find_all('a', href=True):
                    titles.append(title.text)
                    fb_likes.append(SocialUtilsNew().counter_likes(self.itworld(title_link['href']))['Facebook']['like_count'])
        articles_title = zip(fb_likes, titles)
        if reverse:
            articles_title.sort(reverse=True)
        else:
            articles_title.sort()
        articles_title = self.__get_only_titles(articles_title)
        
        return articles_title
    
    def __get_only_titles(self, likes_and_titles):
        """
        Get only title from popular articles
        """
        populate_titles = []
        for like, titles in likes_and_titles:
            populate_titles.append(titles)
        
        return populate_titles
    
    def __get_only_links(self, likes_and_links):
        """
        Get only links from popular articles
        """
        populate_links = []
        for like, titles in likes_and_links:
            populate_links.append(titles)
        
        return populate_links
    
    def __get_populate_links(self, num_links=None, reverse=False):
        """
        Get populate links
        """
        list_with_articles = self.response.find_all('ul', {"class": "tp-list" })
        links = []
        fb_likes = []
        for counter, article in enumerate(list_with_articles):
            if num_links == counter:
                break 
            for title in article.find_all('h3', {"class": "title"}):
                for title_link in title.find_all('a', href=True):
                    links.append(title_link['href'])
                    fb_likes.append(SocialUtilsNew().counter_likes(self.itworld(title_link['href']))['Facebook']['like_count'])
        
        links = zip(fb_likes, links)
        if reverse:
            links.sort(reverse=True)
        else:
            links.sort()
        links = self.__get_only_links(links)
        return links
    
    def get_popular_articles(self, num_articles=None, reverse=False):
        """
        Get popular articles (titles, content)
        """
        sort_links = self.__get_populate_links(num_articles, reverse)
        articles_titles = self.get_content_articles(sort_links, num_articles)
        articles = articles_titles['articles_info']
        titles = articles_titles['title_articles']
        merge_title_info = zip(titles, articles)
        return merge_title_info