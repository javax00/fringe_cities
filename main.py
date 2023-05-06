# if[city], [state1]

# City of [name]
	# if United States, [texas]
# if[name], if[state]
	# FeatureType : city

# [name] + is a city
# The City of [name]
# [name] + is an unincorporated community
# [name] + is a census-designated
# city profile

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from datetime import datetime
from time import sleep
from csv import writer
import pandas as pd
import pycountry
import requests
import gspread
from bs4 import BeautifulSoup
from dateutil.parser import parse
from fake_useragent import UserAgent
import platform
import random
import math
import pytz
import json
import pytz
import time
import json
import glob
import os
from checkData.getESIID import *

filename = 'A - San Antonio'

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def accessLink():
	again = True
	while again == True:
		try:
			ua = UserAgent()

			prefs = {
				"download.open_pdf_in_system_reader": False,
				"download.prompt_for_download": True,
				"download.default_directory": "/dev/null",
				"plugins.always_open_pdf_externally": False,
				"download_restrictions": 3
			}

			options = Options()
			# options.add_argument("--headless")
			options.add_argument('--no-sandbox')
			options.add_argument('--disable-gpu')
			options.add_argument('--start-maximized')
			options.add_argument('--disable-infobars')
			options.add_argument('--disk-cache-size=0')
			options.add_argument('--disable-extensions')
			options.add_argument('--disable-dev-shm-usage')
			options.add_argument("--disable-blink-features")
			options.add_argument('--disable-browser-side-navigation')
			options.add_argument('--ignore-certificate-errors-spki-list')
			options.add_argument('--disable-blink-features=AutomationControlled')
			options.add_experimental_option("prefs", prefs)
			options.add_experimental_option('useAutomationExtension', False)
			options.add_experimental_option("excludeSwitches", ["enable-automation"])
			options.add_experimental_option('excludeSwitches', ['enable-logging'])
			options.add_argument('--log-level=3')


			options.add_argument("window-size="+str(random.randint(1000, 2000))+","+str(random.randint(600, 1050)))
			options.add_argument(f'--user-agent={ua.random}')
			options.add_argument(f'user-agent={ua.random}')

			caps = DesiredCapabilities().CHROME
			caps["pageLoadStrategy"] = "normal" #or "eager" or "none"

			driver = webdriver.Chrome(options=options, desired_capabilities=caps, service=Service(ChromeDriverManager().install()))
			driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
			driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})

			stealth(driver,
					languages=["en-US", "en"],
					vendor="Google Inc.",
					platform="Win32",
					webgl_vendor="Intel Inc.",
					renderer="Intel Iris OpenGL Engine",
					fix_hairline=True)
			again = False
		except Exception as e:
			print(str(e))
			again = True

	driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f'{ua.random}'})
	return driver

df = pd.read_csv(filename+'.csv', low_memory=False)

cities = []
for i in df.index:
	temp = []
	for x in df:
		if x == 'CITY':
			if str(df[x][i]) == 'nan':
				temp.append('')
			else:
				temp.append(str(df[x][i]))
		elif x == 'STATE 1':
			if str(df[x][i]) == 'nan':
				temp.append('')
			else:
				temp.append(str(df[x][i]))
		elif x == 'STATE 2':
			if str(df[x][i]) == 'nan':
				temp.append('')
			else:
				temp.append(str(df[x][i]))
		elif x == 'AREA':
			if str(df[x][i]) == 'nan':
				temp.append('')
			else:
				temp.append(str(df[x][i]))
		elif x == 'COLOR':
			if str(df[x][i]) == 'nan':
				temp.append('')
			else:
				temp.append(str(df[x][i]))
	cities.append(temp)


filepathHeaderCSV = filename+' - Final.csv'
fHeaderCSV = ['City', 'All House Count', 'Area', 'Data Y/N']
try:
	os.remove(filepathHeaderCSV)
	time.sleep(1)
except Exception as e:
	pass
append_list_as_row(filepathHeaderCSV, fHeaderCSV)


driver = accessLink()
for city in cities:
	print(str(cities.index(city)+1)+'/'+str(len(cities))+' - '+city[0])

	driver.get('https://places.us.com/'+city[1]+'/'+city[0])
	time.sleep(2)

	tot_hh,area,data = 'N/A','',''

	if 'Error 404' in driver.find_element(By.TAG_NAME, 'body').text:
		city[0]+', '+city[1]
	else:
		tot_pop = int(driver.find_elements(By.TAG_NAME, 'strong')[0].text.replace(',',''))

		per_hhs = driver.find_element(By.ID, 'details-data').text.split('\n')
		for hh in per_hhs:
			if 'Average # of People Per Household' in hh:
				per_hh = float(hh.split(' : ')[1])

		tot_hh = int(tot_pop/per_hh)

	if city[3] != '':
		area = city[3]+' - '+city[4]
	else:
		area = city[4]

	driver.get('https://www.homes.com/')
	driver.find_element(By.CLASS_NAME, 'multiselect-search').send_keys('')
	driver.find_element(By.CLASS_NAME, 'multiselect-search').send_keys(city[0]+', '+city[2])
	time.sleep(1)
	driver.find_element(By.CLASS_NAME, 'multiselect-search').send_keys(Keys.ENTER)
	time.sleep(2)


	try:
		h_add = driver.find_elements(By.CLASS_NAME, 'property-name')[0].text.split(' ')[:-1]
		esiid = getESIID(' '.join(h_add).upper())
		data = 'Yes'
	except Exception as e:
		data = 'No'

	append_list_as_row(filepathHeaderCSV, [city[0], tot_hh, area, data])
driver.quit()