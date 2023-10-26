import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.parse import urlparse
def fetch_and_store_data(url, domain_name, db):
    response = requests.get(url)
    if response.status_code == 200:
        print(f'Request successful for URL: {url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', {'class': 'row'})
        name_servers = []
        ip_addresses = []
        for div in divs:
            text = div.get_text()
            if "Name Servers" in text:
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith("ns"):
                        name_servers.append(line)
                    elif line.count('.') == 3:
                        ip_addresses.append(line)
        data = {
            "Domain Name": domain_name,
            "Name Servers": name_servers,
            "IP Addresses": ip_addresses
        }
        db.insert_one(data)
        print(f'Data inserted for URL: {url}')
    else:
        print(f'Failed to retrieve data for URL: {url}. Status code:', response.status_code)
def main():
    client_page = MongoClient('mongodb://localhost:27017/')
    db_page = client_page['page_data']
    collection_page = db_page['page_data']
    while True:
        hostname = input("Enter the hostname (e.g., google.com): ")
        if not hostname:
            break
        url = f'https://who.is/whois/{hostname}'
        domain_name = hostname
        fetch_and_store_data(url, domain_name, collection_page)
        time.sleep(1)
    client_page.close()
if __name__ == "__main__":
    main()
