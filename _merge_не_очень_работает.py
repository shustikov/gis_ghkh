'''merge v0.2'''


import codecs
import os.path
from paths import * 

def f2dickt(file_url):
	d = {}
	file = codecs.open(file_url, "r", "utf-8-sig")
	file.readline()
	for line in file.readlines():
		val, *nul, key = line.split(';')
		d[key.strip('\r\n')] = val
	file.close()
	print('\n## Из файла %s загружено %d значений' % (file_url, d))	
	return d	
	
def street_conv(street, file_url):
	file = open(file_url, 'r')
	str_d = {}
	for line in file.readlines():
		k, v = line.strip('\n').split(';')
		k, v = k.strip(' '), v.strip(' \t')
		str_d[k] = v if v != '-' else k
	file.close()
	return str_d[street] if street in str_d.keys() else street	
	
def k2addr(k, url_str_conv = str_conv_url):
	add = k.split(', ')
	add[0] = add[0].strip(' ул.')
	add[0] = street_conv(add[0], url_str_conv)
	add[1] = add[1][2:].upper()
	return add
	
def fs2d_list(kn_url, du_url, pdu_url): -> [{atr:val}]
	kn_d, du_d, pdu_d = map(f2dickt, (kn_url, du_url, pdu_url))
	res = {}
	for k in set(du_d.keys()) & set(pdu_d.keys()) & set(kn_d.keys()):
		add = k2addr(k)
		res += {(add[0], add[1]):
				{'street':add[0],
				'building':add[1],
				'kn':kn_d[k],		
				'url_pdf_contr':(du_folder_url + du_d[k]), 
				'url_pdf_prot':(pdu_folder_url + pdu_d[k])}}
				
	return res
	
def list_of_gadds(ldom_url):
	file = open(ldom_url, 'r')
	res = []
	file.readline()
	for line in file.readlines():
		add = line.strip('\n').split(',')	
		add[0] = add[0][4:]
		add[1] = add[1][4:].upper() 
		res += tuple(add)
	file.close()
	return res	

def filter_gadr(gadds, d):	
	return {k:d[k] for k in (set(d.keys()) - set(gads)))}, {k:d[k] for k in (set(gads) - set(d.keys()))}
	
def filter_wr_street(steet_filter_l, d):
	...
	
def filter_wr_file(list_ojs):
	...	
	
	
	