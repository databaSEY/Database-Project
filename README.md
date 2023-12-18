# Database-Project
23 Güz Dönemi BLG 317 Database Projesi İçin
## How to run
flask --app project run --debug

Şu an sadece drivers.py dosyası sayesinde "http://127.0.0.1:5000/drivers" benzeri url ye gidince tabloyu bastırıyor.

main.py dosyası kullanılmayacak, flask olmadan veritabanını test etmek istersek diye onu da silmedim.

### Drivers
#### CRUD
Create, Update, Delete işlemlerini gerçekleştiriyor.
İşlemler doğru gerçekleşiyor fakat kullanıcı deneyimi çok da iyi değil. Bazı ufak eksikler var. 
Mesela update ettikten sonra tekrar search yapman gerekiyor ki yeni halini görebilesin.
Ama zamanımız az kaldı ve bunlar veritabanı ile alakasız konular.

#### Details
Satırın üstüne basınca details sayfasına gidiyor. Yasin'in yaptığı gibi aynı sayfada satırın altında açılan bir şey yapmadım henüz.
Yapıp yapmama konusunda kararsızım.
#### Profile sayfası
Zamanımız az kaldığı için bu olayı pas geçme ihtimalimizi güçlü görüyorum.
#### Login Register
Bu kısmı yapacağım, hazır halleri var, uzun sürmez

## admin table
CREATE TABLE admin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO admin values (
1,
'semihgencten',
'test'
)