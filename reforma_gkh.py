# -*- coding: utf-8 -*
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

file_url = 'C:/Users/adm/Desktop/list_kn.txt'
file = open(file_url, "a")															# ВВЕСТИ РАСПОЛОЖЕНИЕ ВЫХОДНОГО ФАЙЛА
pages = 23																			# ВВЕСТИ КОЛИЧЕСТВО СТРАНИЦ

browser = webdriver.Firefox() 
url = "https://www.reformagkh.ru/mymanager/profile/7023874/"  						# ВВЕСТИ 1 СТРАНИЦУ СО СПИСКОМ ДОМОВ ДУКА
browser.get(url) 
time.sleep(5)
main_window = browser.current_window_handle

def get_kn_addr_from_page(browser_obj, file):
	elements = browser.find_elements_by_xpath('''//div[@id='tab1-subtab1']/div[3]/table/tbody/tr/td/a''')
	file = open(file_url, "a")
	for element in elements:
		element.send_keys(Keys.CONTROL + Keys.RETURN)
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
		browser.switch_to_window(main_window)
		time.sleep(2)
		ad =  browser.find_element_by_xpath('''//span[2]''')
		kn = browser.find_element_by_xpath('''//div[@id='tab1-subtab1']/div/div/table/tbody/tr[23]/td/div/table/tbody/tr/td''')
		addr =  ad.text.split(',')[2:]
		print(kn.text + ', ' + ', '.join(addr), file = file)
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
		browser.switch_to_window(main_window)
		
	file.close()

get_kn_addr_from_page(browser, file)
	
for i in range(pages - 1):				
	next_page = browser.find_element_by_css_selector('li.next > a')
	next_page.click()
	time.sleep(2)
	get_kn_addr_from_page(browser, file)

browser.close()

	
