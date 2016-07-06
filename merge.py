# -*- coding: utf-8 -*-
import codecs
import os.path

str_conv_url = 'F:\\USB\\logs\\str_conv.txt'    						#Словарь соответсвия улиц
kn_url = 'F:\\USB\\logs\\kn2.csv'										#Список соответствия кадастровых номеров
du_url = 'F:\\USB\\logs\\du2.csv'										#Список	ссылок на договоры управления 
pdu_url = 'F:\\USB\\logs\\pdu2.csv'										#Список ссылок на протоколы
ldom_url = 'F:\\USB\\logs\\list_dom.txt'								#Список добавленных в гис жкх домов
du_folder_url = "C:\\Users\\ADM\\Desktop\\Договоры управления скан\\"	
pdu_folder_url = 'F:\\USB\\Протоколы по договору управления 2011\\'	
	
res_url = 'F:\\USB\\logs\\res.txt ' 									#Выходной файл


def f2dickt(file_url):
	d = {}
	file = codecs.open(file_url, "r", "utf-8-sig")
	file.readline()
	for line in file.readlines():
		val, *nul, key = line.split(';')
		d[key.strip('\r\n')] = val
	file.close()	
	return d	

def fs2d(kn_url, du_url, pdu_url):
	kn_d, du_d, pdu_d = map(f2dickt, (kn_url, du_url, pdu_url))	
	return {k:(v, du_d[k], pdu_d[k]) for k, v in kn_d.items() if k in set(du_d.keys()) & set(pdu_d.keys())}

def street_conv(street, file_url):
	file = open(file_url, 'r')
	str_d = {}
	for line in file.readlines():
		k, v = line.strip('\n').split(';')
		k, v = k.strip(' '), v.strip(' \t')
		str_d[k] = v if v != '-' else k
	file.close()
	return str_d[street] if street in str_d.keys() else '?'	
	
def k2addr(k, url_str_conv = str_conv_url):
	add = k.split(', ')
	add[0] = add[0].strip(' ул.')
	add[0] = street_conv(add[0], url_str_conv)
	add[1] = add[1][2:].upper()
	return add
		
def list_of_adds(d):
	return list(map(k2addr, d.keys()))
		
def list_of_gadds(ldom_url):
	file = open(ldom_url, 'r')
	res = []
	file.readline()
	for line in file.readlines():
		add = line.strip('\n').split(',')	
#		add[0] = add[0][4:]
		add[0] = add[0].strip('ул. ').strip('пр-кт. ').strip('ш. ')
		add[1] = add[1][4:].upper() 
		res += [add]
	file.close()
	return res

def list_of_streets(d):
	a = map(k2addr, d.keys())
	return sorted(list(set(i[0] for i in a)))	
	
def list_of_gstreets(a):
	return sorted(list(set(i[0] for i in a)))

def list_of_mstreets(res_d, gadds):	
	return set(list_of_streets(res_d)) - set(list_of_gstreets(gadds)) 

def wrong_sreet_adds(adds):
	return [tuple(a) for a in adds if a[0] == '?']
	
def d_of_wr_st_adds(w_adds, res_d):
	w_d = {}
	for k, v in res_d.items():
		k1 = tuple(k2addr(k))
		if k1[0] == '?': w_d[k] = v
	return w_d	
	
def merge_adds(adds, gadds, wr_adds):
	r = set(map(tuple, adds)) - set(map(tuple, gadds))
	f = set(map(tuple, wr_adds))
	return sorted(list(r - f))

def merged_d(d, adds):
	m_d = {}
	for k, v in d.items():
		k = tuple(k2addr(k))
		if k in map(tuple, adds) and v[0].lower() != 'не имеется': m_d[k] = v
	return m_d

def f_kn_d(d):
	m_d = {}
	for k, v in d.items():
		if v[0].lower() == 'не имеется': m_d[k] = v
	return m_d	
	
	
def check_files_adds(d, du_folder_url, pdu_folder_url):
	res = []
	for k, v in d.items():
		du = du_folder_url + v[1]
		pdu = pdu_folder_url + v[2]
		res += [k] if not all(map(os.path.isfile, (du, pdu))) else []
	return res

def create_dict_obj_list(res_url):
	file = open(res_url)
	file.readline()
	res = []
	for	line in file.readlines():
		a = line.split(';')
		res += [{'str':a[0], 'building':a[1], 'kn':a[2], 'url_pdf_contr':(du_folder_url + a[3]), 'url_pdf_prot':(pdu_folder_url + a[4])}]
	return res	

def filter(filter_street, filter_adds, d):
	res = []
	for d in sorted(d, key = lambda d: d['str']):
		if all(((d['str'] not in filter_street),
				((d['str'], d['building']) not in filter_adds))):
				res += [d]
	return res	
	

def merge():
#main		
	res_d = fs2d(kn_url, du_url, pdu_url) 							#Объединяем все файлы в один словарь
	gadds = list_of_gadds(ldom_url)                             	#Формируем список адресов из гис жкх
	adds = list_of_adds(res_d)                                  	#Формируем список адресов из файлов
	wr_adds = wrong_sreet_adds(adds)                            	#Формируем список адресов которые не будем вводить по причине невозможности правильного внесения улицы
	madds = merge_adds(adds, gadds, wr_adds)                    	#Формируем список адресов которые будем пытаться внести
	d_wr_adds = d_of_wr_st_adds(wr_adds, res_d)                 	#Формируем словарь адресов которые не будем вводить по причине невозможности правильного внесения улицы для текстового вывода 
	m_d = merged_d(res_d, madds)                                	#Формируем словарь адресов сопоставленных со всей др. информацией
	fkn_d = f_kn_d(res_d)
	fc_adds = check_files_adds(m_d, du_folder_url, pdu_folder_url)	#Формируем список адресов у которых не найдено файлов (!ЭТОТ СПИСОК НЕ ВЫЧИТАЕТСЯ!)
	
	os.remove(res_url) if os.path.isfile(res_url) else None
	res_file = open(res_url, 'a')
	print('## Список адресов которые скрипт постарается занести', file = res_file)
	[print(i[0][0], i[0][1], i[1][0], i[1][1], i[1][2], sep = ';', file = res_file) for i in m_d.items()]
	res_file.close()


#report
	print('\n## Отчёт по подготовленным домам:\n---------')
	print(	'Все адреса: %d' % len(adds), 
			'Занесённые адреса: %d' % len(gadds), 
			'Занесённых адресов нашлось в списке всех адресов: %d' % (len(adds) - len(madds) - len(d_wr_adds)), 
			'Занесённых адресов не распознано: %d' % (len(d_wr_adds) + len(gadds) - (len(adds) - len(madds))),
			'Адресов, улица которых не может быть занесена: %d' % len(d_wr_adds),
			'КН не имеется: %d' % len(fkn_d),
			'Адресов у которых не достаёт файлов НЕ ВЫЧИТАЮТСЯ ИЗ ОБЩЕГО СПИСКА %d' % len(fc_adds),
			'Скрипт постарается занести адресов: %d' % len(m_d.keys()), 
			sep = '\n')
	
	print('\n## Список занесённых не распознанных адресов (возможно их нет в общем списке):\n---------')		
	[print(a,*c, b, sep = ', ' ) for a, *c, b in merge_adds(gadds, adds, wr_adds)]
	
	print('\n## Адреса, улица которых не может быть занесена:\n---------')	
	[print(i) for i in d_wr_adds]
	
	print('\n## Адреса у которых кадастровый номер - Не имется:\n---------')	
	[print(i) for i in fkn_d.keys()]
	
	print('\n------------------------------------------\n')
	
def cdo_list():
	return create_dict_obj_list(res_url)


# print()
# print('\n\n')

#print(set(list_of_gstreets(gadds)))						
		
#[print(i) for i in list_of_gadds(ldom_url)]
#[print(i) for i in list_of_adds(res_d)]	
	
#[print(k2addr(k)) for k, v in res_d.items()]
#print(len(list_of_streets(res_d)))
#[print(i) for i in list_of_streets(res_d)]


# ga = sorted(([gadd for gadd in gadds if gadd[0] == 'Березовская']))
# a = sorted([add for add in adds if add[0] == 'Березовская'])
# for i in range(len(a)):
	# print(ga[i], '\t\t\t', a[i] ) 








