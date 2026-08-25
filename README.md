# 🎾 Saha Tenisi (Multi-Pong)

FastAPI ve WebSocket teknolojileri kullanılarak geliştirilmiş, akıllı telefonların veya tabletlerin birer **kablosuz joystick (kontrolcü)** olarak kullanıldığı, çok oyunculu (multiplayer) modern bir Pong oyun prototipidir.

---

## 🚀 Özellikler

* **Gerçek Zamanlı İletişim:** WebSocket mimarisi sayesinde sıfıra yakın gecikme (low latency) ile akıcı oyun deneyimi.
* **Mobil Kontrolcü Desteği:** Herhangi bir mobil cihazın tarayıcısını kullanarak oyuna anında dahil olma.
* **Kolay Kurulum:** Karmaşık veritabanı veya sunucu yapılandırmalarına ihtiyaç duymayan hafif (lightweight) altyapı.

---

## 📦 Dosya Yapısı ve İşlevleri

```text
├── controller/
│   └── index.html      # Mobil cihazlar için tasarlanmış dokunmatik joystick arayüzü.
├── cube/
│   └── index.html      # Oyunun oynandığı, top fiziği ve skor takibinin yapıldığı ana ekran.
├── main.py             # FastAPI sunucusu. Ekranlar arası WebSocket veri trafiğini yönetir.
└── requirements.txt    # Projenin çalışması için gerekli Python kütüphanelerinin listesi.
```

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda ayağa kaldırmak için aşağıdaki adımları sırasıyla takip edin:

### 1. Depoyu Kopyalayın
```bash
git clone https://github.com/Kevindevin11/Saha_tenisi.git
```

### 2. Gerekli Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Sunucuyu Başlatın
```bash
python main.py
```

---

## 🎮 Nasıl Oynanır?

Oyunun başlayabilmesi için ana ekranın ve kontrolcülerin aynı yerel ağa (Wi-Fi) bağlı olması gerekir.

### A. Ana Oyun Ekranını Açın
Bilgisayarınızın tarayıcısından aşağıdaki adrese giderek oyun alanını açın:
👉 `http://localhost:5000/cube`

### B. Mobil Kontrolcüleri Bağlayın
Oyuncu olarak katılacak mobil cihazların (telefon/tablet) tarayıcısından bilgisayarınızın yerel IP adresini kullanarak giriş yapın:
👉 `http://<BILGISAYAR_IP_ADRESI>:5000/controller`

> 💡 **İpucu:** Bilgisayarınızın IP adresini bulmak için terminale Windows kullanıyorsanız `ipconfig`, macOS/Linux kullanıyorsanız `ifconfig` veya `ip a` yazarak `IPv4` adresinizi öğrenebilirsiniz.
