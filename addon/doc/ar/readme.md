# Weather Plus #

* المطوِّر: Adriano Barbieri
* التوافُق مع NVDA: 2017.3 وما بعده.
* رابط التنزيل: [Stable Version][1]

# حول إضافة WEATHER PLUS: #

* تُضيفُ هذه الإضافة إلى NVDA خاصية معرفة درجة الحرارة المحلية وتوقُّعات الطقس لأربع وعشرين ساعة، إضافةً لتوقُّعات أحوال الطقس ليومين إضافيين.
* حقوقُ الطباعة  (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* منشورة ضمن رخصة GNU GPL (General Public License) v2
* تعمل Weather Plus باستخدام الخدمات الآتية:
* [https://www.weatherapi.com/](https://www.weatherapi.com/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.nvda.it/](https://www.nvda.it/)

# الاستخدام: #

* اضغَطْ NVDA+w للحصول على معلومات عن درجة الحرارة وأحوال الطقس الحالية.
* اضغَطْ NVDA+shift+W للحصول على توقُّعات الطقس للأربع والعشرين الساعة، إضافة لليومين القادمين..
* اضغَطْ NVDA+shift+W مرتين للحصول على توقُّعات درجات الحرارة وأحوال الطقس لكلّ ساعة.
* اضغَطْ NVDA+shift+control+w لضبط مدينةٍ مؤقتة.
* اضغَطْ NVDA+shift+control+alt+w فتح مربّع الحوار الخاص بإعدادات إضافة Weather Plus .
* اضغَطْ NVDA+alt+w للحصول على الوقت والتاريخ عند حُدوث تحديث لتقرير أحوال الطقس.
* اضغَطْ control+shift+w للتبديل بين وحدات القياس المختلفة لدرجة الحرارة: فهرنهايت، مئوية كلفين.

# ضبطُ Weather Plus: #

* You must set the Weather Plus addon before its first use! Go to the Preferences submenu, Weather Plus Settings submenu and choose one of the following options:
 * Set and Manage Your Cities... - Displays or allows to set the current city from a list.
 * Set a temporary city... - Displays and allows to set one temporary city from a list if available.
 * Documentation - Opens the help file for the current language.
 * Check for Update... - Notifies about the availability of the new version.

To add a new city: press the following item:

* Set and Manage Your Cities... - Displays or allows to set the current city from a list.
* The following message is displayed only for the first time! Settings Preset None F1: help placing, F2: last TAB selection, F3: list and edit box, F4: control duration Weather Forecast, F5: volume controls.
* In the edit box, enter a City or choose one from the list, if available. Note: The F5 key is available if the sound effects are activated.
* After pressing enter on the item "Set and Manage Your Cities...", you will find other buttons as follows:
* Test - Test the validity of the city and find the data of it.
* Add - Adds the current city into your list. This button can be activated if you select a city from the list, when the city entered passed the test.
* Details - Displays information about the current city. This button is activated if you select a city from the list, or it has passed the test.
* Define - Allows you to define the area, in order to adapt the sound effects. This button can be activated if the audio effects are installed and activated, and you select a city from the list.
* Preset - Presets a city as the default, will be used every time you restart the plugin. This button is activated if you select a city previously inserted in the list and not preset, or it has passed the test.
* Remove - Deletes the current city from your list. This button can be activated if you select a city previously inserted in the list.
* Rename - Rename the current city. This button can be activated if you select a city previously inserted in the list.
* Import new cities... - This button allows you to import cities from the another list of cities with the extension *.zipcodes; you can select the city you want to import, by turning on the checkbox associated with it.
* Export your cities... - It allows you to save the cities in the specified file with the extension *.zipcodes. This button is activated if you have added and saved at least one city into the list.
* hourly forecast setting... - This button allows you to choose the contents of the hourly forecast report.
* Scale of temperature measurement: Use the radio button to select between Celsius (by default), Fahrenheit and Kelvin.
* Degrees shown as: Use the radio button to select between: Celsius `-` Fahrenheit `-` Kelvin (by default) C `-` F `-` K or Unspecified.
* Combo box: Weather Forecasts up to days: 1; you can choose between 1 to 3 (1 days by default)
* Combo box: API response language: English, en; you can choose the language of the weather conditions text.
* To perform the following actions, toggle the following checkboxes:
* Copy the weather report and weather forecast, including city details to clipboard; checkbox not checked (by default)
* Enable audio effects (only for the current weather conditions); this checkbox also allows you to manage the installation of sound effects; if the sound effects are installed and the checkbox is activated, the F5 key and the volume setting becomes available.
* There will also be available an additional checkbox: "Use only weather effects".
* You can change the overall volume or change the last heard sound effect and filter out the others sounds in your environment. Checkbox is not checked by default.
* Use only weather effects - This option is available if sound effects are enabled; if is enabled, allows to listen only weather effects such as rain, wind, thunder, etc., filtering out all environmental ones. (unchecked by default)
* Enable the reading of the hours in 24-hour format. - If this checkbox is unchecked, announces the time in 12-hour format for example, 12 AM `-` 12 PM. Checkbox is checked (by default)
* Enable help buttons in the settings window; checkbox checked (by default)
* Read wind information; checkbox not checked (by default). If this checkbox is enabled, you can also activate the following checkboxes:
* Add wind direction; indicates the provenance of the wind. Checkbox checked (by default)
* Add speed of the wind; indicates the speed in kilometers or miles per hour. Checkbox checked (by default)
* Add speed in meters per second of the wind; checkbox checked (by default)
* Add wind gust speed of the wind; checkbox checked (by default)
* Add perceived temperature; checkbox checked (by default)
* Read atmospherical information; checkbox not checked (by default). If enabled, you can also check the following checkboxes:
* Add humidity value; indicates the humidity in percent. Checkbox checked (by default)
* Add visibility value; indicate in kilometres or miles the distance visible. Checkbox checked (by default)
* Add atmospheric pressure value; indicates the atmospheric pressure in millibars or inches of mercury. If it's checked, enable an additional checkbox that allows you to indicate the pressure in millimeters of mercury. Checkbox checked (by default)
* Add cloudiness value; check box checked (by default)
* Add precipitation value; check box checked (by default)
* Add ultraviolet radiation value; check box checked (by default)
* Read astronomical information; indicates the time of sunrise and sunset and the time of moonrise and moonset. Checkbox not checked (by default)
* Use the comma to separate decimals; if enabled, uses the comma as a decimal separator, otherwise, use the point. Checkbox not checked (by default)
* Displays output in a window; if is activated this displays the forecast in a window. Checkbox not checked (by default)
* Check for upgrade; if is activated this alerts when there is an update of the addon. Checkbox checked (by default)
* Press the OK button to confirm the action or the Cancel button to cancel the action.
* If you have modified the cities list, by pressing "Cancel", you will be remembered and you can still save it. Note: your settings will be save in the file named:
* "Weather.ini": startup settings of Weather Plus.
* "Weather.volumes": custom audio volume levels, regardless of the overall volume.
* "Weather.zipcodes": list of cities with their zip code and definitions.
* "Weather.default": Your default city.
* "Weather_searchkey": search key saved.

--------------------------------------------------------------------------------
[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
