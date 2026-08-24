# 🎾 Saha Tenisi (Multi Pong)

Bu proje, FastAPI ve WebSocket kullanarak geliştirilmiş, mobil cihazların joystick olarak kullanıldığı çok oyunculu bir Pong prototipidir.

## 🚀 Kurulum ve Çalıştırma

Projeyi çalıştırmak için terminalde aşağıdaki adımları takip edin:

1. Gerekli kütüphaneleri yükleyin:
```
pip install -r requirements.txt
```
2. Sunucuyu başlatın
```
python main.py
````

# 📂 Dosya Yapısı ve İşlevleri
### main.py: FastAPI sunucusu. Oyun ekranı ve kontrolcüler arasındaki veri trafiğini yönetir.
### cube/index.html: Oyunun oynandığı ana ekrandır. Top fiziği ve skor takibi burada yapılır.
### controller/index.html: Joystick arayüzüdür. Telefon veya tabletten bağlanarak oyuncu çubuğunu hareket ettirmenizi sağlar.


# 🎮 Nasıl Bağlanılır?
### Oyun Ekranı: Tarayıcınızda http://localhost:5000/cube adresine gidin.
### Kontrolcü: Aynı ağdaki başka bir cihazdan http://BILGISAYAR_IP_ADRESI:5000/controller adresine girerek oyuna katılın.
