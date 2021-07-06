# Počasí Plus #

* Autor: Adriano Barbieri
* NVDA kompatibilita: 2017.3 a vyžší
* Stáhnout: [Stabilní verzi] [1]

# O doplnku #

* Poskytuje informace o aktuálním počasí a předpověď počasí až na 2 dny
  dopředu a hodinové předpovědi.
* Copyright (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Vydané pod licencí GNU GPL (General Public License) verze 2
* Doplněk využívá tyto služby:
* [https://www.weatherapi.com/](https://www.weatherapi.com/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.nvda.it/](https://www.nvda.it/)

# POUŽITÍ: #

* nvda+W: Oznámí informaci o aktuálním počasí.
* NVDA+shift+W: Oznámí předpověď počasí až na 2 dny dopředu.
* NVDA+shift+W Stiskněte dvakrát, aby jste dostali hodinovou předpověď teploty a atmosférických podmínek.
* NVDA + shift + ctrl + w: Umožňuje nastavit dočasné město.
* NVDA + shift + ctrl + alt + w: Otevře nastavení doplnku.
* NVDA + alt + w: Oznámí datum a čas poslední aktualizace informaci o
  počasí.
* ctrl+ shift + w: přepíná mezi oznamováním teploty v stupních Celsia anebo
  Farenheita.

# Nastavení: #

* Než začnete doplněk používat, je třeba nastavit parametry. V menu Možnosti aktivujte podmenu počasí a tam vyberte jednu z možností:
* Spravovat města: Umožní nastavit město, pro které se budou zobrazovat informace o počasí.
* Nápověda: Zobrazí dokument s pomocníkem v aktuálním jazyku.
* Zkontrolovat aktualizace: Zkontroluje a umožní nainstalovat novou verzi doplňku.

Nové město na sledování přidáte nasledovně:

* Aktivujte položku Spravovat města.
* Zobrazí se táto zpráva: Předvolené město není. f1: Pomocník, f2: Oznámí
  aktuální vybranou záložku, f3: přesune kurzor na editační pole nebo
  seznam, f4: Nastaví délku předpovědi počasí, F5: Nastavení úrovně
  hlasitosti.
* Do textového pole zadejte město nebo vyberte město ze
  seznamu. Poznámka: Klávesa F5 funguje jen když jsou aktivované zvukové efekty.
* Po aktivování položky spravovat města jsou dostupné tyto možnosti:
* Otestovat: Otestujte platnost města a najděte jeho údaje.
* Přidat: přidá aktuální město do seznamu. Toto tlačítko se dá aktivovat, jestliže
  je vybrané město ze seznamu a jestli jste zadané město otestovali.
* Podrobnosti: zobrazuje informace o aktuálním městě. Toto tlačítko se dá
  aktivovat, pokud je ze seznamu vybrané město nebo když jste ho už otestovali.
* Nastavení zvukových efektů: Umožňuje definovat oblast s cílem
  přizpůsobit zvukové efekty. Toto tlačítko se dá aktivovat, pokud jsou zvukové
  efekty nainstalované a aktivované a ze seznamu je vybrané město.
* Předvolené město: Jestliže nastavíte město jako předvolené, použije se při každém
  restartu doplňku. Toto tlačítko se dá aktivovat, když vyberete město,
  které bylo předtím vložené do seznamu a není zatím předvolené alebo když
  prošlo testováním.
* Odstranit: Odstraní aktuální město ze seznamu. Toto tlačítko se dá
  aktivovat, pokud vyberete město, které bylo předtím vložené do seznamu.
* Přejmenovat: Přejmenuje aktuální město. Toto tlačítko se dá aktivovat, když
  vyberete město, které bylo předtím vložené do seznamu.
* Importovat: Toto tlačítko umožňuje importovat města z jiného seznamu měst
  s příponou * .zipcodes. Během  importu můžete zaškrtnout města, která
  chcete importovat.
* Exportovat: Umožňuje vám uložit města do souboru s příponou *
  .zipcodes. Exportovat můžete jen tehdy, když je v seznamu alespoň jedno město.
* nastavení hodinové předpovědi ... - Toto tlačítko umožňuje zvolit obsah zprávy hodinové předpovědi.
* Jednotky měření teploty: Pomocí přepínače vyberte mezi stupněmi Celzia
  (předvolené), Fahrenheita nebo Kelvina.
* Zobrazit stupně jako: Pomocí přepínače vyberte mezi Celzia `-`
  Fahrenheita `-` Kelvina (předvolené) C` -` F `-` K anebo neurčovat.
* Délka předpovědi: Nastavte počet dní předpovědi počasí. Maximálně 3.
* Seznamový rámec: API odpovídající jazyk:: English, en; můžete zvolit jazyk textu předpovědi.
* Dostupné jsou i tyto zaškrtávací pole:
* kopírovat předpověď počasí, aktuální počasí a informace o městě do
  schránky - předvolene vypnuté
* Předpověď oznamovat také Zvukem: Po zaškrtnutí můžete spravovat zvukové
  efekty. Jestliže jsou nainstalované zvukové efekty a pole je zaškrtnuté, můžete
  upravovat hlasitost zvuků klávesou F5.
* Přibyde též zaškrtávací políčko Nepřehrávat zvuky Prostředí.
* Můžete změnit celkovú úroveň hlasitosti, případně upravit hlasitost pro
  jednotlivé události. Předvolené není zaškrtnuté.
* Nepřehrávat zvuky Prostředí: Tato možnost je k dispozici, pokud jsou zvukové
  efekty povolené. Po zaškrtnutí se budou přehrávat jen zvuky počasí (déšť,
  bouřka, vítr) a ne zvuky prostředí. Předvolené je vypnuté.
* Používat 24-hodinový formát: Pokud je odškrtnuté, oznamuje čas v
  12-hodinovém formátu, například 12 AM `-` 12 PM. Předvolené je zapnuté.
* Povolit texty Pomocníka v oknech s nastaveními: Předvolené je zapnuté.
* Oznamovat povětrnostní podmínky: Předvolené je vypnuté. Po zapnutí budou
  dostupné tyto možnosti:
* Oznamovat směr větru: bude oznamovat při počasí aj směr větru. Předvolené
  zapnuté.
* Oznamovat rychlost větru: Bude oznamovat rychlost větru v mílech nebo
  kilometrech za hodinu. Předvolené zapnuté.
* Oznamovat rychlost větru v metrech za sekundu: Předvolené zapnuté.
* Oznamovat pocitovou teplotu: Předvolené zapnuté.
* Přidat rychlost  nárazů větru: Předvolené zapnuté
* Oznamovat atmosferické informace: Předvolené je vypnuté. Po zapnutí budou
  dostupné tyto možnosti:
* Oznamovat vlhkost: Oznamuje vlhkost vzduchu v procentech. Předvolené
  zapnuté.
* Oznamovat Viditelnost: Oznamuje viditelnost v mílech nebo
  kilometrech. Předvolené zapnuté.
* Oznamovat hodnotu Atmosferického tlaku: Oznamuje stav tlaku v milibarech
  nebo palcích ortuti. Předvolené je zapnuté. Po zaškrtnutí je též možné
  zaškrtnout oznamování tlaku v milimetrech ortuti.
* Přidat hodnotu oblačnosti: Předvolené zapnuté
* Přidat hodnotu srážek: Předvolené zapnuté
* Přidat hodnotu ultrafialového záření: Předvolené zapnuté
* Oznamovat astronomické informace: oznamuje čas východu a západu slunce a čas východu a západu měsíce. Předvolené vypnuté
* Desetinné čísla oddělovat čárkou: Pokud je zaškrtnuté, použije na oddělení
  celých a desetinných čísel desetinnou čárku (,). Předvolené je vypnuté a
  používá se tečka (.)
* Zobrazuje výstup v okně; pokud je aktivována, zobrazí se předpověď v okně. Zaškrtávací políčko není zaškrtnuto (ve výchozím nastavení)
* Skontrolovat aktualizace: Skontroluje dostupnost nové verze doplňku.
* Nastavení uložíte tlačítkem OK a zrušíte tlačítkem Zrušit.
* Pokud jste upravili seznam s městy a aktivujete tlačítko Zrušit, doplněk vás
  upozorní, že jste zapomněli uložit změny. Nastavení se ukládají do souborů:
* "Weather.ini": prvotní nastavení doplňku.
* "Weather.volumes": Nastavení hlasitosti pro jednotlivé události.
* "Weather.zipcodes": seznam měst.
* "Weather.default": Vaše výchozí město.
* "Weather_searchkey": Uložené vyhledávané řetězce.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
