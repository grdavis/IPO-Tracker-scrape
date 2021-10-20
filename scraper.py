from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import requests

URL = 'https://endpts.com/ipo-tracker/'

def main():
	content = requests.get(URL).content
	soup = BeautifulSoup(content, 'html.parser').find_all('div', {'class':'epn_ipo_card_table_list'})
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

if __name__ == '__main__':
	main()