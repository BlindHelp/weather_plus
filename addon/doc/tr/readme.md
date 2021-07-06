# Weather Plus #

* Yazar: Adriano Barbieri
* NVDA uyumluluğu: 2017.3 ve  sonrası
* İndir: [Kararlı sürüm][1]

# WEATHER PLUS Hakkında: #

* Bu eklenti seçilen yerle ilgili anlık ya da saatlik hava durumu bilgisinin ve  istenirse önümüzdeki 2 gün dahil 24 saatlik hava raporunun NVDA ile alınmasına olanak tanır.
* Telif hakkı (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* GNU GPL (Genel Kamu Lisansı) v2 altında yayınlandı
* Weather Plus, aşağıdaki hizmetlerin kullanımı ve varlığı üzerinden çalışır:
* [https://www.weatherapi.com/](https://www.weatherapi.com/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.nvda.it/](https://www.nvda.it/)

# KULLANIM: #

* Mevcut sıcaklık ve hava koşulları hakkında bilgi almak için NVDA+w tuşlarına basın.
* 24 saatlik  ve 2 güne kadar hava tahmini almak için NVDA+shift+W tuşlarına basın.
* Saatlik sıcaklık ve atmosfer koşulları tahminini almak için NVDA+shift+W tuşlarına iki kez basın.
* Geçici bir şehir ayarlamak için NVDA+shift+control+w tuşlarına basın.
* Weather Plus ayarları iletişim kutusunu açmak için NVDA+shift+control+alt+w tuşlarına basın.
* Hava durumu raporunun güncellendiği tarih ve saati almak için NVDA+alt+w tuşlarına basın.
* Fahrenheit, Celsius veya Kelvin sıcaklık ölçekleri arasında geçiş yapmak için control+shift+w tuşlarına basın.

# Weather Plus kurulumu: #

* İlk kullanımdan önce Weather Plus eklentisini ayarlamalısınız! Tercihler alt menüsü, Weather Plus Ayarları alt menüsüne gidin ve aşağıdaki seçeneklerden birini seçin::
 * Şehirlerinizi Ayarlayın / Yönetin... - Listeden bir şehir seçmenize ya da eklemenize olanak tanır.
 * Geçici bir şehir belirleyin... - Liste varsa içinden birini geçici olarak belirlemenize olanak tanır.
 * Dokümantasyon - Geçerli dil için yardım dosyasını açar.
 * Güncellemeleri kontrol et... - Yeni sürümün varlığı hakkında bilgilendirir.

Yeni bir şehir eklemek için: aşağıdaki seçeneği kullanın:

* Şehirlerinizi Ayarlayın / Yönetin... - Şehri varsa listeden seçmenize veya yeni bir tane eklemenize olanak tanır.
* Aşağıdaki mesaj yalnızca ilk seferinde  gösterilir! Bir şehir belirlenmemiş F1: Yardım mesajını söyler, F2: son SEKME seçimi, F3: liste ve düzenleme kutusu, F4: hava tahmin süre alanı, F5: ses denetimleri.
* Düzenleme kutusunda, bir Şehir girin veya varsa listeden birini seçin. Not: Ses efektleri etkinleştirilirse F5 tuşu kullanılabilir.
* "Şehirlerinizi Ayarlayın ve Yönetin..." dedikten  sonra, aşağıdaki diğer düğmeleri bulacaksınız:
* Sına - Şehir geçerliliğini test edin ve verilerini bulun.
* Ekle - Girilen şehri listenize ekler. Bu düğme, girilen şehir sınamayı geçtiğinde  gösterilir.
* Ayrıntılar - Geçerli şehir hakkında bilgi verir. Bu düğme, listeden bir şehir seçerseniz veya girdiğiniz sınamayı geçtiyse etkinleştirilir.
* Tanımla - Ses efektlerini uyarlamak için alanı tanımlamanızı sağlar. Bu düğme, ses efektleri yüklenip etkinleştirilirse ve listeden bir şehir seçerseniz etkinleştirilebilir.
* Varsayılan yap - Bir şehri varsayılan olarak ayarlar, eklentiyi her yeniden başlattığınızda bu şehir kullanılacaktır. Bu düğme, daha önce listeye eklenmiş ve önceden varsayılan yapılmamış bir şehri seçerseniz veya girdiğiniz şehir sınamayı geçmişse etkinleştirilir.
* Kaldır - Bulunduğunuz şehri listenizden siler. Bu düğme, daha önce listeye eklenmiş bir şehri seçerseniz etkinleştirilebilir.
* Yeniden Adlandır - Mevcut şehri yeniden adlandırın. Bu düğme, daha önce listeye eklenmiş bir şehri seçerseniz etkinleştirilebilir.
* Yeni şehirleri içe aktar... - Bu düğme, *.zipcodes uzantılı bir başka dosyada kayıtlı şehirleri listenize eklemenizi sağlar; İçe aktarmak istediğiniz şehri, onunla ilişkili onay kutusunu işaretleyerek seçebilirsiniz.
* Şehirlerinizi dışa aktarın... - Şehirleri *.zipcodes uzantısıyla belirtilen dosyaya kaydetmenizi sağlar. Listeye en az bir şehir eklediyseniz ve kaydettiyseniz bu düğme etkinleştirilebilir.
* saatlik tahmin ayarı... - Bu düğme, saatlik tahmin raporunun içeriğini seçmenizi sağlar.
* Sıcaklık ölçüm birimi: Celsius (varsayılan olarak), Fahrenheit ve Kelvin arasında seçim yapmak için radyo düğmesini kullanın.
* Derece şu şekilde gösterilsin: Şunlar arasında seçim yapmak için radyo düğmesini kullanın: Celsius `-` Fahrenheit `-` Kelvin (varsayılan olarak) C `-` F `-` K veya Belirtilmemiş.
* Şu kadar günlük hava tahmini seçim kutusu: Günlere kadar Hava Tahminleri: 1; 1 ila 3 arasında seçim yapabilirsiniz (varsayılan olarak 1 gün)
* Seçim kutusu: API yanıt dili:: İngilizce, tr; hava durumu metninin dilini seçebilirsiniz.
* Aşağıdaki eylemleri gerçekleştirmek için aşağıdaki onay kutularını işaretleyin:
* Panoya şehir ayrıntıları dahil hava raporu ve hava tahminini Kopyala; onay kutusu işaretli değil (varsayılan olarak)
* Ses efektlerini etkinleştirin (yalnızca mevcut hava koşulları için); bu onay kutusu ayrıca ses efektlerinin kurulumunu yönetmenizi sağlar; ses efektleri kuruluysa ve onay kutusu etkinleştirilmişse, F5 tuşu ve ses düzeyi ayarı kullanılabilir hale gelir.
* Yukarıdaki işaretlenirse ayrıca ek bir onay kutusu olacak: "Yalnızca hava efektlerini kullan".
* Genel ses seviyesini değiştirebilir veya son duyulan ses efektini değiştirebilir ve ortamınızdaki diğer sesleri filtreleyebilirsiniz. Onay kutusu varsayılan olarak işaretli değildir.
* Yalnızca hava efektlerini kullan - Bu seçenek, ses efektleri etkinleştirilmişse kullanılabilir; etkinleştirilirse, tüm çevresel efektleri filtreleyerek yalnızca yağmur, rüzgar, gök gürültüsü vb. gibi hava efektlerinin dinlenmesine izin verir. (varsayılan olarak işaretli değil)
* Saatler 24 saat formatında seslendirilsin . - Bu onay kutusu işaretli değilse, saati 12 saatlik biçimde duyurur, örneğin, 12 AM `-` 12 PM. Onay kutusu işaretli (varsayılan olarak)
* Ayarlar penceresindeki düğmelerle ilgili yardım mesajlarını etkinleştir; onay kutusu işaretli (varsayılan olarak)
* Rüzgar bilgisini  seslendir; onay kutusu işaretli değil (varsayılan olarak). Bu onay kutusu etkinleştirilirse, aşağıdaki onay kutularını da etkinleştirebilirsiniz:
* Rüzgar yönü bilgisini ekle; rüzgarın nereden  estiğini gösterir. Onay kutusu işaretli (varsayılan olarak)
* Rüzgar hızını ekle; hızı kilometre veya mil/saat olarak gösterir. Onay kutusu işaretli (varsayılan olarak)
* Rüzgarın saniyede kaç metre hızla estiği  bilgisini ekle; onay kutusu işaretli (varsayılan olarak)
* Rüzgar esinti  hızını ekle; onay kutusu işaretli (varsayılan olarak)
* Hissedilen sıcaklığı ekle; onay kutusu işaretli (varsayılan olarak)
* Atmosferik bilgileri seslendir; onay kutusu işaretli değil (varsayılan olarak). Etkinleştirilirse, aşağıdaki onay kutularını da işaretleyebilirsiniz:
* Nem değerini ekle; yüzde olarak nemi gösterir. Onay kutusu işaretli (varsayılan olarak)
* Görüş mesafe değerini ekle; görünür mesafeyi kilometre veya mil olarak belirtin. Onay kutusu işaretli (varsayılan olarak)
* Atmosferik basınç değerini ekle; atmosfer basıncını milibar veya inç cıva olarak gösterir. İşaretliyse, basıncı milimetre cıva cinsinden belirtmenize izin veren ek bir onay kutusunu etkinleştirin. Onay kutusu işaretli (varsayılan olarak)
* Bulutluluk değerini ekle; onay kutusu işaretli (varsayılan olarak)
* Yağış değerini ekle; onay kutusu işaretli (varsayılan olarak)
* Ultraviyole radyasyon değerini ekle; onay kutusu işaretli (varsayılan olarak)
* Astronomik bilgileri seslendir; gündoğumu / günbatımı  ve ay doğumu ve batışı zamanlarını gösterir. Onay kutusu işaretli değil (varsayılan olarak)
* Ondalık sayıları ayırmak için virgül kullanın; etkinleştirilirse, ondalık ayırıcı olarak virgül kullanır, aksi takdirde noktayı kullanın. Onay kutusu işaretli değil (varsayılan olarak)
* Güncelleme olup olmadığını denetle; etkinleştirilirse, eklenti güncellemesi olduğunda bu uyarı verir. Onay kutusu işaretli (varsayılan olarak)
* Çıktıyı bir pencerede görüntüler; etkinleştirilirse bu, tahmini bir pencerede görüntüler. Onay kutusu işaretli değil (varsayılan olarak)
* Değişiklikleri onaylamak için Tamam düğmesine veya iptal etmek için İptal düğmesine basın.
* Şehirler listesini değiştirdiyseniz, "İptal" düğmesine basarsanız bu konuda uyarılırsınız ve yine de kaydedebilirsiniz. Not: Ayarlarınız şu dosyaya kaydedilecektir:
* "Weather.ini": Weather Plus'ın başlangıç ayarları.
* "Weather.volumes": genel ses seviyesinden bağımsız olarak belirlenmiş özel ses seviyesi seviyeleri.
* "Weather.zipcodes": posta kodları ve tanımları ile şehirlerin listesi.
* "Weather.default": Varsayılan şehriniz.
* "Weather_searchkey": kaydedilen arama ifadeleri.

--------------------------------------------------------------------------------
[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
