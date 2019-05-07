# Weather Plus #

* Autor: Adriano Barbieri
 * NVDA-Kompatibilität: 2017.3 bis 2019.1
* [Stabile Version herunterladen][1]

# Weather Plus Lies-mich: #

* Dieses Plugin zeigt die aktuellen Wetterbedingungen und Vorhersagen für 24 Stunden und bis zu 9 zusätzlichen Tagen
* Copyright (C) [Adriano Barbieri] (mailto://adrianobarb@yahoo.it)
* Freigegeben unter der GNU GPL (General Public License) v2
* Version: 6.0.

# Weather Plus funktioniert durch die Nutzung folgender Dienste: #
* [https://developer.yahoo.com/weather/](https://developer.yahoo.com/weather/)
* [http://woeid.rosselliot.co.nz/lookup/](http://woeid.rosselliot.co.nz/lookup/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.timeanddate.com/](https://www.timeanddate.com/)
* [http://www.nvda.it/](http://www.nvda.it/)

# NUTZUNG: #
* Drücken Sie NVDA + w für die aktuelle Temperatur und zusetzliche Wetterdetails, die Sie in den Einstellungen anpassen können.
* Drücken Sie NVDA + Umschalt + W für die Wettervorhersage für 24 Stunden und bis zu 9 zusetzlichen Tagen.
* Drücken Sie NVDA + Umschalt + Strg + W, um eine temporäre Stadt festzulegen.
* Drücken Sie NVDA + Umschalt + strg + alt + w, um den Dialog Weather Plus Einstellungen zu öffnen.
* Drücken Sie NVDA + alt + w, um die letzte Aktualisierung des Wetterberichts zu erfahren.
* Drücken Sie strg + Umschalt + w, um zwischen Fahrenheit, Celsius oder Kelvin umzuschalten.

# Um Weather Plus einzustellen: #
Lesen Sie den Abschnitt: Weather Plus Erste Einstellungen.

-------------------------------------------------- ------------------------------

# Weather Plus Erste Einstellungen: #

Sie müssen das Weather Plus-Addon vor der ersten Verwendung einstellen!

Gehen Sie zu:

Einstellungen Untermenü

Untermenü Weather Plus Einstellungen

Konfigurationseinträge anzeigen

# Wählen Sie zwischen folgenden Einträgen: #

* Einstellungen und Stadtverwaltung...
	* Zeigt das Einstellungsfenster für Weather Plus.
* Dokumentation
	* Öffnet den Ordner mit den Hilfedateien für die aktuelle Sprache
* Nach Updates suchen...
	* Benachrichtigt, ob ein Update zur verfügung steht.

Wählen sie:

#Einstellungen und Stadtverwaltung... #

Zeigt das Einstellungsfenster für Weather plus

Die folgende Meldung wird nur zum ersten Mal angezeigt!

Einstellungen - voreinstellung:

Keine

F1: Hilfe, F2: Letzte Auswahl, F3: Stadtauswahl bzw. Suche, F4: Dauer der Wettervorhersage einstellen, F5: Lautstärkeregler.

Geben Sie einen Stadtnamen ein oder wählen Sie, falls Sie schon Städte hinzugefügt haben, eine mit den Pfeiltasten rauf und runter aus.

Hinweis: Die Taste F5 ist verfügbar, wenn die Soundeffekte aktiviert sind.

Nachdem Sie diesen Punkt ausgewählt haben, finden Sie weitere Schaltflächen wie:

# Test #

Testet die Gültigkeit der WOE-ID und findet den Namen der Stadt heraus, und umgekehrt.

# Hinzufügen #

fügt die ausgewählte Stadt Ihrer Liste hinzu.

Diese Schaltfläche ist aktiv, wenn Sie eine Stadt aus der Liste ausgewählt haben, die in der Ergebnisliste angezeigt wird.

# Details #

Zeigt Informationen zur aktuellen Stadt.

Diese Schaltfläche ist aktiv, wenn Sie eine Stadt aus der Liste auswählen oder den Test bestanden haben.

# Definieren #

Dies lässt Sie die Gegend definieren, um die Soundeffekte entsprechend anzupassen.

Diese Schaltfläche ist aktiv, wenn die Audioeffekte installiert und aktiviert sind und Sie eine Stadt aus der Liste auswählen.

# Voreinstellung #

Dadurch wird eine Stadt als Standardeinstellung festgelegt, die bei jedem Neustart des Plugins verwendet wird.

Diese Schaltfläche ist aktiv, wenn Sie eine Stadt ausgewählt haben, die zuvor in der Liste eingefügt und nicht voreingestellt wurde oder den Test bestanden hat.

# Entfernen #

entfernt die Stadt aus der Liste.

Diese Schaltfläche ist aktiv, wenn Sie eine Stadt auswählen, die zuvor in der Liste eingefügt wurde.

# Umbenennen #

Benennt die Stadt um.

Diese Schaltfläche ist aktiv, wenn Sie eine Stadt auswählen, die zuvor in der Liste eingefügt wurde.

# Neue Städte importieren ... #

Hiermit kann eine Städteliste durch Importieren von Dateien mit der Erweiterung *.zipcodes hinzugefügt werden. Sie können die zu importierenden Städte auswählen, indem Sie das entsprechende Kontrollfeld für die Stadt aktivieren.

# Städte exportieren... #

Hiermit kann die Städteliste an einem bestimmten Ort gespeichert werden.

Diese Schaltfläche ist aktiv, wenn Sie mindestens eine Stadt zur Liste hinzugefügt haben.

# Temperaturskala: #

Wählen Sie zwischen:

* Celsius (standard)
* Fahrenheit
* Kelvin

# Grad anzeigen als: #

Wählen Sie zwischen:

* Celsius `-` Fahrenheit` -` Kelvin (standard)
* C `- 'F` -' K
* Ohne Einheit

Kombinationsfeld:

# Wettervorhersage bis Tage: 3 #

Wählen Sie zwischen 1 und 10 (standardmäßig 3 Tage)

Des weiteren gibt es folgende Kontrollkästchen:

# Wetterbericht und Stadtdetails in die Zwischenablage kopieren #

standardmäßig nicht aktiviert

# Soundeffekte aktivieren (nur für aktuelle Wetterbedingungen) #

Mit diesem Kontrollkästchen können Sie auch die Installation von Soundeffekten verwalten.

Wenn die Soundeffekte installiert sind und das Kontrollkästchen aktiviert ist, stehen die Taste F5 und somit die Lautstärkeregelung zur Verfügung.

Es wird auch ein zusätzliches Kontrollkästchen verfügbar :

* Nur Wetter-Effekte verwenden

Sie können die Gesamtlautstärke oder den zuletzt gehörten Soundeffekt ändern und die anderen Sounds in Ihrer Umgebung herausfiltern.

standardmäßig nicht aktiviert

# Nur Wetter-Effekte verwenden #

ist verfügbar, wenn Soundeffekte aktiviert sind;

Wenn aktiviert, werden nur Wetterklänge wie Regen, Wind, Donner usw. abgespielt und alle Umgebungsgereusche werden weggelassen.

standardmäßig nicht aktiviert

# Stunden im 24-Stunden-Format ausgeben #

Wenn deaktiviert, wird die Uhrzeit im 12-Stunden-Format ausgegeben, Beispiel: 12 AM `-` 12 PM.

standardmäßig aktiviert

# Signalton abspielen, wenn das Suchen von Daten länger dauert #

Wenn diese Option aktiviert ist, ertönt ein Signalton, um anzuzeigen, dass die Suche noch etwas dauert,  bis Daten gefunden werden oder vielleicht auch nichts gefunden wird und die Daten als ungültig erklärt werden.

Standardmäßig aktiviert

# Hilfetexte für die Schalter in den Einstellungen zeigen #

standardmäßig aktiviert

# Windinformationen ausgeben #

standardmäßig nicht aktiviert

Wenn aktiviert, können Sie auch Folgendes aktivieren:

* Windrichtung ausgeben;

Zeigt die Richtung des Windes an.

Standardmäßig aktiviert

* Windgeschwindigkeit ausgeben;

Zeigt die Geschwindigkeit in Kilometern oder Meilen pro Stunde an.

Standardmäßig aktiviert

* Meter pro Sekunde bei der Ausgabe der Windgeschwindigkeit hinzufügen;

Standardmäßig aktiviert

* Gefühlte Temperatur ausgeben;

Standardmäßig aktiviert

# Atmosphärische Informationen ausgeben #

Standardmäßig nicht aktiviert.

Wenn aktiviert, können Sie auch Folgendes aktivieren:

* Fäuchtigkeit ausgeben;

Zeigt die Luftfeuchtigkeit in Prozent an.

Standardmäßig aktiviert

* Sichtweite ausgeben;

gibt die maximale Sicht in Kilometern oder Meilen an.

Standardmäßig aktiviert

* Luftdruck ausgeben;

Zeigt den Luftdruck in Millibar oder Zoll Quecksilbersäule an.

Wenn dies aktiviert ist, wird ein zusätzliches Kontrollkästchen sichtbar, mit dem Sie die Ausgabe des Luftdrucks in Millimeter Quecksilbersäule ein- oder ausschalten können.

Standardmäßig aktiviert

* Status des Luftdrucks ausgeben;

Standardmäßig aktiviert

# Astronomische Informationen ausgeben #

Zeigt die Zeit von Sonnenaufgang und Sonnenuntergang an.

Standardmäßig nicht aktiviert

# Komma als Dezimaltrennzeichen benutzen #

Wenn diese Option aktiviert ist, wird das Komma als Dezimaltrennzeichen verwendet, andernfalls wird der Punkt verwendet.

Standardmäßig nicht aktiviert

# automatisch nach Updates suchen #

Wenn aktiviert, wird gemeldet, wenn eine neue Version des Addons verfügbar ist.

Standardmäßig aktiviert

# Drücken Sie OK, um Ihre Änderungen zu speichern, oder Abbrechen, um sie zu verwerfen. #

Wenn Sie die Städte-Liste geändert haben und auf "abbrechen" drücken, werden Sie daran Erinnert, sodass sie dies trotzdem speichern können.

# Hinweis: Ihre Einstellungen werden in folgenden Dateien gespeichert: #

* "Weather.ini": Starteinstellungen von Weather Plus.
* "Weather.volumes": Benutzerdefinierte Lautstärkepegel, unabhängig von der Gesamtlautstärke.
* "Weather.zipcodes": Liste der Städte mit Postleitzahl und Definitionen.

-------------------------------------------------- ------------------------------

# Änderungsverlauf: #

# Version 6.0 #
* Weather Plus kehrt zur Verwendung der Yahoo Weather API zurück.
* Praktisch alle Funktionen der Vorgängerversion 4.8 sind zurück und behalten den "Umbenennen" Schaltfläche.
* Jetzt auch mit Python 3 kompatibel.

	# Version 5.0.1 #
* Fehler behoben, der bei einer Windgeschwindigkeit von 0 mph eine leere Zeichenkette zurückgeben ließ.
* Fehler korrigiert, der die Soundeffekte nicht folgerichtig mit der Zeitzone abspielen ließ.
* Taganzahl der Wettervohersage im Liesmich von 9 auf 6 korrigiert.

# Version 5.0 #
* Weather Plus verwendet jetzt das bessere APIXU-API.

`#`Änderungen im Fenster "Weather Plus-Einstellungen":

* Altes Kontrollfeld "Luftdruckzustand" entfernt.
* Ersetzt durch neues Kontrollkästchen "Trübung ausgeben";
	* Es gibt Ihnen den Prozentsatz der Trübung.
* Neues Kontrollkästchen "Niederschlagswert hinzufügen" hinzugefügt.
	* Es gibt Ihnen die Menge in Millimetern des Niederschlags.
* altes Kontrollkästchen zum Anzeigen des Wartens mit einem Piepton entfernt;
	* Standardmäßig aktiviert.
* Zeit von Mondaufgang und Monduntergang zu den astronomischen Informationen hinzugefügt.
* Neuer Schalter "Umbenennen" hinzugefügt;
	* Städte bequemer umbenennen.
* Verbesserte Funktion des "Test" Schalters;
	* Akzeptiert nun einige Befehle, um die Suche nach Städten zu erleichtern.
	* Diese neuen Befehle sind in der Hilfefunktion beschrieben, die mit F1 aufgerufen werden kann.

# Version 4.8 #
`#`Änderungen im Weather-Plus-Einstellungsfenster:

* Neues Kontrollkästchen hinzugefügt.
	* "Nur Wetter-Effekte verwenden";
	* Dadurch können Sie alle anderen Umgebungsgereusche herausfiltern.
   * Verbesserte Zufallswiedergabe und 71 neue Soundeffekte hinzugefügt;
	* Sie müssen sie aktualisieren, indem Sie zweimal auf das Kontrollkästchen "Audioeffekte aktivieren" klicken.
* Der vom Benutzer zugewiesene Lautstärketyp, die allgemeine und die aktuelle Audio-Lautstärke, wird jetzt beibehalten, wenn die Konfiguration gespeichert wird.
* Unnötiger Sound während des Auswahltexts im Eingabefeld durch Drücken von Strg + a entfernt.
* Verbesserte Lesbarkeit des Hilfefensters, das mit der Funktionstaste F1 aufgerufen werden kann.
* Kompatibilitätskenzeichnung für NVDA 2019.1 und die aktuellen Alpha-Versionen hinzugefügt.

# Version 4.7.7 #
* Die überflüssige Benachrichtigung des erfolgreichen Downloads eines Updates wurde entfernt.
* 6 neue Soundeffekte hinzugefügt;
	* Es ist notwendig, sie von den Einstellungen des Plugins zu aktualisieren.

# Version 4.7.6 #
* Ein kleiner Fehler in der Funktion GetCoords() wurde behoben;
	* 2 Werte wurden bei fehlender Verbindung nicht zurückgegeben.

# Version 4.7.5 #
* MenuItem.GetLabel () ist veraltet und wurde durch MenuItem.GetItemLabelText () ersetzt.
* Einige Deklarationen von globalen Variablen korrigiert.

# Version 4.7.3 #
* Die Funktion "Details" wurde aktualisiert;
	* Der Einfachheit halber werden die Informationen zur Höhe jetzt von velouroutes.org zur Verfügung gestellt.
	* Dies führt zu kleinen Unterschieden von geringer Relevanz.

# Version 4.7.2 #
* Ein Codierungsfehler wurde bei der Removeupdate-Funktion behoben.

# Version 4.7.1 #
* Ein Fehler in GetTimezone wurde behoben;
	* Im Fall von Nulldaten wurde ein Wert zurückgegeben, nicht drei wie erforderlich.

# Version 4.7 #
* Update-Prozedur vereinfacht;
	* Falls beim Start von NVDA ein Update durch die automatische überprüfung gefunden wird, ist es nun möglich, es sofort von diesem Dialog aus herunterzuladen.
* Die Dateiauswahl beim Update-Vorgang wurde entfernt;
	* Die neue Version wird jetzt in einen temporären Ordner geladen. Dies macht das Updaten für Einsteiger einfacher.

# Version 4.6.9 #
* Arabische Lokalisierung hinzugefügt (dank Wafik Immaculate).

# Version 4.6.8 #
* Die Portugiesisch-Portugiesischen- und Brasilianisch-Portugiesischen Übersetzungen wurden, dank Alberto Mendonça, aktualisiert.

# Version 4.6.7 #
* Fehler in der Uhrzeitausgabe behoben;
	* In manchen Städten war sie nicht korrekt.
* Sommerzeit hinzugefügt;
	* Nur verfügbar für die Länder, bei denen sie auch eingesetzt wird.

# Version 4.6.5 #
* Fehler beim Ausgeben der aktuellen Uhrzeit behoben;
	* Das Trennzeichen ":" wurde bei der Umwandlung in Integer nicht entfernt.

# Version 4.6.4 #
* Die lokale Uhrzeitausgabe wurde verbessert;
	* Die Suchschlüsselwörter sind jetzt genauer.

# Version 4.6.2 #
* Fehler behoben: Nach einer Überprüfung auf Updates war der Menüpunkt "Eine temporäre Stadt festlegen..." aktiv, auch wenn keine Städte in der Liste vorhanden waren.
* Fehler behoben: Weather Plus konnte nicht konfiguriert werden, wenn keine weather.ini-Datei vorhanden war.

# Version 4.6 #
* Der Menüpunkt "Eine temporäre Stadt festlegen ..." wurde hinzugefügt;
	* Der Vollständigkeit halber können Sie nun auch die temporäre Stadtliste aus dem Menü öffnen.
* Verbesserte Verwaltung der Temperaturskala;
	* Das Einstellungsfenster gibt immer den Standardwert zurück.
* Verbesserte Verhinderung der mehrfachen Öffnung der Hauptfenster;
	* Wenn eine dieser Optionen bereits geöffnet ist, wird sie zusätzlich zum akustischen Alarm in den Vordergrund gestellt.
* Verbesserte Audioeffekte;
	* Sie basieren nun auf der aktuellen Ortszeit der verwendeten Stadt.

`#` Änderungen im Einstellungsfenster und der Detailausgabe:

* Aktuelle Uhrzeit hinzugefügt.
* Festgelegter Höhenwert;
	* Er wird jetzt zurückgesetzt, wenn der Wert kleiner oder gleich Null ist.
* Fehler in der Importfunktion behoben;
	* Wenn die Standardstadt entfernt wurde, wird sie nicht mehr in der Titelleiste angezeigt.

# Version 4.5.5 #
* Fehlerkorrekturen in der serbischen Lokalisierung und Dokumentation.
* Fehlerkorrekturen in der deutschen Lokalisierung.

`#` Änderungen im Weather-Plus-Einstellungsfenster:

* Neues Kontrollfeld hinzugefügt;
	* Sie können das Komma als Dezimaltrennzeichen aktivieren, andernfalls ist das Trennzeichen der Punkt.

# Version 4.5.3 #
* 2 Strings in russischer und ukrainischer Lokalisierung korrigiert.
* der Titel im Fenster Nach Updates suchen wurde korrigiert.
* Verbesserter Update-Algorithmus;
	* Jetzt wird der Link zum Update direkt aus der URL der Manifest.ini-Datei gelesen.

# Version 4.5 #
* Kurztaste NVDA + Umschalt + Strg + Alt + w hinzugefügt;
	* der Einstellungsdialog von Weather Plus wird damit geöffnet.
* einige englische Prompts korrigiert.

`#` Änderungen im Fenster Weather Plus Einstellungen:

* 8 neue Kontrollkästchen hinzugefügt;
	* Es ist jetzt möglich, die Ausgabe weiter anzupassen:
* Windrichtung.
* Windgeschwindigkeit.
* Gefühlte Temperatur.
* Luftfeuchtigkeit.
* Sichtweite.
* Luftdruck.
* den Druck in Millimeter Quecksilbersäule (mmHg) ausgeben.
* Status des Luftdrucks.

# Version 4.4.8 #
* Polnische Übersetzung hinzugefügt (dank Zvonimir Staneczyć).
* Weather Plus ist jetzt auch mit der zukünftigen wx Version 4 kompatibel;
	* Hinweis: Im Moment wird in Version 4.0.0b1 msw (phoenix) bei der Verwendung der Pfeiltasten rauf/runter in vielen Eingabefeldern ein lästiger Fehler erzeugt:

wxAssertionError: C ++ - Assertion "Assert failure" failed at .. \ .. \ src \ common \ evtloopcmn.cpp (110) in wxEventLoopBase :: Yield (): wxYield called recursively.

# Version 4.4.1 #
* SSL-Unterstützung hinzugefügt;
	* Wird nur verwendet, wenn eine SSL-zertifikatüberprüfung fehlgeschlagen ist.

# Version 4.4 #
* Fehler beim Lesen der neuen Versionszeichenfolge während einer Verbindungszeitüberschreitung behoben.
* Verbessertes Upgrade-Fenster;
	* Der Dialog stört nun nicht mehr das NVDA-Menü.
* Fehlerkorrekturen in der russischen Lokalisierung.
* ukrainische Übersetzung Hinzugefügt (dank Alex Yeshanu).

# Version 4.3.4 #
* Fehlerkorrekturen in der deutschen Lokalisierung.

# Version 4.3.3 #
* Deutsche Lokalisierung hinzugefügt (dank Karl Eick).

# Version 4.3.2 #
* Rumänische Lokalisierung hinzugefügt (dank Florian Ionaşcu).

# Version 4.3.1 #
* Ein kleiner Fehler in der Funktion "Details" wurde behoben;
	* Breiten- und Längengrad wurden im Vergleich zum richtigen Wert umgekehrt.

# Version 4.3 #
* Der Öffentliche Ordner Links wird am 15. März inaktiv sein.
	* Er  wird dann zu einem Standard-Dropbox-Ordner und kann vom Addon nicht mehr verwendet werden.
	* Die Upgrade-Links des Addons und der Samples wurden aktualisiert, deshalb werden diese Sachen ab jetzt vollständig von der italienischen Seite von NVDA aus verwaltet.

# Version 4.2.4 #
* Ein kleiner Fehler wurde behoben, wenn die Verbindung nicht aktiv ist.

# Version 4.2.3 #
* Nun kann Weather Plus einige Verbindungsversuche ausführen, bevor über die Ungültigkeit der Daten informiert wird. Bei jedem Versuch ertönt ein Signalton;
	* Dieser Signalton kann, wenn Sie möchten, mithilfe eines neuen Kontrollkästchens in den Einstellungen deaktiviert werden.

# Version 4.2.2 #
* Fehler in der Übersetzung der Temperaturskala behoben;
	* In einigen Sprachen wurden Kelvin, Celsius und Fahrenheit nicht übersetzt.

# Version 4.2.1 #
* Update-Benachrichtigung von Weather Plus während des Windows-Starts behoben;
	* Wenn Sie eine neue Version von Weather Plus installieren, wird die Version in der Systemkonfiguration nicht beeinträchtigt. Um die neueste Version in der Systemkonfiguration nutzen zu können, müssen sie die Einstellungen erneut mithilfe der allgemeinen Einstellungen von NVDA in die Systemkonfiguration kopieren.

# Version 4.2 #
* 5 neue Soundeffekte hinzugefügt;
	* Es ist notwendig, sie von den Einstellungen des Plugins zu aktualisieren.
* Fehler in der Importfunktion behoben;
	* Die Liste der Städte wird nun alphabetisch sortiert.
* Importmodus in der Importfunktion hinzugefügt;
	* Sie können Ihre eigene Liste vollständig ersetzen oder einfach neue Städte hinzufügen.
* das Lesen der Wettervorhersage, aktueller Wetterbericht, wurde aktualisiert;
	* Die gefühlte Temperatur (Wind Chill) wurde hinzugefügt.
* Neue Strings zur Liste "Weather reports" hinzugefügt.
 
# Version 4.1 #
* Fehler in der Wettervorhersage für bis zu 10 Tage behoben;
	* Wenn nicht für alle Tage Daten abgerufen werden konnten, werden die fehlenden Tage als unbekannt ausgegeben.
* Fehler beim drücken von NVDA + Umschalt + W behoben.
* Überarbeitete und aktualisierte Dokumentation.

# Version 4.0 #
* Einige Teile des Codes wurden aktualisiert und alle Anweisungen dem entsprechend  ersetzt.

# Version 3.9.7 #
* Fehler im Verhältnis der Wettervorhersagen behoben;
	* Jetzt werden die Temperaturen korrekt gelesen.

# Version 3.9.6 #
* Die Rundung bei der Umwandlung des Drucks von mbar in Zoll Quecksilbersäule wurde geändert;
	* Jetzt wird der Wert im Defekt berechnet, während er vorher überschritten wurde.

# Version 3.9.5 #
* Die Liste der Wetterberichte wurde um 2 neue Strings erweitert.
* 2 Fehler behoben.
* Aktualisierte Sounds für den Effekt bei nur Wind;
	* Jetzt kann der Klang des Windes zufällig variieren.

# Version 3.9.4 #
* Dokumentationen und Lokalisierungen auf Kroatisch und Deutsch entfernt, Weil sie nicht mehr von den jeweiligen Übersetzern unterstützt werden.
* Fehler in der Serbischen Lokalisierung behoben.
* Aktualisierte tschechische Lokalisierung.
* Galizische Dokumentation und Lokalisierung aktualisiert.

# Version 3.9 #
* Erneut geänderter API-Service;
	* Weather Plus verwendet jetzt das neue Yahoo Weather API mit Language Yahoo! Query und JQuery:
	* [yahoo-weather-api-with-yahooquery] (http://codesimplified.blogspot.it/2013/10/yahoo-weather-api-with-yahooquery.html)
* Die Eingabe eines Schlüssels ist nicht mehr notwendig.
* Die Suche nach gleichnamigen Städten wurde verbessert;
	* Es ist möglich, aus einer Liste genau die gewünschte Stadt auszuwählen.
* Optimierung der Ausgabe von allgemeinen Klängen;
	* Jetzt sind sie mit der Sprachsynthese synchronisiert und schneller.
* Der Cache für Offline-Daten wurde verbessert;
	* Er wird jetzt nur noch alle 10 Minuten oder durch Ändern der Stadt geleert.
* Der Druck wird jetzt in mbar oder in Zoll Quecksilbersäule (falls auf Fahrenheit eingestellt) gemessen.

# Version 3.8 #
* Das Datenpaket-API wurde vom XML-Format ins JSON-Format geändert;
	* Die Daten sind jetzt genauer, insbesondere die Zeitzone.
* die automatische Einstellung der Sprache wurde aktiviert;
	* Die API sendet nun die Daten der Wetterbedingungen in der von NVDA eingestellten Sprache.
* Cache für Wettervorhersagen hinzugefügt;
	* Wenn die Stadt, die Gradskala oder die Taganzahl der Wettervorhersage nicht geändert wurden, können Sie die Daten auch nach einer Verbindung offline für 10 Minuten lesen.
	* Der Cache wird bei jeder oben beschriebenen Änderung zurückgesetzt.
	* ER wurde hinzugefügt, da sich die Wetterbedingungen in dieser Zeitspanne nicht ändern. Außerdem werden die häufigen Anfragen an das API reduziert, sodass mit Soundeffekten gespielt werden kann.
* Verbessertes Updaten;
	* Wenn der Download abgeschlossen ist, wird die Installation automatisch aktiviert bzw. bei einer portablen Version von NVDA der Ordner geöffnet, in dem das Addon gespeichert wurde.
* Alle Sounds wurden aktualisiert;
	* Statt dem Tongenerator von NVDA werden jetzt kleine Dateien im Wav-Format verwendet.

# Version 3.7 #
* Möglichkeit, die Umwandlung in Meter pro Sekunde des Windes zu deaktivieren.
* Möglichkeit, Maßeinheiten in Pfund pro Quadratzoll zu verwenden.
* 2 Fehler behoben.

# Version 3.6 #
* Der API-Dienst (Anwendungsprogrammierschnittstelle) wurde geändert.
	* Jetzt verwendet WP den von OpenWeatherMap.org angebotenen Service statt Yahoo Weather.com.
* Die Windklassifikation wurde bei dem detailierten Wetterbericht für den heutigen Tag hinzugefügt.
* Ein Trübungsgrad im detailierten Wetterbericht für den heutigen Tag wurde hinzugefügt.
* Im detailierten Wetterbericht für den heutigen Tag wurden die Einheiten der Druckmessung in Hektopascal hinzugefügt.

`#` Änderungen im Fenster Weather Plus Einstellungen:

* Geänderte Einfügung / Suche aus Yahoo Postleitzahl / WoeId in ID Nummer, Identifizierer der Stadt;
	* ID Nummern sind ähnlich wie woeid, aber die WoeId funktioniert nicht mehr, auch nicht die alte Postleitzahl.
	* Sie können einen großen Teil der Städte wiederfinden, indem Sie den Namen oder einen Teil davon eingeben.
* Einfügung / Suche nach geografischen Koordinaten hinzugefügt.
* Einfügung / Suche nach Postleitzahl hinzugefügt.
* Die Funktion "Details" wurde verbessert.
* Die Taste F1 wurde für die Eingabe / Suchhilfe zugewiesen.
* Taste f4 zugewiesen, um in das Kombinationsfeld für die Einstellung der Dauer der Wettervorhersage zu kommen.
	* Achtung, wenn Sie eine Wettervorhersage für mehr als 10 Tage in die Zwischenablage kopieren möchten, wird dies nicht funktionieren!
* Zugewiesen F5-Taste für Audio-Steuerelemente.
* Temperaturskala Kelvin hinzugefügt.
* Überprüfung auf Updates hinzugefügt;
	* Sie können über Einstellungen festlegen, ob automatisch auf Aktualisierungen geprüft werden soll oder manuell über das Menü prüfen.
* die Schaltfläche "Finden Sie Ihre Stadt" in "Verwaltung ihres API-Schlüssels ..." umbenannt;
	* ermöglicht es Ihnen, den API-Schlüssel einzugeben oder zu ändern.

# Version 3.5 #
* Kroatische Übersetzung hinzugefügt (dank Gordan Radić).
* Zusätzliche Kontrolle für nicht mehr gültige WoeId und Postleitzahl im Netzwerk hinzugefügt;
	* Es gab Berichte über Codes, die aufgehört haben, von einem Tag auf den anderen zu funktionieren. WP warnt nun, wenn einer dieser Einträge im Suchfenster eingefügt wurde.
	* Wenn dies mit der Funktion "Finden Sie ihre Stadt..." geschieht, melden Sie es mir bitte, damit ich den Weather_buffer aktualisieren und aus der Liste entfernen kann.
* Ein Fehler in der Suchfunktion wurde behoben. Es fehlte die mbcs Codierung, daher konnten keine akzentuierten Zeichen erkannt werden.
* Das Fenster zum Festlegen einer Postleitzahl wurde aktualisiert;
	* Zusätzliche Funktion "Suchen" Wie in den anderen Fenstern von Weather Plus:
	* Steuerung + F3 = Suchen ..., F3 = weitersuchen, Shift + F3 = Rückwärts suchen.

# Version 3.4 #
* Galizische Übersetzung hinzugefügt (dank Iván Novegil).
* Portugiesische Übersetzung hinzugefügt (dank Ângelo Miguel Abrantes).
* Deutsche Übersetzung hinzugefügt (unvollständig).

# Version 3.3 #
* Das Maß der Windgeschwindigkeit in Metern pro Sekunde hinzugefügt.
* Kodierung in "mbcs" geändert;
	* Dies erlaubt, auch die diakritischen Zeichen in den Städtenamen zu verwenden.

# Version 3.2 #
* Aktualisierung der Wettervorhersagen, des aktuellen Wetterberichts und des Datums des aktuellen Wetterberichts;
Die Yahoo Wetterprognose ermöglicht es, ab einiger Zeit und in zufälligen Beträgen, eine historische Wettervorhersage von -10 bis -5 Tagen, die zwischen den aktualisierten Daten eingefügt werden soll, die  gelesen werden soll, anzuzeigen.
	* es wurde ein Filter hinzugefügt, der es Ihnen ermöglicht, nur die letzten aktualisierten Wetterdaten zu lesen und einen diskreten Signalton abzuspielen, wenn er eingreift;
	* Dieser Signalton kann bei Bedarf durch ein Kontrollkästchen in den Weather Plus-Einstellungen deaktiviert werden.
	* Offensichtlich beinhaltet das Filtern von Daten manchmal eine kurze Antwortverzögerung, ist jedoch immer noch akzeptabel.
* Prognosen für die auf 10 Tage verlängerte Zeit.

# Version 3.1 #
* Übersetzung auf Serbisch (Dank der freundlichen Zusammenarbeit von Gašić Dejan `-` Gashich Deyan).
* Behoben: Befehl einfügen + alt + w;
	* Es überprüfte nicht die Gültigkeit der verwendeten Postleitzahl und überprüfte nicht, ob die Verbindung aktiv war, wie es die anderen Befehle tun.
* Die Wiedergabefunktion von Soundeffekten wurde aktualisiert;
	* Mp3 wird jetzt verwendet, mit einer beträchtlichen Einsparung an Downloadzeit und Speicherplatz, dank der reduzierten Größe der komprimierten Dateien.
* 55 neue Soundeffekte hinzugefügt;
	* Es ist notwendig, sie von den Einstellungen des Plugins zu aktualisieren.

`#` Änderungen im Fenster Weather Plus Einstellungen:

* Hilfetexte für die Schalter in den Einstellungen hinzugefügt;
	* Diese können nun durch ein neues Kontrollkästchen ein- oder ausgeschaltet werden.
* 3 Kurztasten hinzugefügt, um schneller im Fenster zu navigieren:
* F1 springt in die Liste und bearbeitet die Postleitzahl.
* F2 kehrt zur letzten mit TAB erreichten Auswahl zurück.
* F3 springt zum Lautstärkeregler (wenn die Soundeffekte installiert und aktiviert sind).
* Verknüpfungsbefehle für alle Kontrollkästchen und Schaltflächen hinzugefügt;
	* Die beiden Optionsknöpfe, so wie sie nacheinander vorhanden sind, sind weggelassen und die erste ist mit dem Befehl Steuerung + shift + w erreichbar.
* Geändert, die Schaltfläche "Gegend definieren" ist jetzt deaktiviert, wenn die Soundeffekte nicht installiert und aktiviert sind.
* Zusätzliche Lautstärkeregelungen hinzugefügt;
	* Sie können die Gesamtlautstärke und den zuletzt gehörten Klangeffekt einstellen.
	* Diese Option ist aktiviert, wenn die Soundeffekte installiert und aktiviert sind.
* Möglichkeit, die Systemzeit im 12-Stunden-Format (12:30 AM `- '12:30 PM) oder im 24-Stunden-System (12:30` -' 00:30 Uhr) einzustellen.

# version 3.0 #
* Übersetzung ins Slowakische (dank der freundlichen Zusammenarbeit von Vitek Jirasek).
* Übersetzung ins brasilianisch-portugiesische und portugiesisch-portugiesische (dank der freundschaftlichen Zusammenarbeit von Adair Knaesel).
* Neue Strings zur Liste Wetterberichte hinzugefügt.
* Es wurden 171 neue Soundeffekte hinzugefügt, jetzt ist die Gesamtmenge 213.
* Befehl einfügen + alt + w, um die letzte Aktualisierung des aktuellen Wetterberichts auszugeben, hinzugefügt.
* Im dialog "Eingaben" hat Weather plus jetzt eine eigene Kategorie, in der alle Kurztasten aufgeführt sind.

`#` Änderungen im Fenster Weather Plus Einstellungen:

* Auswahlschalter hinzugefügt, um einzustellen, wie die Temperaturskala angezeigt wird;
	* Die Wahl ist zwischen:
* Celsius `-` Fahrenheit
* C `-` F
* Ohne Einheit
* Schaltfläche "Gegend definieren" hinzugefügt;
Diese  erlaubt, die Zone einer Stadt zu definieren als:
* Hinterland
* Meeresgebiet
* Wüste
* Arktische Zone
* Gebirgszone
	* Die Wahl wird Weather Plus erlauben, für jede einzelne Stadt geeignetere Soundeffekte zu verwenden;
	* Dies ist der Grund für die Steigerung der Anzahl neuer Soundeffekte in dieser Version des Addons;
	* Viele der neuen Soundeffekte habe ich von Tapin bekommen, denen ich aufrichtig danke.

# Version 2.9 #
* Option beim Import hinzugefügt, um den Inhalt der importierten Datei auszuwählen.
* Vier neue Klangeffekte wurden hinzugefügt.
* Übersetzung ins Russische (dank Alex Yeshanu).
* Übersetzung ins Tschechische (dank Jirimu Holzingerovi).

# Version 2.8 #
* Fehler in "Details" behoben, der das Fenster der Ereignisse öffnete, als er die Stadt nicht finden konnte.
* Regexp korrigiert, um nach der Höhe zu suchen;
	* Es hat keine einstelligen Parameter akzeptiert.
* Verbesserter Parser von Eingabefeldern;
	* Es sollte leichter die Stadt finden.
* Verbindungen, die jetzt von urllib2 statt von urllib gehandhabt werden;
	* Dies sollte das Funktionieren des Addons auch auf einem Computer ermöglichen, der mit einem durch Proxy geschützten Firmennetzwerk verbunden ist.
* Feature "Suchen" hinzugefügt;
	* Steuerung + F3 = Suchen ..., F3 = weitersuchen, Shift + F3 = rückwärts suchen.

# Version 2.7 #
* Falscher Name einer Zeichenkette "Motorcycle" in "Motorcycle00" behoben;
	* Es bat nach einer Aktualisierung der Soundeffekte, da die Datei nicht gefunden werden konnte.
* Zusätzliche Fähigkeit, Windinformationen zu lesen;
	* Richtung, Geschwindigkeit und Temperatur des Windes.
* Fähigkeit, atmosphärische Informationen zu lesen;
	* Luftfeuchtigkeit, Sicht, Luftdruck und Status des Luftdrucks.
* Zusätzliche Fähigkeit zum Lesen der astronomischen Informationen;
	* Zeitpunkt des Sonnenaufgangs und Sonnenuntergangs.

`#` Änderungen im Fenster Weather Plus Einstellungen:

* 3 Kontrollkästchen hinzugefügt, um die oben aufgeführten Informationen zu verwalten.
* Schaltfläche "Details" hinzugefügt;
	* Bietet einige Informationen wie den tatsächlichen Namen der Stadt (von Yahoo Wetterprognose zugewiesen), den Staat / die Region und die Nation, zu der sie gehört;
	* Mit geografischen Koordinaten und Höhe über dem Meeresspiegel.
* Erkennung von WoeID (Ortscodes, zB Bologna entspricht 711080).
* Jetzt können Sie den Namen der Stadt eingeben. In diesem Fall werden die Vorkommen aufgelistet und Sie können wählen.

# Version 2.6 #
* Die Funktionen der Schaltflächen "Hinzufügen" und "Entfernen" wurden in der Listenverwaltung der Postleitzahl optimiert;
	* Jetzt sind die Operationen viel schneller!
* Die Funktion des Schalters "Test" wurde optimiert, jetzt werden bis zu 13 Suchschlüssel benutzt;
	* Eigendlich sollten so alle Städte gefunden werden.
* Die Funktion der Schaltfläche "Finden sie ihre Stadt ...", findet jetzt mehr Länder;
	* Es wurde ein automatischer Test hinzugefügt, der die funktionsfähigen Postleitzahlen sammelt und eine schnelle Visualisierung dank der Erstellung eines kleinen Puffers entsprechend dem Namen des jeweiligen Landes erlaubt.
* Drei neue Klangeffekte wurden hinzugefügt;
	* Es ist notwendig, sie von den Einstellungen des Plugins zu aktualisieren.

# Version 2.5 #
* Befehl hinzugefügt, um vorübergehend die Temperaturskala von Celsius in Fahrenheit umzuschalten, der Befehl ist auch im Einstellungsfenster wirksam.
* Fehler behoben: wenn der Benutzer die Schalter "Hinzufügen" oder "Voreinstellung" nicht gedrückt hat, konnte der Name der Stadt nicht laut gesprochen werden, da er nicht in der Liste enthalten war.
* Neue Strings zur Liste Wetterberichte hinzugefügt.

`#` Änderungen im Fenster Weather Plus Einstellungen:

* Schaltfläche hinzugefügt, um eine Recherche-Webseite zu öffnen, um nach den weltweiten Postleitzahlen zu suchen.
* Die Möglichkeit hinzugefügt, Postleitzahlen von Freunden zu importieren / exportieren.
* Möglichkeit, den Wetterbericht oder die Wettervorhersage in die Zwischenablage zu kopieren.
* Zusätzliche Möglichkeit, die meteorologischen Audioeffekte zu hören, ermöglicht auch die Option zur Installation / Aktualisierung der Audioeffekte.
* Zusätzliche Fähigkeitstasten für die Verwaltung von Postleitzahlen.
* Wechseln Sie in den Anzeigemodus des Fensters, die Menüs von NVDA sind nicht eingeschränkt, wenn es geöffnet ist.

# Version 2.4.4 #
* 2 neue Strings zur Liste Wetterberichte hinzugefügt.
* Übersetzung in Spanisch und Französisch (dank Pablo Vargas und Rémy Ruiz).

# Version 2.4.3 #
* Hinzufügen der Wettervorhersage für die nächsten 4 Tage.
* Hinzufügen eines Strings zur Liste Wetterberichte.
* Die Liste der temporären Postleitzahlen wird jetzt zu jeder neuen Einfügung geordnet.

#Version 2.4 #
* Ein Fehler wurde behoben, durch den die Stadtnamen mit akzentuierten Vokalen nicht richtig gespeichert und verwaltet werden konnten.

# Version 2.3 #
* Das Dialogfeld zum Einstellen der Temperatturskala wurde entfernt;
	* Es wurde ein neues GUI hinzugefügt, was es erlaubt, alles in einem Fenster festzulegen.
* Sie können dann auch als Standard-Postleitzahl, die als Liste gesammelt wurde, testen / hinzufügen / löschen / voreingestellt werden.
* Das Dialogfeld für die Eingabe einer Postleitzahl wurde geändert. Im temporären Modus können Sie eine Postleitzahl einrichten, die zuvor in der Liste unter Einstellungen im Menü hinzugefügt wurde.
* Die Dokumentation kann jetzt in Englisch gelesen werden, wenn die Spracheinstellung nicht in den Dokumenten enthalten ist.

# Version 2.2 #
* Fehler behoben, durch den Sie die Dokumentation für die endgültigen Versionen von NVDA nicht öffnen konnten.

# Version 2.1 #
* Ein Fehler wurde behoben, durch den das Plugin nicht ordnungsgemäß geschlossen wurde. Dadurch wurde das Symbol NVDA update in der Taskleiste nicht angezeigt.

# Version 2.0 #
* Wetter Plus Einstellungen im Untermenü "Einstellungen" verschoben.
* Die korrekte Eingabe im Flug wird nicht mehr gespeichert, daher ist es vorübergehend;
	* Um die in den Einstellungen eingestellte Stadt anzurufen, drücken Sie INSERT + control + f3.

# Version 1.9 #
* Zusätzliche Hilfe bei der Eingabe von Funktionen.
* Hinzufügung einer neuen Funktion für die schnelle Eingabe von Postleitzahlen.
* Die read / write-Konfiguration weather.ini wurde hinzugefügt. Die Quelldatei muss nun nicht mehr bearbeitet werden.
* Das Wettermenü wurde in der Systemablage hinzugefügt.
* hinzugefügt Einstellung Untermenü Postleitzahl.
* Untertemperatur-Skala (Fahrenheit oder Celsius) hinzugefügt.
* hinzugefügter Menüpunkt Dokumentation.
* Italienische Lokalisierung hinzugefügt.

# Vorherige Version 1.1 #
* aktualisiertes NVDA-Addon.
* provisorische Übersetzung in der Quelle.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
