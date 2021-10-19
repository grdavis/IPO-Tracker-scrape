from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import pandas as pd
from datetime import datetime

URL = 'https://endpts.com/ipo-tracker/'

def get_chrome_data(url, driver):
	driver.get(url)
	return driver.page_source

def new_driver():
	chrome_options = webdriver.ChromeOptions()  
	chrome_options.add_argument("--headless")
	return webdriver.Chrome(options = chrome_options)

def main():
	driver = new_driver()
	data = get_chrome_data(URL, driver)
	soup = BeautifulSoup(data, 'html.parser').find_all('div', {'class':'epn_ipo_card_table_list'})
	all_data = []
	for table in soup:
		row = {}
		row['name'] = table.find('h2').text.replace('\xad', '')
		for item in table.find_all('div', {'class':'col-8'})[1:]:
			row[item.find('span').text] = item.find('h6').text
		for item in table.find_all('div', {'class':'col-4'}):
			row[item.find('span').text] = item.find('h6').text
		all_data.append(row)
	output = pd.DataFrame(all_data)
	output.to_csv('all_data_%s.csv' % str(datetime.today())[:10], index = False)
	driver.quit()

if __name__ == '__main__':
	main()