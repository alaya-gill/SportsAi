import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

class DataScraper:
    def __init__(self) -> None:
        self.data = {}
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.parser = 'html.parser'
        
    def read_isl_data(self):
        df = pd.read_excel("./scraping/chatgptISL.xlsx")
        # convert into dictionary
        data = df.to_dict()
        for k,v in data.items():
            self.data[k] = list(v.values())
        
        print(data)
    
    def scrape_isl(self):
        links = []
        for i in self.data['Player Name']:
            page = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=" + i
            pageTree = requests.get(page, headers=self.headers)
            pageSoup = BeautifulSoup(pageTree.content, self.parser)
            links.append("https://www.transfermarkt.com"+pageSoup.find('tr', {"class": "odd"}).find('td', {"class": "hauptlink"}).find('a')['href'])
        self.data['Age'] = []
        self.data['DOB'] = []
        self.data['Contract Expires'] = []
        self.data['Contact'] = []
        for link in links:
            page = link
            pageTree = requests.get(page, headers=self.headers)
            pageSoup = BeautifulSoup(pageTree.content, self.parser)
            # for k in pageSoup.find("div", {"class":"info-table info-table--right-space"}).find_all('span',{"class": "info-table__content info-table__content--regular"}):
            #     print(k.text)
            # for k in pageSoup.find("div", {"class":"info-table info-table--right-space"}).find_all('span',{"class": "info-table__content info-table__content--bold"}):
            #     print(k.text)
            
            self.data['Age'].append(pageSoup.find("span", string="Age:").next_sibling.next_sibling.text)
            self.data['DOB'].append(pageSoup.find("span", string="Date of birth:").next_sibling.next_sibling.text)
            self.data['Contract Expires'].append(pageSoup.find("span", string="Contract expires:").next_sibling.next_sibling.text)
            self.data['Contact'].append(pageSoup.find("div",class_="socialmedia-icons").find('a')['href'])
        df = pd.DataFrame(self.data).set_index('Player Name')
        print(df)
        df.to_excel('ISL.xlsx')
            
            
    
obj = DataScraper()
obj.read_isl_data()
obj.scrape_isl()
    
