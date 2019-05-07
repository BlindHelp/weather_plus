# Weather Plus #

* Autor: Adriano Barbieri
* NVDA kompatibilnost: 2017.3 do 2019.1
* Preuzmi: [stabilnu verziju][1]

# O DODATKU WEATHER PLUS: #

* Ovaj NVDA dodatak daje dvadesetčetvoročasovni vremenski izveštaj i prognozu za 9 dana unapred.
* Copyright (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Objavljeno u GNU GPL (General Public License; Opšta Javna Licenca) v2
* Verzija: 6.0.

# Weather Plus koristi sledeće servise:: #
* [https://developer.yahoo.com/weather/](https://developer.yahoo.com/weather/)
* [http://woeid.rosselliot.co.nz/lookup/](http://woeid.rosselliot.co.nz/lookup/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.timeanddate.com/](https://www.timeanddate.com/)
* [http://www.nvda.it/](http://www.nvda.it/)

# Korišćenje: #
* Pritisnite NVDA + w da čujete trenutnu temperaturu i prognozu vremena.
* Pritisnite NVDA + Shift + w za 24 časovnu prognozu i prognozu do 9 dana unapred.
* Pritisnite NVDA + Shift + ctrl + w da postavite privremeni grad.
* Pritisnite NVDA + šift + kontrol + alt + w da otvorite dijalog sa podešavanjima weather plus dodatka.
* Pritisnite NVDA + Alt + w da saznate zadnje ažuriranje vremenske prognoze.
* Pritisnite Ctrl + Shift + w da izaberete između Farenhajt, Celzijus ili Kelvin merne jedinice za temperaturu.

# Da podesite Weather Plus: #
Pročitajte sekciju: Weather Plus Prva Podešavanja.

--------------------------------------------------------------------------------

# Weather Plus Prva Podešavanja: #

Morate podesiti Weather Plus dodatak pre prvog korišćenja!

Idite u:

Podešavanja podmeni

Podešavanja Weather Plus podmeni

Prikaži stavke konfiguracije.

# Pritisnite stavku: #

* Postavi i upravljaj gradom...
	* Prikazuje ili dozvoljava postavljanje trenutnog grada sa liste
* Dokumentacija
	* Otvara datoteku pomoći za trenutni jezik
* Proveri nadogradnje...
	* Obavesti ako je dostupna nadogradnja

Pritisnite stavku:

# Postavi i upravljaj gradom... #

Prikazuje ili dozvoljava postavljanje trenutnog grada sa liste

Ova se poruka prikazuje samo prvi put!

Podešavanja Zadato Podešavanje

Nema

F1: pomoć u postavljanju, F2: zadnji tab položaj, F3: lista i edit polje, F4: kontrola trajanja vremenske prognoze, F5: jačina zvuka.

Unesite Grad, voeID ili izaberite sa liste, ako postoji.

Napomena: F5 je aktivno ako su uključeni zvučni efekti.

Kada pritisnete stavku "Postavi i upravljaj gradom...", pronađite sledeću dugmad kako slede:

# Testiranje #

Testira validnost unetog voeID_a i nalazi ime dodeljenog grada ili obrnuto.

# Dodaj #

Dodaje trenutni grad u vašu listu.

Ovo dugme je vidljivo ako ste izabrali grad sa liste, ili ako je prošao test.

# Detalji #

Ovo prikazuje informacije za izabrani grad.

Ovo dugme je vidljivo ako ste izabrali grad sa liste, ili ako je prošao test.

# Odredite #

Ovo vam omogućava da definišete regiju, radi dodavanja zvučnih efekata.

Ovo dugme je vidljivo ako su zvučni efekti instalirani i aktivirani, ili ako ste odabrali grad sa liste, ili ako je prošao test.

# Zadato Podešavanje #

Postavlja trenutni grad kao podrazumevani, što znači da će isti biti učitan svaki put kad se restartuje dodatak.

Ovo dugme je aktivno ako ste odabrali grad predhodno unet na vašu listu Ako već nije podrazumevan, ili ako je prošao test.

# Ukloni #

Za prisanje grada sa liste.

Ovo dugme je aktivno ako ste odabrali grad predhodno unet na vašu listu.

# Neimenovan #

Za brisanje grada iz vaše liste.

Ovo dugme je aktivno ako ste odabrali grad predhodno unet na vašu listu.

# Uvezite nove gradove... #

Dozvoljava vam da u vašu listu ugradite nove gradove uvezene iz druge liste sa ekstenzijom *.zipcodes; možete odabrati grad koji ćete uvesti, štikliranjem čekboksa uz njegovo ime.

# Izvezite vaše ID_ove... #

Dozvoljava vam da sačuvate vašu listu gradova na određenom mestu.

Ovo dugme je aktivno ako ste dodali i sačuvali bar jedan grad u svoju listu.

# Jedinice za merenje temperature: #

Koristite radio dugmad da odaberete sledeće:

* Celzijus (podrazumevano)
* Farenhajt
* Kelvin

# Stepeni prikazani kao: #

Koristite radio dugmad da odaberete između:

* Celzijus `-` Farenhajt `-` Kelvin(podrazumevano)
* C `-` F `-` K
* Nije određeno

Kombo box (ili odabirni okvir):

# Vremenska prognoza do dana: 3 #

Izaberite između 1 i 10 (3 dana je podrazumevano)

Uključite ili isključite čekboks za:

# Kopiraj vremenski izveštaj i vremensku prognozu, uključujući i podatke o gradu u međuspremnik (klipbord) #

Čekboks nije štikliran (podrazumevano)

# Povoliť zvukové efekty (iba za aktuálnych poveternostných podmienok) #

Toto začiarkavacie pole vám tiež umožňuje spravovať inštaláciu zvukových efektov;

Ak sú zvukové efekty nainštalované a začiarkavacie políčko je aktivované, tlačidlo F5 a nastavenie hlasitosti budú dostupné.

K dispozícii bude tiež ďalšie začiarkávacie pole:

* Použite len efekty počasia.

Môžete zmeniť celkovú hlasitosť alebo zmeniť posledný počúvaný zvukový efekt a filtrovať ostatné zvuky vo vašom prostredí.

vo východzom stave nezačiarknuté

# Použiť iba efekty počasia #

je k dispozícii, ak sú zapnuté zvukové efekty;

Ak je povolené, umožňuje počúvať iba efekty počasia, ako je dážď, vietor, hrom, atď., ktoré sú odfiltrované od všetkého okolitého.

vo východzom stave nezačiarknuté

# Omogućuje očitavanje sata u dvadeset i četvoročasovnom formatu #

Ako nije štiklirano, Očitava vreme u dvanaestočasovnom formatu, na primer 12AM ili 12PM

Čekboks je štikliran (podrazumevano)

# Označava Čekanje kraja traženja zadnjeg vremenskog izveštaja sa zvučnim signalom #

Ako je omogućeno, čućete zvučni bip signal koji označava progres pretrage novog vremenskog izveštaja, sve dok se izveštaj ne ažurira.

Čekboks je štikliran (podrazumevano)

# Omogućuje prikazivanje dugmeta pomoći u prozoru za podešavanje NVDA dodataka #

Čekboks je štikliran (podrazumevano)

# Pročitaj izveštaj o vetru #

Ček boks nije štikliran (podrazumevano)

Ako je štiklirano (označeno), takođe možete da aktivirate:

* Dodaj pravac vetra;

Prikazuje pravac vetra.

Ček boks je štikliran (označen) (podrazumevano)

* Dodaj brzinu vetra;

Prikazuje brzinu u kilometrima, ili miljama na čas.

Ček boks je štikliran (podrazumevano)

* Dodaj brzinu vetra u metrima po sekundi;

Ček boks je štikliran (podrazumevano)

* Dodaj  subjektivni osećaj temperature;

Ček boks je štikliran (podrazumevano)

# pročitaj atmosferski izveštaj #

Ček boks nije štikliran (podrazumevano)

Ako je štiklirano, takođe aktivirate:

* Dodaj vrednost vlažnosti;

Prikazuje vlažnost vazduha u procentima.

Ček boks je štikliran (podrazumevano)

* Dodaj vrednost vidljivosti;

Prikazuje vidljivost u daljinu u kilometrima ili miljama.

Ček boks je štikliran (podrazumevano)

* Dodaj vrednost atmosferskog pritiska;

Prikazuje atmosferski pritisak u milibarima ili milimetrima živinog stuba.

Ako je opcija označena, dodaje dodatno izborno polje koje vam dozvoljava da prikažete Pritisak u milimetrima živinog stuba.

Ček boks je štikliran (podrazumevano)

* Dodaj status barometarskog pritiska;

Ček boks je štikliran (podrazumevano)

# Pročitaj astronomski izveštaj #

Prikazuje vreme izlaska i zalaska Sunca.

Ček boks nije štikliran (podrazumevano)

# Koristite zarez da razdvojite decimale #

ako je štiklirano, koristiće se zarez za razdvajanje decimala, a ako nije štiklirano, koristiće se tačka.

Čekboks nije štikliran (podrazumevano)

# Proveri ima li nove verzije #

Ako je štiklirano, obaveštava o novoj verziji WP dodatka.

Čekboks je štikliran (podrazumevano)

Pritisnite U redu dugme da potvrdite promene, ili odkaži dugme da odkažete.

# Napomena: vaša podešavanja će biti sačuvana u datoteci: #

* "Weather.ini": startna podešavanja za Weather plus.
* "Weather.volumes": prilagođava jačinu zvuka nezavisno od sistemske jačine zvuka.
* "Weather.zipcodes": lista gradova sa njihovim Zip Kodovima i ostalim podacima.

--------------------------------------------------------------------------------

# Šta je novo: #

# Version 6.0 #
* Weather Plus returns to using the Yahoo Weather API.
* Virtually all the features of the previous version 4.8 are back and keeps the "Rename" button.
* Now compatible also with Python 3.

# Version 5.0.1 #
* Fixed bug, that returned an empty string if the wind speed in mph was 0.
* Fixed bug that caused sound effects not consistent with the time zone to be reproduced.
* adjusted the number of forecast days from 9 to 6 in readme.

# Version 5.0 #
* Weather Plus now uses the APIXU API, in my opinion better than the previous one.

`#`Changes in the Weather Plus Settings window:

* Removed old checkbox "State of barometric pressure".
* Replaced with new checkbox "Add cloudiness value";
	* It gives you the percentage of cloudiness.
* Added new checkbox "Add precipitation value";
	* It gives you the amount in millimeters of precipitation.
* Removed old checkbox "Indicates the wait with a beep while you search for the latest bulletin";
	* Left active by default.
* Added to the Astronomic informations;
	* Time of moonrise and moonset.
* Added new button "Rename";
	* To rename cities more conveniently.
* Improved function of the "Test" button;
	* Now accept some commands to facilitate the search for cities;
	* These new commands are described in the help function that can be called up with F1.

# Verzija 4.8 #
`#`Promene u prozoru podešavanja Weather Plus:

* Dodato je novo izborno polje;
  	* "Koristi samo vremenske efekte";
	* Ovo vam omogućuje da odbacite sve ostale ambijentalne zvukove.
  * Poboljšana je nasumična reprodukcija i dodato je 71 novih zvukova;
	* Trebaćete da ih nadogradite  dvostrukim klikom na izborno polje "Omogući audio efekte" .
* Vrsta jačine zvuka odabrana od strane korisnika, opšta ili trenutna jačina zvuka, sada se optimizuje kada se podešavanja sačuvaju.
* Uklonjen je beskoristan zvuk prilikom selektovanja teksta u edit polju, pritiskom na prečicu control+a.
* Poboljšana je čitljivost prozora pomoći pomoću F1 funkcijskog tastera.
* Omogućena je kompatibilnost sa NVDA 2019.1, i trenutnim alfa verzijama.

# Verzija 4.7.7 #
* Uklonjeno je nepotrebno obaveštenje o završenom preuzimanju posle nadogradnje Weather Plus.
* Dodato je 6 novih zvučnih efekata;
	* Biće potrebno da se zvučni efekti ažuriraju da bi svi bili dostupni, što se može učiniti u postavkama za ovaj dodatak.

# Verzija 4.7.6 #
* Popravljena je mala greška u funkciji GetCoords();
	* Dve vrednosti se nisu očitavale kod problema sa konekcijom.

# Verzija 4.7.5 #
* MenuItem.GetLabel() je zamenjen sa MenuItem.GetItemLabelText().
* Gde su ispravljeni neki zapisi globalnih varijabli.

# Verzija 4.7.3 #
* Ažurirana je funkcija u "detalji";
	* Radi poboljšanja, podatke o geografskoj širini sada obezbeđuje  veloroutes.org.
	* Ovo vodi malim razlikama u tačnosti.

# Verzija 4.7.2 #
* Popravljena je greška u kodiranju ufunkciji uklanjanja nadogradnje (removeupdate).

# Verzija 4.7.1 #
* Popravljena je gre¹ka u GetTimezone;
	* U sluèaju nule, podaci su prikazivani kao jedna a ne tri predviðene vrednosti.

# Verzija 4.7 #
* Pojednostavljena je nadogradnja;
	* Sada će, ako postoji nadogradnja, biti moguće sve odraditi u samo jednom dijalogu.
* Nema više ručnog izbora datoteke za nadogradnju tokom ažuriranja;
	* Sada će datoteka za ažuriranje biti preuzeta u privremeni folder, čime će biti rešen problem  koji imaju korisnici početnici.

# Verzija 4.6.9 #
* Dodat je prevod lokalizacije na arapski jezik ( zahvaljujući Wafik Immaculate).

# Verzija 4.6.8 #
* Ažurirani su prevodi na portugalskom i Brazilskom portugalskom u lokalizaciji (zahvaljujući Albertu Mendonçi).

# Verzija 4.6.7 #
* Ispravljeno je čitanje trenutnog vremena;
	* Za neke gradove vreme nije bilo pravilno prikazano.
* Dodato je letnje računanje vremena u detaljima o gradu;
	* Omogućeno za zemlje koje prihvataju letnje računanje vremena.

# Verzija 4.6.5 #
* Popravljena je mala greška u izgovaranju trenutnog vremena;
	* Razdvajač decimala ":" nije bio uklonjenkad se vrednost pretvori u ceo broj.

# Verzija 4.6.4 #
* Popravljeno je čitanje trenutnog lokalnog vremena; Pretraga je još preciznija.

# Verzija 4.6.2 #
* Popravljena je greška: posle provere nadogradnje, komanda menija  "Postavite privremeni grad..." je bila omogućena i ako nije bilo dostupne liste gradova.
* Popravljena je greška; nije moguće konfigurisati wp dok još datoteka weather.ini nije konfigurisana.

# Verzija 4.6 #
* Dodata je stavka menija "Postavi privremeni grad...";
	* Sada se lista gradova za izbor privremenog grada može dobiti i iz menija.
* Popravljeno je upravljanje mernim jedinicama temperature;
Od sada će prozor za podešavanja uvek vraćati odabir na zadatu vrednost.
* Ispravljeno je višestruko otvaranje glavnih prozora;
Ako je jedan od prozora već otvoren, biće postavljen u fokus, uz zvučni signal.
* Popravljeni su zvučni efekti;
	* Sada će se oni prilagođavati lokalnom vremenu za trenutno korišćeni grad.
	* Promene u funkciji dugmeta detalji u prozoru za podešavanje:
* Dodato je trenutno lokalno vreme.
* Popravljena je vrednost nadmorske visine;
	* Sada se vrednosti nadmorske visine vraćaju, ako su manje ili jednake nuli.
* Popravljena je funkcija uvoza gradova;
	* Ako je podrazumevani grad uklonjen, više se neće prikazivati u naslovnoj traci.

# Verzija 4.5.5 #
* Ispravljen je prevod za Srpski jezik u lokalizaciji dodatka i u dokumentaciji.
* Ispravljen je prevod za Nemački jezik u lokalizaciji.

`#`Promene u prozoru za podešavanja Weather Plus:

* Dodato je novo polje za označavanje (čekboks);
	* Možete omogućiti zarez kao decimalni razdvajač, ili će decimalni razdvajač ostati tačka.

# Verzija 4.5.3 #
* Ispravljena su dva stringa na  Ruskom i ukrainskom jeziku.
* Ispravljen je naslov na Češkom jeziku za prozor nadogradnje.
* Poboljšan je algoritam za nadogradnju;
	* Sada se veza za direknu nadogradnju iščitava iz manifest datoteke i njenog linka za nadogradnju.

# Verzija 4.5 #
* Dodata prečica NVDA+šift+kontrol+alt+w;
	* Otvara weather plus podešavanja.
* Ispravljeni su neki engleski stringovi.

`#`Promene u Weather Plus prozoru za podešavanja:

* Dodato je 8 novih čekboksova (polja za označavanje-štikliranje);
	* Sada je moguće dodatno podešavanje informacija:
* Pravac vetra.
* Brzina vetra.
* Subjektivni osećaj temperature.
* Vrednost vlažnosti.
* Vrednost vidljivosti.
* Vrednost atmosferskog pritiska.
* Prikazuje atmosferski pritisak u milimetrima živinog stuba (mmHg).
* Status barometarskog pritiska.

# Verzija 4.4.8 #
* Dodat je prevod na Poljskom (zahvaljujući Zvonimiru Staneczyću).
* Weather Plus je sada kompatibilan, a i u buduće bi trebalo da bude sa wx verzijom 4;
	* Napomena: Trenutno sa wx verzijom 4.0.0b1 msw (phoenix) generiše grešku pri korišćenju strelica gore ili dole u mnogim edit poljima:

wxAssertionError: C++ assertion "Assert failure" failed at ..\..\src\common\evtloopcmn.cpp(110) in wxEventLoopBase::Yield(): wxYield called recursively.

# Verzija 4.4.1 #
* Dodata je SSL podrška;
	* Koristi se samo ako se pojavi greška u verifikovanju SSL sertifikata.

# Verzija 4.4 #
* Popravljena je greška u čitanju stringa za novu verziju tokom pauze u povezivanju.
* Poboljšana je sekcija za nadogradnju;
	* Sada dijalog više ne ometa NVDA meni.
* Revidirana je i popravljena Ruska lokalizacija.
* Dodat je prevod na Ukrainski (zahvaljujući Alex Yeshanu).

# Verzija 4.3.4 #
* Revidirana je i popravljena Nemačka lokalizacija.

# Verzija 4.3.3 #
* Dodat je prevod na Nemački jezik (zahvaljujući Karlu Eicku).

# Verzija 4.3.2 #
* Dodat je prevod na Rumunskom (zahvaljujući Florian Ionașcu).

# Verzija 4.3.1 #
* Ispravljena je mala greška u funkciji "detalji";
	* Stringovi "Geografska širina" and "Geografska dužina"su pravilno povezani sa svojim vrednostima.

# Verzija 4.3 #
* Linkovi sa Dropboxpablik foldera će postati neaktivni 15_og marta.
	* Od tog datuma, Pablik folder će postati standardni Dropbox folder i neće biti upotrebljiv za WP dodatak.
	* Linkovi za nadogradnju dodatka i zvučnih datoteka su ažurirani, Zbog toga, od sada će se nadogradnjeza WP dodataknalaziti na Italijanskoj Weather Plus stranici.

# Verzija 4.2.4 #
* Fixed a minor bug when the connection is not active.

# Verzija 4.2.3 #
* Weather Plus sada može da pokuša nekoliko puta da se poveže pre nego pročita obaveštenje
	* Kod neispravnosti trenutno korišćenog voeID_a, pri svakom pokušaju konekcije čuće se zvučni signal;
	* Ovaj zvučni signal se može isključiti, ako želite, uWeather Plus podešavanjima.

# Verzija 4.2.2 #
* Popravljena je greška u prikazivanju mernih jedinica;
	* U nekim jezicima Kelvin, Farenhajt i Celzijus nisu bili prevedeni.

# Verzija 4.2.1 #
* Popravljeno je obaveštavanje o ažuriranju u toku podizanja sistema;
	* Kada se u opštim podešavanjima pritisne dugme "Koristi trenutno sačuvana podešavanja na ekranu za prijavljivanje i drugim bezbednosnim ekranima (zahteva administratorske privilegije )", prilikom podizanja windowsa, javljalo se obaveštenje o ažuriranju WP_a bez obzira na realno stanje dodatka zbog neusaglašenosti trenutne i globalne konfiguracije NVDA.
	* Ako vam se nekad to dešavalo zbog tako podešene opcije u Weather Plus dotatku, posle ovog ažuriranja se više neće ponavljati.

# Verzija 4.2 #
* Dodato je 5 novih zvučnih efekata;
	* Biće potrebno da se zvučni efekti ažuriraju da bi svi bili dostupni, što se može učiniti u postavkama za ovaj dodatak.
* Popravljena je greška u funkciji uvoza gradova;
	* Lista gradova nije bila složena po azbučnom redu.
* Dodat je uvozni režim u funkciji uvoza gradova;
	* Možete odlučiti da zamenite celu listu, ili da pojedinačno dodate novi grad.
* Ažurirano je iščitavanje trenutne vremenske prognoze u vremenskom izveštaju;
 	* Dodat je doživljaj temperature (wind chill).
 * Dodati su i novi stringovi u listi vremenskih izveštaja.

# Verzija 4.1 #
* Popravljena je prognoza za narednih 10 dana;
	* Sada, ako je broj dobijenih prognoza manji od onoga što je naveo korisnik, navedeni dani se beleže kao nepoznati.
* Prepravljen je string za komandu NVDA + shift + w.
* Dokumentacija je revidirana i obnovljena.

# Verzija 4.0 #
* Unapređeni su neki delovi koda i zamenjene sve instrukcije eval().

# Verzija 3.9.7 #
* Ispravljena je greška u korišćenju vremenske prognoze;
	* Sada se temperatura iščitava korektno.

# Verzija 3.9.6 #
* Izmenjeno je odabiranje jedinice mere za atmosferski pritisak iz bara u inčama po merkuriju;
	* Sada se vrednost zaokružuje na manju umesto na veću decimalu (primer: 10.5 se zaokružuje na 10 umesto na 11).

# Verzija 3.9.5 #
* Dodata su dva nova stringa u listi vremenskog izveštaja.
* Popravljene su dve greške.
* Ažurirani su zvukovi koji prate vremenski izveštaj samo za vetar;
	* Sada zvuk vetra može nasumično da varira.

# Verzija 3.9.4 #
* Dokumentacija, lokalizacija za Hrvatski i Nemački jezik je uklonjena jer za njih više nema podrške;
	* Zbog toga što prevodioci ovih jezika više ne sarađuju na prevodu.
* Popravljena je greška za srpsku lokalizaciju.
* Nadograđena je češka lokalizacija.
* Nadograđena je dokumentacija i lokalizacija za Galego.

# Verzija 3.9 #
* Ponovo promenjen API servis;
	* Weather Plus sada koristi novi Yahoo meteo API sa jezikom Yahoo!Query and JQuery:
	* [yahoo-weather-api-with-yahooquery](http://codesimplified.blogspot.it/2013/10/yahoo-weather-api-with-yahooquery.html)
* API ključ više nije potreban.
* Vraćena je pretraga po homonimima gradova;
	* Biće moguće izabrati tačno određeni grad sa liste.
* Usklađena je jačina zvuka pozadinskih efekata;
	* Sada su oni usklađeni sa govorom i brže se odazivaju.
* Unapređena je keš memorija podataka van mreže;
	* Osvežava se svakih 10 minuta ili promenom grada.
* atmosferski pritisak se meri u milibarima, ili u inča živinog stuba (ako je podešeno na farenhajt).

# Verzija 3.8 #
* Izmenjen je API paket podataka;
	* iz XML u JSON format, podaci su tačniji, posebno vremenska zona.
* Omogućeno je automatsko podešavanje jezika;
	* Sada API šalje podatke o vremenskoj prognozi u izabranom jeziku.
* Dodata je keš memorija za vremensku prognozu i izveštaj;
	* Ako grad ili jedinica za merenje temperature, ili broj dana za prognozu nije promenjen, moći ćete da dobijete izveštaj do 10 minuta nakon prekidanja internet veze.
	* Keš memorija se briše nakon svake izmene predhodno navedene.
	* Ovo je zato što se izveštaji ne menjaju u u tom vremenskom periodu i da bi se smanjilo učestalo pozivanje API_ja, ili zbog mogućeg reprodukovanja zvučnih efekata.
* Poboljšana je pretraga za nadogradnjama;
	* Sada kad se preuzme, biće aktivirana instalacija, ili u slučaju portabilne verzije NVDA biće otvorena fascikla gde će se moći sačuvati nadogradnja.
* Nadograđena su sva zvučna obaveštenja;
	* Više se ne koristi modul "tones" već su sada to mali wave fajlovi.

# Verzija 3.7 #
* Dodata je mogućnost da se isključi merenje brzine vetra u metrima po sekundi.
* Dodata je mogućnost korišćenja merne jedinice funta po kvadratnom inču.
* Ispravljene su dve greške.

# Verzija 3.6 #
* Promenjen API servis (aplikacijsko programski izgled);
	* sada WP koristi servis sa  OpenWeatherMap.org umesto Yahoo Weather.com.
* Dodata je klasifikacija vetrova u trenutnoj prognozi.
* Dodata je oblačnost u procentima u trenutnoj prognozi.
* Usvojen je Hektopaskal kao merna jedinica pritiska.

`#`Promene u Weather Plus prozoru podešavanja:

* Promenjeno je umetanje ili pretraga iz Yahoo zipkoda ili VoeID parametra u brojčani identifikator grada, ID;
	* ID je sličan kao voeID, ali voeID više nije u funkciji, kao ni stari Zip kodovi.
	* Bićete u mogućnosti da pretražite veliki broj gradova upisivanjem njihovog imena ili samo dela imena.
* Dodata je pretraga ili upisivanje po geografskim koordinatama.
* Dodato je upisivanje ili pretraga prema poštanskom broju.
* Popravljena je funkcija "detalji".
* F1 tasteru je dodeljena funkcija pomoći za unos  ili pretragu.
* F4 tasteru je dodeljena kontrola izbora prognoze od 1 do 16 dana;
	* Pažnja! Ako odaberete da u međuspremnik (clipboard) kopirate vrednosti veće od 10 dana,to neće biti pročitano!
* F5 tasteru su dodeljene kontrole jačine zvuka.
* Dodat je Kelvin kao merna jedinica temperature.
* Dodata je provera nadogradnje;
	* Ovo možete podesiti kroz podešavanja ili ručno proveriti preko menija.
* Promenjena je funkcija dugmeta "Pronađite svoj grad" u "Uređivanje vašeg API ključa...";
	* Dozvoljava vam da unesete ili izmenite vaš ključ-API.

# Verzija 3.5 #
* Dodat prevod na hrvatskom (zahvaljujući Gordanu Radiću).
* Dodata kontrola za nevažeće WOEid i ZIP kodove sa mreže;
	* Prijavljeno je da neki kodovi povremeno ne rade, WP sada upozorava ako se ovo dogodi u pretrazi na internetu.
	* Ako se ovo desi kada se koristi funkcija "Pronađite svoj grad...", Molim da mi to prijavite kako bih uklonio neispravne kodove i ubacio nove u listu.
* Popravljena je greška u funkciji pretrage za sledeće i predhodno nedostajuće za mbcs kodiranje i kada nisu mogli da budu prepoznati akcentovani ili karakteri sa dijakritikom.
* Ažuriran je prozor za biranje privremenog ZIP koda;
	* Dodata mogućnost pretrage kao i u drugim Weather Plus prozorima:
	* Control+F3 = Pronađi..., F3 = Pronađi sledeće, Shift+F3 = Pronađi predhodno.

# Verzija 3.4 #
* Dodat prevod na Galicijskom (Zahvaljujući Ivánu Novegilu).
* Dodat Portugalski prevod (Zahvaljujući Angelu Miguelu Abrantesu).
* Dodat prevod na nemačkom (nekompletan).

# Verzija 3.3 #
* Dodato merenje brzine vetra u metrima po sekundi.
* Promenjeno kodiranje u "mbcs";
	* Ovo omogućuje korišćenje karaktera sa dijakritikom u imenima gradova.

# Verzija 3.2 #
* Ažurirano čitanje vremenske prognoze, trenutnog vremenskog izveštaja i datuma trenutnog vremenskog izveštaja;
	* Yahoo vremenska prognoza, u kratkom i nasumično odabranom vremenskom periodu, dozvoljava od -5 do -10 predhodnih dana da budu umetnuti u vremenski izveštaj koji želimo da pročitamo;
	* Dodat je filter koji omogućuje čitanje samo zadnjeg ažuriranog vremenskog izveštaja, praćen diskretnim zvučnim signalom koji označava njegov rad;
	* ovaj zvučni bip signal može, ako želite, da bude isključen preko čekboksa u Weather Plus podešavanjima.
	* Očigledno, filtriranje podataka ponekad uzrokuje kratki zastoj u odgovoru, ali je i dalje korisno.
* Prognoza je proširena na 10 dana.

# verzija 3.1 #
* Dodat prevod na Srpski (zahvaljujući ljubaznosti Gašić Dejana `-` Gashich Deyan).
* Popravljena komanda insert+alt+w;
	* Ova komanda nije proveravala validnost Zip Koda u upotrebi i nije proveravala aktivnost internet veze, kao što to rade druge komande.
* Unapređena je funkcija puštanja zvučnih efekata;
	* Sada se koristi kompresovani mp3 format, zahvaljujući kome se skraćuje vreme preuzimanja i smanjuje se potreban prostor na disku.
* Dodato je 55 novih zvučnih efekata;
	* Biće potrebno da se oni ažuriraju kroz podešavanja ovog plugina.

`#`Promene u Weather Plus prozoru podešavanja:

* Popravljen izgled pomoći za dugmad;
	* Sada se uključuju/isključuju u realnom vremenu kroz odgovarajuće čekboksove.
* Dodate su 3 prečice za brže kretanje u prozoru:
* F1 prebacivanje na listu ili edit polje za upis Zip Koda.
* F2 vraća na zadnju poziciju na koju ste došli tabom.
* F3 postavlja vas na kontrolu zvuka (ako su zvučni efekti instalirani i aktivirani).
* Dodate su slovne prečice za sve čekboksove i dugmad;
	* Izostavljena su dva radio dugmeta u nizu, ali je prvo dostupno preko komande control+shift+w.
* Promenjeno je dugme "odredite" koje je sada nedostupno ako zvučni efekti nisu instalirani i aktivirani.
* Dodate su kontrole za podešavanje zvuka;
	* Možete podesiti jačinu zvuka na osnovu zadnjeg zvučnog efekta koji ste čuli;
	* Ova mogućnost je dostupna ako su zvučni efekti instalirani i aktivirani.
* Dodata je mogućnost da podesite sistemsko vreme na dvanaestočasovno (12:30AM `-` 12:30PM), ili dvadesetčetvoročasovno (12:30 `-` 00:30).

# verzija 3.0 #
* Dodat prevod na Slovački (Zahvaljujući ljubaznosti Viteka Jiraseka).
* Dodat prevod na Portugalski i Brazilski Portugalski (zahvaljujući ljubaznosti Adaira Knaesela).
* Dodati novi stringovi u listu vremenskog izveštaja.
* Dodato 171 novih zvučnih efekata i sada ih je ukupno 213.
* Dodata komanda insert + alt + w za izgovaranje zadnjeg ažuriranja vremenske prognoze.
* Dodata skripta koja postavlja sve komande Weather plus na svoje mesto u "Ulazne komande..."

`#`Promene u Weather Plus prozoru podešavanja:

* Dodata su radio dugmad kojima se određuje merna jedinica temperature;
	* može se birati između:
* Celzijus `-` Farenhajt
* C `-` F
* Nije određeno
* Dodato dugme "Odredite";
	* Koje definiše zonu vašeg grada u jedno od sledećih:
* Zaleđe
* Priobalno područje
* Pustinjska zona
* Arktička zona
* Planinska zona
	* Ovo omogućava da za svaki grad koji izaberete imate odgovarajuću zvučnu podlogu;
	* Zbog toga je dodato još mnogo zvučnih efekata u ovoj verziji dodatka;
	* Mnoga od tih zvučnih efekata mi je ustupio Tapin, kome sam iskreno zahvalan.

# verzija 2.9 #
* Dodata mogućnost kada se uvoze podaci, da se vidi sadržaj datoteke iz koje se uvozi.
* Dodata nova 4 zvučna efekta.
* Dodat prevod na Ruski (zahvaljujući Alexu Yeshanuu).
* Dodat prevod na Češki (zahvaljujući Jirimuu Holzingeroviu).

# verzija 2.8 #
* Otklonjena greška u "Detalji"  gde se u prozoru nisu prikazivali detalji o gradu.
* Popravljen regext za pretragu visine koji nije prihvatao parametre pojedinačnih brojki.
* Poboljšan parser za edit polje
	* Sada bi trebalo lakše da pretražuje gradove.
* Internet konekciju sada kontroliše urllib2 umesto urllib
	* što omogućuje da se ovaj dodatak poveže i preko korporativne mreže zaštićene proksijem.
* Dodata opcija "Pronađi"
	* Control+F3 = Pronađi..., F3 = Pronađi sledeće, Shift+F3 = Pronađi predhodno.

# Verzija 2.7 #
* Popravljeno pogrešno ime stringa "Motorcycle" u "Motorcycle00" in "Motorcycle00"
	* On je tražio ažuriranje zvučnih efekata jer nije pronalazio datoteku.
* Dodata je mogućnost očitavanja podataka o vetrovima ;
	* Pravac, brzina i temperatura vetra.
* Dodata mogućnost očitavanja atmosferskih podataka;
	* Vlažnost, vidljivost, pritisak i stanje barometarskog pritiska.
* Dodata mogućnost očitavanja astronomskih podataka;
	* Vreme izlaska i zalaska Sunca.

`#`Promene u Weather Plus prozoru podešavanja:

* Dodata su 3 čekboksa za upravljanje gore opisanim informacijama.
* Dodato je dugme "Detalji";
	* Daje neke informacije, kao što je pravo ime grada (dodeljeno od Yahoo vremenske prognoze), Država/regija i nacija kojoj pripada;
	* Sa geografskim kordinatama i nadmorskom visinom.
* Dodata mogućnost prepoznavanja WoeID_a (Lokalni Kodovi, na primer Bolonja koja korespondira sa  711080).
* Sada možete odkucati ime grada i ako postoji, prikazaće se u listi rezultata i moćićete da ga odaberete.

# Verzija 2.6 #
* Funkcije dugmadi "Dodaj" i "Ukloni" su optimizovane u upravljaču Zip Kodova;
	* Sada je funkcija mnogo brža!
* Funkcija dugmeta "test" je optimizovana, sada radi do 13 rezultata pretrage;
	* Ako sada ne pronađete svoj grad, to je zaista loša sreća!
* Funkcija dugmeta "Pronađite svoj grad...", sada nalazi više država;
	* Dodata je mogućnost da se automatski testiraju sakupljeni podaci koji funkcionišu u Zip Kodovima i koji su nadalje usaglašeni sa dodatim malim buferom za vizualizaciju pojedinih država.
* Dodata su 3 nova zvučna efekta;
	* Biće neophodno da se ažuriraju iz podešavanja ovog dodatka.

# Verzija 2.5 #

* Dodata je komanda za privremenu promenu mernih jedinica temperature između Celzijusa i Farenhajta, a komanda je moguća i u prozoru podešavanja.
* Ispravljena je greška, ako korisnik nije pritisnuo dugme "Dodaj" ili "Podesi kao podrazumevano", nije dozvoljeno oglašavanje grada jer nije u listi.
* Dodati su novi stringovi u vremenskom izveštaju.

`#`Promene u Weather Plus prozoru podešavanja:

* Dodato je dugme koje otvara stranicu za pretraživanje svih Zip Kodova.
* Dodata je mogućnost za uvoz i izvoz Zip Kodova od prijatelja.
* Dodata je mogućnost kopiranja vremenske prognoze i izveštaja u međuspremnik (klipboard).
* Dodata je mogućnost zvučnih efekata koji se mogu instalirati i ažurirati.
* Dodato je dugme pomoći u upravljaču Zip Kodova.
* Promene u izgledu prozora, NVDA meniji nisu onemogućeni kada je ovaj prozor otvoren.

# Verzija 2.4.4 #
* Dodata su 2 nova stringa u vremenskom izveštaju
* Dodati su prevodi na Španski i Francuski (zahvaljujući Pablu Vargasu i Remi Ruisu)

# Verzija 2.4.3 #
* Dodata je mogućnost vremenskog izveštaja za 4 naredna dana
* Dodat je string za vremenski izveštaj
* Poredak Zip Kodova je sada prema svakom novom unošenju sledećeg Zip Koda

#Verzija 2.4 #
* Ispravljena je greška koja je sprečavala pravilno čuvanje i upravljanje kada su imena gradova sadržavala akcentovana slova.

# Verzija 2.3 #
* Uklonjen je dijalog za određivanje mernih jedinica temperature i zamenjen je novom opcijom koja omogućuje sve promene u jednom prozoru.
* Sada takođe možete dodati/testirati/brisati/postaviti kao podrazumevan Zip Kodove sakupljene u listu.
* Modified Prepravljen je dijalog za upisivanje Zip Kodova i sada je u privremenom režimu moguće postaviti Zip Kod predhodno dodat u listu u podešavanjimapreko menija.
* Sada je moguće pročitati dokumentaciju na engleskom ako ona nije prevedena u podešenom jeziku.

# Verzija 2.2 #
* Ispravljena je greška koja nije dozvoljavala otvaranje dokumentacije za određenu verziju NVDA

# Verzija 2.1 #
* ispravljena je greška kada se nije pravilno isključivao ovaj dodatak u NVDA, što je sprečavalo NVDA da ažurira ikonicu u System Tray_u.

# Verzija 2.0 #
* Weather Plus meni podešavanja u opcionom submeniju je pomeren
	* pravilan leteći unos više nije sačuvan, Zato je privremeno.
	* Da bi ste pozvali grad podešen u opcijama, pritisnite INSERT + control + f3.

# verzija 1.9 #
* Dodata je pomoć pri unošenju funkcija.
* Dodata je nova funkcija za brzo unošenje Zip Koda
* Dodata je čitaj/piši konfiguracija weather.ini, zato više nije potrebno uređivati izvornu datoteku.
* Meni ovog dodatka je dodat i u sistem tray (sistemsku traku poslova).
* Dodata je postavka Zip Kod podmeni .
* Dodata je pod-postavka temperaturna skala (Farenhajt ili Celzijus).
* Dodat je meni dokumentacija
* Dodat je prevod na Italijanski jezik

# Predhodna verzija 1.1 #
* Ažuriran je NVDA-dodatak
* Provizorni prevod u izvoru

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
