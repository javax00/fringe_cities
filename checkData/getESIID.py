#takes in an address and returns an ESIID

import requests
import sys
import json
import time

def getESIID(inAddress):

	# print("getESIID Called")

	parameters = {'query' : inAddress, "activeStatusOnly" : "true"}
	url = "https://www.energybot.com/api/prospects/account/TX/search"
	s = requests.Session()
	try:
		r = s.get(url, params=parameters, timeout=5)
	except:
		raise Exception(f'Request Failed: URL = {url} : Parameters = {parameters}')
	if r.status_code != 200:
		raise Exception(f'Response Status Code: {r.status_code}: {r.text}')
	results = r.json()
	returnedAddress = results[0]['displayAddress']
	splitReturnedAddress = returnedAddress.split(" ")
	splitAddress = inAddress.split(" ")
	# if returnedAddress != inAddress and splitReturnedAddress[0] == splitAddress[0]:
	#     # print("INSIDE IF________________________________________")
	#     inAddress = returnedAddress
	#     parameters = {'query' : returnedAddress, "activeStatusOnly" : "true"}
	#     url = "https://www.energybot.com/api/prospects/account/TX/search"
	#     s = requests.Session()
	#     try:
	#         r = s.get(url, params=parameters, timeout=5)
	#     except:
	#         raise Exception(f'Request Failed: URL = {url} : Parameters = {parameters}')
	#     if r.status_code != 200:
	#         raise Exception(f'Response Status Code: {r.status_code}: {r.text}')
	#     results = r.json()
	

	if len(results) < 1:
		raise Exception(f'Empty Results from getESIID')
	if 'displayAddress' not in results[0]:
		raise Exception(f'Results is Missing Display Address')   
	
	if results[0]['displayAddress'] != inAddress:
		raise Exception(f'Could Not Find Matching Display Address for {inAddress} : The Best Matching Address Was {results[0]["displayAddress"]}')
	if 'utilityAccountNumber' not in results[0]:
		raise Exception('Results is Missing utilityAccountNumber')
	# print(results[0]['displayAddress'])
	
	return results[0]['utilityAccountNumber']




if __name__ == '__main__':
	esiid = getESIID('4420 Barwyn Ln, Plano, TX'.upper())
	print(esiid)
	from getMonthlyData import getMonthlyData
	print(getMonthlyData(str(esiid)))