# Pembukaan
_Optical Character Recognition_ (OCR) adalah teknologi untuk mengubah gambar menjadi teks, bisa dari gambar foto ataupun dokumen hasil scan. Ia biasa digunakan untuk pengumpulan data dari dokumen terformat, misalnya _invoice_, dokumen identitas data diri, ataupun dokumen yang dicetak. Kemajuan teknologi telah membuat mesin OCR mampu membaca gambar resolusi rendah, miring, ataupun tulisan tangan dengan akurat.

Aplikasi ini menggunakan [RapidOCR](https://github.com/rapidai/rapidocr) untuk membaca gambar. Dibuat dalam _command-line interface_, aplikasi menerima input direktori gambar dan mengeluarkan output file teks dan file gambar berisi hasil OCR.

## Link
Dokumentasi dari [RapidOCR](https://github.com/rapidai/rapidocr).\
File berisi [perubahan terbaru](docs/changelog.md) dari aplikasi ini.\
File berisi [pembahasan mendetail](docs/theory.md) terkait teknologi OCR dari sudut pandang penulis.
# Petunjuk instalasi
1. Clone direktori Github ini dengan perintah `git clone https://github.com/Master-FroSt/rapidocr-cli.git` di cmd
2. Jalankan salah satu dari kode berikut untuk menginstall dependency
```
pip install rapidocr pyperclip
pip install -r requirements.txt
```
# Petunjuk penggunaan
1. Jalankan file .bat untuk membuat window.
2. Copy Paste direktori gambar dan tekan enter. Pada Windows, klik kanan pada gambar, lalu 'copy as path' atau tarik gambar dari file explorer ke terminal.
3. File hasil OCR disimpan pada folder 'out' pada direktori `git clone` dilakukan.
4. Masukkan gambar baru untuk melakukan OCR berulang.
## Petunjuk shortcut
- 'q' untuk quit.
- 't' untuk toggle quiet (menyembunyikan pesan log RapidOCR).
- 'I' untuk membuka gambar hasil OCR dengan image viewer default.
- 'N' untuk membuka teks hasil OCR dengan text editor default.