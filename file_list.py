# -*- coding: utf-8 -*-
from glob import glob
import os

url_file_dir = 'F:/USB/Протоколы по договору управления 2011'
os.chdir(url_file_dir)
folders = glob('.')
file_url = 'C:/Users/adm/Desktop/pdu.txt'
file = open(file_url, 'a')

for folder in folders: 
	pdf_urls = glob("%s/*.pdf" % folder)
	[print(i + '; ' + i.split('\\')[-1][:-4], file = file) for i in pdf_urls if i.split('.')[-1] == 'pdf']
	
file.close()	


