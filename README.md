# TSM_Balikesir
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
