import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CBIRSystem:
    def __init__(self):
        # Inisialisasi variabel atau model CBIR di sini
        self.reference_images = {}
        self.image_features = {}

    def add_reference_image(self, label, image_path):
        # Fungsi untuk menambahkan gambar referensi dan mengekstraksi fitur
        image = cv2.imread(image_path)
        features = self.extract_features(image)
        self.reference_images[label] = image
        self.image_features[label] = features

    def extract_features(self, image):
        # Implementasi ekstraksi fitur, misalnya menggunakan teknik pengolahan citra
        # (harap disesuaikan sesuai kebutuhan)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ... lakukan ekstraksi fitur lainnya ...
        return gray_image.flatten()  # Mengembalikan vektor fitur dalam bentuk flat

    def classify_image(self, query_image_path):
        global result_label, similarities
        # Membaca gambar query
        query_image = cv2.imread(query_image_path)
        query_features = self.extract_features(query_image)

        # Menghitung cosine similarity dengan gambar referensi
        similarities = {}
        for label, ref_features in self.image_features.items():
            similarity = cosine_similarity([query_features], [ref_features])
            similarities[label] = similarity[0][0]

        # Mengembalikan label dengan cosine similarity tertinggi
        result_label = max(similarities, key=similarities.get)
        return result_label

# Contoh penggunaan
if __name__ == "__main__":
    cbir_system = CBIRSystem()

    # Menambahkan gambar referensi untuk "Good" dan "Not Good"
    cbir_system.add_reference_image("Good", "./img/baut-mur.jpg")
    cbir_system.add_reference_image("Not Good", "./img/baut.jpg")

    # Melakukan inspeksi untuk gambar query
    query_image_path = "./img/mur2.jpg"
    
    result = cbir_system.classify_image(query_image_path)

    print(f"Score {similarities}")
    print("Hasil Inspeksi: {}".format(result))
