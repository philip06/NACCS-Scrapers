import requests
import re
import logging
import json
from bs4 import BeautifulSoup as soup
from pprint import pprint
    
# class used to pull in fresh data at given interval (seconds)
class Scoreboard:
    def __init__(self, match_url):
        self.scoreboard_log = logging.getLogger("scoreboard_log")
        logging.basicConfig(filename='scoreboard.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        
        self.match_url = match_url
        
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
        self.headers = {
            "User-Agent": user_agent
        }

    # method to automatically pull in a fresh proxy
    def get_proxy(self, retry_count=2):
        req_url = "https://gimmeproxy.com/api/getProxy"
        while retry_count >= 0:
            try:
                ret_body = requests.get(req_url).text
                ret_json = json.loads(ret_body)
                ip_port = ret_json["ipPort"]
                protocol = ret_json["protocol"]
                return {protocol: ip_port}
            except Exception as e:
                self.scoreboard_log.warning(e)
                retry_count -= 1
    
    # parses generic html table for header data and table data
    def parse_html_table(self, table):
        table_data = []
        table_headers = []
        
        try:
            # filter table rows and headers into lists
            for tr in table.find_all('tr')[1:]:
                table_data.append([td.string.strip() for td in tr.find_all('td') if td.string and td.string.strip() != ""])
                
                table_headers.append([th.string.strip() for th in tr.find_all('th') if th.string and th.string.strip() != ""])
                
            # filter out empty lists
            table_data = [data for data in table_data if data]
            table_headers = [data for data in table_headers if data]
    
            return table_headers, table_data
        except Exception as e:
            self.scoreboard_log.error(e)
            return "Error"
    
    # method run on each refresh to collect new data
    def get_scoreboards(self, proxy_retry_count=2):
        try:
            proxies_dict = self.get_proxy()
            response = requests.get(self.match_url, headers=self.headers, proxies=proxies_dict)
            page_soup = soup(response.text, "html.parser")
            page_soup = page_soup.find("div", {"id": "stats-match-view"})
            
            # list of all tables within div wrapper
            table_list = page_soup.find_all("table")
            
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
                ret_json["period_table_team"+str(i)] = {"captain": name, "headers": period_headers_filtered, "body": period_body[i]}
            
            self.output_json = json.dumps(ret_json)
            return json.dumps(ret_json)
        except Exception as e:
            self.scoreboard_log.error(e)
            return "Error"

if __name__ == "__main__":
    req_url = "https://play.esea.net/match/14570353"
    
    proxies_dict = {
                        "http": "35.245.183.119:3128"
                    }
            
    s = Scoreboard(req_url)
    scoreboard_json = s.get_scoreboards()
    pprint(scoreboard_json)