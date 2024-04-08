"""Forked from https://github.com/NicholasMontalbano/apt_finder_streeteasy_scrape/blob/main/scripts/01_streeteasy.py.
"""
import requests
from bs4 import BeautifulSoup
import re
import csv
import time

class StreetEasyScraper(): 
    results = []
    # developer tools -> network -> name=url -> request headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Cookie': 'g_state=; _actor=eyJpZCI6ImRkbXZHUDNzcnJhb25CSWV1ZHdod2c9PSJ9--59a52d02856db5edb8c67d152a153dd1ebc712e7; _se_t=352d0a4d-c428-432e-9d0c-4da50d39a258; _gcl_au=1.1.836853459.1712532396; _ga=GA1.2.871353341.1712532396; _gid=GA1.2.847992196.1712532396; zjs_user_id=null; zg_anonymous_id=%228e33101d-83c9-4bbd-b88b-22c77ab57ebf%22; __spdt=2070c27d391d4199a8519b3ceb7edba2; zjs_anonymous_id=%22352d0a4d-c428-432e-9d0c-4da50d39a258%22; _fbp=fb.1.1712532396933.1196130482; google_one_tap=0; _pin_unauth=dWlkPU5UZGlNR05tTTJFdFltVmpNUzAwTXprMUxUa3dNamt0WldZd01EZzVOVGhqTWpZMA; post_views=2; ezab_uds_srp_tabs=test; ezab=%7B%22uds_srp_tabs%22%3A%22test%22%7D; savedZoom=11; windowWidth=2560; windowHeight=1294; pxcts=130f4c0b-f540-11ee-86a1-f830614d910b; _pxvid=130f3e7c-f540-11ee-86a1-649b631ae05b; __gads=ID=cc157cf23a0c9f94:T=1712532396:RT=1712536604:S=ALNI_Mau6KvWfK1ze7_lL3Gu5_A8UOJAcw; __gpi=UID=00000a1b62f05254:T=1712532396:RT=1712536604:S=ALNI_MbnihALSES2h7FVZYWNcmPP3phW7Q; __eoi=ID=c653af8218b50e18:T=1712532396:RT=1712536604:S=AA-AfjaLRUePBaAxijFAnkS9iCxF; tfpsi=9b826e6c-8f46-4a6b-8b72-d45f0aa97adc; savedMapDataInRect=null; savedMapDataCenterLat=40.712041; savedMapDataCenterLong=-73.868061; savedMapDataZoom=11; recent_searches=%5B%2245%7C1712536615%22%2C%222405662%7C1712536610%22%5D; _dc_gtm_UA-122241-1=1; g_state=; _rdt_uuid=1712532396489.d0414b1c-c273-41c9-af98-e3e9168c2144; _px3=f800ab9af6dbfa57cfc116613aafc582f7b0f2b402c3ad7eee3de9ceb151d316:8uxOuZEJEkTQZiLEnfHRQqslYZW0XUkNHiSS92UPM+m88U+ZA1b7R5IToymMuJWjjFtx7o8wfeXe193FqylypA==:1000:Cl/1wrcOiiPWIaZ0h5Xb2L4WHOTvuct0l/UhKu1kgL+9S4vUPVtrfw2jmogB30eT8Y/h7i58bGKhrH9pItaSWe6apb2/qj1ilLPykJgk1I+qw28eMqK1OKQY3Z96bYEjNIwr01c2loAyAcrHIqEaek20hEELlt9ZgoYhrbcZZutK4g2bPfMK6ZSpevVrJQegMcgKOYLYmKD59R36b64NX+1mffe0HUSlRVHoMbDN5z8=; last_search_tab=rentals; _ga_L14MFV0VR8=GS1.2.1712535882.2.1.1712537621.33.0.0; se_lsa=2024-04-07+20%3A53%3A41+-0400; anon_searcher_stage=initial; _ses=VDYyTDZ2L0xBSEhCYzlxVVMzZGJodjE2Yjd3ZUlZcmlvamwyc0lrYWREZTg1NW81VzVwTE9HcStNdHgzUklMc1VKNEE4OTBlaSsrdkhWTmI2eG41VWxhaFRZekRWQ3dQTmNSZlFxN2JPM1dEeDZwZVpyYkF5K1RRKzJVVDlMTm13YkZGQkNtcXNPZG9OMU9uSCtqK29LQzA5c1lub2NnL1YzNjBndWY1SHYxOTBXZWJFS0ozUWp1bHBxU1BRZjdQeVpEZkNTblJtVHJ5Z1BjOHFucytJamxBOU5HWFg2T0JyRk1NY3BZY1Aya2hLSE4rblFmQUZ6YTcwSDR3VnJMNlEzM1BYS0t5V2JrZGQyQVJhT3pPYlFQaWhlOWMyUis4dk9IK3VzckpycXlIZDdaU3N6YS9UeXlXZmQ1VzBjRlNIT1pmdi95a01vZmgvTmM4NWIzNzgyUUNOQ3NFbGtUZEdPZEJXWmY3Qm1JNytLOWJOTkY4aE9GRFdxQVNiTGoyL3lITlJsN3hkdFBqMkk1ekRUYVQ2c0pXNVFMY3BLYUFSSmpVUkdUY0toekY2dEl2dHE1N0pMVGI5cjA1eHBKODZMb25XdHpIMlE5NW56TmsreWtUbjgwVHBpNjFzZWFXQjRaRkIxSDBCQXRiaGNxazZiRU1NaUpDU3JRRUZjS2FlVGg4cnpXUEdMWFVSZHpLbTdqSzRnPT0tLXhxOTlPOWJ6Mmx2YWsvWk9XZCs3RUE9PQ%3D%3D--915eb0b9767a52b4384b48a888053a0740a1edef',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
        }
    # default pages is 1
    max_page = 1

    def fetch(self, url):
        response = requests.get(url, headers=self.headers)
        print(response)
        return(response)

    # parses the first webpage to find the total number of pages to be scraped
    def parse_pagenum(self, response):
        content = BeautifulSoup(response, features="lxml")
        deck = content.find('ul', {'class': 'pagination-list-container'})
        page_nums = []
        for card in deck.select('li'): 
            if card.a is not None: 
                page = card.a.text if re.search("[0-9]", card.a.text) else 0
            else: 
                page = 0
            
            page_nums.append(page)
        self.max_page = max([int(item) for item in page_nums])
        print("num pages:", self.max_page)
    
    # parses each page to pull type, beds, baths, url, etc. 
    def parse(self, response):
        content = BeautifulSoup(response, features="lxml")
        deck = content.find('ul', {'class': 'searchCardList'})

        for card in deck.select('li'):
            # type and neighborhood
            type_neighborhood = card.find('div', {'class': 'listingCard listingCard--rentalCard jsItem'})
            if not type_neighborhood:
                continue
            type_neighborhood = type_neighborhood.span.text
            type = re.search("(.+) in", type_neighborhood).group(1) if re.search("(.+) in", type_neighborhood) else 'NA'
            neighborhood = re.search("in (.+) at", type_neighborhood).group(1) if re.search("in (.+) at", type_neighborhood) else 'NA'
            # address and url
            address_url = card.find('address', {'class': 'listingCard-addressLabel listingCard-upperShortLabel'}) 
            address = address_url.a.text if address_url else 'NA'
            url = address_url.a['href'] if address_url else 'NA'
            # price
            price = card.find('div', {'class': 'listingCardBottom-emphasis'}).span.text if card.find('div', {'class': 'listingCardBottom-emphasis'}) else 'NA'
            # beds, baths, sqft
            beds_bath_sqft = card.find_all('div', {'class': 'listingDetailDefinitionsItem'})
            if len(beds_bath_sqft)==3:
                beds = beds_bath_sqft[0].find('span', {'class':'listingDetailDefinitionsText'}).text if beds_bath_sqft[0].find('span', {'class':'listingDetailDefinitionsText'}) else 'NA'
                baths = beds_bath_sqft[1].find('span', {'class':'listingDetailDefinitionsText'}).text if beds_bath_sqft[1].find('span', {'class':'listingDetailDefinitionsText'}) else 'NA'
                sqft = re.search("[0-9]+", beds_bath_sqft[2].find('span', {'class':'listingDetailDefinitionsText'}).text).group(0) if beds_bath_sqft[2].find('span', {'class':'listingDetailDefinitionsText'}) else 'NA'
            elif len(beds_bath_sqft)==2:
                beds = beds_bath_sqft[0].find('span', {'class':'listingDetailDefinitionsText'}).text if beds_bath_sqft[0].find('span', {'class':'listingDetailDefinitionsText'}) else 'NA'
                baths = beds_bath_sqft[1].find('span', {'class':'listingDetailDefinitionsText'}).text if beds_bath_sqft[1].find('span', {'class':'listingDetailDefinitionsText'}) else 'NA'
                sqft = 'NA'
            elif len(beds_bath_sqft)==1:
                beds = beds_bath_sqft[0].find('span', {'class':'listingDetailDefinitionsText'}).text if beds_bath_sqft[0].find('span', {'class':'listingDetailDefinitionsText'}) else 'NA'
                baths = 'NA', 
                sqft = 'NA'
            else:
                beds = 'NA'
                baths = 'NA'
                sqft = 'NA'

            # combine into dictionary
            self.results.append({
                    'type': type,
                    'neighborhood': neighborhood,
                    'address': address, 
                    'price': price,
                    'beds': beds, 
                    'baths': baths, 
                    'sqft': sqft,
                    'url': url
            })

    def to_csv(self):
        with open('data/streeteasy.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        url = 'https://streeteasy.com/for-rent/nyc/price:-2400%7Carea:336,331,310,334,306,338,305,321,364,322,328,325,307,303,332,304,320,301,367,340,339,365,319,326,329,355,318,323,302,324,102,119,139,135,155,148,147,165,149,153,401,416,415,424,420,402,411,414,403,404%7Cbeds%3C=1%7Camenities:laundry?page=1'
        res = self.fetch(url)
        self.parse_pagenum(res.text)
        time.sleep(3)

        for page in range(1,self.max_page + 1):
            url = f'https://streeteasy.com/for-rent/nyc/price:-2400%7Carea:336,331,310,334,306,338,305,321,364,322,328,325,307,303,332,304,320,301,367,340,339,365,319,326,329,355,318,323,302,324,102,119,139,135,155,148,147,165,149,153,401,416,415,424,420,402,411,414,403,404%7Cbeds%3C=1%7Camenities:laundry?page={page}'
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(3)
        self.to_csv()


    
if __name__ == '__main__':
    scraper = StreetEasyScraper()
    scraper.run()
