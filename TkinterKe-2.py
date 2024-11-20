import tkinter as tk
from tkinter import ttk
import sqlite3

# Fungsi untuk membuat database dan tabel jika belum ada
def setup_database():
    # Membuat atau membuka koneksi ke database SQLite
    conn = sqlite3.connect("data_siswa.db")
    cursor = conn.cursor()
    # Membuat tabel jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi

# Fungsi untuk menyimpan data ke database
def submit_nilai():
    # Mengambil data dari entry
    nama = nama_entry.get()
    biologi = int(biologi_entry.get())
    fisika = int(fisika_entry.get())
    inggris = int(inggris_entry.get())
    
    # Menentukan prediksi berdasarkan nilai tertinggi
    if biologi > fisika and biologi > inggris:
        prediksi = "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        prediksi = "Teknik"
    elif inggris > biologi and inggris > fisika:
        prediksi = "Bahasa"
    else:
        prediksi = "Tidak Diketahui"

    # Menyimpan data ke database
    conn = sqlite3.connect("data_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi
    
    # Menampilkan hasil prediksi
    output_label.config(text=f"Hasil Prediksi: {prediksi}")
    load_data()  # Memuat ulang data untuk tabel

# Fungsi untuk memuat data dari database ke dalam tabel
def load_data():
    # Menghapus data lama di tabel
    for item in tree.get_children():
        tree.delete(item)
    
    # Membaca data dari database
    conn = sqlite3.connect("data_siswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()

    # Menambahkan data ke tabel
    for row in rows:
        tree.insert("", "end", values=row)

# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("600x600")

# Label judul
title_label = ttk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 16))
title_label.pack(pady=10)

# Input untuk nama siswa
nama_label = ttk.Label(root, text="Nama Siswa:")
nama_label.pack(anchor="w", padx=20, pady=2)
nama_entry = ttk.Entry(root)
nama_entry.pack(padx=20, pady=2)

# Input untuk nilai Biologi
biologi_label = ttk.Label(root, text="Nilai Biologi:")
biologi_label.pack(anchor="w", padx=20, pady=2)
biologi_entry = ttk.Entry(root)
biologi_entry.pack(padx=20, pady=2)

# Input untuk nilai Fisika
fisika_label = ttk.Label(root, text="Nilai Fisika:")
fisika_label.pack(anchor="w", padx=20, pady=2)
fisika_entry = ttk.Entry(root)
fisika_entry.pack(padx=20, pady=2)

# Input untuk nilai Inggris
inggris_label = ttk.Label(root, text="Nilai Inggris:")
inggris_label.pack(anchor="w", padx=20, pady=2)
inggris_entry = ttk.Entry(root)
inggris_entry.pack(padx=20, pady=2)

# Tombol untuk submit nilai
submit_button = ttk.Button(root, text="Submit Nilai", command=submit_nilai)
submit_button.pack(pady=10)

# Label untuk output hasil prediksi
output_label = ttk.Label(root, text="Hasil Prediksi:", font=("Arial", 12), foreground="blue")
output_label.pack(pady=10)

# Tabel untuk menampilkan data
tree = ttk.Treeview(root, columns=("Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi"), show="headings")
tree.heading("Nama Siswa", text="Nama Siswa")
tree.heading("Biologi", text="Nilai Biologi")
tree.heading("Fisika", text="Nilai Fisika")
tree.heading("Inggris", text="Nilai Inggris")
tree.heading("Prediksi", text="Prediksi Fakultas")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Memuat database
setup_database()
load_data()  # Memuat data awal dari database

# Menjalankan GUI
root.mainloop()
