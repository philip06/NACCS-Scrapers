import requests
import re
from bs4 import  BeautifulSoup as soup
from pprint import pprint

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'

headers = {
    "User-Agent": user_agent
}


def get_matches(req_url):
    response = requests.get(req_url, headers=headers)
    pprint(response.text)
    page_soup = soup(response.text, "html.parser")
    # uses class searching in bs4 to find and parse table
    matches = page_soup.find("table", {"class": "club-recent-matches-table"})
    match_ids = []

    # regex filtering to remove html
    for match in matches:
        match_ids.append(re.findall("href=\"(.*?)\">", str(match))[0])

    return matches
    
# class Scoreboard:
#     def __init__(self, monitor_url):

def get_proxy(retry_count):
    req_url = "http://pubproxy.com/api/proxy"
        

def get_scoreboards(req_url):
    response = requests.get(req_url, headers=headers)
    page_soup = soup(response.text, "html.parser")
    page_soup = page_soup.find("div", {"id": "stats-match-view"})# {"class": "match-header"})
    # list of all tables within div wrapper
    table_list = page_soup.find_all("table")
    # translate soup objects to unicode
    table_list = [x.text for x in table_list]
    
    def parse_period_scores(inner_soup):
        return inner_soup.find()
        
    # def parse_regex(reg, table):
    #     re_sequence = re.compile(reg, re.MULTILINE)
        
    for table in table_list:
        

req_url = "https://play.esea.net/match/14570353"

get_scoreboards(req_url)