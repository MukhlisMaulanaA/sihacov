import os

# Load directori
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = (f"{current_dir}\save_luas.txt")

# Membaca dari file
with open(file_path, "r") as file:
    lines = file.readlines()

# Mendapatkan nilai luas dari setiap baris
areas = [float(line.split("Area: ")[1].split(" ")[0]) for line in lines]

# Gunakan nilai luas sesuai kebutuhan aplikasi lain
print(f"Luas dari gambar referensi adalah {areas[0]} cm^2")
