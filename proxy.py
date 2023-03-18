import requests
import multiprocessing
import time
from bs4 import BeautifulSoup

# fungsi untuk mengambil proxy dari proxyscrape.com
def get_proxies():
    url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all'
    r = requests.get(url)
    proxies = r.text.split('\r\n')
    return proxies


# fungsi untuk mengecek proxy yang valid dengan bing.com 
def check_proxy(proxy):
    try:
        url = 'http://www.bing.com'  # url yang akan digunakan untuk mengecek proxy 
        proxies = {'http': proxy}  # set proxy yang akan digunakan 

        r = requests.get(url, proxies=proxies, timeout=10)  # request ke bing dengan proxy yang telah diset 

        if r.status_code == 200:  # jika status code 200 maka proxy valid 

            soup = BeautifulSoup(r.text, 'html.parser')  # parsing html dari response bing 

            title = soup.find('title').text  # ambil title dari response bing 

            if title == 'Bing':  # jika title sama dengan Bing maka proxy valid dan ditulis ke file txt  

                with open('proxy.txt', 'a') as f:
                    f.write(proxy + '\n')

                print('[+] Valid Proxy :', proxy)

            else:  # jika title tidak sama dengan Bing maka proxy tidak valid  

                print('[-] Invalid Proxy :', proxy)

        else:  # jika status code bukan 200 maka proxy tidak valid  

            print('[-] Invalid Proxy :', proxy)

    except Exception as e:  # jika terjadi error maka proxy tidak valid  

        print('[-] Invalid Proxy :', proxy)


if __name__ == '__main__':

    start_time = time.time()  # waktu mulai program  

    proxies = get_proxies()  # ambil semua proxy dari proxyscrape  

    print('[*] Total Proxies :', len(proxies))  # tampilkan total jumlah proxy yang didapatkan  

    with multiprocessing.Pool(processes=20) as pool:  # buat pool dengan 10 proses  

        pool.map(check_proxy, proxies)  # lakukan check_proxy untuk setiap item di list proxies  

    end_time = time.time() - start_time  # hitung waktu selesai program  

    print('[*] Selesai dalam waktu : %s detik' % end_time)
