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

## Log in for admin:
Eğer elinizdeki Formula1.sqlite instance'ında admin tablosu oluşmamışsa aşağıdaki sql sorgusuyla tabloyu oluşturup kullanıcı ekleyebilirsiniz.
Register sayfası oluşturmadım çünkü bu sadece adminler için, her isteyen register olsa adminliğin anlamı kalmaz.
Eğer log in olmuşsa Welcome username şekline sağ üstte adı görünüyor ve yanında logout görünüyor. Log in olmamışsa log in görünüyor.



## Base html 
kendi sayfamı ve edanın sayfasını base den extend ettim fakat yasin'in sayfasında denediğimde düzgün olmadı. Kullandığı css den dolayı.
Kendisime bırakıyorum o kısmı

# Create update delete işlemleri için login required
@login_required ı fonksiyonun başına koyarak sadece log in olmuşsa fonksiyonun çalışmasını sağlayabilirsiniz
Fakat edit create butonlarının login olmamışsa görünmemesi için:
Burada basit bir şey yaparak bunu sağlayabiliyoruz. templates/drivers/index sayfasına giderseniz en altta create için yazdığım formun başında ve sonundaki
  {% if g.user %}{% endif %}
ifadelerini görebilirsiniz. Bunlar sayesinde içindeki kısımlar sadece kullanıcı giriş yapmışsa render ediliyor ve basitçe istediğimiz özelliği elde etmiş oluyoruz.