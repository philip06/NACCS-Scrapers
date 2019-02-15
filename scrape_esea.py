import requests
import re
import json
from bs4 import BeautifulSoup as soup
from pprint import pprint
    
# class used to pull in fresh data at given interval (seconds)
class Scoreboard:
    def __init__(self, match_url, refresh_rate=5):
        self.match_url = match_url
        self.refresh_rate = refresh_rate
        
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
        self.headers = {
            "User-Agent": user_agent
        }
    
    # method to create feed updated at set interval
    # TODO
    def get_data_feed(self):
        print("get_data_feed")

    # method to pull in a fresh proxy
    # TODO
    def get_proxy(self, retry_count=1):
        req_url = "http://pubproxy.com/api/proxy"
        while retry_count >= 0:
            ret_body = requests.get(req_url).text
            pprint(ret_body)
            ret_json = json.loads(ret_body)
            pprint(ret_json["ip"])
            break
    
    def parse_html_table(self, table):
        table_data = []
        table_headers = []
        
        for tr in table.find_all('tr')[1:]:
            table_data.append([td.string.strip() for td in tr.find_all('td') if td.string and td.string.strip() != ""])
            
            table_headers.append([th.string.strip() for th in tr.find_all('th') if th.string and td.string.strip() != ""])
            
        pprint(table_data)
        pprint(table_headers)
        return table_data
    
    # method run on each refresh to collect new data
    def get_scoreboards(self, proxies_dict):
        response = requests.get(self.match_url, headers=self.headers, proxies=proxies_dict)
        page_soup = soup(response.text, "html.parser")
        page_soup = page_soup.find("div", {"id": "stats-match-view"})# {"class": "match-header"})
        # list of all tables within div wrapper
        table_list = page_soup.find_all("table")
        
        # # translate soup objects to unicode
        # table_list = [x.text for x in table_list]
        
        period_table = []
        
        def parse_period_scores(inner_soup):
            period_table = self.parse_html_table(inner_soup)
            
        for table in table_list:
            if table.find(text=re.compile("Period Scores")):
                parse_period_scores(table)
                pprint(period_table)
                break

req_url = "https://play.esea.net/match/14570353"
proxies_dict = {
                    "http": "35.245.183.119:3128"
                }
        
s = Scoreboard(req_url)
s.get_scoreboards(proxies_dict)
# proxy = get_proxy(retry_count=1)