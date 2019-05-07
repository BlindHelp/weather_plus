#Weather Plus #

* Author: Adriano Barbieri
* NVDA compatibility: 2017.3 to 2019.1 
* Download: [Stable Version][1]

# ABOUT WEATHER PLUS: #

* This plugin adds local temperature and forecasts to 24 hours up to 9 additional days for NVDA
* Copyright (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Released under the GNU GPL (General Public License) v2
* Version: 6.0.

# Weather Plus works through the use and presence of the following services:: #
* [https://developer.yahoo.com/weather/](https://developer.yahoo.com/weather/)
* [http://woeid.rosselliot.co.nz/lookup/](http://woeid.rosselliot.co.nz/lookup/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.timeanddate.com/](https://www.timeanddate.com/)
* [http://www.nvda.it/](http://www.nvda.it/)

# USE: #
* Press NVDA + w to the current temperature and weather conditions.
* Press NVDA + shift + W for 24 hours forecast and forecast up to 9 days.
* Press NVDA + shift + ctrl + w to set a temporary city.
* Press NVDA + shift + control + alt + w to open the Weather Plus settings dialog.
* Press NVDA + alt + w to know the last update of the weather report.
* Press control + shift + w to toggle between Fahrenheit, Celsius or Kelvin.

# To set Weather Plus: #
Read the section: Weather Plus First Settings.

--------------------------------------------------------------------------------

# Weather Plus First Settings: #

You must set the Weather Plus addon before its first use!

Go to:

Preferences submenu

Weather Plus Settings submenu

Show configuration items.

# Press the item for: #

* Set and Manage Your Cities...
	* Displays or allows to set the current city from a list.
* Documentation
	* Opens the help file for the current language.
* Check for Update...
	* Notify if there is an updated version available.

Press the item:

# Set and Manage Your Cities... #

Displays or allows to set the current city from a list

The following message is displayed only for the first time!

Settings Preset

None

F1: help placing, F2: last TAB selection, F3: list and edit box, F4: control duration Weather Forecast, F5: volume controls.

Enter a City, woeID or choose one from the list, if available.

Note: The F5 key is available if the sound effects are activated.

After pressing the item "Set and Manage Your Cities...", find you other buttons as follows:

# Test #

Testing the validity of woeID entry and find the name of city assigned or viceversa.

# Add #

Add the current city into your list.

This button is activated if you select a city from the list, or it has passed the test.

# Details #

Displays information on the current city.

This button is activated if you select a city from the list, or it has passed the test.

# Define #

Allows you to define the area, in order to adapt the sound effects.

This button is activated if the audio effects are installed and activated, and you select a city from the list.

# Preset #

Presets a city as the default, will be used every time you restart the plugin.

This button is activated if you select a city previously inserted in the list and not preset, or it has passed the test.

# Remove #

Delete the current city from your list.

This button is activated if you select a city previously inserted in the list.

# Rename #

Rename the current city.

This button is activated if you select a city previously inserted in the list.

# Import new cities... #

Permits to incorporate in your list new cities importing them from another list with the extension *.zipcodes; you can select the city you want to import, by turning on the check box associated.

# Export your cities... #

Permits to save your list of cities in a specified path

This button is activated if you have added and saved at least one city into the list.

# Scale of temperature measurement: #

Use the radio button to select between:

* Celsius (by default)
* Fahrenheit
* Kelvin

# Degrees shown as: #

Use the radio button to select between:

* Celsius `-` Fahrenheit `-` Kelvin (by default)
* C `-` F `-` K
* Don't specify

Combo box:

# Weather Forecasts up to days: 3 #

Choose between 1 to 10 (3 days by default)

Toggle the check box for:

# Copy the weather report and weather forecast, including city details to clipboard #

check box not checked (by default)

# Enable audio effects (only for the current weather conditions) #

This check box also allows you to manage the installation of sound effects;

If the sound effects are installed and the check box is activated, the F5 key and the volume setting becomes available.

It will also be available an additional check box:

* Use only weather effects.

You can change the overall volume or change the last  heard sound effect and filter out the others sounds in your environment.

check box not checked (by default)

# Use only weather effects #

is available if sound effects are enabled;

If is enabled, allows to listen only weather effects such as rain, wind, thunder, etc., filtering out all environmental ones.

check box not checked (by default)

# Enable the reading of the hours in 24-hour format #

If disabled announces the time in 12-hour format, example: 12 AM `-` 12 PM.

check box checked (by default)

# Enable help buttons in the settings window #

check box checked (by default)

# Read wind informations #

check box not checked (by default)

If enabled, you can also activate:

* Add wind direction;

Indicates the provenance of the wind.

check box checked (by default)

* Add speed of the wind;

Indicates the speed in kilometers or miles per hour.

check box checked (by default)

* Add speed in meters per second of the wind;

check box checked (by default)

* Add perceived temperature;

check box checked (by default)

# Read atmospherical informations #

check box not checked (by default)

If enabled, you can also activate:

* Add umidity value;

Indicates the humidity in percent.

check box checked (by default)

* Add visibility value;

Indicate in kilometres or miles the distance visible.

check box checked (by default)

* Add atmospheric pressure value;

Indicates the atmospheric pressure in millibars or inches of mercury.

If it's checked, enable an additional check box that allows you to indicate the pressure in millimeters of mercury.

check box checked (by default)

* Add status of barometric pressure;

check box checked (by default)

# Read astronomical informations #

Indicates the time of sunrise and sunset.

check box not checked (by default)

# Use the comma to separate decimals #

If enabled, uses the comma as a decimal separator, otherwise, use the point.

check box not checked (by default)

# Check for upgrade #

If is activated this alerts when there is an update of the addon.

check box checked (by default)

# Press the OK button to confirm the action or the Cancel button to cancel the action. #

If you have modified the cities list, by pressing "Cancel", you will be remembered and you can still save it.

# Note: your settings will be save in the file named: #

* "Weather.ini": startup settings of Weather Plus.
* "Weather.volumes": custom audio volume levels, regardless of the overall volume.
* "Weather.zipcodes": list of cities with their zip code and definitions.

--------------------------------------------------------------------------------

# What's new: #

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

# Version 4.8 #
`#`Changes in the Weather Plus Settings window:

* Added new checkbox;
	* "Use only weather effects";
	* This allows you to filter out all other environmental effects.
* Improved random playback and added 71 new sound effects;
  	* You will need to update them by clicking twice in "enable audio effects" check box.
* The volume type assigned by the user, between the general and current audio volume, now is maintained when the configuration is saved.
* Removed useless sound during selection text in edit box by pressing control+a.
* Improved readability into help window invokable with F1 function key.
* Added new compatibility flag for NVDA 2019.1, and the current alpha versions.

# Version 4.7.7 #
* Removed unnecessary notification of download complete when the update of Weather Plus.
* Added 6 new sound effects;
	* It will be necessary to update them from the settings of the plugin.

# Version 4.7.6 #
* Fixed a minor bug in the function GetCoords();
	* 2 values were not returned in the lack of connection.

# Version 4.7.5 #
* MenuItem.GetLabel() is deprecated and has been replaced by MenuItem.GetItemLabelText().
* Were correct some declarations of global variables.

# Version 4.7.3 #
* For convenience has been updated the function in "details";
	* The information about the altitude are now provided by veloroutes.org.
	* This leads to small differences of little relevance.

# Version 4.7.2 #
* Fixed encoding bug in Removeupdate function.

# Version 4.7.1 #
* Fixed a bug in GetTimezone;
	* In case of null data was returned only one value instead of 3 required.

# Version 4.7 #
* Simplified the update section;
	* Now at the start, in case an update is available it will be possible to proceed directly through a single dialog box.
* removed the file selector in the update section;
	* Now the update file is uploaded to the temporary folder, thereby solving problems due to non-expert users.

# Version 4.6.9 #
* Added arab localization (thanks to Wafik Immaculate).

# Version 4.6.8 #
* Updated Portuguese and Brasilian localizations (thanks to Alberto Mendonça).

# Version 4.6.7 #
* Improved the reading of the current time;
	* In some cities, it was not correct.
* Added daylight saving time to the details;
	* Available only for the countries that adopt it.

# Version 4.6.5 #
* Fixed a small bug during the reading of the current time;
	* The separator ":" not being removed during conversion to integer.

# Version 4.6.4 #
* Improved the reading  of current local time; search keys are more accurate.

# Version 4.6.2 #
* Fixed bug: after a check for updates, the "set a temporary city..." menu was enabled even if there was no available list of cities.
* Fixed bug; unable to configure WP when the weather.ini has not been created yet,.

# Version 4.6 #
* Added the menu item "Set a temporary city...";
	* For the sake of completeness, now you can open the temporary city's list  also from the menu.
* Improved management of temperature scale;
	* Now the settings window will always return the default value.
* Improved prevention of the multiple opening of the main windows;
	* If one of these is already opened, in addition to the sound alert, puts it in foreground.
* Improved audio effects;
	* Now are based on the current local time from the city in use.

`#`Changes in details button function in settings window:

* Added current local time.
* Fixed altitude value;
	* Now return the altitude values when the value is less than or equal to zero.
* Fixed import function;
	* If it was removed the default city, no longer appears in the title bar.

# Version 4.5.5 #
* Correct location and documentation in Serbian.
* Correct the German localization.

`#`Changes in the Weather Plus Settings window:

* Added new checkbox;
	* You can enable the comma as the decimal separator, otherwise the separator will be the point.

# Version 4.5.3 #
* correct 2 strings in Russian and ukraine localization.
* Correct title in Check for upgrade window.
* Improved update algorithm;
	* Now the link to update is directly read from manifest url.

# Version 4.5 #
* Added hotkey NVDA+shift+control+alt+w;
	* Open the Weather Plus settings dialog.
* Correct some English strings.

`#`Changes in the Weather Plus Settings window:

* Added 8 new check boxes;
	* It is now possible to further customize the output:
* wind direction.
* wind speed.
* Perceived temperature.
* Humidity value.
* Visibility value.
* Atmospheric pressure value.
* Indicates the atmospheric pressure in millimeters of mercury (mmHg).
* State of the barometric pressure.

# Version 4.4.8 #
* Added Polish translation (thanks to Zvonimir Staneczyć).
* Weather Plus it's now compatible also for future wx version 4;
	* Note: at the moment  with wx version 4.0.0b1 msw (phoenix) generates an annoying error when using the vertical arrows in many edit boxes:

wxAssertionError: C++ assertion "Assert failure" failed at ..\..\src\common\evtloopcmn.cpp(110) in wxEventLoopBase::Yield(): wxYield called recursively.

# Version 4.4.1 #
* Added SSL support;
	* Is used only if there is a SSL error certificate verify failed.

# Version 4.4 #
* Fixed bug in the reading of the new version string, during a connection time-out.
* Improved the upgrade section;
	* Now the dialog do not interferes with the nvda menu.
* Revised and corrected russian Localization.
* Adding Ukrainian translation (thanks to Alex Yeshanu).

# Version 4.3.4 #
* Revised and corrected German Localization.

# Version 4.3.3 #
* Added German localization (thanks to Karl Eick).

# Version 4.3.2 #
* Added Romanian localization (thanks to Florian Ionașcu).

# Version 4.3.1 #
* Fixed a minor bug in the function "details";
	* The strings "latitude" and "longitude" were reversed compared to the value.

# Version 4.3 #
* The Public folder links will become inactive on March 15.
	* On that date, the Public folder will become a standard Dropbox folder, and will not be useable by the addon.
	* The upgrade links of the addon and of the samples have been updated, therefore, from now on, WP will lean completely on the italian page of NVDA.

# Version 4.2.4 #
* Fixed a minor bug when the connection is not active.

# Version 4.2.3 #
* Now Weather Plus is able to run some connection attempts before notifying the malfunction of the WoeId in use, it emits a beep at each attempt;
	* This beep, if you want, can be disabled by using a check box by Weather Plus settings.

# Version 4.2.2 #
* Fixed bug in the translation of the scale measurement.
	* In some languages, Kelvin, Celsius and Fahrenheit have not been translated.

# Version 4.2.1 #
* Fixed update notice of Weather Plus during the Windows start-up;
	* This happens when the button was pressed "Use currently saved settings on the logon and other secure screens (requires administrator privileges)" from the general settings of nvda, which copies the configuration, and all of the add-on folder systemConfig, but these are not synchronized with subsequent updates of the add-ons.
	* If you have ever used at least once this option, you will have to do it again one last time just after to have up-to-date Weather Plus.

# Version 4.2 #
* Added 5 new sound effects;
	* It will be necessary to update them from the settings of the plugin.
* Fixed bug in the import function;
	* The list of cities was not sorted alphabetically.
* Added import mode in the import function;
	* You may decide to completely replace your own list, or simply add new cities to it.
* Updated the reading of the weather forecast, current weather report;
	* Adding the perceived temperature (wind chill).
* Added new strings to the list weather reports.

# Version 4.1 #
* Fixed bug in the forecast for up to 10 days;
	* Now if the estimates received are in number less than the request of the user, the missing days are indicated as unknown.
* Fixed string help entry on the command nvda+shift+w.
* Revised and updated documentation.

# Version 4.0 #
* Updated some parts of code and replace all instructions eval().

# Version 3.9.7 #
* Fixed bug during the ratio of weather forecasts;
	* Now the temperatures are read correctly.

# Version 3.9.6 #
* Changed the rounding in the conversion of atmospheric pressure from mbar in inches of mercury;
	* Now the value is calculated in defect, while before it was in excess.

# Version 3.9.5 #
* Added 2 new strings to the list weather reports.
* Fixed 2 bugs.
* Updated running sounds for the effect in conditions of only wind;
	* Now the sound of the wind can vary randomly.

# Version 3.9.4 #
* documentation, localizations for Croatian and german language eliminated;
	* Because they are no longer supported by the respective translators.
* Fixed bug on Serbian localization.
* Updated Czech localization.
* Updated documentation and localization Gallega.

# Version 3.9 #
* Changed again API service;
	* Weather Plus now uses the new Yahoo Weather API with language Yahoo!Query and JQuery:
	* [yahoo-weather-api-with-yahooquery](http://codesimplified.blogspot.it/2013/10/yahoo-weather-api-with-yahooquery.html)
* The key-API is no longer required.
* Restored The search of the homonymous cities;
	* It will be possible to choose exactly the desired city from a list.
* Optimized the output of general sounds;
	* Now they are synchronized with the voice synthesis and are faster.
* Improved the cache for data off-line;
	* Is zeroed every 10 minutes or only by changing the city.
* barometric pressure measured in mbar, or in inches of mercury (if set to Fahrenheit).

# Version 3.8 #
* Changed the  data package API;
	* From the xml format to JSON format, the data are more accurate, especially the time zone.
* Enabled the automatic setting of the language;
	* Now the API sends the data of the weather conditions in the language set by nvda.
* Adding a cache for bulletin and weather forecasts;
	* If not changed the city, degree scale or the days of forecast set, you will be able to read the data for 10 minutes even when connection off-line.
	* The cache is reset at each change described above.
	* This is because the bulletins do not change in this period of time and to reduce the frequent calls to the API, maybe playing with sound effects.
* Improved search updates;
	* Now once downloaded, It will be  activated to its installation, or in the case of a portable version of nvda It will be opened the folder where you saved the update.
* Updated all sounds general notice;
	* Is no longer used the module "tones", but are used small files in WAV format.

# Version 3.7 #
* Added possibility to disable the conversion in meters per second of the wind.
* Added possibility to use units of measure in pounds per square inch.
* Fixed 2 bugs.

# Version 3.6 #
* Changed the API service (application programming interface);
	* Now WP uses the service offered by OpenWeatherMap.org instead of Yahoo Weather.com.
* Added Wind classification in the current bulletin.
* Added a  cloudiness percentage  in the current bulletin.
* Adopted the units of pressure measurement in hectopascal in the current bulletin.

`#`Changes to the Weather Plus Settings window:

* Changed insertion/search from yahoo zipcode/woeId in ID number, Identifier of the city;
	* ID numbers city are similar to woeid, but the woeId will no longer work, even the old zipcode.
	* You will be able to rediscover a great part of the cities by typing the name or part of it.
* Added insertion/Search for geographical coordinates.
* Added insertion/search by postal code.
* Improved the function "details".
* assigned to F1 key the entry/search help.
* assigned to F4 key the controls to the forecasts from 1 to 16 days set;
	* Attention, if you choose to copy to the clipboard a value greater than 10, it will not be read!
* Assigned F5 key for audio controls.
* Adding measurement scale degrees Kelvin.
* Added check for updates;
	* You can set the control by settings or check manually from menu.
* reassigned the button "Find your city" in "Management of your API Key...";
	* Allows you to enter or change the key-API.

# Version 3.5 #
* Added Croatian translation (thanks to Gordan Radić).
* Added control for no longer valid WoeId and Zip Code found in the network;
	* There have been reports of codes that have stopped working from one day to another, WP now warns if one of these has been inserted from the windows of search on the net.
	* If this occurs using the function "Find your city...", please report it to me so that I can update the Weather_buffer and remove them from the list.
* Fixed a bug in the search function the next and previous; lacked the mbcs encoding and could not recognize accented characters.
* Updated the window to set one temporary zip code;
	* Added feature "Find" As in the other windows of Weather Plus:
	* Control+F3 = Find..., F3 = Find next, Shift+F3 = Find previous.

# Version 3.4 #
* Added Galician translation (thanks to Iván Novegil).
* Added Portuguese translation (thanks to Ângelo Miguel Abrantes).
* Added German translation (incomplete).

# Version 3.3 #
* Added the measure of the speed of wind in meters per second.
* Modified the encode in "mbcs";
	* This permits to use also the diacritical marks in the city names.

# Version 3.2 #
* Updated the reading of the weather forecast, current weather report and reading of the date of the current weather report;
	* Yahoo weather forecast, from a bit of time and in random amounts, allows it to pass a historic from -10 to -5 days of weather forecast to be inserted between the updated data that we want to read;
	* It was added a filter that allows you to read only the last weather data updated, and a discreet beep alerts when it intervenes;
	* This beep, if you want, can be disabled by using a check box by Weather Plus settings.
	* Obviously, the filtering of data sometimes involves a short delay in reply, but is still acceptable.
* Forecasts of the time extended to 10 days.

# Version 3.1 #
* Added translation in Serbian (thanks to the kind cooperation of Gašić Dejan `-` Gashich Deyan).
* Fixed command insert+alt+w;
	* It did not check the validity of the zipcode in use and did not check if the connection was active as the other commands do.
* Updated the playback function of sound effects;
	* Mp3 are now used, with a considerable saving on the download time and disk space, thanks to the reduced size of compressed files.
* Added 55 new sound effects;
	* It will be necessary to update them from the settings of the plugin.

`#`Changes to the Weather Plus Settings window:

* Fixed display help on the buttons;
	* Now disables / enables real-time through the appropriate check box.
* Added 3 shortcut commands to navigate more quickly in the window:
* F1 jumps into list and edit box of zip code.
* F2 returns to the last selection reached with TAB.
* F3 jumps into volume controls (if the sound effects are installed and activated).
* Added shortcut commands for all check boxes and buttons;
	* Omitted the two radio buttons as they are present in succession and the first is reachable with the command control+shift+w.
* Changed, the button "define" is now disabled if the sound effects are not installed and activated.
* Added volume controls;
	* You can adjust the overall volume and the last heard sound effect;
	* This option is enabled if the sound effects are installed and activated.
* Added ability to set the system time in 12-hour format (12:30 AM `-` 12:30 PM) , or the 24-hour system (12:30 `-` 00:30).

# Version 3.0 #
* Added translation in Slovak (thanks to the kind cooperation of Vitek Jirasek).
* Added translation in Portuguese-Brazilian and Portuguese-Portugal (thanks to the kind cooperation of Adair Knaesel).
* Added new strings to the list weather reports.
* Added 171 new sound effects, now the total amount is 213.
* Added command insert+alt+w in the gesture to announce last update of current bulletin.
* Added scriptCategory which shifts in the correct position the rapid keys of Weather Plus in "Input gestures..."

`#`Changes to the Weather Plus Settings window:

* Added radio button to set how to indicate the temperature scale;
	* The choice is between:
* Celsius `-` Fahrenheit
* C `-` F
* No indication
* Added button " Define";
	* It permits to define the zone of one city between:
* Hinterland
* Maritime area
* Desert zone
* Arctic zone
* Mountain zone
	* The choice will consent to Weather Plus to use more appropriate sound effects for every single city;
	* This is the reason for the boost of the number of new sound effects in this versione of the addon;
	* Many of the new sound effects I got them from Tapin, whom I thank sincerely.

# Version 2.9 #
* Added option when importing to select the contents of the imported file.
* Four new sounds effects were added.
* Adding translation into Russian (thanks to Alex Yeshanu).
* Adding translation into Czech (thanks to Jirimu Holzingerovi).

# Version 2.8 #
* Fixed bug in "details", it used to open the window of the occurrences when he could not find the city.
* Fixed regexp to search for the altitude;
	* It did not accept parameters of single digits.
* Improved parser of the edit box;
	* It should find more easily the city.
* Connections now handled by urllib2, instead of urllib;
	* This should allow the functioning of the addon even on a computer connected to the corporate network protected by proxy.
* Added feature "Find";
	* Control+F3 = Find..., F3 = Find next, Shift+F3 = Find previous.

# Version 2.7 #
* Fixed wrong name of a string "Motorcycle" in "Motorcycle00";
	* He asked updated sound effects because they could not find the file.
* Added ability to read about wind ;
	* Direction, speed and temperature of the wind.
* Added ability to read atmospherical informations;
	* Humidity, visibility, pressure and state of the barometric pressure.
* Added ability to read the Astronomic informations;
	* Time of sunrise and sunset.

`#`Changes to the Weather Plus Settings window:

* Added 3 check boxes to manage their information listed above.
* Added button " Details ";
	* Provides some informations such as the real name of the city ( assigned by Yahoo Weather Forecast), the state / region and the nation to which it belongs;
	* With geographic coordinates, and height above sea level.
* Added recognition of WoeID (location codes, eg. Bologna it corresponds to 711080).
* Now you can type the name of the city, in this case, if any, the occurrences will be listed and you will be able to choose.

# Version 2.6 #
* The functions of the buttons "Add" and "Remove" were optimized in the zip code's list management;
	* Now the operation are a lot more fast!
* The function of the button "Test" was optimized, now it exploits until 13 research keys;
	* Now if it doesn't find the name of the city it is a real bad luck!
* The function of the button "Find your city...", now finds more countries;
	* It was added an automatic test that collects the functioning zip codes, and it further consents a rapid visualization thanks to the creation of a little buffer corresponding to the name of the specific country.
* Three new sounds effects were added;
	* It will be necessary to update them from the settings of the plugin.

# Version 2.5 #
* Added command in the gesture to switch temporarily the temperature scale from Celsius to Fahrenheit, the command is also effective in the settings window.
* Fixed bug, if the user did not press the "Add" or "Preset" buttons, it did not allow to vocalize the name of the city since it was not included in the list.
* Added new strings to the list weather reports.

`#`Changes to the Weather Plus Settings window:

* Added button to open a research web page in order to check for the world-wide Zip Codes.
* Added the possibility to import / export the Zip Codes from friends.
* Added possibility to copy the wheather report or the weather forecast to the clipboard.
* Added possibility to listen to the meteorological audio effects, the option also allows the installation / upgrade of the audio effects.
* Added ability help buttons on the management of Zip Code.
* Change to the display mode of the window, the menus of nvda are unrestrained when it is open.

# Version 2.4.4 #
* Added 2 new strings to the list weather reports.
* Adding translation into Spanish and French (thanks to Pablo Vargas and Rémy Ruiz).

# Version 2.4.3 #
* Adding up the weather forecast for the next 4 days.
* Adding a string to the list weather report.
* The list of temporary zipcode is now ordered to each new insertion.

# Version 2.4 #
* Fixed a bug that prevented to save and manage properly the city names containing accented vowels.

# Version 2.3 #
* Eliminated dialog box to set the scale of temperature measurement, has now been added a new gui that allows you to set all in one window.
* You will then also possible to test / add / delete / preset as the default Zip Code collected as a list.
* Modified the dialog box for entering typed a Zip Code, now in temporary mode allows you to set a Zip Code previously added to the list in Preferences from the menu.
* Now the documentation can be read in English if the language setting is not included in the documents.

# Version 2.2 #
* Fixed bug that did not allow you to open the documentation for the definitive versions of NVDA.

# Version 2.1 #
* Fixed a bug that did not close properly the plugin, this prevented the NVDAupdate the icon in the system tray.

# Version 2.0 #
* Weather Plus Settings menu in Preferences submenu moved.
* correct input on the fly is no longer saved, so it is temporary;
	* To call the city set in the preferences, press INSERT + control + f3.

# Version 1.9 #
* added help entering functions.
* added a new function for quick entry of Zip Code.
* added read / write configuration weather.ini, now no longer need to edit the source file.
* Weather menu added in the System Tray.
* added setting submenu Zip Code .
* added sub-setting temperature scale (Fahrenheit or Celsius).
* added menu Documentation.
* Added Italian localization.

# Previous Version 1.1 #
* updated NVDA-addon.
* provisional translation inside the source.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
