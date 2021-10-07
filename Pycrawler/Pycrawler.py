import requests
import re
from urllib.parse import urlparse
import os
from time import sleep
from fake_useragent import UserAgent



#class to house the functions
class Pycrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.visited = set()

    #send request for html layout of page
    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return " "
        return html.content.decode('latin-1')

    #gets links from page
    def get_links(self,url):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html) 
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base +link
                links[i] = link_with_base
        
        return set(filter(lambda x: 'mailto' not in x, links))
        


#extracts the infomation from the webpage
    def extract_info(self, url):
        html = self.get_html(url)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)
        sleep(20)
        return dict(meta)
    

    #sets up crawler 
    def crawler(self, url):
        for link in self.get_links(url):
            if link in self.visited:
                continue
            self.visited.add(link)
            info = self.extract_info(link)
            
            print(f"""Link: {link}    
Description: {info.get('description')}    
Keywords: {info.get('keywords')}    
            """)    

            self.crawler(link)

    
    def start(self):
        self.crawler(self.starting_url)


if __name__ == "__main__":
    crawler = Pycrawler("https://www.reddit.com/")
    crawler.start()