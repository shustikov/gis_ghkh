# -*- coding: utf-8 -*-
import merge
import domgos

domgos.ilogin_gis()
domgos.iget_contr()										#делает файл list_dom.txt
merge.merge()											#читает файлы list_dom.txt, du2.csv, pdu2.csv, kn2.csv делает файл res.txt 
do_list =  merge.cdo_list()								#читает файл res.txt

#Фильтры #Фильтры #Фильтры #Фильтры #Фильтры #Фильтры 

filter_street = ['Александра Люкина']                 	#Эти улицы ДОБАВИМ [str]
filter_adds = []									  	#Эти дома добавлять НЕ ДОБАВИМ [(str, building)]
			
#Фильтры #Фильтры #Фильтры #Фильтры #Фильтры #Фильтры 


dl = merge.filter(filter_street, filter_adds, do_list)

print('\n## Дома которые постораемся добавить')	
[print(d['str'], d['building']) for d in dl]

[domgos.inp_du(domgos.browser,d) for d in dl]