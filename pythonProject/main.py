import requests
from bs4 import BeautifulSoup
import csv


def check_hreflang(url, target_hreflang):
    sitemap_url = "https://www.listerine.com/sitemap.xml"
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'lxml')

    for url_entry in soup.find_all('url'):
        loc = url_entry.find('loc').text
        if loc == url:
            for link in url_entry.find_all('xhtml:link'):
                if link.get('rel') == 'alternate' and link.get('hreflang') == target_hreflang:
                    print(f"URL: {url} - Hreflang found")
                    result = "Hreflang found"
                    break  # Exit the inner loop once hreflang is found
                else:
                    result = "Hreflang not found"
            with open('hreflang_results.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([url, result])
            return  # Exit the function after writing to CSV


# Read your list of URLs
with open('ur_list.txt', 'r') as f:
    for line in f:
        url = line.strip()
        check_hreflang(url, 'en-US')
