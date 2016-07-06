# -*- coding: utf-8 -*-
import img2pdf
import os
import glob
 
files_dir = '''C:/Users/ADM/Desktop/Сканированные протоколы по дог.управ.2011'''				#Папка содержащая папки с папками с картинками
out_url = '''C:/Users/adm/Desktop/Сканированные протоколы по дог.управ.2011/out/'''				#Папка куда будут выгружаться готовые pdf
log_file_url = out_url + '!log.txt'																#Файл со списком pdf которые не вышли
log_f = open(log_file_url, 'w')
            
os.chdir(files_dir)
folders  = glob.glob("*\*")
                        
def con(img_urls : tuple, pdf_url):         
    img_bytes = map(img2pdf.input_images, img_urls) 
    try:    
        pdf_bytes = img2pdf.convert(*img_bytes)
        file = open(pdf_url, 'wb')
        file.write(pdf_bytes)
        file.close()
    
    except Exception as e:
        print(pdf_url, file = log_f)
    
    

for folder in folders:
    addr = folder.split('\\')[1]
    pdf_url = out_url + addr + '.pdf'   
    img_urls = glob.glob("%s/*.jpg" % folder)
    con(img_urls, pdf_url)  
	
log_f.close()	