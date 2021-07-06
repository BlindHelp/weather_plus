# Počasie Plus #

* Autor: Adriano Barbieri
* NVDA kompatibilita: 2017.3 a vyššie
* Stiahnuť: [Stabilnú verziu] [1]

# O doplnku #

* Poskytuje informácie o aktuálnom počasí a predpoveď počasia až na 2 dni
  dopredu a hodinové predpovede.
* Copyright (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Vydané pod licenciou GNU GPL (General Public License) verzia 2
* Doplnok využíva tieto služby:
* [https://www.weatherapi.com/](https://www.weatherapi.com/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.nvda.it/](https://www.nvda.it/)

# POUŽITIE: #

* nvda+W: Oznámi informáciu o aktuálnom počasí.
* NVDA+shift+W: Oznámi predpoveď počasia až na 2 dni dopredu.
* NVDA+shift+W Stlačte dvakrát, aby ste dostali hodinovú predpoveď teploty a atmosférických podmienok.
* NVDA + shift + ctrl + w: Umožňuje nastaviť dočasné mesto.
* NVDA + shift + ctrl + alt + w: Otvorí nastavenia doplnku.
* NVDA + alt + w: Oznámi dátum a čas poslednej aktualizácie informácií o
  počasí.
* ctrl+ shift + w: prepína medzi oznamovaním teploty v stupňoch Celsia alebo
  Farenheita.

# Nastavenia: #

* Skôr, než začnete doplnok používať, je potrebné nastaviť parametre. V menu Možnosti aktivujte podmenu počasie a tam vyberte jednu z možností:
* Spravovať mestá: Umožní nastaviť mesto, pre ktoré sa budú zobrazovať informácie o počasí.
* Nápoveda: Zobrazí dokument s pomocníkom v aktuálnom jazyku.
* Skontrolovať aktualizácie: Skontroluje a umožní nainštalovať novú verziu doplnku.

Nové mesto na sledovanie pridáte nasledovne:

* Aktivujte položku Spravovať mestá.
* Zobrazí sa táto správa: Predvolené mesto nie je. f1: Pomocník, f2: Oznámy
  aktuálne vybratú záložku, f3: presunie kurzor na editačné pole alebo
  zoznam, f4: Nastaví dĺžku predpovede počasia, F5: Nastavenie úrovne
  hlasitosti.
* Do textového poľa zadajte mesto alebo vyberte mesto zo
  zoznamu. Poznámka: Kláves F5 funguje len ak sú aktivované zvukové efekty.
* Po aktivovaní položky spravovať mestá sú dostupné tieto možnosti:
* Otestovať: Otestujte platnosť mesta a nájdite jeho údaje.
* Pridať: pridá aktuálne mesto do zoznamu. Toto tlačidlo sa dá aktivovať, ak
  je vybraté mesto zo zoznamu, a ak ste zadané mesto otestovali.
* Podrobnosti: zobrazuje informácie o aktuálnom meste. Toto tlačidlo sa dá
  aktivovať, ak je zo zoznamu vybraté mesto alebo ak ste ho už otestovali.
* Nastavenie zvukových efektov: Umožňuje definovať oblasť s cieľom
  prispôsobiť zvukové efekty. Toto tlačidlo sa dá aktivovať, ak sú zvukové
  efekty nainštalované a aktivované a ak je zo zoznamu vybraté mesto.
* Predvolené mesto: Ak nastavíte mesto ako predvolené, použije sa pri každom
  reštarte doplnku. Toto tlačidlo sa dá aktivovať, keď vyberiete mesto,
  ktoré bolo predtým vložené do zoznamu a nie je zatiaľ predvolené alebo ak
  prešlo testovaním.
* Odstrániť: Odstráni aktuálne mesto zo zoznamu. Toto tlačidlo sa dá
  aktivovať, ak vyberiete mesto, ktoré bolo predtým vložené do zoznamu.
* Premenovať: Premenuje aktuálne mesto. Toto tlačidlo sa dá aktivovať, ak
  vyberiete mesto, ktoré bolo predtým vložené do zoznamu.
* Importovať: Toto tlačidlo umožňuje importovať mestá z iného zoznamu miest
  s príponou * .zipcodes. Počas importu môžete začiarknuť mestá, ktoré
  chcete importovať.
* Exportovať: Umožňuje vám uložiť mestá do súboru s príponou *
  .zipcodes. Exportovať môžete len vtedy, ak je v zozname aspoň jedno mesto.
* nastavenie hodinovej predpovede... - Toto tlačidlo umožňuje zvoliť obsah správy hodinovej predpovede.
* Jednotky merania teploty: Pomocou prepínača vyberte medzi stupňami Celzia
  (predvolené), Fahrenheita alebo Kelvina.
* Zobraziť stupne ako: Pomocou prepínača vyberte medzi Celzia `-`
  Fahrenheita `-` Kelvina (predvolené) C` -` F `-` K alebo neurčovať.
* Dĺžka predpovede: Nastavte počet dní predpovede počasia. Maximálne 3.
* Zoznamový rámik: API zodpovedajúci jazyk:: English, en; môžete zvoliť jazyk textu predpovede.
* Dostupné sú aj tieto začiarkávacie polia:
* kopírovať predpoveď počasia, aktuálne počasie a informácie o meste do
  schránky - predvolene vypnuté
* Predpoveď oznamovať aj Zvukom: Po začiarknutí môžete spravovať zvukové
  efekty. Ak sú nainštalované zvukové efekty a pole je začiarknuté, môžete
  upravovať hlasitosť zvukov klávesom F5.
* Pribudne tiež začiarkávacie políčko Neprehrávať zvuky Prostredia.
* Môžete zmeniť celkovú úroveň hlasitosti, prípadne upraviť hlasitosť pre
  jednotlivé udalosti. Predvolene nie je začiarknuté.
* Neprehrávať zvuky Prostredia: Táto možnosť je k dispozícii, ak sú zvukové
  efekty povolené. Po začiarknutí sa budú prehrávať len zvuky počasia (dážď,
  búrka, vietor) a nie zvuky prostredia. Predvolene je vypnuté.
* Používať 24-hodinový formát: Ak je odčiarknuté, oznamuje čas v
  12-hodinovom formáte, napríklad 12 AM `-` 12 PM. Predvolene je zapnuté.
* Povoliť texty Pomocníka v oknách s nastaveniami: Predvolene je zapnuté.
* Oznamovať poveternostné podmienky: Predvolene je vypnuté. Po zapnutí budú
  dostupné tieto možnosti:
* Oznamovať smer vetra: bude oznamovať pri počasí aj smer vetra. Predvolene
  zapnuté.
* Oznamovať rýchlosť vetra: Bude oznamovať rýchlosť vetra v mýľach alebo
  kilometroch za hodinu. Predvolene zapnuté.
* Oznamovať rýchlosť vetra v metroch za sekundu: Predvolene zapnuté.
* Oznamovať pocitovú teplotu: Predvolene zapnuté.
* Pridať rýchlosť  nárazov vetra: Predvolene zapnuté
* Oznamovať atmosferické informácie: Predvolene je vypnuté. Po zapnutí budú
  dostupné tieto možnosti:
* Oznamovať vlhkosť: Oznamuje vlhkosť vzduchu v percentách. Predvolene
  zapnuté.
* Oznamovať Viditeľnosť: Oznamuje viditeľnosť v míľach alebo
  kilometroch. Predvolene zapnuté.
* Oznamovať hodnotu Atmosferického tlaku: Oznamuje stav tlaku v milibaroch
  alebo palcoch ortuti. Predvolene je zapnuté. Po začiarknutí je tiež možné
  začiarknuť oznamovanie tlaku v milimetroch ortuti.
* Pridať hodnotu oblačnosti: Predvolene zapnuté
* Pridať hodnotu zrážok: Predvolene zapnuté
* Pridať hodnotu ultrafialového žiarenia: Predvolene zapnuté
* Oznamovať astronomické informácie: oznamuje čas východu a západu slnka a čas východu a západu mesiaca. Predvolene vypnuté
* Desatinné čísla oddeľovať čiarkou: Ak je začiarknuté, použije na oddelenie
  celých a desatinných čísel desatinnú čiarku (,). Predvolene je vypnuté a
  používa sa bodka (.)
* Zobrazí výstup v okne; ak je aktivovaná, zobrazí sa predpoveď v okne. Začiarkavacie políčko nie je začiarknuté (predvolene)
* Skontrolovať aktualizácie: Skontroluje dostupnosť novej verzie doplnku.
* Nastavenia uložíte tlačidlom OK a zrušíte tlačidlom Zrušiť.
* Ak ste upravili zoznam s mestami a aktivujete tlačidlo Zrušiť, doplnok vás
  upozorní, že ste zabudli uložiť zmeny. Nastavenia sa ukladajú do súborov:
* "Weather.ini": prvotné nastavenia doplnku.
* "Weather.volumes": Nastavenia hlasitosti pre jednotlivé udalosti.
* "Weather.zipcodes": zoznam miest.
* "Weather.default": Vaše predvolené mesto.
* "Weather_searchkey": Uložené vyhľadávané reťazce.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
