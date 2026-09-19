8Python tabanlı otomatik Discord DM (Direct Message) temizleme aracı.
# Discord DM Cleaner

**Developed by M0RTE**

Discord DM Cleaner, kendi hesabınız üzerinden gönderdiğiniz doğrudan mesajları (DM) otomatik olarak temizlemenizi sağlayan, Python tabanlı hafif bir araçtır. Gelişmiş menü sistemi sayesinde isterseniz **tüm DM geçmişinizi**, isterseniz de **sadece belirlediğiniz kişilere** attığınız mesajları silebilirsiniz.

⚠️ **Uyarı:** Discord hesabınız üzerinden (self-botting) otomatik işlemler yapmak Discord Hizmet Şartları'na (ToS) aykırıdır. Bu araç eğitim ve kişisel kullanım amacıyla geliştirilmiştir. Olabilecek hesap kapatılma (ban/lock) durumlarından kullanıcının kendisi sorumludur.

## Özellikler
- **Otomatik ID Tespiti:** Sadece Token girmeniz yeterlidir; araç kendi Kullanıcı ID'nizi otomatik çeker.
- **Tümünü Sil Modu:** Açık olan tüm DM kutularınızı sayfa sayfa tarar ve size ait mesajları temizler.
- **Hedefli Silme Modu:** Yalnızca ID'sini belirteceğiniz kullanıcılara/arkadaşlarınıza attığınız mesajları siler.
- **Anti-Spam Koruması:** Discord'un `429 Too Many Requests` (Rate Limit) engellerine takılmamak için otomatik bekleme sürelerine (sleep) sahiptir.

## Gereksinimler
- Python 3.6 veya üzeri
- `requests` kütüphanesi

## Kurulum

1. Depoyu bilgisayarınıza klonlayın veya indirin:
   ```bash
   git clone [https://github.com/them0rte/discord-dm-cleaner.git](https://github.com/them0rte/discord-dm-cleaner.git)
   cd discord-dm-cleaner
   pip install requests
   python morte_cleaner.py



