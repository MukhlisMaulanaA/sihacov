import json
import os

# Nama file untuk membaca nilai variabel dari file JSON
nama_file = 'nilai_variabel.json'

# Mendapatkan path ke direktori skrip saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mencetak direktori kerja saat ini
print("Direktori Kerja Saat Ini:", current_dir)

# Membaca nilai variabel dari file JSON
with open(os.path.join(current_dir, nama_file), 'r') as file:
    data_terbaca = json.load(file)

# Menampilkan nama dan nilai variabel yang telah dibaca
print("Nama dan Nilai variabel yang dibaca:")
for nama_variabel, nilai_variabel in data_terbaca.items():
    print(f"{nama_variabel}: {nilai_variabel}")
