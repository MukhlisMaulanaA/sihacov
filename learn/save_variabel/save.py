import json
import os

# Contoh variabel yang akan disimpan
nilai_variabel1 = 40.12

# Nama file untuk menyimpan nilai variabel
nama_file = 'nilai_variabel.json'

# Mendapatkan path ke direktori skrip saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mencetak direktori kerja saat ini
print("Direktori Kerja Saat Ini:", current_dir)

# Menyimpan nilai variabel dalam format JSON
data = {
    'variabel1': nilai_variabel1,
    # 'variabel2': nilai_variabel2,
    # 'variabel3': nilai_variabel3
}

# Menyimpan ke file JSON
with open(os.path.join(current_dir, nama_file), 'w') as file:
    json.dump(data, file)

# Membaca nilai variabel dari file JSON
with open(os.path.join(current_dir, nama_file), 'r') as file:
    data_terbaca = json.load(file)

# Menampilkan nilai variabel yang telah dibaca
print("Nilai variabel yang dibaca:")
for nama_variabel, nilai_variabel in data_terbaca.items():
    print(f"{nama_variabel}: {nilai_variabel}")
