# Weather Plus #

* Autor: Adriano Barbieri
* NVDA compatibility: 2017.3 to beyond
* Baixar: [versão estável][1]

# Acerca do WEATHER PLUS: #

* Este addon para o NVDA fornece a temperatura local e a previsão do tempo
  actual para as próximas 24 horas e a previsão até 2días adicionais and hourlyforecast.
* Copyright (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Lançado sob a licença GNU GPL (General Public License) v2

* O Weather Plus funciona com base na utilização e presença dos seguintes
  serviços:
* [https://www.weatherapi.com/](https://www.weatherapi.com/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.nvda.it/](https://www.nvda.it/)

# USAGE: #
* Press NVDA+w to get the information about current temperature and weather
  conditions.
* Press NVDA+shift+W to get 24 hours forecast and forecast up to 2 days.
* Press NVDA+shift+W twice to get hourlyforecast of temperature and atmospheric conditions.
* Press NVDA+shift+ctrl+w to set a temporary city.
* Pressione NVDA+shift+control+alt+w Para abrir o diálogo de configurações
  do weather plus;
* Press NVDA+alt+w to get the date and time, when the weather report was
  updated.
* Press control+shift+w to toggle between Fahrenheit, Celsius or Kelvin
  temperature scales.

# Weather Plus setup: #

* You must set the Weather Plus addon before its first use! Go to the
  Preferences submenu, Weather Plus Settings submenu and choose one of the
  following options:


* Set and Manage Your Cities... - Displays or allows to set the current city
  from a list.
* Documentation - opens the help file for the current language.
* Check for Update... - notifies about the availability of the new version.

To add a new city: press the following item:

* Set and Manage Your Cities... Displays or allows to set the current city
  from a list

* The following message is displayed only for the first time! Settings
  Preset None F1: help placing, F2: last TAB selection, F3: list and edit
  box, F4: control duration Weather Forecast, F5: volume controls.

* In the edit box, enter a City or choose one from the list, if
  available. Note: The F5 key is available if the sound effects are
  activated.

* After pressing enter on the item "Set and Manage Your Cities...", you will
  find other buttons as follows:

* Test - Test the validity of the city and find the data of it.

* Add - adds the current city into your list. This button can be activated
  if you select a city from the list, when the city entered passed the test.

* Details - displays information about the current city. This button is
  activated if you select a city from the list, or it has passed the test.

* Define - Allows you to define the area, in order to adapt the sound
  effects. This button can be activated if the audio effects are installed
  and activated, and you select a city from the list.

* Preset - Presets a city as the default, will be used every time you
  restart the plugin. This button is activated if you select a city
  previously inserted in the list and not preset, or it has passed the test.

* Remove - Deletes the current city from your list. This button can be
  activated if you select a city previously inserted in the list.

* Rename - Rename the current city. This button can be activated if you
  select a city previously inserted in the list.

* Import new cities... - This button allows you to import cities from the
  another list of cities with the extension *.zipcodes; you can select the
  city you want to import, by turning on the check box associated with it.

* Export your cities... - It allows you to save the cities in the specified
  file with the extension *.zipcodes. This button is activated if you have
  added and saved at least one city into the list.

* hourly forecast setting... - This button allows you to choose the contents of the hourly forecast report.

* Scale of temperature measurement: Use the radio button to select between
  Celsius (by default), Fahrenheit and Kelvin.

* Degrees shown as: Use the radio button to select between: Celsius `-`
  Fahrenheit `-` Kelvin (by default C `-` F `-` K or unspecified.

* Combo box: Weather Forecasts up to days: 1 You can choose between 1 to 3
  (1 days by default)

* Combo box: API response language:: English, en; you can choose the language of the weather conditions text.

* To perform the following actions, toggle the following checkboxes:

* Copy the weather report and weather forecast, including city details to
  clipboard check box not checked (by default)

* Enable audio effects (only for the current weather conditions) This check
  box also allows you to manage the installation of sound effects; If the
  sound effects are installed and the check box is activated, the F5 key and
  the volume setting becomes available.

* There will also be available an additional check box: Use only weather
  effects.

* You can change the overall volume or change the last heard sound effect
  and filter out the others sounds in your environment. Checkbox is not
  checked by default.)

* Use only weather effects - This option is available if sound effects are
  enabled; If is enabled, allows to listen only weather effects such as
  rain, wind, thunder, etc., filtering out all environmental
  ones. (unchecked by default)

* Enable the reading of the hours in 24-hour format. - If this checkbox is
  unchecked, announces the time in 12-hour format for example, 12 AM `-` 12
  PM. check box is checked (by default)

* Enable help buttons in the settings window check box checked (by default)

* Read wind information check box not checked (by default) If this checkbox
  is enabled, you can also activate the following checkboxes:

* Add wind direction; Indicates the provenance of the wind. check box
  checked (by default)

* Add speed of the wind; Indicates the speed in kilometers or miles per
  hour. check box checked (by default)

* Add speed in meters per second of the wind; check box checked (by default)

* Add wind gust speed of the wind; checkbox checked (by default)

* Add perceived temperature; check box checked (by default)

* Read atmospherical information check box not checked (by default) If
  enabled, you can also check the following checkboxes:

* Add humidity value; Indicates the humidity in percent. check box checked
  (by default)

* Add visibility value; Indicate in kilometres or miles the distance
  visible. check box checked (by default)

* Add atmospheric pressure value; Indicates the atmospheric pressure in
  millibars or inches of mercury. If it's checked, enable an additional
  check box that allows you to indicate the pressure in millimeters of
  mercury. check box checked (by default)

* Add cloudines value; check box checked (by default)

* Add precipitation value; check box checked (by default)

* Add ultraviolet radiation value; check box checked (by default)

* Read astronomical information; indicates the time of sunrise and sunset and the time of moonrise and moonset. Checkbox not checked (by default)

* Use the comma to separate decimals If enabled, uses the comma as a decimal
  separator, otherwise, use the point. check box not checked (by default)

* Displays output in a window; if is activated, this displays the forecast in a window.
  Checkbox not checked (by default)

* Check for upgrade If is activated this alerts when there is an update of
  the addon. check box checked (by default)

* Pressione "ok", para confirmar as configurações ou "cancelar", para as
  rejeitar.

* If you have modified the cities list, by pressing "Cancel", you will be
  remembered and you can still save it Note: your settings will be save in
  the file named:

* "Weather.ini": As configurações iniciais do weather plus.
* "Weather.volumes": níveis de volume de áudio personalizados,
  independentemente do volume total.
* "Weather.zipcodes": lista de cidades com o seu código postal e definições.
* "Weather.default": Your default city.
* "Weather_searchkey": search key saved.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
