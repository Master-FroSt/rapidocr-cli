# Changelog
File ini berisi perjalanan aplikasi selama pengembangan, termasuk komentar penulis dan hal yang akan dilakukan selanjutnya.

## Keresahan
Ide pembuatan _Optical Character Recognition_ (OCR) berawal dari kesulitanku mencari lirik lagu dalam bahasa Mandarin dan Jepang. Beberapa situs lirik menuliskan lirik asli (Hanzi/Kana) beserta cara bacanya (Pinyin/Romaji) dalam bentuk tabel. Ketika di-_copy_, pemformatannya berantakan karena _select_ memilih kedua baris baru ke bawah (misalnya situs fandom). Aku ingin menyalin lirik tersebut menjadi dua teks terpisah. Dulu aku pakai AI buat memisahkannya, dan _task_ ini cukup _token intensive_ jadi Gemini pro ku habis cepat (kalau pakai flash biasanya rusak, aneh jg).

Terkadang pula ada situs yang ga bisa _select_. Itu sebenernya bisa aku akalin dengan _inspect element_, tapi kepikiran pakai OCR sekalian.

Setelah bikin aplikasi ini, aku juga sadar OCR bakal bisa memudahkanku baca manga atau webtoon bahasa lain tanpa bolak-balik ke Google Translate. Mungkin aku tambahin fitur translate nanti.
## To do
<details>
<summary>Klik untuk membuka</summary>

- [x] Tulis dokumentasi awal
- [ ] Tulis dokumentasi docs/Theory untuk RapidOCR
- [ ] Modularisasi
- [ ] Buat logging yang lebih baik
- [ ] Percepat proses input image dan shortcut
- [ ] Buat fitur translate
- [ ] 

</details>

## Initial Commit
- Implementasi RapidOCR CLI dengan drag n drop
- Shortcut
- Dokumentasi awal