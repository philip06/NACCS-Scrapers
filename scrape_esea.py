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
    
    # parses generic html table for header data and table data
    def parse_html_table(self, table):
        table_data = []
        table_headers = []
        
        for tr in table.find_all('tr')[1:]:
            table_data.append([td.string.strip() for td in tr.find_all('td') if td.string and td.string.strip() != ""])
            
            table_headers.append([th.string.strip() for th in tr.find_all('th') if th.string and th.string.strip() != ""])
            
        # filter out empty lists
        table_data = [data for data in table_data if data]
        table_headers = [data for data in table_headers if data]

        return table_headers, table_data
    
    # method run on each refresh to collect new data
    def get_scoreboards(self, proxies_dict):
        response = requests.get(self.match_url, headers=self.headers, proxies=proxies_dict)
        page_soup = soup(response.text, "html.parser")
        page_soup = page_soup.find("div", {"id": "stats-match-view"})# {"class": "match-header"})
        # list of all tables within div wrapper
        table_list = page_soup.find_all("table")
        
        # # translate soup objects to unicode
        # table_list = [x.text for x in table_list]
        
        ret_json = {}
        
        period_headers, period_body = [], []
        stats_headers, stats_body = [], []
        
        # filter html tables by type
        for table in table_list:
            # filter for data from period table
            if table.find(text=re.compile("Period Scores")):
                period_headers, period_body = self.parse_html_table(table)
            
            # filter for data from stats tables
            elif table.find(text=re.compile("Statistics")):
                stats_headers, temp_body = self.parse_html_table(table)
                stats_body.append(temp_body)
        
        # pprint(period_body)
        # pprint(stats_headers)
        
        team_captains = []
        period_headers_filtered = []
        
        # pull out team captain names from period headers
        for h in period_headers:
            if len(h) == 1:
                team_captains.append(h[0])
            else:
                period_headers_filtered = h
                
        # generate data structure to be converted into json
        for i, name in enumerate(team_captains):
            ret_json["stats_table_team"+str(i)] = {"captain": name, "headers": stats_headers[0], "body": stats_body[i]}
            # add period table data
            ret_json["period_table"] = {"headers": period_headers_filtered, "body": period_body}
        
        pprint(json.dumps(ret_json))

req_url = "https://play.esea.net/match/14570353"
proxies_dict = {
                    "http": "35.245.183.119:3128"
                }
        
s = Scoreboard(req_url)
s.get_scoreboards(proxies_dict)
# proxy = get_proxy(retry_count=1)