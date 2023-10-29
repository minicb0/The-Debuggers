import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def scrape_url(url, output_dir):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    data = soup.find('div', {'class': 'example-class'}).get_text()

    filename = os.path.join(output_dir, 'data_' + url.replace('/', '_').replace(':', '') + '.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

    driver.quit()

    links = soup.find_all('a')
    for link in links:
        child_url = link.get('href')
        if child_url and child_url.startswith('https://netcontechnologies.com/'):
            scrape_url(child_url, output_dir)

if __name__ == '__main__':
    start_url = 'https://netcontechnologies.com/'  # Replace with the starting URL
    output_directory = 'scraped_data'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    scrape_url(start_url, output_directory)

