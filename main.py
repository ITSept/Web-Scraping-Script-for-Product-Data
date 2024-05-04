# Liberary 
# pip install requests
# pip install beautifulsoup4
# pip install pandas
# pip install openpyxl

import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.malasngoding.com/shop"
page = requests.get(URL)

all_jobs = []  # List untuk menyimpan semua data pekerjaan dari setiap halaman
job_number = 1  # Nomor urut untuk seluruh pekerjaan

while page.status_code == 200:  # Selama status halaman OK
    soup = BeautifulSoup(page.text, "html.parser")

    jobs = soup.find_all('div', {'class': 'post card card-post card-product mb-4 rounded-3'})

    for job in jobs:
        title_job = job.find('a', {'class': 'text-inherit line-clamp-2'})
        harga = job.find('span', {'class': 'fw-bold text-dark'})
        all_jobs.append({'No': job_number,'Judul': title_job.text.strip(), 'Harga': harga.text.strip()})
        job_number += 1

    next_page = soup.find('a', {'class': 'next page-numbers'})  # Cari link ke halaman berikutnya
    if next_page:
        next_page_url = next_page.get('href')  # Dapatkan URL halaman berikutnya
        page = requests.get(next_page_url)  # Lakukan permintaan ke halaman berikutnya
    else:
        print("Halaman berikutnya tidak ditemukan. Proses selesai.")
        break

# Konversi data ke dataframe pandas
df = pd.DataFrame(all_jobs)

# Ekspor dataframe ke file Excel
excel_filename = 'data_produk.xlsx'
df.to_excel(excel_filename, index=False)

print("Data telah disimpan ke:", excel_filename)

