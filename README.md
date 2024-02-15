![Ekran Resmi 2024-01-22 03 19 20](https://github.com/OmerErbalta/TSM_Balikesir/assets/74858739/0c9e6274-058c-44c9-90cb-8a4e97e6ae42)# TSM_Balikesir
Travelling Salesman Problem Çözümü

Bu proje, Travelling Salesman problemi için genetik algoritma kullanarak hem kuş uçuşu hem de araba ile en kısa rotayı Balıkesir ili içerisinde hesaplayan bir Python uygulamasını içerir.

Kurulum

Proje dosyalarını bilgisayarınıza kopyalayın veya indirin.
Gerekli bağımlılıkları yükleyin


Kullanım

main.py dosyasını çalıştırarak programı başlatın.
Program, başlangıç noktası ve destinasyonları belirlemek için sizi yönlendirecektir.
Program, hem kuş uçuşu hem de araba ile en kısa rotayı hesaplayacak ve sonuçları gösterecektir.

Nasıl Çalışır?

Genetik Algoritma: Program, genetik algoritma kullanarak her bir destinasyonun bir listesini oluşturur ve en kısa rotayı bulmak için iteratif olarak geliştirir.
Kuş Uçuşu Hesaplama: Kuş uçuşu hesaplama, destinasyonlar arasındaki doğrudan mesafeyi hesaplar.
Araç Rotası Hesaplama: Araç rotası hesaplama, Google Maps API'ı kullanarak destinasyonlar arasındaki en kısa sürüş rotasını hesaplar.
Örnek Kullanım

Destinasyonlar: A,B, C, D, E
Sonuçlar:
Kuş uçuşu en kısa rota: A -> B -> C -> D -> E
Araç ile en kısa rota: A -> C -> B -> E -> D

![Ekran Resmi 2024-01-22 03 17 38](https://github.com/OmerErbalta/TSM_Balikesir/assets/74858739/8b7982f2-38d1-4d4c-95a6-6b5c174e121e)
