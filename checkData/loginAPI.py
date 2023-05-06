from unittest import result
import requests
import sys
# import library
import logging

import os
import json
import pathlib
from os import path
# from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
# from openpyxl import load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from supabase import create_client, Client
url = 'https://btfrfcjlmnkkestzuwdz.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0ZnJmY2psbW5ra2VzdHp1d2R6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE0Nzk1MjYsImV4cCI6MTk4NzA1NTUyNn0.rTw6kZQpRf_FjPTAWYt_ymdhamF6fF0Ktsu6joMLsag'
supabase: Client = create_client(url, key)

urlSmartMeter = "https://www.smartmetertexas.com/home"

DefaultHeader = {
		"accept": "application/json, text/plain, */*",
		"accept-language": "en-US,en;q=0.9",
		"cache-control": "no-cache",
		"content-type": "application/json;charset=UTF-8",
		"origin": "https://www.smartmetertexas.com",
		"pragma": "no-cache",
		"referer": "https://www.smartmetertexas.com/home",
		"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"Windows"',
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
	}



file_path = pathlib.Path('login.json')
def constructSession():
	if not file_path.is_file():
		return login()
	else:
		with file_path.open() as open_file:
			json_data = json.load(open_file)
		s = requests.Session()
		for name, value in json_data["cookies"].items():
			s.cookies.set(name, value)
		s.headers.update({
			"authorization": "Bearer " + json_data["token"]
		})
		s.headers.update(DefaultHeader)
		testRequestData = {
			"esiid": "*"
		}
		try:
			r = s.post('https://www.smartmetertexas.com/api/meter', json=testRequestData, timeout = 5)
		except:
			return login()
		if r.status_code != 200:
			return login()
		return s


def login(attempts = 2):
	if attempts <= 0:
		raise ValueError("Failed to Login after multiple attempts")
	print("LOGIN CALLED")
	# chromedriver
	path = "chromedriver.exe"
	chrome_options = Options()
	# chrome_options.add_argument("--headless")
	userAgent = "Chrome/96.0.4664.45"
	chrome_options.add_argument(f"user-agent={userAgent}")
	chrome_options.add_argument('--disable-blink-features=AutomationControlled')
	# driver = webdriver.Chrome(path, chrome_options=chrome_options)
	# CHROME DRIVER MANAGER
	driver = webdriver.Chrome(chrome_options=chrome_options, service=Service(ChromeDriverManager().install()))
	driver.get(urlSmartMeter)

	time.sleep(3)

	authData = {
		"username": 'vaglenn2023@outlook.com',
		"password": 'vaglenn2023',
		"rememberMe": "true"
	}
	
	s = requests.Session()
	login_cookies = {}
	for cookie in driver.get_cookies():
		s.cookies.set(cookie["name"], cookie["value"])
		login_cookies[cookie["name"]] = cookie["value"]

	driver.quit()

	s.headers.update(DefaultHeader)

	r = s.post('https://www.smartmetertexas.com/api/user/authenticate', json=authData)
	try:
		results = r.json()
	except Exception as ex:
		logging.error("Attempts left: " + str(attempts - 1))
		logging.error(str(ex))
		logging.error(r.text)
		time.sleep(1000)
		if attempts > 1:
			login(attempts - 1)
		else:
			raise

				
	print(results)

	s.headers.update({
		"authorization": "Bearer " + results["token"]
	})

	 # Save file
	data = {"cookies":login_cookies, "token":results["token"]}
	with file_path.open('w') as open_file:
		json.dump(data, open_file)

	return s

if __name__ == '__main__':
	login()