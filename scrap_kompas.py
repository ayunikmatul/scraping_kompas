import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def generate_tgl(tgl_awal, tgl_akhir, bulan, tahun):
    tgl_ambil=[]
    if(bulan<10):
        bulan='-0'+str(bulan)
    else:
        bulan='-'+str(bulan)
    for i in range(tgl_awal,tgl_akhir+1):
        if i<10:
            i='-0'+str(i)
        else:
            i='-'+str(i)
        tgl_ambil.append(str(tahun)+bulan+i)
    return tgl_ambil

def scraping_kompas(key, tgl_ambil):
    key_tgl=['https://indeks.kompas.com/?site={}&date={}'.format(key, j) for j in tgl_ambil]
    list1=[]
    for url in tqdm(key_tgl, total=len(key_tgl)):
        req=requests.get(url)
        soup=BeautifulSoup(req.text, 'lxml')
        kumpulan_page=soup.find_all('div',class_='article__asset')
        link_page=[kumpulan_page[i].a['href'] for i in range(len(kumpulan_page))]
        # print('ini url page', url)
        count=0
        for i in link_page:
            temp={}
            count+=1
            i=i+'?page=all' #to make view all page
            req_berita=requests.get(i)
            soup_berita=BeautifulSoup(req_berita.text, 'lxml')
            temp['title']=soup_berita.find_all('title')[0].text
            temp['tanggal']=soup_berita.find_all('div', {'class':'read__time'})[0].text.split(',')[0].split('-')[1].replace(' ',"")
            temp['berita']=soup_berita.find_all('div', {'class':'read__content'})[0].text.strip().replace('\n' , ' ')
            # print(berita)
            temp['photo']=soup_berita.find_all('div', {'class':'photo'})[0].img['data-src']
            list1.append(temp)
            # print(title, tgl, photo)
    return list1

if __name__ == "__main__":
    range_tgl=generate_tgl(1,12,12,2019)
    key='tekno'
    df=pd.DataFrame(scraping_kompas(key, range_tgl))
    df.to_csv('output/berita_'+key+'_'+range_tgl[0].replace('-','')+'_'+range_tgl[-1].replace('-','')+'.csv')