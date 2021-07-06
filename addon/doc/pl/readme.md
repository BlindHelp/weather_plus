# Weather Plus #

* Autor: Adriano Barbieri
* NVDA compatibility: 2017.3 to beyond
* Pobierz: [Wersja stabilna][1]

# O Weather Plus: #

* Ten dodatek dodaje lokalną temperaturę i prognozę pogody do 24 godzin i do
  dodatkowych 2 dni and hourlyforecast dla NVDA
* prawa autorskie (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Wydano pod licencją GNU GPL (General Public License v2)

# Weather Plus działa przy użyciu i obecności następujących serwisów: #
* [https://www.weatherapi.com/](https://www.weatherapi.com/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.nvda.it/](https://www.nvda.it/)

# Użycie: #
* naciśnij NVDA + w dla aktualnej temperatury i warunków pogodowych.
* Naciśnij NVDA + shift + W dla 24-godzinnej pogody i prognozy do 2 dni.
* Press NVDA+shift+W twice to get hourlyforecast of temperature and atmospheric conditions.
* naciśnij NVDA + shift + ctrl + w, aby ustawić tymczasowe miasto.
* naciśnij NVDA + shift + control + alt + w, aby otworzyć ustawienia Weather
  plus.
* naciśnij NVDA + alt + w, aby się dowiedzieć, kiedy ostatnio był
  zaktualizowany biuletyn pogodowy.
* Naciśnij control + shift + w aby przełączać się między skałami mierzenia
  temperatury.

# Aby ustawić weather plus: #
Proszę przeczytać rożdział: Weather Plus pierwsze ustawienia.

--------------------------------------------------------------------------------

# Weather plus pierwsze ustawienia #

Powinno się ustawić dodatek przed jego pierwszym użyciem!

idź do:

meni rozwijane ustawienia

Ustawienia weather plus rozwijane

Pokazuje elementy konfiguracji.

# Naciśnij element dla: #

* Ustaw i zarządzaj swoimi miastami...
	* Wyświetla i umożliwia ustawianie aktualnego miasta z listy.
* Dokumentacja
	* Otwiera meni pomocy dla aktualnego języka.
* sprawdź aktualizację...
	* Oznajmia o dostępności nowje wersji.

Naciśnij element:

# Ustaw i zarządzaj swoimi miastami... #

Wyświetla listę miasta, a także umożliwia ustawianie go z niej.

Następujący komunikat pokazywany jest tylko przy pierwszym uruchomieniu!

Predefiniowane ustawienia

Nic

F1: pomóż mi znaleźć miasto, F2: gdzie się znajduję, F3: lista i pole
edycji, F4: czas trwania pogody, F5: kontrola głośności.

Wpisz nazwę miasta lub wybierz jeden z listy, jeżeli jest dostępny.

Uwaga: kombinacja klawiszy f5 jest dostępna, gdy efekty dźwiękowe są
aktywne.

Po naciśnięciu przycisku ustaw i zarządzaj swoimi miastami następujące
przyciski są dostępne:

# Testuj #

Test the validity of the city and find the data of it.

# Dodaj #

Dodaje aktualne miasto do listy.

Ten przycisk jest dostępny gdy miasto przeszedło test, lub jest ono
dostępne.

# Szczegółu #

Pokazuje informację o aktualnym mieście.

Ten przycisk jest dostępny gdy miasto przeszedło test, lub jest ono
dostępne.

# Zdefiniuj #

Umożliwia zdefiniowanie obszaru, aby dostosować dźwięki pogodowe do
rzeczywistości.

Ten przycisk jest dostępny, gdy dźwiękowe efekty są zainstalowane i
aktywowane, przy czym miasto musi być wybrane.

# Ustaw miasto jako domyślne #

Ustawia miasto jako domyślne, ędzie używane przy każdym ponownym
uruchomieniu.

Ten przycisk jest aktywny, gdy zaznaczone jest miasto i nie jest ono
domyślne, lub ono przeszło test.

# Usuń #

Usuwa aktualne miasto z listy.

Ten przycisk jest aktywowany jeśli jest zaznaczone miasto, które uprzednio
istniało na liście.

# Zmień nazwę #

Zmienia nazwę aktualnego miasta..

Ten przycisk jest aktywowany jeśli jest zaznaczone miasto, które uprzednio
istniało na liście.

# Zaimportuj nowe miasta... #

Pozwala dołączać do listy nowe miasta zaimportowane z innej listy o
rozszerzeniu *.zipcodes; Miasto do zaimportowania można wybrać zaznaczając
odpowiadające mu pole wyboru.

# Eksportuj miasta #

Zapisuje listę miast w określonej lokalizacji.

Przycisk ten jest aktywny, jeśli na liście znajduje się przynajmniej jedno
miasto.

# hourly forecast setting... #

This button allows you to choose the contents of the hourly forecast report.

# Skala pomiaru temperatury: #

Użyj przycisku opcji aby wybrać:

* Celsjusz (domyślnie)
* Farenhajt
* Kelwin

# Pokazuj stopnie jako: #

Użyj przycisku opcji aby wybrać:

* Celsjusz `-` Farenhajt `-` Kelwin (domyślnie)
* C `-` F `-` K
* Nieokreślone

Lista rozwijana:

# Prognoza pogody do 3 dni #

Wybierz od 1 do 3 (domyślnie na 1 dni)

Przełącz pole wyboru aby:

# Combo box API response language #

English, en; you can choose the language of the weather conditions text.

# Skopiuj prognozę i biuletyn pogodowy do schowka wraz ze szczegółami miasta. #

Domyślnie odznaczone.

# Włącz efekty dźwiękowe (tylko dla aktualnych warunków pogodowych) #

To pole wyboru pozwala też zarządzać instalowaniem efektów dźwiękowych;

Gdy efekty dźwiękowe są zainstalowane a pole wyboru zaznaczone, uaktywniają
się ustawienia głośności i klawisz F5.

Pojawia się także dodatkowe pole wyboru:

* Używaj tylko efektów pogodowych.

Można zmienić głośność ogólną, lub głośność ostatnio usłyszanego dźwięku, a
także odfiltrować inne dźwięki z otoczenia.

Domyślnie odznaczone.

# Używaj tylko efektów pogodowych. #

Dostępne gdy efekty dźwiękowe są włączone;

Po zaznaczeniu umożliwia słuchanie wyłącznie efektów pogodowych, takich jak
deszcz, wiatr, grzmoty itd. Inne dźwięki otoczenia zostają odfiltrowane.

Domyślnie odznaczone.

# Włącz odczytywanie godzin w formacie 24-godzinnym. #

Gdy odznaczone, czas odczytywany jest w formacie 12-godzinnym, np. 12 AM `-`
12 PM.

Domyślnie zaznaczone.

# Włącz przyciski pomocy w oknie ustawień. #

Domyślnie zaznaczone.

# Odczytuj informacje o wietrze. #

Domyślnie odznaczone.

Gdy włączone, można uaktywnić również:

* Dodaj kierunek wiatru;

Określa skąd wieje wiatr.

Domyślnie zaznaczone.

* Dodaj prędkość wiatru;

Podaje prędkość wiatru w kilometrach, lub milach na godzinę.

Domyślnie zaznaczone.

* Dodaj prędkość wiatru w metrach na sekundę;

Domyślnie zaznaczone.

	* Add wind gust speed of the wind; checkbox checked (by default)

* Dodaj temperaturę odczuwalną;

Domyślnie zaznaczone.

# Odczytuj informacje atmosferyczne. #

Domyślnie odznaczone.

Gdy włączone, można uaktywnić również:

* Dodaj wskaźnik wilgotności powietrza;

Podaje wilgotność powietrza w procentach.

Domyślnie zaznaczone.

* Dodaj stopień widzialności;

Podaje widoczną odległość w kilometrach, lub milach.

Domyślnie zaznaczone.

* Dodaj wartość ciśnienia atmosferycznego;

Podaje ciśnienie atmosferyczne w milibarach, lub calach słupa rtęci.

Gdy jest włączone, można zaznaczyć dodatkowe pole wyboru, które umożliwia
podawanie ciśnienia w milimetrach słupa rtęci.

Domyślnie zaznaczone.

* Add cloudines value; check box checked (by default)
* Add precipitation value; check box checked (by default)
* Add ultraviolet radiation value; check box checked (by default)

# Odczytuj informacje astronomiczne. #

indicates the time of sunrise and sunset and the time of moonrise and moonset.

Domyślnie odznaczone.

# Użyj przecinka do oddzielania wartości dziesiętnych. #

Gdy jest zaznaczone, wartości dziesiętne oddzielane są przecinkiem, w
przeciwnym razie kropką.

Domyślnie odznaczone

# Wyświetla dane wyjściowe w oknie #

Gdy jest zaznaczone, wyświetla prognozę w oknie.

Domyślnie odznaczone

# Sprawdź aktualizacje #

Po uaktywnieniu tej opcji dodatek powiadamia o dostępnych aktualizacjach

Domyślnie zaznaczone.

# Naciśnij przycisk OK aby potwierdzić akcję, lub przycisk Anuluj aby ją anulować. #

Jeśli po zmodyfikowaniu listy miast naciśniesz "Anuluj", dodatek przypomni
Ci o zmianach na liście i umożliwi jej zapisanie.

# Uwaga: Twoje ustawienia zostaną zapisane w pliku o nazwie: #

* "Weather.ini": ustawienia uruchamiania Weather Plus.
* "Weather.volumes": Dostosuj poziom głośności dźwięku niezależnie od
  głośności ogólnej.
* "Weather.zipcodes": Lista miast wraz z kodami pocztowymi i definicjami.
* "Weather.default": Your default city.
* "Weather_searchkey": Słowo kluczowe zapisane.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
