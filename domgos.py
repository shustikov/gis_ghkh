# -*- coding: utf-8 -*
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
import merge
import pywinauto
from pywinauto.application import Application
import os



file_url = 'F:/USB/logs/list_dom.txt'												# ВВЕСТИ РАСПОЛОЖЕНИЕ ВЫХОДНОГО ФАЙЛА
m_res_url = 'F:\\USB\\logs\\res.txt ' 												# Расположение файла с массивом домов для внесения
added_url = 'F:\\USB\\logs\\added.txt'												# Добавленные ДУ
error_folder = 'F:\\USB\\logs\\errors\\'											# Папка со скриншотами ошибок
	

# РЕГИСТРАЦИОННЫЕ ДАННЫЕ      РЕГИСТРАЦИОННЫЕ ДАННЫЕ       РЕГИСТРАЦИОННЫЕ ДАННЫЕ     РЕГИСТРАЦИОННЫЕ ДАННЫЕ
login = ''
password = ''	
# РЕГИСТРАЦИОННЫЕ ДАННЫЕ      РЕГИСТРАЦИОННЫЕ ДАННЫЕ       РЕГИСТРАЦИОННЫЕ ДАННЫЕ     РЕГИСТРАЦИОННЫЕ ДАННЫЕ
				
browser = webdriver.Firefox()
url = "https://dom.gosuslugi.ru/#/main"  
browser.get(url)
time.sleep(3)


def login_gis(login, password, browser):
	main_window = browser.current_window_handle	
	browser.find_element_by_xpath("//a[contains(@href, '/sp-web/sp/login')]").click()
	time.sleep(1)
	browser.find_element_by_xpath("//input").send_keys(login)																								
	browser.find_element_by_xpath("//dl[3]/dd/input").send_keys(password)
	browser.find_element_by_xpath("//button").click()	
	browser.find_element_by_xpath("//div[2]/div/span[2]").click()
	browser.switch_to_window(main_window)
	time.sleep(3)
	browser.find_element_by_xpath("//input").click()
	browser.find_element_by_xpath("//td[2]/input").click()
	browser.find_element_by_xpath("//div/button").click()
	time.sleep(3)
	print('\n## Удачно установлено соединение с ГИС ЖКХ\n')


def get_contr(file_url, browser):
	print('\n## Сканирование внесённых в ГИС ЖКХ договоров\n')
	browser.get('https://my.dom.gosuslugi.ru/organization-cabinet/#/agreements')
	os.remove(file_url) if os.path.isfile(file_url) else None
	file = open(file_url, "a")
	print("### Занесённые договора:", file = file)
	file.close()
	while True:
		try:
			time.sleep(10)
			elements = browser.find_elements_by_xpath('''//div/ef-agr-srch-contract/div/div[4]/div/div/table/tbody/tr/td/a''')
			file = open(file_url, "a")
			for element in elements:
				addr = element.text.split(', ')[2:]
				print(', '.join(addr), file = file)	if addr != [] else None
			file.close()	
			browser.find_element_by_xpath("//ul[3]/li/a/span").click()

		except:
			file.close()
			break

def upload_file(file):			
	
	app = Application()
	time.sleep(2)
	w_handle = pywinauto.findwindows.find_windows(title='Выгрузка файла', class_name='#32770')[0]
	window = app.window_(handle=w_handle)
	window.Wait('ready')
	edit = window.Edit
	edit.Select().TypeKeys(file.replace(' ', '{SPACE}'))
	time.sleep(2)
	button = window.Button
	button.ClickInput()
	time.sleep(2)
	

def inp_du_du(browser, d):	
	browser.get('https://my.dom.gosuslugi.ru/organization-cabinet/#/agreements/contract/add')
	#time.sleep(17)																				#иногда не появляется это окно от ебучей почты
	#browser.find_element_by_xpath('//div/button').click()
	time.sleep(2)
	browser.find_element_by_xpath("//input[@name='']").click()
	browser.find_element_by_xpath('//div/input').send_keys('б/н')
	browser.find_element_by_xpath('//span/input').send_keys('01012011')
	browser.find_element_by_xpath('//div[4]/div/hcs-datepicker/span/input').send_keys('31122020')
	browser.find_element_by_xpath('//div[2]/div/div/div/a/span').click()
	browser.find_element_by_xpath('//div[2]/div/div/div/a/span').send_keys(Keys.ARROW_DOWN)
	browser.find_element_by_xpath('//div[2]/div/div/div/a/span').send_keys(Keys.RETURN)
	
	browser.find_element_by_xpath('//div[2]/span/input').click()
	upload_file(d['url_pdf_contr'])
	browser.find_element_by_xpath("//form[@id='agreementInfo']/div[3]/div/div/div/div/div/table/tbody/tr/td/div/div[2]/div/attachment-element/div/ef-prf-form/div/div[3]/div/a[2]").click()
	
	browser.find_element_by_xpath('//div[4]/div/attachment-element/div/ef-prf-form/div/div[2]/div/div[2]/span/input').click()
	upload_file(d['url_pdf_prot'])
	browser.find_element_by_xpath("//form[@id='agreementInfo']/div[3]/div/div/div/div/div[2]/table/tbody/tr/td/div/div[4]/div/attachment-element/div/ef-prf-form/div/div[3]/div/a[2]").click()
	
	time.sleep(40)
	#yy = input('yy')
	browser.find_element_by_xpath('//button[2]').click()										#submit
	time.sleep(3)
	browser.find_element_by_xpath('//div[3]/button[2]').click()									#ДУ с данным номером уже в реестре
	time.sleep(3)
	browser.find_element_by_xpath('//div/div/div[3]/button').click()							#Операция успешно завершена
	time.sleep(5)
	browser.find_element_by_xpath('//span[2]/button').click()									#Далее
	
	print('\n## Договор упраления дома по адресу %s %s загружен на сайт'% (d['str'], d['building']))
	
def inp_du_ou(browser, d):
	browser.find_element_by_xpath('//ef-ct-dog-pd-list-of-houses/div/div[2]/button').click()	#добавить управляемый объект	
	browser.find_element_by_xpath('//form/div/div/div/div/div/div[2]/button').click()		  	#Выбрать	
	time.sleep(1)	
	browser.find_element_by_xpath('/html/body/div[9]/div/div/div/div[2]/div/div/ef-pa-form/div/form/div/div/div/div[1]/div[1]/div/div/a').click()
	browser.find_element_by_xpath("/html/body/div[10]/div/input").send_keys('Нижегородская') 
	browser.find_element_by_xpath("/html/body/div[10]/div/input").send_keys(Keys.RETURN)
	
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div/div/ef-pa-form/div/form/div/div/div/div[1]/div[3]/div/div/a').click()
	browser.find_element_by_xpath("/html/body/div[11]/div/input").send_keys('Нижний Новгород')
	time.sleep(2)
	browser.find_element_by_xpath("/html/body/div[11]/div/input").send_keys(Keys.RETURN)
	
	browser.find_element_by_xpath("/html/body/div[8]/div/div/div/div[2]/div/div/ef-pa-form/div/form/div/div/div/div[2]/div[1]/div/div/a").click()
	time.sleep(2)
	browser.find_element_by_xpath("/html/body/div[12]/div/input").send_keys(d['str'])
	time.sleep(2)
	browser.find_element_by_xpath("/html/body/div[12]/div/input").send_keys(Keys.RETURN)
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div/div/ef-pa-form/div/form/div/div/div/div[2]/div[2]/div[1]/div/div/div/a').click()
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[13]/ul/li[1]').click()
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div/div/ef-pa-form/div/form/div/div/div/div[2]/div[2]/div[1]/div/div/div/a').click()
	li = browser.find_elements_by_xpath('/html/body/div[13]/ul/li')								#Выбор дома
	build_flag = False
	for a in li:
		if a.text == d['building']:
			a.click()
			build_flag = True
			break	
	time.sleep(10)		
	#yy = input('yy')		
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[3]/button[2]').click()									# submit
	time.sleep(2)
	browser.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/div/button[2]').click()								#save
	time.sleep(2)
	browser.find_element_by_xpath('/html/body/div[9]/div/div/div/div[3]/button').click()									#ok
	time.sleep(2)
	
	print('\n## Управляемый объект %s %s выбран'% (d['str'], d['building'])) if build_flag == True else print('\n##%s %s не выбран'% (d['str'], d['building']))

def aproove(browser, d):
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[3]/div/span[2]/button[1]').click()					# Подтвердить
	time.sleep(2)
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[3]/button[2]').click()									# Вы уверены
	time.sleep(2)
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[3]/div/button[2]').click()								# Отправить заявку на утверждение
	time.sleep(2)
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[3]/button[1]').click()									# NoButton
	time.sleep(2)
	browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[3]/button').click()									# Сведения размещены успешно
	time.sleep(2)
	print('\n## Договор %s %s добавлен'% (d['str'], d['building']))
	

def inp_ou(browser, d):
	browser.get('https://my.dom.gosuslugi.ru/organization-cabinet/#/house/choose-address')
	time.sleep(6)
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div/ef-vas/div[1]/ef-pa-form-2/div/form/div/div/div/div[1]/div[1]/div/div/a').click()
	
	browser.find_element_by_xpath("/html/body/div[6]/div/input").send_keys('Нижегородская') 
	browser.find_element_by_xpath("/html/body/div[6]/div/input").send_keys(Keys.RETURN)
	
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div/ef-vas/div[1]/ef-pa-form-2/div/form/div/div/div/div[1]/div[3]/div/div/a').click()
	browser.find_element_by_xpath("/html/body/div[7]/div/input").send_keys('Нижний Новгород')
	time.sleep(2)
	browser.find_element_by_xpath("/html/body/div[7]/div/input").send_keys(Keys.RETURN)
	
	browser.find_element_by_xpath("/html/body/div[1]/div[5]/div/div/div/ef-vas/div[1]/ef-pa-form-2/div/form/div/div/div/div[2]/div[1]/div/div/a").click()
	time.sleep(2)
	browser.find_element_by_xpath("/html/body/div[8]/div/input").send_keys(d['str'])
	time.sleep(2)
	browser.find_element_by_xpath("/html/body/div[8]/div/input").send_keys(Keys.RETURN)
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div/ef-vas/div[1]/ef-pa-form-2/div/form/div/div/div/div[2]/div[3]/div[1]/div/div/div/div/a').click()
	time.sleep(3)
	li = browser.find_elements_by_xpath('/html/body/div[9]/ul/li')								#Выбор дома
	for a in li:
		if a.text == d['building']:
			a.click()
			break	
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div/ef-vas/div[2]/div/div/div[2]/button').click()								#Submit
	
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/div[1]/div/div/div[3]/div[2]/button').click()					#oktmo
	time.sleep(6)
	browser.find_element_by_xpath('//ef-poktmo-form/div/div/div/div/div/div/div/a/span[2]').click()
	browser.find_element_by_xpath('/html/body/div[5]/div/input').send_keys('22701000001')
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[5]/div/input').send_keys(Keys.RETURN)
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div[2]/ef-poktmo-form/div/div/div/div[1]/div[2]/button').click()					#Find
	time.sleep(3)
	
	browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div[2]/ef-poktmo-rzp-form/ng-simple-grid/div/div[1]/table/tbody/tr/td[1]/div/span[1]/input[2]').click()
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[3]').click()
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/ef-hcs-rao-xd-house-detail/div/div/div[1]/div[1]/rosregister-field/div/div/div/a').click()
	browser.find_element_by_xpath('/html/body/div[3]/ul/li[1]').click()
	
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/div[1]/div/div/div[1]/table/tbody/tr/td[2]/a').click() 										#Сведения с реформы ЖКХ
	
	time.sleep(5)
	browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
	time.sleep(15)
	browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button').click()
	time.sleep(3)
	
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/ef-hcs-rao-xd-house-detail/div/div/div[1]/div[2]/div/input').send_keys(d['kn'])				#kn
	
	#browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/ef-hcs-rao-xd-house-detail/div/div/div[1]/div[3]/div/div/input').click()  					#no kn
	
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/ef-hcs-rao-xd-house-detail/div/div/div[1]/div[5]/div/div/a').click()
	browser.find_element_by_xpath('/html/body/div[4]/ul/li[3]').click()  																									#Исправный
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/div[2]/div/div[1]/div[3]/rosregister-field/div/div/input').send_keys('0') 					#Количество подземных гаражей
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[1]/div/form/ef-hcs-rao-xd-house-detail/div/div/div[1]/div[8]/rosregister-field/div/div/div/a').click() 	#Статус культурного наследия
	time.sleep(1)
	browser.find_element_by_xpath('/html/body/div[5]/ul/li[2]').click()
	time.sleep(10)
	#yy = input('yy')
	
	browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[2]/button[2]').click()							#Разместить
	time.sleep(3)
	browser.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button').click()								#дом успешно добавлен
	time.sleep(3)
	print('\n## Объект %s %s добавлен'% (d['str'], d['building']))
	
	
def inp_du(browser, d):
	try:
		inp_du_du(browser, d)	
		inp_du_ou(browser, d)
		aproove(browser, d)
		file = open(added_url, 'a')
		print(d['str'], d['building'], sep = ' ;', file = file)
		file.close()
	except Exception as e:
		print(*e.args, sep = '\n') 
		print('\n## Договор %s %s не добавлен'% (d['str'], d['building']))
		browser.get_screenshot_as_file(error_folder + d['str'] + d['building'] + '.png')
		browser.get('https://dom.gosuslugi.ru/#/main')
		time.sleep(10)
		pass
	else: 	
		try:	
			inp_ou(browser, d)
		except Exception as e:
			print(*e.args, sep = '\n')
			print('\n## Объект %s %s не добавлен'% (d['str'], d['building']))
			browser.get_screenshot_as_file(error_folder + d['str'] + d['building'] + '.png')
			browser.get('https://dom.gosuslugi.ru/#/main')
			time.sleep(10)
			pass	
	
	
	
def ilogin_gis():	
	login_gis(login, password, browser)

def iget_contr():	
	get_contr(file_url, browser)

#do_list = merge.cdo_list()	
#login_gis(login, password, browser)	
#inp_du(browser,do_list[0])
	
	
