#-*- coding:utf-8 -*- 
#Weather Plus Addon for NVDA 
#Yahoo API Weather 
#Weather and 24 hour forecast 
#More forecast up to 9 days 
# Copyright (C) Adriano Barbieri 
#Email: adrianobarb@yahoo.it
# Released under GPL 2 
#This file is covered by the GNU General Public License. 
#See the file COPYING for more details. 
#Version 6.0 - python 3 compatible
import os,sys, winsound, config, globalVars, ssl, json
import globalPluginHandler, scriptHandler, languageHandler, addonHandler
import random, ui, gui, wx,wx.adv, re, calendar, math
from logHandler import log
from gui import guiHelper
from datetime import *
import time
from configobj import ConfigObj
from contextlib import closing
"""other temporary imported libraries in the code
api, winsound, zipfile, tempfile, shutil"""
#include the modules directory to the path
sys.path.append(os.path.dirname(__file__))
from oauth import Parse
from pybass  import *
try:
	#running in Python 3?
	_pyVersion = 3
	from urllib.request import urlopen
except ImportError:
	_pyVersion = 2
	from urllib2 import urlopen

del sys.path[-1]
addonHandler.initTranslation()

#global constants
if _pyVersion == 2:
	_addonDir = os.path.join(os.path.dirname(__file__), "..", "..").decode("mbcs")
else:
	_addonDir = os.path.join(os.path.dirname(__file__), "..", "..")
_curAddon = addonHandler.Addon(_addonDir)
_addonAuthor = _curAddon.manifest['author']
_addonSummary = _curAddon.manifest['summary']
_addonVersion = _curAddon.manifest['version']
_addonPage = _curAddon.manifest['url']
_zipCodes_path = os.path.join(globalVars.appArgs.configPath,"Weather.zipcodes")
_volumes_path = os.path.join(globalVars.appArgs.configPath,"Weather.volumes")
_samples_path = os.path.join(globalVars.appArgs.configPath,"Weather_samples")
_sounds_path = _addonDir.replace('..\..', "") + "\sounds"
_volume_dic = {'0%': 0, '10%': 0.1, '20%': 0.2, '30%': 0.3, '40%': 0.4, '50%': 0.5, '60%': 0.6, '70%': 0.7, '80%': 0.8, '90%': 0.9, '100%': 1}
_tempScale = [_("Fahrenheit"), _("Celsius"), _("Kelvin")]
_fields = ['city', 'region', 'country', 'country_acronym', 'timezone_id', 'lat', 'lon']
_nr = _("unknown")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _addonSummary
	def __init__(self):
	#variables definition
		self.note = [1, ''] #errors counter and woeId in use
		self.woeIdDialog = None #woeId error dialog opened
		self.openedTemporary = None #temporary city setting dialog opened
		self.OpenedSettings = None #settings dialog opened
		self.dom = "" #Yahoo weather API data corresponding to the woeID in use
		self.defaultZipCode = "" #preset woeId
		self.tempZipCode = "" #temporary woeId
		self.test = [""] * 2 #temporary woeID and current time
		self.defaultString = "" #the last search string
		self.randomizedSamples = [] #used by Play_samples()
		self.current_zipCode = "" #used by Play_samples()
		#load woeID list and definitions
		z, self.define_dic, self.details_dic = Shared().LoadZipCodes()
		#exclude the wrong lines
		self.zipCodesList = Shared().Check_content(z, "", False)
		del z
		#load sounds effects volumes
		global samplesvolumes_dic
		samplesvolumes_dic = Shared().Personal_volumes()
		#Reads the settings from weather.ini
		self.ReadConfig()
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.menu = gui.mainFrame.sysTrayIcon.menu.GetMenuItems()[0].GetSubMenu()
		self.WeatherMenu = wx.Menu()
		self.mainItem = self.menu.AppendSubMenu(self.WeatherMenu, _("Weather Plus &Settings"), _("Show configuration items."))
		self.setZipCodeItem = self.WeatherMenu.Append(wx.ID_ANY, _("Set and &manage your cities..."), _("Displays or allows to set the current cities from a list"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSetZipCodeDialog, self.setZipCodeItem)
		self.setTempZipCodeItem = self.WeatherMenu.Append(wx.ID_ANY, _("Set a &temporary city..."), _("Allows to set one temporary city from a list"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.setZipCodeDialog, self.setTempZipCodeItem)
		if not self.zipCodesList: self.setTempZipCodeItem.Enable(False)
		self.AboutItem = self.WeatherMenu.Append(wx.ID_ANY, _("&Documentation"), _("Opens the help file for the current language"))
		self.AboutItem.Enable(self.isDocFolder())
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, self.AboutItem)
		self.UpgradeAddonItem = self.WeatherMenu.Append(wx.ID_ANY, _("&Check for Upgrade..."), _("Notify if there is an upgraded version available"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onUpgrade, self.UpgradeAddonItem)
		#check if a new version is available
		if self.toUpgrade: self.onUpgrade()
		#delete the update file from the temporary folder
		self.Removeupdate()


	def terminate(self):
		super(GlobalPlugin, self).terminate()
		try:
			if wx.version().split(".")[0] >= "4":
				self.menu.Remove(self.mainItem)
			else:
				self.menu.RemoveItem(self.mainItem)
		except: pass #(wx.PyDeadObjectError, RuntimeError, AttributeError)
		#frees the memory allocated by the audio sample
		Shared().FreeHandle()


	def Removeupdate(self):
		"""Delete the update file from the temporary folder"""
		import tempfile
		if _pyVersion == 2:
			temp = tempfile.gettempdir().decode("mbcs")
		else: temp = tempfile.gettempdir()
		files = [
		"/".join((temp, "%s%s.nvda-addon" % (_addonSummary, _addonVersion.split()[0]))),
		"/".join((temp, "%s%s.nvda-addon" % ("weather plus", '5.0')))]
		for file in files:
			if os.path.isfile(file):
				os.remove(file)


	def onSetZipCodeDialog(self, evt):
		"""Opens the Weather Plus settings window"""
		#prevents multiple windows open at the same time
		self.OpenedSettings = True; self.EnableMenu(False)
		try:
			#set the correct encoding in the title
			if _pyVersion == 2:
				preset = self.defaultZipCode.decode("mbcs")
			else:
				preset = self.defaultZipCode
		except (UnicodeEncodeError, UnicodeDecodeError): preset = self.defaultZipCode
		#opens the Weather Plus settings window
		title = '%s - %s - (%s: %s)' % (_addonSummary, _("Settings"), _("Preset"), preset or _("None"))
		message = _("Enter a City, woeId or choose one from the list, if available.")
		saved_celsius = self.ReadConfig("c") or self.celsius
		Shared().Play_sound("winopen", 1)
		dlg = EnterDataDialog(gui.mainFrame, message =message, title = title,
		defaultZipCode = self.defaultZipCode,
		tempZipCode = self.tempZipCode,
		zipCode = self.zipCode,
		city = self.city,
		dom = self.dom,
		toAssign = self.toAssign,
		celsius =saved_celsius,
		toClip = self.toClip,
		toSample = self.toSample,
		toHelp = self.toHelp,
		toWind = self.toWind,
		toWinddir = self.toWinddir,
		toWindspeed = self.toWindspeed,
		toSpeedmeters = self.toSpeedmeters,
		toPerceived = self.toPerceived,
		toUmidity = self.toUmidity,
		toVisibility = self.toVisibility,
		toPressure = self.toPressure,
		toMmhgpressure = self.toMmhgpressure,
		toBarometric = self.toBarometric,
		toAtmosphere = self.toAtmosphere,
		toAstronomy = self.toAstronomy,
		scaleAs = self.scaleAs,
		to24Hours = self.to24Hours,
		defaultString = self.defaultString,
		define_dic = self.define_dic,
		details_dic = self.details_dic,
		forecast_days = self.forecast_days,
		toUpgrade = self.toUpgrade,
		toComma = self.toComma,
		toWeatherEffects = self.toWeatherEffects
		)
		self.dlg = dlg

		def callback2(result):
			if result == wx.ID_OK:
				#update the settings modified by the user
				(forecast_days,
				toUpgrade,
				zipCodesList,
				define_dic,
				details_dic,
				defaultZipCode,
				self.tempZipCode,
				modifiedList,
				celsius,
				scaleAs,
				toClip,
				toSample,
				toHelp,
				toWind,
				toSpeedmeters,
				toAtmosphere,
				toAstronomy,
				to24Hours,
				toPerceived,
				toUmidity,
				toVisibility,
				toPressure,
				toBarometric,
				toWinddir,
				toWindspeed,
				toMmhgpressure,
				toComma,
				toWeatherEffects,
				toAssign,
				self.defaultString) = dlg.GetValue()
				#save the configuration if some data were changed
				save = beep = False
				if modifiedList:
					#Save current cities list, area definitions and cities details
					self.define_dic = define_dic
					self.details_dic = details_dic
					if self.WriteList(zipCodesList):
						self.zipCodesList = zipCodesList
						beep = True

				global samplesvolumes_dic

				if celsius != saved_celsius: self.celsius = celsius; save = True
				if forecast_days != self.forecast_days: self.forecast_days = forecast_days; save = True
				if toClip != self.toClip: self.toClip = toClip; save = True
				if toSample != self.toSample: self.toSample = toSample; save = True
				if toHelp != self.toHelp: self.toHelp = toHelp; save = True
				if toWind != self.toWind: self.toWind = toWind; save = True
				if toWinddir != self.toWinddir: self.toWinddir = toWinddir; save = True
				if toWindspeed != self.toWindspeed: self.toWindspeed = toWindspeed; save = True
				if toSpeedmeters != self.toSpeedmeters: self.toSpeedmeters = toSpeedmeters; save = True
				if toPerceived != self.toPerceived: self.toPerceived = toPerceived; save = True
				if toUmidity != self.toUmidity: self.toUmidity = toUmidity; save = True
				if toVisibility != self.toVisibility: self.toVisibility = toVisibility; save = True
				if toPressure != self.toPressure: self.toPressure = toPressure; save = True
				if toMmhgpressure != self.toMmhgpressure: self.toMmhgpressure = toMmhgpressure; save = True
				if toBarometric != self.toBarometric: self.toBarometric = toBarometric; save = True
				if toAtmosphere != self.toAtmosphere: self.toAtmosphere = toAtmosphere; save = True
				if toAstronomy != self.toAstronomy: self.toAstronomy = toAstronomy; save = True
				if toComma != self.toComma: self.toComma = toComma; save = True
				if toWeatherEffects != self.toWeatherEffects: self.toWeatherEffects = toWeatherEffects; save = True
				if scaleAs != self.scaleAs: self.scaleAs = scaleAs; save = True
				if to24Hours != self.to24Hours: self.to24Hours = to24Hours; save = True
				if _volume != self.volume: self.volume = _volume; save = True
				if toAssign != self.toAssign: self.toAssign = toAssign; save = True
				if toUpgrade != self.toUpgrade: self.toUpgrade = toUpgrade; save = True
				if (any(map(lambda x: True, (k for k in samplesvolumes_dic if k not in self.samplesvolumes_dic)))\
				or sorted(samplesvolumes_dic.values()) != sorted(self.samplesvolumes_dic.values())):
					#save the individual volumes of the sound effects
					beep = Shared().Personal_volumes(samplesvolumes_dic, sav = True)
					self.samplesvolumes_dic = dict(samplesvolumes_dic)

				if defaultZipCode != self.defaultZipCode:
					self.ExtractData(defaultZipCode)
					self.defaultZipCode = defaultZipCode; save = True

				if save:
					beep = True
					if self.zipCode != Shared().GetZipCode(self.defaultZipCode):
						#preserve the  city in use
						backup = self.zipCode
						self.zipCode = Shared().GetZipCode(self.defaultZipCode)
						self.SaveConfig()
						self.zipCode = backup
					else: self.SaveConfig()

				if beep: Shared().Play_sound("save")
				#Set temporary Zip Code
				test = self.ExtractData(self.tempZipCode)
				if (not self.defaultZipCode or self.city != "Error" and not save and self.defaultZipCode != test) and not self.dontShowAgain:
					message = '%s "%s" %s "%s", %s\n%s' % (
					_("The woeID"), self.zipCode,
					_("assigned to"), self.city,
					_("has not been preset."),
					_("Will be used in temporary mode!"))
					dl = NoticeAgainDialog(gui.mainFrame, message = message, title = '%s %s' % (_addonSummary, _("Notice!")))
					if dl.ShowModal():
						dontShowAgain = dl.GetValue()
						if dontShowAgain != self.dontShowAgain:
							self.dontShowAgain = dontShowAgain
							#preserve the default zip code and celsius values
							backup_celsius = self.celsius
							self.celsius = self.ReadConfig('c')
							backup_zipCode = self.zipCode
							self.zipCode = Shared().GetZipCode(self.defaultZipCode)
							self.SaveConfig()
							#reassign the temporary zip code and celsius
							self.zipCode = backup_zipCode
							self.celsius = backup_celsius
							del backup_celsius, backup_zipCode

						dl.Destroy()

			else:
				#button cancell or eskape key
				n, n, zipCodesList, define_dic, details_dic, defaultZipCode, n, modifiedList, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, self.defaultString = dlg.GetValue()
				del n
				volume = self.volume
				samplesvolumes_dic = dict(self.samplesvolumes_dic)
				if modifiedList:
					#offers to save the list changed
					title = '%s %s' % (_addonSummary, _("Notice!"))
					message = '%s.\n%s' % (_("You have modified the list of your cities"), _("Do you want to save it?"))
					winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
					dl= wx.MessageBox(message, title, wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
					if dl == 2:
						#Save current list of cities
						self.defaultZipCode = defaultZipCode
						self.define_dic = define_dic
						self.details_dic = details_dic
						if self.WriteList(zipCodesList):
							self.zipCodesList = zipCodesList
							Shared().Play_sound(True)
			dlg.Destroy()
			Shared().Play_sound("winclose", 1)
			#enable the window for fast access of woeID and Weather setting menu
			del self.dlg
			self.OpenedSettings = False
			self.EnableMenu(True)

		gui.runScriptModalDialog(dlg, callback2)


	def EnableMenu(self, flag):
		"""Change status menu"""
		self.setZipCodeItem.Enable(flag)
		if not self.zipCodesList and flag is True:
			self.setTempZipCodeItem.Enable(False)
		else:
			self.setTempZipCodeItem.Enable(flag)
		self.UpgradeAddonItem.Enable(flag)


	def setZipCodeDialog(self, evt = None):
		"""Create a dialog box for select a temporary city"""
		def Find_index(cityList, city):
			"""Try to find index from list"""
			s = None
			if _pyVersion == 2:
				try:
					s = cityList.index(city.encode("mbcs"))
				except (AttributeError, IndexError, ValueError): pass
				if s == None:
					try:
						s = cityList.index(city.decode("mbcs"))
					except (AttributeError, IndexError, ValueError): pass

			if s == None:
				try:
					s = cityList.index(city)
				except (AttributeError, IndexError, ValueError): pass

			return s

		s = sel = 0
		zipCodesList = sorted([i for i in self.zipCodesList if not Shared().GetCoords(i)])
		if not zipCodesList:
			message = '%s\n%s' % (
			_("The cities on your list are not compatible with the Yahoo API!"),
			_("They have to be tested and validated, you can do it from the addon settings window."))
			title = '%s %s' % (_addonSummary, _("Notice!"))
			gui.mainFrame.prePopup()
			dialog = MyDialog(gui.mainFrame, message, title, zipCodesList = None, newVersion = '', setZipCodeItem = self.setZipCodeItem, setTempZipCodeItem = self.setTempZipCodeItem, UpgradeAddonItem = self.UpgradeAddonItem, buttons = None, simple = True)
			dialog.Show()
			gui.mainFrame.postPopup()
			return

		s = Find_index(zipCodesList, self.tempZipCode)
		if s == None:
			s = Find_index(zipCodesList, self.defaultZipCode)

		title = '%s - %s' % (_addonSummary, _("Setting up a temporary city"))
		message = '%s\n%s %d' % (
		Shared().Find_keys(),
		_("Cities List available:"),
		len(zipCodesList))
		choices=zipCodesList
		if s!= None: sel, t = s,0
		else: s, sel, t = 0, 0, -1
		Shared().Play_sound("winopen", 1)
		d = SelectDialog(gui.mainFrame, title = title, message = message, choices = choices, last = [s], sel = 0, defaultString = self.defaultString)
		self.openedTemporary = d
		self.EnableMenu(False)

		def callback(result):
			if result == wx.ID_OK:
				selection, self.defaultString = d.GetValue()
				self.tempZipCode = zipCodesList[selection]
				self.ExtractData(self.tempZipCode)
				if t == -1 or s != selection: Shared().Play_sound(True)

			else:
				n, self.defaultString = d.GetValue()

			d.Destroy()
			Shared().Play_sound("winclose", 1)
			self.EnableMenu(True)

		gui	.runScriptModalDialog(d, callback)


	def onAbout(self, evt):
		"""Open the folder of the local documentation"""
		try:
			os.startfile(self._docFolder)
		except WindowsError:
			ui.message (_("Documentation not available for the current language!"))


	def isDocFolder(self):
		"""Checks if there is documentation for the language set"""
		lang = languageHandler.getLanguage()
		pre = lang.split('_')[-1]
		availableLangs = languageHandler.getAvailableLanguages()
		langs = [i[-2].split('_')[-1] for i in availableLangs if i[-2].split('_')[-1].isupper()]
		if '_' in lang and pre not in langs: lang = lang.split('_')[0]
		if _pyVersion == 2:
			docFolder = os.path.dirname(__file__).decode("mbcs")
		else:
			docFolder = os.path.dirname(__file__)
		listDocs = os.listdir(docFolder.split("globalPlugins")[0]+"\\doc\\")
		if lang not in listDocs: lang = 'en'
		docFolder = docFolder.split("globalPlugins")[0]+"\\doc\\"+lang
		if os.listdir(docFolder) == []:
			docFolder = docFolder.split("doc")[0]+"\\doc\\"+'en'
		if os.path.exists(docFolder):
			self._docFolder = docFolder
			return True
		else:
			return False


	def onUpgrade(self, evt = None):
		"""Check for upgrade"""
		if globalVars.appArgs.secure: return #if run from systemConfig, does not check anyting

		def NoteDialog(message = "", title = "", newVersion = "", buttons = None):
			#call the upgrade dialog
			self.EnableMenu(False)
			gui.mainFrame.prePopup()
			dialog = MyDialog(gui.mainFrame, message, title, self.zipCodesList, newVersion, self.setZipCodeItem, self.setTempZipCodeItem, self.UpgradeAddonItem, buttons)
			dialog.Show()
			gui.mainFrame.postPopup()

		message, ask = "", False
		#title of the dialog box
		title = self.UpgradeAddonItem.GetItemLabelText().rstrip('.').replace("&", "")
		#read the version from addon page
		data = Shared().GetUrlData(_addonPage)
		if not data or data == "no connect":
			if evt:
				Shared().Play_sound("warn", 1)
				NoteDialog(_("Sorry, i can not receive data, verify that your internet connection is active, or try again later!"), title)

			return

		#assign addon base url
		if "_addonBaseUrl" not in globals():
			global _addonBaseUrl
			_addonBaseUrl = Shared().GetAddonBaseUrl(data)

		#search for new version string
		try:
			newVersion = re.search(r'Version\: (\d\.\d( - \d{1,2}\.\d{1,2}\.\d{4})*)', data).group(1)
		except: newVersion = ""
		#finally checks to see if a new version is available
		if newVersion and (float(newVersion.split()[0]) > float(_addonVersion.split()[0])):
			message = '%s %s %s %s\r\n%s: %s.\n%s' % (
			_addonSummary, _("version"), newVersion, _("is available."),
			_("Installed version"), _addonVersion,
			_("Do you want to download and install it?"))
			ask= view = True
		else:
			if evt: return NoteDialog(_("Sorry, at the time an update is not available."), title)

		if ask:
			return NoteDialog(message, title, newVersion, True)


	def ExtractData(self, v):
		"""Extract city and woeID from woeID string"""
		if _pyVersion >= 3 and "bytes" in str(type(v)): v = v.decode("mbcs")
		self.zipCode = Shared().GetZipCode(v)
		if _pyVersion >= 3: self.city = v[:-len(self.zipCode)-1]
		else:
			try:
				self.city = v[:-len(self.zipCode)-1].decode("mbcs")
			except (UnicodeEncodeError, UnicodeDecodeError): self.city = v[:-len(self.zipCode)-1]

		test= '%s %s' % (self.city.capitalize(), self.zipCode.upper())
		encoded_test = test
		if _pyVersion == 2: encoded_test = test.encode("mbcs")
		if self.zipCodesList and encoded_test in self.zipCodesList: return test
		else:
			#not in list
			city1, n = Shared().ParseEntry(self.zipCode)
			if city1 and city1 != self.city:
				#assign real name of the city
				self.city = city1
				test = '%s %s' % (self.city.capitalize(), self.zipCode.upper())

		return test


	def Play_Sample(self, condition = None, degrees = None):
		"""Plays the sound effect if found"""
		samples_dic = {
		'Bright': '*',
		'Sun': '*',
		'Sunny': '*',
		'Mostly Dry': '*',
		'Mostly Clear': '*',
		'Clearing': '*',
		'No Rain': '*',
		'Clear': '*',
		'Fair': '*',
		'Dry': '*',
		'Mild': '*',
		'Mostly Sunny': '*',
		'Overcast': '*',
		'Clouds': '*',
		'Cloudy': '*',
		'Partly Cloudy': '*',
		'Mostly Cloudy': '*',
		'Partly Bright': '*',
		'Mixed Rain And Snow': 'Rain and snow',
		'Mixed Rain and Snow': 'Rain and snow',
		'Mixed Rain And Sleet': 'Rain and snow',
		'Mixed Rain and Sleet': 'Rain and snow',
		'Mixed Snow And Sleet': 'Sleet',
		'Mixed Snow and Sleet': 'Sleet',
		'Snow Flurries': 'Sleet',
		'Severe Thunderstorms': 'Heavy rain',
		'Scattered Thunderstorms': 'Light rain',
		'Scattered Showers': 'Light rain',
		'Light Showers': 'Light rain',
		'Light Drizzle': 'Light rain',
		'Light Rain': 'Light rain',
		'Isolated Showers': 'Light rain',
		'Isolated Thunderstorms': 'Light rain',
		'Isolated Thundershowers': 'Light rain',
		'Frequent Showers': 'Rain',
		'Drizzle': 'Light rain',
		'Light Rain Shower': 'Light rain',
		'Rain Shower': 'Rain',
		'Rain': 'Rain',
		'Showers': 'Rain',
		'Shower': 'Rain',
		'Light Rain with Thunder': 'Continuous thunder',
		'Light Rain With Thunder': 'Continuous thunder',
		'Thundery Showers': 'Heavy rain',
		'Heavy Thunderstorm': 'Heavy rain',
		'Heavy Thunderstorms': 'Heavy rain',
		'Thundershowers': 'Heavy rain',
		'Thunderstorm': 'Continuous thunder',
		'Thunderstorms': 'Continuous thunder',
		'Few Showers': 'Heavy rain',
		'Heavy Showers': 'Heavy rain',
		'Showers Early': 'Heavy rain',
		'Heavy Rain': 'Heavy rain',
		'Storm': 'Hailstorm00',
		'Hail': 'Hailstorm00',
		'Freezing Rain': 'Hailstorm00',
		'Mixed Rain And Hail': 'Hailstorm00',
		'Mixed Rain and Hail': 'Hailstorm00',
		'Lightning': 'Continuous thunder',
		'Thunder': 'Continuous thunder',
		'Snow': 'Snow',
		'Heavy Snow': 'Snow storm',
		'Heavy Snow Shower': 'Snow storm',
		'Light Snow': 'Snow',
		'Rain and Snow': 'Rain and snow',
		'Rain And Snow': 'Rain and snow',
		'Light Snow Showers': 'Snow',
		'Light Snow Shower': 'Snow',
		'Scattered Snow Showers': 'Snow',
		'Snow Shower': 'Rain and snow',
		'Snow Showers': 'Rain and snow',
		'Snowdrift': 'Snow',
		'Snow Grains': 'Sleet',
		'Freezing Drizzle': 'Sleet',
		'Drifting Snow': 'Snow',
		'Blowing Snow': 'Snow storm',
		'Wintry Mix': 'Sleet',
		'Ice to Rain': 'Sleet',
		'Ice To Rain': 'Sleet',
		'Blizzard': 'Snow storm',
		'Sleet': 'Sleet',
		'Flurries': 'Snow storm',
		'Breezy': 'Wind00',
		'Blustery': 'Wind00',
		'Windy': 'Wind00',
		'Wind': 'Wind00',
		'Blowing Dust': 'Sand',
		'Widespread Dust': 'Sand',
		'Low Drifting Sand': 'Sand',
		'Sandstorm': 'Sand storm00',
		'Sand storm': 'Sand storm00',
		'Sand': 'Sand storm00',
		'Dust': 'Sand',
		'Ice': 'Ice',
		'Cold': 'Ice',
		'Hot': 'Hot',
		'Fog': 'Fog ambience',
		'Foggy': 'Fog ambience',
		'Shallow Fog': 'Fog ambience',
		'Mist': 'Fog ambience',
		'Haze': 'Fog ambience',
		'Unknown': 'Fog ambience',
		'Smoke': 'Smoke',
		'Smoky': 'Smoke',
		'Tornado': 'Tornado00',
		'Hurricane': 'Hurricane00'
		}

		v = p = sp_condition = define = ''
		current_season, p = self.Get_Season()
		if self.zipCode in self.define_dic: define = self.define_dic[self.zipCode]

		def No_double(samples_list):
			#try to avoid repeating the last sample played
			sample = _curSample
			if samples_list.count(samples_list[0]) == len(samples_list):
				#exit if the last 2 or more are the same
				self.randomizedSamples = []; return samples_list[0]

			#takes a samplle different from the last played
			while sample == _curSample:
				sample = random.choice(samples_list)
			return sample

		def SampleShuffle(sample_list):
			#mix list contents
			shuffled_list = []
			while len(sample_list) > 0:
				i = random.choice(sample_list)
				shuffled_list.append(i);
				sample_list.remove(i)
			return shuffled_list

		def RandomizeSamples(samples_list):
			#Delete alwais from the list the last sample played
			if (self.zipCode == self.current_zipCode) and len(self.randomizedSamples) > 1 and _curSample in self.randomizedSamples: self.randomizedSamples.remove(_curSample); return No_double(self.randomizedSamples)
			self.current_zipCode = self.zipCode
			#when the list is empty or zipCode is changed, is rebuilt
			self.randomizedSamples = SampleShuffle(samples_list)
			return No_double(self.randomizedSamples)

		def WindParse():
			#Delete alwais from the list the last sample played
			if (self.zipCode == self.current_zipCode) and len(self.randomizedSamples) > 1 and _curSample in self.randomizedSamples: self.randomizedSamples.remove(_curSample); return No_double(self.randomizedSamples)
			self.current_zipCode = self.zipCode
			#when the list is empty or zipCode is changed, is rebuilt
			if define == '3' or define == '4':
				# arctic zone or mountain zone
				self.randomizedSamples = ['Wind mountain canyon', 'Wind mountain storm, heavy howling whistling', 'Wind through big trees creaking', 'Wind whistling wind', 'Wind with metal banging', 'Wind00', 'Wind01', 'Wind02', 'Wind04', 'Wind05', 'Wind06']
			elif define == '1':
				#maritime area
				self.randomizedSamples = ['Sea storm00', 'Sea storm01', 'Sea storm02', 'Sea storm03', 'Sea storm04', 'Wind through big trees creaking', 'Wind with metal banging', 'Wind00', 'Wind01', 'Wind02', 'Sea storm00', 'Sea storm01', 'Sea storm02', 'Sea storm03', 'Sea storm04', 'Wind through big trees creaking', 'Wind with metal banging', 'Wind00', 'Wind01', 'Wind02']
			elif define == '2':
				#desert area
				self.randomizedSamples = ['Desert wind00', 'Dry gusty and whistling wind, weather', 'Dry gusty wind, leaves and sand blowing, weather', 'Wind heavy storm very strong gusts', 'Wind heavy storm very strong gusts sand and light debris', 'Wind storm wind', 'Wind00', 'Wind01', 'Wind02']
			else:
				#interland (default)
				self.randomizedSamples = ['Wind heavy gusting storm', 'Wind heavy storm very strong gusts', 'Wind strong metal rattles', 'Wind through big trees creaking', 'Wind violent storm very strong gusts', 'Wind with metal banging', 'Wind00', 'Wind01', 'Wind02', 'Wind03', 'Wind07', 'Windhowling and whistling']
			return No_double(self.randomizedSamples)

		if condition.endswith('in the Vicinity'):
			condition = condition[:-16]
		elif condition.endswith('Precipitation'):
			condition = condition[:-14]
		elif '/' in condition:
			sp_condition = condition.split('/')
			sp_condition[0] = sp_condition[0].rstrip(' ')
			sp_condition[-1] = sp_condition[-1].lstrip(' ')
			condition = sp_condition[0]

		if condition in samples_dic: v = samples_dic[condition]
		#special conditions
		if sp_condition:
			for i in range(1, len(sp_condition)):
				if sp_condition[i] in ['Wind', 'Windy'] and v in ['Snow', 'Sleet']:
					v = RandomizeSamples(['Snow and wind storm', 'Snow and wind00', 'Snow and wind01', v])
				elif (sp_condition[0] in ['Overcast', 'Clouds', 'Cloudy', 'Partly Cloudy', 'Mostly Cloudy', 'Partly Bright'] and sp_condition[i] in ['Wind', 'Windy'])\
				or (v == '*' and sp_condition[i] in ['Wind', 'Windy'])\
				or (v == 'Fog ambience' and sp_condition[i] in ['Wind', 'Windy']):
					v = WindParse()
				elif sp_condition[i] in ['Wind', 'Windy'] and v in ['Light rain', 'Rain', 'Heavy rain', 'Continuous thunder']:
					v = RandomizeSamples(['Rain and wind', 'Rain thunder heavy rain on skylight thunder rumble and wind', 'Rain thunder heavy rain with thunder rumble and wind', 'Rain, wind and thunder', v])

		elif v == 'Wind00':
			v = WindParse()
		elif v == 'Tornado00':
			v = random.choice([v, 'Tornado01'])
		elif v == 'Hurricane00':
			v = random.choice([v, 'Hurricane01'])
		elif v == 'Light rain':
			v = RandomizeSamples(['Rain light rain on grass with trickle from downspout', 'Rain light rain on roof', 'Rain thunder light rain with constant thunder', 'Rain thunder light rain with thunder rumble', 'Thunder rain thunder clap with light rain01', 'Thunder rain thunder clap with light rain02', 'Thunder rain thunder rumble with light rain01', 'Thunder rain thunder rumble with light rain02', 'Wet road00', 'Wet road01', 'Wet road02', v])
		elif v == 'Rain': 
			v = RandomizeSamples(['Rain auto interior of car_ medium rain hitting roof', 'Rain heavy rain on thick vegetation and wood', 'Rain heavy rain on vegetation and cement intensity varies', 'Thunder rain thunder clap with medium rain01', 'Thunder rain thunder clap with medium rain02', 'Thunder rain thunder rumble with medium rain01', 'Thunder rain thunder rumble with medium rain02', 'Wet road00', 'Wet road01', 'Wet road02', v])
		elif v == 'Heavy rain':
			v = RandomizeSamples(['Rain heavy rain on cement', 'Rain heavy rain on grass and roof', 'Rain heavy rain on hard surface', 'Rain heavy rain on water', 'Thunder rain thunder clap with heavy rain01', 'Thunder rain thunder clap with heavy rain02', 'Thunder rain thunder rumble with heavy rain', 'Wet road00', 'Wet road01', 'Wet road02', v])
		elif v == 'Continuous thunder':
			v = RandomizeSamples(['Thunder clap and rumble01', 'Thunder clap and rumble02', 'Thunder clap and rumble03', 'Thunder clap and rumble05', 'Wet road00', 'Wet road01', 'Wet road02', v])
		elif v == 'Hailstorm00': v = random.choice([v, 'Hailstorm01'])
		elif v == 'Sand storm00': v = random.choice([v, 'Sand storm01'])
		elif v == 'Rain and snow':
			v = RandomizeSamples(['Wet road00', 'Wet road01', 'Wet road02', v])
		elif v == 'Snow':
			play_list = ['Snowy road00', 'Snowy road01', 'Snowy road02', 'Snowy road03', v]
			if p != 'night': play_list += ['Footsteps in snow00', 'Footsteps in snow01', 'shovel snow', 'Snowy road and a shovel']
			v = RandomizeSamples(play_list)

		elif self.toWeatherEffects: return #use only weather effects
		elif v == 'Fog ambience' or v == 'Unknown':
			#Unknown, Mist, Fog, Foggy, Shallow Fog, Haze
			if define == '1':
				#sea fog
				v = RandomizeSamples(
				['Car09', 'Fog ambience', 'Car10', 'Fog ambience', 'Airplane00', 'Fog ambience', 'Airplane01', 'Airplane02', 'Fog ambience', 'Bus01', 'Bus02', 'Fog ambience', 'Foghorn00', 'Fog ambience', 'Foghorn01', 'Fog ambience', 'Level crossing',
				'Fog ambience', 'Foghorn02', 'Dogs00', 'Fog ambience', 'Dogs01', 'Fog ambience', 'Car00', 'Fog ambience', 'Car01', 'Fog ambience', 'Car02', 'Car03', 'Fog ambience', 'Train passing00', 'Fog ambience', 'Train passing01', 'Truck', 'Fog ambience', 'Tram, door opening'])
			elif define == '2':
				#desert fog
				v = RandomizeSamples(
				['Airplane00', 'Fog ambience', 'Airplane01', 'Airplane02', 'Fog ambience', 'Bus02', 'Fog ambience', 'Car06', 'Fog ambience', 'Car07', 'Fog ambience', 'Coyote00', 'Fog ambience', 'Coyote01', 'Fog ambience', 'Night dog01', 'Truck', 'Fog ambience', 'Tram, door opening'])
			elif define == '3':
				#arctic fog
				v = RandomizeSamples(['Airplane00', 'Fog ambience', 'Airplane01', 'Airplane02', 'Fog ambience', 'Foghorn00', 'Fog ambience', 'Wind playground wind', 'Foghorn01', 'Foghorn02', 'Wind playground wind', 'Fog ambience', 'Night dog00', 'Fog ambience', 'Night dog01'])
			else:
				#interland and mountain fog
				v = RandomizeSamples(
				['Car09', 'Fog ambience', 'Car10', 'Fog ambience', 'Airplane00', 'Fog ambience', 'Airplane01', 'Airplane02', 'Fog ambience', 'Bus00', 'Fog ambience', 'Bus01', 'Fog ambience', 'Tram, door opening',
				'Level crossing', 'Fog ambience', 'Night dog00', 'Fog ambience', 'night dog01', 'Fog ambience', 'Car00', 'Car01', 'Fog ambience', 'Car02', 'Car03', 'Fog ambience', 'Truck', 'Fog ambience', 'Dogs01', 'Train passing00', 'Fog ambience', 'Train passing01'])

		elif v == '*':
			#Drizzle end so on
			def LimitSeasonal(birds_date= None):
				#checking a determinate time of the season
				current_month, current_day = self.Get_Season(return_date = True)
				if birds_date:
					#restricts birds after the 10 november
					if current_month < 11\
					or current_month == 11 and current_day < 10: return current_season
					return "winter" #forced
				#adds winter sports from November 5 to march
				if current_month in [1, 2, 3, 12] or (current_month == 11 and current_day >= 5):
					return True
				return False

			#constants
			aircraft = ['Airplane00', 'Airplane01', 'Airplane02']
			bus = ['Bus00', 'Bus01', 'Bus02']
			cars = ['Car' + str(i).rjust(2, '0') for i in range(11)] + ['Car park on gravel']
			bathers = ['Bathers on the beach' + str(i).rjust(2, '0') for i in range(4)]
			bikers = ['Bike' + str(i).rjust(2, '0') for i in range(4)]\
			+['Motorcycle' + str(i).rjust(2,'0') for i in range(11)]
			sport_bikers =['Bike trial', 'Mountain bike00', 'Mountain bike01']
			birds = ['Birds' + str(i).rjust(2, '0') for i in range(5)]\
			+['Birds' + str(i).rjust(2, '0') for i in range(7,13)]\
			+['Birds' + str(i).rjust(2, '0') for i in range(14, 29)]\
			+['Robin', 'Solitary sparrow', 'Swallows']
			trains = ['Level crossing', 'Train passing00', 'Train passing01', 'Train passing02']
			bikers_dic = {
			"spring": bikers,
			"summer": bikers,
			"autumn": ['Motorcycle00', 'Motorcycle03', 'Motorcycle04']}
			sea_light = ['Sea light00', 'Sea light01', 'Sea light02', 'Sea light03', 'Sea light04', 'Sea medium03']
			seaShips = ['Motorboat' + str(i).rjust(2, '0') for i in range(7)]\
			+['Jet ski' + str(i).rjust(2, '0') for i in range(4)]\
			+['Ferryboat', 'Ship']
			seagulls = ['Seagulls00', 'Seagulls01', 'Seagulls02']
			sea_dic = {
			"autumn": ['Sea medium00', 'Sea medium01', 'Sea medium02', 'Sea medium04', 'Sea medium05'],
			"winter":['Sea heavy00', 'Sea heavy01', 'Sea heavy02', 'Sea heavy03'],
			"spring": sea_light,
			"summer": sea_light}
			birds_dic  = {
			"autumn": ['Birds08', 'Birds09', 'Birds10', 'Birds11', 'Birds12', 'Birds14', 'Birds15', 'Birds18', 'Magpie thief'],
			"winter": ['Birds10', 'Birds26']}
			winter_sports_dic = {False: [],
			True: ['Skier00', 'Skier01', 'Skier02', 'Skier03', 'Skier04', 'Skier05', 'Skier06', 'Snowboard', 'Cross country skiing00', 'Cross country skiing01', 'Cross country skiing02', 'Kids sledding', 'Toboggan passing by']}
			snow_machine_dic = {False: [],
			True: ['Snow guns in the night']}
			city_grounds = ["City ground" + str(i).rjust(2, '0') for i in range(15)] + ['Tram, door opening']
			city_grounds_night = ['City ground night00', 'City ground night01', 'City ground night02']
			desert_city_grounds = ["Desert city" + str(i).rjust(2, '0') for i in range(10)]
			arctic_samples = [
			'Albatross00', 'Albatross01', 'Arctic background00', 'Arctic background01', 'Arctic birds00',
							'Arctic birds01', 'Arctic birds02', 'Arctic birds03', 'Arctic birds04', 'Arctic birds05', 'Arctic whale', 'Arctic wolfs00', 'Arctic wolfs01', 'Footsteps in snow00', 'Footsteps in snow01',
							'Helicopter00', 'Helicopter01', 'Sea lions00', 'Sea lions01', 'Seals', 'Sled dogs00', 'Sled dogs01',
							'Snowmobile00', 'Snowmobile01', 'Snowmobile02', 'Sleet'] + aircraft
			arctic_night_samples = [
			'Airplane00', 'Airplane02', 'Arctic wolfs00', 'Arctic wolfs01', 'Night dog00', 'Night dog01']\
			+ ['Arctic background00', 'Arctic background01', 'Wind playground wind'] * 3
			desert_night_samples = [
			'Airplane00', 'Airplane02', 'Bus02', 'Car04', 'Car05', 'Car06', 'Car07', 'Car08', 'Coyote00', 'Coyote01',
			'Kite', 'Night dog00', 'Night dog01', 'Truck']\
			+['Desert, night crickets', 'Desert, night owl, crickets02'] * 6 + ['Desert, night owl, crickets, dog'] * 3\
			+['City ground night00', 'City ground night01'] * 3 + ['Desert breeze'] * 6\
			+ ['Campfire & crickets'] * 3

			def seasonalElements():
				#Adds bathers, cicadas if temperature exceed respectively 24 and 22 degrees celsius
				bathers_dic = {0: 76, 1: 24, 2: 297}
				cicadas_dic = {0: 72, 1: 22, 2: 295}
				samples_list = []
				cicada_beach = []
				dt = int(degrees)
				if dt > bathers_dic[self.celsius] and define == "1":
					#adds bathers on the beach
					samples_list = ['Bathers on the beach00', 'Bathers on the beach01', 'Bathers on the beach02', 'Bathers on the beach03']
				if dt > cicadas_dic[self.celsius]:
					#adds the cicadas
					if define == '1': cicada_beach = ['Cicada beach']
					samples_list += [
					'Cicada00', 'Cicada01', 'Cicada02', 'Cicada03', 'Cicada04', 'Cicada05', 'Cicada06',
					'Cicada07', 'Cicada08', 'Cicada09', 'Cicada10', 'Cicada11', 'Cicada12',
					'Cicada13', 'Cicada14', 'Cicada15', 'Cicada16', 'Cicada17', 'Cicada18']\
					+cicada_beach

				return samples_list

		# parsing according to the seasons
			if current_season in ['winter', 'autumn']:
				if p == 'morning' or p == 'evening':
					if define == '1':
						#sea samples, winter and autumn
						v = RandomizeSamples(
						['Dogs00', 'Dogs01', 'Ferryboat', 'Helicopter00', 'Motorboat02', 'Motorboat04', 'Ship', 'Truck']\
						+city_grounds + sea_dic[current_season] * 5 + bus\
						+aircraft + cars + birds_dic[current_season] + trains)
					elif define == '2':
						#desert samples, winter and autumn
						cars2 = cars; [cars2.remove(i) for i in ['Car00', 'Car09', 'Car10', 'Car park on gravel'] if i in cars2]
						v = RandomizeSamples(
						['Bedouins00', 'Bedouins01', 'Bedouins02', 'Bedouins03', 'Birds11', 'Birds12', 'Birds26', 'Birds27',
						'Caravan00', 'Caravan01', 'Caravan02', 'Caravan03', 'Caravan04', 'Caravan05', 'Coyote00', 'Coyote01',
						'Desert birds00', 'Desert birds01', 'Desert birds02', 'Desert birds03', 'Desert wind01', 'Desert wind02', 'Falcon', 'Footsteps in sand', 'Helicopter00',
						'Helicopter01', 'Iena', 'Market in the desert', 'Motorcycle00', 'Motorcycle02', 'Motorcycle03', 'Motorcycle05',
						'Bus02', 'Camels00', 'Truck', 'Vulture00', 'Vulture01', 'Wigeon']\
						+aircraft + ['Wind playground wind'] * 2 + trains\
						+['Desert breeze'] * 2 + cars2\
						+desert_city_grounds)
					elif define == '3':
						#arctic samples, winter and autumn
						v = RandomizeSamples(arctic_samples)
					elif define == '4':
						#mountain samples, winter and autumn
						city_grounds2 = city_grounds
						sheeps = ['Sheep and car', 'Sheep and pawn']
						sport_bikers2 = sport_bikers + ['Motorcycle00', 'Motorcycle07']
						mountain_creek = ['Mountain creek00', 'Mountain creek01']
						if current_season == 'winter':
							[city_grounds2.remove(i) for i in ['Motorcycle02', 'Motorcycle04', 'City ground06', 'City ground07', 'City ground08', 'City ground09'] if i in city_grounds2]
							mountain_creek = ['Mountain creek00']; sheeps = []; sport_bikers2 = []
						v = RandomizeSamples(
				['Birds11', 'Birds16', 'Birds26', 'Dogs00', 'Dogs01', 'Eagle00',
				'Tractor', 'Truck', 'Helicopter00']\
				+trains + bus + sport_bikers2\
				+winter_sports_dic[LimitSeasonal()] + sheeps + mountain_creek * 2\
				+aircraft + city_grounds2)
					else:
						#interland samples, winter and autumn
						tractor = ['Tractor']; city_grounds2 = city_grounds
						bikers2 = ['Motorcycle00', 'Motorcycle07']
						if current_season == 'winter':
							[city_grounds2.remove(i) for i in ['Motorcycle02', 'Motorcycle04', 'City ground07', 'City ground08', 'City ground09'] if i in city_grounds2]
							tractor = []; bikers2 = []
						v = RandomizeSamples(
						['Helicopter00', 'Truck']\
						+aircraft + bus + city_grounds2 + birds_dic[LimitSeasonal(birds_date = True)]\
						+cars + tractor + trains + bikers2)
				elif p == 'night':
					if define == '1':
						#sea night samples, winter and autumn
						sea = sea_dic[current_season]
						[sea.remove(i) for i in sea if i in ['Sea light00', 'Sea medium03']]
						volatile_dic = {"autumn": ['Desert, night owl, crickets01', 'Birds06', 'Birds13'], "winter": []}
						v = RandomizeSamples(
						['Airplane00', 'Airplane02', 'Bus02', 'Car04', 'Car05', 'Car06', 'Car08',
						'Car09', 'Car10', 'Night dog00', 'Night dog01', 'Truck']\
						+sea * 4 + ['Winter night'] * 6 + volatile_dic[current_season]\
						+city_grounds_night * 3)
					elif define == '2':
						#desert night samples, winter and autumn
						v = RandomizeSamples(
						['Airplane00', 'Airplane02', 'Bus02', 'Car04', 'Car05', 'Car06', 'Car07', 'Car08', 'Coyote00', 'Coyote01',
						'Kite', 'Night dog00', 'Night dog01', 'Truck']\
						+['Desert, night crickets'] * 9 + ['Desert, night owl, crickets, dog'] * 3\
						+['Desert, night owl, crickets01', 'Desert, night owl, crickets02'] * 3 + ['Desert breeze'] * 6\
						+['Campfire & crickets'] * 3)
					elif define == '3':
						#arctic night samples , winter and autumn
						v = RandomizeSamples(arctic_night_samples) 
					elif define == '4':
						#mountain night samples, winter and autumn
						volatile_dic = {"autumn": ['Eagle00', 'Eagle01', 'Falcon', 'Kite'], "winter": []}
						v = RandomizeSamples(
						['Airplane00', 'Airplane02', 'Bus02', 'Car01', 'Car03', 'Car04', 'Car05', 'Car06', 'Car07',
						'Car08', 'Night dog00', 'Night dog01', 'Truck']\
				+['Winter night'] * 8 + ['Wind playground wind'] * 8\
				+volatile_dic[current_season] + snow_machine_dic[LimitSeasonal()] * 6\
				+city_grounds_night * 4)
					else:
						#interland night samples, winter and autumnn
						v = RandomizeSamples(
						['Airplane00', 'Airplane02', 'Bus02',
				'Car01', 'Car03', 'Car04', 'Car05', 'Car06', 'Car07',
				'Car08', 'Night dog00', 'Night dog01', 'Truck']\
				+['Wind playground wind'] * 9 + ['Winter night'] * 9\
				+city_grounds_night * 6)
			elif current_season in ['summer', 'spring']:
				if p == 'morning' or p == 'evening':
					if define == '1':
						#sea samples, summer and spring
						birds2 = birds; [birds2.remove(i) for i in birds2 if i in ['Birds16']]
						v = RandomizeSamples(
						['Dogs00', 'Dogs01', 'Helicopter00', 'Helicopter01', 'Truck', 'Wigeon', 'Swimming pool']\
						+city_grounds + sea_dic[current_season] * 6 + trains\
						+aircraft + seaShips + ['Blackbird'] * 3\
						+cars + bikers_dic[current_season] + birds2\
						+seagulls * 2\
						+seasonalElements() + bus)
					elif define == '2':
						#desert samples, summer and spring
						cars2 = cars; [cars2.remove(i) for i in ['Car00', 'Car09', 'Car10', 'Car park on gravel'] if i in cars2]
						v = RandomizeSamples(
						['Bedouins00', 'Bedouins01', 'Bedouins02', 'Bedouins03', 'Birds11',
						'Birds12', 'Birds26', 'Birds27', 'Bus02', 'Camels00', 'Caravan00', 'Caravan01', 'Caravan02',
						'Caravan03', 'Caravan04', 'Caravan05', 'Coyote00', 'Coyote01', 'Desert birds00', 'Desert birds01', 'Desert birds02',
						'Desert birds03', 'Desert wind01', 'Desert wind02', 'Falcon', 'Footsteps in sand', 'Helicopter00', 'Helicopter01', 'Iena', 'Market in the desert',
						'Motorcycle00', 'Motorcycle02', 'Motorcycle03', 'Motorcycle05', 'Truck', 'Vulture00', 'Vulture01', 'Wigeon']\
						+aircraft + ['Wind playground wind'] * 3 + trains\
						+['Desert breeze'] * 4 + cars2 + ['Swimming pool'] * 2\
						+desert_city_grounds)
					elif define == '3':
						#arctic samples, summer and spring
						v = RandomizeSamples(arctic_samples + ['Polar bear'] *2)
					elif define == '4':
						#mountain samples, summer and spring
						birds2 = birds
						[birds2.remove(i) for i in ['Birds00', 'Birds01', 'Birds02', 'Birds03', 'Birds04', 'Birds18'] if i in birds2]
						v = RandomizeSamples(
						['Cow bells', 'Cows in the pasture01', 'Cows in the pasture02', 'Eagle00', 'Eagle01', 'Falcon',
						'Helicopter00', 'Helicopter01', 'Magpie thief', 'Mountain forest ambience',
						'Robin', 'Sheep01', 'Sheep and car', 'Sheep and pawn',
						'Sheep in the pasture', 'Solitary sparrow', 'Tractor', 'Truck']\
						+aircraft + city_grounds + ['Blackbird'] * 3 + trains\
						+birds2 + cars + bikers + bus + ['Mountain creek00', 'Mountain creek01'] * 3\
						+['Swimming pool'] * 2 + sport_bikers)
					else:
						#interland samples, summer and spring
						v = RandomizeSamples(
						['Birds05', 'Dogs00', 'Dogs01', 'Helicopter00', 'Helicopter01', 'Magpie thief',
						'Sheep00', 'Sheep01', 'Sheep in the pasture', 'Tractor', 'Truck', 'Swimming pool']\
						+aircraft + bus + city_grounds + bikers\
						+cars + birds + ['Blackbird'] * 3\
				+seasonalElements() + trains)
				elif p == 'night':
					if define == '1':
						#sea night, summer and spring
						sea = sea_dic[current_season]
						[sea.remove(i) for i in sea if i in ['Sea light00', 'Sea medium03']]
						v= RandomizeSamples(
						['Airplane00', 'Airplane02', 'Birds06', 'Birds13', 'Car04', 'Car05', 'Car09', 'Car10',
						'Falcon', 'Kite', 'Motorcycle03', 'Night cats', 'Night dog00', 'Night dog01', 'Truck']\
						+['Night crickets'] * 10 + ['Winter night'] * 6\
						+['Frogs'] * 3 + sea * 5\
						+city_grounds_night * 3)
					elif define == '2':
						#desert night samples, summer and spring
						v = RandomizeSamples(desert_night_samples)
					elif define == '3':
						#arctic night samples, summer and spring
						v = RandomizeSamples(arctic_night_samples)
					elif define == '4':
						#mountain night samples, summer and spring
						night_elements_dic = {'summer': ['Night crickets'] * 10 + ['Frogs'] * 3,
						'spring': ['Night crickets'] * 3}
						v = RandomizeSamples(
						['Airplane00', 'Airplane02', 'Birds06', 'Birds13', 'Bus02', 'Car04', 'Car05', 'Car09', 'Car10',
						'Eagle00', 'Eagle01', 'Falcon', 'Kite', 'Night cats', 'Night dog00', 'Night dog01', 'Truck']\
						+['Winter night'] * 6 + night_elements_dic[current_season]\
						+city_grounds_night * 3)
					else:
						#interland night samples, summer and spring
						v = RandomizeSamples(
						['Airplane00', 'Airplane02', 'Birds06', 'Birds13', 'Bus02', 'Car04', 'Car05', 'Car09', 'Car10',
						'Falcon', 'Kite', 'Night cats', 'Night dog00', 'Night dog01', 'Truck']\
						+['Winter night'] * 6 + ['Night crickets'] * 10\
						+['Frogs'] * 3 + city_grounds_night * 3)

		#create file path to play sample.
		filePath = _samples_path+"\\"
		try:
			if not v: v = samples_dic[condition]
		except KeyError: pass
		if v:
			ext = ".mp3"
			filename = '%s%s%s' % (filePath, v, ext)
			if os.path.isfile(filename):
				global _curSample, _handle
				_curSample = v
				if _curSample in samplesvolumes_dic:
					#use the volume assigned to the sound effect
					playVol = samplesvolumes_dic[_curSample]
					#adjust sound effect volume proportioning to total volume
					playVol = Shared(). AdjustVol(playVol)
				else:
					#use the overall volume
					playVol = _volume

				Shared().FreeHandle() #cleanup previous stream into memory
				try:
					BASS_Init(-1, 44100, 0, 0, 0)
					_handle = BASS_StreamCreateFile(False, b'%s' % filename.encode("mbcs"), 0, 0, 0)
					BASS_ChannelPlay(_handle, False)
					BASS_ChannelSetAttribute(_handle, BASS_ATTRIB_VOL, _volume_dic[playVol]) #set volume (0 = mute, 1 = full)
				except Exception as e:
					Shared().SendToLog(e)

			else:
				#sample not found, notify and disable audio check box
				self.toSample = 0
				message = '"%s%s" %s\n%s %s.\n%s %s.' % (
				v, ext, _("not found!"),
				_("You need to upgrade the sound effects by reactivating the appropriate option from the settings of"),
				_addonSummary,
				_("But if these are already updated, then you need to update"), _addonSummary)
				wx.CallAfter(gui.messageBox, message, _addonSummary, wx.ICON_EXCLAMATION)
				#Try to disable the audio controls in the Settings window
				if self.OpenedSettings:
					self.dlg.message1.SetLabel(self.dlg.hotkeys[-1])
					self.dlg.cbt_toSample.SetValue(False)
					self.dlg.ch_vol.Enable(False)
					self.dlg.cb_vol.Enable(False)


	def Get_Season(self, return_date=None):
		"""Return season and part of the day"""
		current_month = datetime.today().date().month
		current_day = datetime.today().date().day
		if return_date: return current_month, current_day
		current_hour = self.current_hour
		if current_hour is None:
			current_hour = datetime.today().time().hour

		#I decided to divide the day into 3 parts, morning and evening at the moment are equivalent
		day_parts = ['morning', 'evening', 'night']
		day_time = [
		[5, 6, 7, 8, 9, 10, 11, 12], #Morning
		[13, 14, 15, 16, 17, 18, 19, 20], #evening
		[21, 22, 23, 00, 1, 2, 3, 4]] #night

		seasons_names = ['winter', 'spring', 'summer', 'autumn']
		''' [start day of the first mounth range, [mounth range], end day of the last mounth range]'''
		seasons = [
		[21, [12, 1, 2, 3],20], #winter
		[21, [3, 4, 5, 6], 20], #spring
		[21, [6, 7, 8, 9], 23], #summer
		[24, [9, 10, 11, 12], 20]] #autumn
		#Find the current season
		for current_season in range(len(seasons)):
			if current_month in seasons[current_season][1]:
				if (current_day >= seasons[current_season][0] and current_month == seasons[current_season][1][0]) \
				or (current_day <= seasons[current_season][2] and current_month == seasons[current_season][1][-1]): break
				elif current_month == seasons[current_season][1][1] \
				or current_month == seasons[current_season][1][2]: break

		#Find the part of the day
		for p in range(len(day_time)):
			if current_hour in day_time[p]: break
		return seasons_names[current_season], day_parts[p]


	def ReadConfig(self, singleRead = None):
		"""Read configuration set from Weather.ini"""
		#Default values
		if not singleRead:
			self.city = self.defaultZipCode = self.tempZipCode = self.zipCode = ""
			#radio buttons values
			self.celsius = 1 #Fahrenheit, Celsius, Kelvin
			self.scaleAs = 0 #indication degrees: Celsius Fahrenheit Kelvin - C f k - do not specify
			#check boxes
			self.toClip= False #copy into the clipboard
			self.toSample = False #use sound effects
			self.toWeatherEffects = False #uses only weather effects
			self.toHelp = True #help on the buttons
			self.toWind = False #add wind values
			self.toWinddir = True #add wind direction
			self.toWindspeed = True #add wind speed
			self.toSpeedmeters = True #add speed in meters per second
			self.toPerceived = True #add perceived temperature
			self.toUmidity = True #add umidity value
			self.toVisibility = True #add visibility value
			self.toPressure = True #add pressure value
			self.toMmhgpressure = False #indicates pressure in mmHg
			self.toBarometric = True #add barometric values
			self.toAtmosphere = False #add atmosphere values
			self.toAstronomy = False #add astronomy values
			self.to24Hours = True #use 24 hours format
			self.dontShowAgain = False #check box no longer display this message
			self.toComma = False #use the comma as decimal separator
			self.toUpgrade = True #check for upgrades
			#total days forecast
			self.forecast_days = "3" # forecast days (1 - 10)min 1, max 10
			#volume controls
			self.toAssign = 0 #general audio volume - 1 = current audio volume
			self.samplesvolumes_dic = dict(samplesvolumes_dic)#set volume from percentage to float (0, 0.1, 0.2, etc. up to 1)
			global _handle, _curSample
			self.handle = _handle = None #sound allocated in memory
			self.curSample = _curSample = None #name of audio effect in memory
			self.volume = "60%" #default volume of the current sample

		config_weather = os.path.join(globalVars.appArgs.configPath,"Weather.ini")
		if os.path.isfile(config_weather):
			config = ConfigObj(config_weather)
			config.bools = {'True': True, 'False': False, 'true': True, 'false': False, '': False}
			try:
				if singleRead == "c":
					return int(config['Weather Settings']['Celsius'])

				self.celsius = int(config['Weather Settings']['Celsius'])
				self.zipCode = config['Weather Settings']['Zip Code']
				self.toClip = config.bools[config['Weather Settings']['To Clipboard']]
				self.toSample = config.bools[config['Weather Settings']['Audio Effects']]
				self.toHelp = config.bools[config['Weather Settings']['Help Buttons']]
				self.toWind = config.bools[config['Weather Settings']['Add wind']]
				self.toAtmosphere = config.bools[config['Weather Settings']['Add atmosphere']]
				self.toAstronomy = config.bools[config['Weather Settings']['Add astronomy']]
				self.scaleAs = int(str(config['Weather Settings']['Scale as']))
				self.to24Hours = config.bools[config['Weather Settings']['24 hours clock']]
				self.toAssign = int(config['Weather Settings']['Assigned volume'])
				self.volume = '%s' % config['Weather Settings']['Samples volume']
				self.forecast_days = config['Weather Settings']['Forecast max days']
				self.toUpgrade = config.bools[config['Weather Settings']['Check for upgrade']]
				self.toSpeedmeters = config.bools[config['Weather Settings']['Addspeedtometers']]
				self.toPerceived = config.bools[config['Weather Settings']['Addperceivedtemperature']]
				self.toUmidity = config.bools[config['Weather Settings']['Addumidity']]
				self.toVisibility = config.bools[config['Weather Settings']['Addvisibility']]
				self.toPressure = config.bools[config['Weather Settings']['Addpressure']]
				self.toBarometric = config.bools[config['Weather Settings']['Addbarometricstate']]
				self.toWinddir = config.bools[config['Weather Settings']['Addwinddirection']]
				self.toWindspeed = config.bools[config['Weather Settings']['Addwindspeed']]
				self.toMmhgpressure = config.bools[config['Weather Settings']['Indicate pressure to mmHg']]
				self.toComma = config.bools[config['Weather Settings']['Use a comma as separator']]
				self.toWeatherEffects = config.bools[config['Weather Settings']['Use only weather effects']]
				self.dontShowAgain = config.bools[config['Weather Settings']['Dont show again']]
			except IOError:
				Shared().Play_sound("warn", 1)
				return ui.message(_("I can not load the settings!"))
			except KeyError: pass
			#*global _volume
			#*_volume = self.volume
			if not self.zipCode or self.zipCode.isspace(): return
			if not self.zipCodesList:
				#if does not exist the list, picks the name of the city from woeID
				city, zipCode = Shared().ParseEntry(self.zipCode)
				if city and city != "no connect":
					if _pyVersion >= 3:
						self.tempZipCode = '%s %s' % (city.capitalize(),str(zipCode).upper())
					else:
						self.city = city.decode("mbcs"); self.tempZipCode = '%s %s' % (city.capitalize(),str(zipCode).upper())

			else:
				#search in list
				city = self.FindCity(self.zipCode)
				if city:
					if _pyVersion == 2:
						self.defaultZipCode = self.tempZipCode= city =city.decode("mbcs")
					else:
						self.defaultZipCode = self.tempZipCode= city

					self.city = city[:city.find(self.zipCode)-1] #takes the name of city and state

		global _volume
		_volume = self.volume


	def SaveConfig(self):
		"""Save datas into configuration Weather.ini"""
		config = ConfigObj()
		config_weather = os.path.join(globalVars.appArgs.configPath,"Weather.ini")
		config.filename = config_weather
		config ["Weather Settings"] = {
		"Celsius": self.celsius,
		"Zip Code": self.zipCode,
		"To Clipboard": self.toClip,
		"Audio Effects": self.toSample,
		"Help Buttons": self.toHelp,
		"Add wind": self.toWind,
		"Add atmosphere": self.toAtmosphere,
		"Add astronomy": self.toAstronomy,
		"Scale as": self.scaleAs,
		"24 hours clock": self.to24Hours,
		"Assigned volume": self.toAssign,
		"Samples volume": self.volume,
		"Forecast max days": self.forecast_days,
		"Check for upgrade": self.toUpgrade,
		"Addwinddirection": self.toWinddir,
		"Addwindspeed": self.toWindspeed,
		"Addspeedtometers": self.toSpeedmeters,
		"Addperceivedtemperature": self.toPerceived,
		"Addumidity": self.toUmidity,
		"Addvisibility": self.toVisibility,
		"Addpressure": self.toPressure,
		"Addbarometricstate": self.toBarometric,
		"Indicate pressure to mmHg": self.toMmhgpressure,
		"Use a comma as separator": self.toComma,
		"Use only weather effects": self.toWeatherEffects,
		"Dont show again": self.dontShowAgain
		}
		try:
			config.write()
		except IOError:
			Shared().Play_sound("warn", 1)
			return ui.message(_("I can not save the settings!"))


	def WriteList(self, zipCodesList):
		"""Save woeID list """
		try:
			with open(_zipCodes_path, 'w') as file:
				file.write("[cities list]\n")
				for r in sorted(zipCodesList):
					splitr = r.split()
					if len(splitr) == 5 and Shared().GetCoords(r):
						#apixu city
						r = '%s %s\t%s\t%s\t%s\n' % (splitr[0], splitr[1], splitr[2], splitr[3], splitr[4])
					else:
						#Yahoo citi and zipcode
						r = '%s\t%s\n' % (r[:-len(r.split()[-1])-1], r.split()[-1])

					try:
						file.write(r)
					except (UnicodeDecodeError, UnicodeEncodeError):
						file.write('%s, %s\t%s\n' % (_("invalid name").capitalize(), r.split()[1].lower(), r.split()[-1]))

			#adds cities definitions
			with open(_zipCodes_path, 'a') as file:
				file.write("\n[Cities Definitions]\n")
				for i in self.define_dic:
					r = '#%s\t%s\n' % (i, self.define_dic[i])
					file.write(r)

			#adds cities details
			with open(_zipCodes_path, 'a') as file:
				file.write("\n[Cities Details]")
				for i in self.details_dic:
					r = '\n%s' % i #add zip code number (record name)
					for f in _fields:
						#adds all the fields to record
						r += '\t%s' % self.details_dic[i][f]

					try:
						file.write(r)
					except (UnicodeEncodeError, UnicodeDecodeError):
						r = '\n%s\tfail\t\t\t\t\t\t' % i
						file.write(r)

		except IOError:
			Shared().WriteError(_addonSummary)
			return False
		else: return True


	def FindCity(self, zipCode):
		"""Find the name of the 	city from woeID list"""
		lzc = [x.split()[-1] for x in self.zipCodesList]
		try:
			i = False
			i = lzc.index(zipCode)
		except (IndexError, ValueError): return i
		return self.zipCodesList[i]


	def getWeather(self, zip_code, forecast = False):
		"""Main getWeather function gets weather from Yahoo API"""
		if zip_code != "" and not zip_code.isspace():
			mess = ""
			wait_delay = 10 #it's necessary to update after at least 10 minutes to limit frequent API calls, please don't change it!
			if self.dom == "no connect" or self.dom and (self.tempZipCode != self.test[0]) or not self.dom or (datetime.now() - self.test[-1]).seconds/60 >= wait_delay:
				#but refresh dom if the city are changed or if the waiting time is finished
				self.dom, mess = self.Open_Dom(zip_code)
				self.test[0] = self.tempZipCode
				self.test[-1] = datetime.now()

			if not self.dom or self.dom in ["not authorized", "no connect"]: self.dom = None; return
			try:
				self.dom['current_observation']['pubDate']
			except (KeyError, TypeError): self.dom = None; return self.ZipCodeError()
			if mess:
				#notify last build date failed
				Shared().Play_sound("messagefailure", 1)
				ui.message(mess)

			#Indication of the degrees
			scale_as = _tempScale[self.celsius]
			if self.scaleAs == 1: scale_as = scale_as[0]
			elif self.scaleAs == 2: scale_as = ""
			if not forecast:
				condition = self.dom['current_observation']['condition']['text']
				# to limit API calls, use the default parameter u = f for Fahrenheit
				#for celsius and kelvin I convert them to metric
				temperature =self.dom['current_observation']['condition']['temperature']
				wind_chill = self.dom['current_observation']['wind']['chill']
				win = self.dom['current_observation']['wind']['speed']
				wind_speed = self.IntClean(win)
				if self.toComma: wind_speed = wind_speed.replace('.', ',')
				unit_speed = "mi/h"
				unit_distance = _("miles")
				pre = self.dom['current_observation']['atmosphere']['pressure']
				if self.toMmhgpressure == True:
					pressure = self.Pressure_convert(pre, mmHg = True) #takes the value in mmHg
					unit_pressure = _("millimeters of mercury")
				else:
					unit_pressure = _("inches of mercury")

				pressure = self.IntClean(pre)
				if self.toComma: pressure = pressure.replace('.', ',')
				vis = self.dom['current_observation']['atmosphere']['visibility']
				visibility = self.IntClean(vis)
				if self.toComma: visibility = visibility.replace('.', ',')
				sptm = self.Speedtometers(win, convert = False, meters = True) #takes speed in meters per second
				if self.celsius != 0:
					#only for Celsius and Kelvin
					temperature = self.Temperature_convert(temperature, self.celsius)
					wind_chill = self.Temperature_convert(wind_chill, self.celsius)
					unit_speed = "km/h"
					unit_distance = _("kilometers")
					if not self.toMmhgpressure:
						unit_pressure = _("millibars")
						pressure = self.Pressure_convert(pre)

					wind_speed = self.Speedtometers(win)
					visibility = self.Speedtometers(vis)

				if not self.toSpeedmeters: sptm = ""
				weatherReport = '%s %s %s %s, %s.' % \
				(_("the weather report is currently"),
				temperature, _("degrees"),
				scale_as,
				condition
				)
				weatherReport = weatherReport.replace(" , ", ", ")
				if self.toWind is True:
					#adds wind information to the string 
					winddirstring = _("The wind direction is from")
					winddirvalue = self.GetCardinalDirection('%s' % self.dom['current_observation']['wind']['direction']) or _nr
					if self.toWinddir and self.toWindspeed:
						weatherReport += '\n%s %s %s %s %s %s.' % (
						winddirstring, winddirvalue,
						_("with speed of"), wind_speed or _nr, unit_speed,
						sptm
						)
					elif self.toWindspeed and not self.toWinddir:
						weatherReport += '\n%s %s %s %s.' % (
						_("The wind speed is"), wind_speed or _nr, unit_speed,
						sptm
						)
					elif self.toSpeedmeters and self.toWinddir:
						weatherReport += '\n%s %s, %s %s.' % (
						winddirstring, winddirvalue,
						_("with speed of"), sptm[2:-1]
						)
					elif self.toSpeedmeters and not self.toWindspeed and not self.toWinddir:
						weatherReport += '\n%s %s.' % (
						_("The wind speed is"), sptm[2:-1]
						)
					elif self.toWinddir and not self.toWindspeed and not self.toSpeedmeters:
						weatherReport += '\n%s %s.' % (
						winddirstring, winddirvalue
						)

					if self.toPerceived is True:
						weatherReport += '\n%s %s %s.' % (
						_("The perceived temperature is"), wind_chill or _nr, _("degrees")
						)

					weatherReport = weatherReport.replace("  ", " ")
					weatherReport = weatherReport.replace(" .", ".")
				if self.toAtmosphere is True:
					#adds information on the atmosphere
					rising_dic = {"": "", "0": _("steady"), "1": _("rising"), "2": _("falling")}
					umiditystring = _("The humidity is")
					umidityvalue = self.dom['current_observation']['atmosphere']['humidity'] or _nr
					if self.toUmidity and self.toVisibility:
						weatherReport += '\n%s %s%%, %s %s %s.' % (
						umiditystring, umidityvalue,
						_("and the visibility is up to"),
						visibility or _nr, unit_distance
						)
					elif self.toUmidity and not self.toVisibility:
						weatherReport += '\n%s %s%%.' % (
						umiditystring, umidityvalue
						)
					elif self.toVisibility and not self.toUmidity:
						weatherReport += '\n%s %s %s.' % (
						_("The visibility is up to"),
						visibility or _nr, unit_distance
						)
					if self.toPressure and self.toBarometric:
						weatherReport += '\n%s %s %s, %s %s.' % (
						_("The pressure is"),
						pressure or _nr, unit_pressure,
						_("and the state of the barometric pressure is"),
						rising_dic[str(self.dom['current_observation']['atmosphere']['rising'])] or _nr
						)
					elif self.toPressure and not self.toBarometric:
						weatherReport += '\n%s %s %s.' % (
						_("The pressure is"),
						pressure or _nr, unit_pressure
						)
					elif self.toBarometric and not self.toPressure:
						weatherReport += '\n%s %s.' % (
						_("The state of the barometric pressure is"),
						rising_dic[self.dom['current_observation']['atmosphere']['rising']] or _nr
						)

				weatherReport = self.WeatherReport(weatherReport)
				if self.toAstronomy is True:
					#adds astronomical information
					sr = self.dom['current_observation']['astronomy']['sunrise']
					ss = self.dom['current_observation']['astronomy']['sunset']
					if self.to24Hours:
						sr = Shared().To24h(sr) #sunrise
						ss = Shared().To24h(ss) #sunset
					else:
						sr = Shared().Add_zero(sr)
						ss = Shared().Add_zero(ss)
					weatherReport += '\n%s %s %s %s.' % (
					_("The sun rises at"), sr or _nr,
					_("and sets at"), ss or _nr
					)

				if self.toSample and os.path.exists(_samples_path):
					self.Play_Sample(condition, temperature) #He plays the appropriate sound effect if present

			else:
				#gets forecast from Yahoo API
				month1 = ""
				high = self.dom['forecasts'][0]['high']
				low = self.dom['forecasts'][0]['low']
				if self.celsius != 0: #conversion only for Celsius and Kelvin degrees scale
					high = self.Temperature_convert(high, self.celsius)
					low = self.Temperature_convert(low, self.celsius)
				weatherReport = '%s %s %s %s %s %s %s %s.' % \
				(_("the forecast for today is"),
				self.dom['forecasts'][0]['text'],
				_("with a maximum temperature of"), high,
				_("and a minimum of"), low,
				_("degrees"), scale_as)
				weatherReport = weatherReport.replace(" .", ".")
				#Adds the remaining days set from user into the string
				error = 0
				for i in range(1, int(self.forecast_days)):
					try:
						week_day = date.fromtimestamp(self.dom['forecasts'][i]['date'])
					except IndexError:
						#limit days weather forecast reached
						error = i; break

					month = week_day.month
					if month1 == month:
						week_day = self.ConvertDate(week_day, False) #Omit the month
					else:
						week_day = self.ConvertDate(week_day)
						month1 = month
					high = self.dom['forecasts'][i]['high']
					low = self.dom['forecasts'][i]['low']
					if self.celsius != 0: #conversion only for Celsius and Kelvin degrees scale
						high = self.Temperature_convert(high, self.celsius)
						low = self.Temperature_convert(low, self.celsius)

					weatherReport += ' %s %s %s %s %s %s %s.' % \
					(week_day,
					self.dom['forecasts'][i]['text'],
					_("with a maximum temperature of"), high,
					_("and a minimum of"), low,
					_("degrees"))

				#Adds warning if it's missing a forecast of the day
				if error:
					for i in range(int(self.forecast_days) - error):
						weatherReport += '\n%s, %s.' % (_nr, _("not available"))
					self.forecast_days = str(error) #sets the maximum limit of forecast days

				weatherReport = self.WeatherReport(weatherReport)
			#this does not replace the name of the city
			weatherReport = '%s %s %s' % \
			(_("In"), self.city[:self.city.find(',')+1] or _("Unnamed"), weatherReport)

			if self.toClip:
				# Copy the bulletin or weather forecasts to the clipboard.
				import api
				weatherReport = weatherReport.replace(". ", ".\r\n")
				api.copyToClip(weatherReport)
		else:
			Shared().Play_sound(False, 1)
			weatherReport = _("Sorry, the woeID is not set!")
		return weatherReport


	def WeatherReport(self, weatherReport):
		"""These are necessary for the localization"""
		weatherReport = weatherReport.replace("km/h", _("kilometers per hour"))
		weatherReport = weatherReport.replace("mi/h", _("miles per hour"))
		#weather condition
		weatherReport = weatherReport.replace("AM", _("in the morning"))
		weatherReport = weatherReport.replace("PM", _("in the evening"))
		weatherReport = weatherReport.replace("/", _(" and "))
		weatherReport = weatherReport.replace(" and ", _(" and "))
		weatherReport = weatherReport.replace(" And ", _(" and "))
		weatherReport = weatherReport.replace(" to ", _(" to "))
		weatherReport = weatherReport.replace("Unknown", _nr)
		weatherReport = weatherReport.replace("in the Vicinity", _("in the vicinity"))
		weatherReport = weatherReport.replace("Tornado", _("tornado"))
		weatherReport = weatherReport.replace("Tropical Storm", _("tropical storm"))
		weatherReport = weatherReport.replace("Hurricane", _("hurricane"))
		weatherReport = weatherReport.replace("Severe Thunderstorms", _("severe thunderstorms"))
		weatherReport = weatherReport.replace("Mixed Rain And Snow", _("mixed rain and snow"))
		weatherReport = weatherReport.replace("Mixed Rain And Hail", _("mixed rain and hail"))
		weatherReport = weatherReport.replace("Mixed Rain And Sleet", _("mixed rain and sleet"))
		weatherReport = weatherReport.replace("Mixed Snow And Sleet", _("mixed snow and sleet"))
		weatherReport = weatherReport.replace("Snow Flurries", _("snow flurries"))
		weatherReport = weatherReport.replace("Smoke", _("smoke"))
		weatherReport = weatherReport.replace("Smoky", _("smoky"))
		weatherReport = weatherReport.replace("Precipitation", _("precipitation"))
		weatherReport = weatherReport.replace("Sunny Intervals", _("sunny intervals"))
		weatherReport = weatherReport.replace("Sunny Interval", _("sunny intervals"))
		weatherReport = weatherReport.replace("Sunny Period", _("sunny period"))
		weatherReport = weatherReport.replace("Light Snow", _("light snow"))
		weatherReport = weatherReport.replace("Scattered Snow Showers", _("scattered snow showers"))
		weatherReport = weatherReport.replace("Snow Showers", _("snow showers"))
		weatherReport = weatherReport.replace("Snow Shower", _("snow shower"))
		weatherReport = weatherReport.replace("Snowstorm", _("snowstorm"))
		weatherReport = weatherReport.replace("Snowdrift", _("snowdrift"))
		weatherReport = weatherReport.replace("Drifting Snow", _("drifting snow"))
		weatherReport = weatherReport.replace("Wintry Mix", _("wintry Mix"))
		weatherReport = weatherReport.replace("Ice to Rain", _("ice to rain"))
		weatherReport = weatherReport.replace("Ice To Rain", _("ice to rain"))
		weatherReport = weatherReport.replace("Ice", _("ice"))
		weatherReport = weatherReport.replace("Blizzard", _("blizzard"))
		weatherReport = weatherReport.replace("Blowing Snow", _("blowing snow"))
		weatherReport = weatherReport.replace("Snow", _("snow"))
		weatherReport = weatherReport.replace("Light Rain with Thunder", _("light rain with thunder"))
		weatherReport = weatherReport.replace("Few Showers", _("few showers"))
		weatherReport = weatherReport.replace("Heavy Showers", _("heavy showers"))
		weatherReport = weatherReport.replace("Heavy Thunderstorms", _("heavy thunderstorms"))
		weatherReport = weatherReport.replace("Heavy Thunderstorm", _("heavy thunderstorm"))
		weatherReport = weatherReport.replace("Lightning", _("lightning"))
		weatherReport = weatherReport.replace("Isolated Clouds", _("isolated clouds"))
		weatherReport = weatherReport.replace("Partly Cloudy", _("partly cloudy"))
		weatherReport = weatherReport.replace("Partly Bright", _("partly bright"))
		weatherReport = weatherReport.replace("Showers Early", _("showers early"))
		weatherReport = weatherReport.replace("Light Rain Shower", _("light rain"))
		weatherReport = weatherReport.replace("Light Rain", _("light rain"))
		weatherReport = weatherReport.replace("Heavy Rain", _("heavy rain"))
		weatherReport = weatherReport.replace("Isolated Showers", _("isolated showers"))
		weatherReport = weatherReport.replace("Isolated Thunderstorms", _("isolated thunderstorms"))
		weatherReport = weatherReport.replace("Isolated Thundershowers", _("isolated thundershowers"))
		weatherReport = weatherReport.replace("Mostly Cloudy", _("mostly cloudy"))
		weatherReport = weatherReport.replace("Mostly Dry", _("mostly dry"))
		weatherReport = weatherReport.replace("Mostly Clear", _("mostly clear"))
		weatherReport = weatherReport.replace("Clearing", _("clearing"))
		weatherReport = weatherReport.replace("No Rain", _("no rain"))
		weatherReport = weatherReport.replace("Sleet", _("sleet"))
		weatherReport = weatherReport.replace("Blowing Dust", _("blowing dust"))
		weatherReport = weatherReport.replace("Widespread Dust", _("widespread dust"))
		weatherReport = weatherReport.replace("Low Drifting Sand", _("low drifting sand"))
		weatherReport = weatherReport.replace("Sandstorm", _("sandstorm"))
		weatherReport = weatherReport.replace("Sand Storm", _("sand storm"))
		weatherReport = weatherReport.replace("Dust", _("dust"))
		weatherReport = weatherReport.replace("Sand", _("sand"))
		weatherReport = weatherReport.replace("Thundery Showers", _("thundery showers"))
		weatherReport = weatherReport.replace("Thundershowers", _("thundershowers"))
		weatherReport = weatherReport.replace("Scattered Thunderstorms", _("scattered thunderstorms"))
		weatherReport = weatherReport.replace("Scattered Showers", _("scattered showers"))
		weatherReport = weatherReport.replace("Thunderstorms", _("thunderstorms"))
		weatherReport = weatherReport.replace("Thunderstorm", _("thunderstorm"))
		weatherReport = weatherReport.replace("Storm", _("storm"))
		weatherReport = weatherReport.replace("Hail", _("hail"))
		weatherReport = weatherReport.replace("Foggy", _("foggy"))
		weatherReport = weatherReport.replace("Fog", _("fog"))
		weatherReport = weatherReport.replace("Haze", _("haze"))
		weatherReport = weatherReport.replace("Mist", _("mist"))
		weatherReport = weatherReport.replace("Clear", _("clear"))
		weatherReport = weatherReport.replace("Fair", _("fair"))
		weatherReport = weatherReport.replace("Fine", _("fine"))
		weatherReport = weatherReport.replace("Overcast", _("overcast"))
		weatherReport = weatherReport.replace("Light Showers", _("light showers"))
		weatherReport = weatherReport.replace("Light Drizzle", _("light drizzle"))
		weatherReport = weatherReport.replace("Freezing Rain", _("freezing rain"))
		weatherReport = weatherReport.replace("Frequent Showers", _("frequent showers"))
		weatherReport = weatherReport.replace("Rain Shower", _("rain shower"))
		weatherReport = weatherReport.replace("Rain", _("rain"))
		weatherReport = weatherReport.replace("Freezing Drizzle", _("freezing drizzle"))
		weatherReport = weatherReport.replace("Showers", _("showers"))
		weatherReport = weatherReport.replace("Drizzle", _("drizzle"))
		weatherReport = weatherReport.replace("Dry", _("dry"))
		weatherReport = weatherReport.replace("Mild", _("mild"))
		weatherReport = weatherReport.replace("Clouds", _("clouds"))
		weatherReport = weatherReport.replace("Cloudy", _("cloudy"))
		weatherReport = weatherReport.replace("Mostly Sunny", _("mostly sunny"))
		weatherReport = weatherReport.replace("Sunny", _("sunny"))
		weatherReport = weatherReport.replace("Sun", _("sun"))
		weatherReport = weatherReport.replace("Bright", _("bright"))
		weatherReport = weatherReport.replace("Thunder", _("thunder"))
		weatherReport = weatherReport.replace("Shower", _("shower"))
		weatherReport = weatherReport.replace("Breezy", _("breezy"))
		weatherReport = weatherReport.replace("Blustery", _("blustery"))
		weatherReport = weatherReport.replace("Windy", _("windy"))
		weatherReport = weatherReport.replace("Wind", _("wind"))
		weatherReport = weatherReport.replace("Flurries", _("flurries"))
		weatherReport = weatherReport.replace("Late", _("late"))
		weatherReport = weatherReport.replace("Early", _("early"))
		weatherReport = weatherReport.replace("Isolated", _("isolated"))
		weatherReport = weatherReport.replace("Shallow Fog", _("shallow fog"))
		weatherReport = weatherReport.replace("Heavy", _("heavy"))
		weatherReport = weatherReport.replace("Cold", _("cold"))
		weatherReport = weatherReport.replace("Hot", _("hot"))
		return weatherReport


	def Open_Dom(self, zip_code):
		"""Upload DOM data from the Yahoo API"""
		attempts = 2 #connection attempts
		curDate = datetime.now()

		def Read_API(): return Shared().WeatherConnect(yql_query = 'woeid=%s' % zip_code)
		dom = Read_API()
		if dom == "not authorized": return dom, ""
		if not dom:
			#If it doesn't receive data, try again a few times
			repeat = attempts
			while not dom:
				time.sleep(0.1)
				Shared().Play_sound("wait", 1)
				dom = Read_API()
				repeat -= 1
				if repeat == 0: break
			if not dom: return self.ZipCodeError(), ""
		elif "no connect" in dom:
			Shared().Play_sound("warn", 1)
			wx.CallAfter(ui.message, _("Sorry, i can not receive data, verify that your internet connection is active, or try again later!"))
			return "no connect", ""

		t = 0; repeat = attempts
		error = False
		while True:
			pubDate = Shared().GetLastUpdate(dom)
			if not pubDate: error = True; break
			#Filter old data
			dt = pubDate.date() - curDate.date()
			delta = dt.days
			if delta >= 0 or (delta >= -2 and delta <= 0): break #pubDate build data found
			else:
				sleep(0.1)
				t = (t + 1) % 6  #this construct cicle from 0 to 5
				if t == 0:
					Shared().Play_sound("wait", 1)
					dom = Read_API()
					repeat -= 1
					if repeat == 0: break

		message = ""
		if repeat == 0:
			message = '%s %s' % (
			_("Sorry, it was not possible to load the most recent update!"),
			_("Please try again later."))

		if error: return self.ZipCodeError(), ""
		try:
			country_acronym = Shared().GetAcronym(dom['location']['country'])
			region = dom['location']['region']
			city = dom['location']['city']
		except KeyError: return dom, ""
		self.current_hour, n, n = Shared().GetTimezone(country_acronym, region, city, to24Hours = True)
		if not self.current_hour:
			#probable non-codable city
			self.current_hour, n, n = Shared().GetTimezone(country_acronym, region, region, self.to24Hours, full = True)

		return dom, message


	def IntClean(self, v):
		"""remove .0 at the end of the value"""
		v = str(v)
		if v.endswith('.0'): v = v[:-2]
		return v


	def ConvertDate(self, dd, m = True):
		"""Convert month and day into date string"""
		dt = '%s %s' % (
		Shared().TranslateCalendar(calendar.weekday(dd.year, dd.month, dd.day)),
		dd.day
		)
		if m: dt = '%s %s' % (dt, Shared().TranslateCalendar(str(dd.month).rjust(2,'0')))
		return dt


	def Speedtometers(self, v, convert = True, meters = None):
		"""Returns a string converted from miles to kilometers or meters per second """
		if not v: return ""
		v = vm = float(v)
		if convert:
			v = v * 1.61 #Convert miles to kilometers

		if meters:
			ms = 0.44704*vm #convert miles into meters per second
			ms = (math.ceil(ms*100)/100) #round to 2 decimals
			if ms == 0.0: return ""
			ms = self.IntClean(ms)

			if self.toComma:
				return ' (%s %s)' % (ms.replace('.', ','), _("meters per second"))
			else: return ' (%s %s)' % (str(ms), _("meters per second"))

		v = self.IntClean((math.ceil(v*100)/100)) #round to 2 decimals
		v = v.split('.')[0] 
		if self.toComma: v = v.replace('.', ',')
		return v


	def Pressure_convert(self, pressure, mmHg = None):
		"""convert inhg to millibar or mmHg"""
		if not pressure: return ""
		pressure = float(pressure)
		c = 33.863782
		if mmHg: c = 25.4
		pre = (round((c*pressure)*100)/100) #round to 2 decimals
		pre = self.IntClean(pre)
		if self.toComma:
			return pre.replace('.', ',')
		else: return pre


	def Temperature_convert(self, temperature, scale):
		"""convert Fahrenheit to Celsius or Kelvin"""
		if not temperature or not scale: return ""
		temperature = float(temperature)
		if scale == 1:
			#Celsius
			tem = (temperature - 32)*5/9
		elif scale == 2:
			#Kelvin
			tem = int((temperature + 459.67)*5/9)

		return int(round(tem))


	def ZipCodeError(self):
		"""This construct cycles between 0, 1, every two errors of the same zip code he warns"""
		self.note[0] = (self.note[0] + 1) % 2
		self.note[1] = self.zipCode
		if not self.setZipCodeItem.IsEnabled(): self.note[0] = 1
		check, n, i = Shared().ZipCodeInList(self.zipCode, self.zipCodesList)
		if self.note[0] and check:
			#Problems with the woeID from the list
			self.Notice(i)
			return ""

		Shared().Play_sound(False,1)
		ui.message(_("Sorry, the woeID set is not valid or contains incomplete data!"))


	def GetCardinalDirection(self, degrees):
		"""Convert wind degrees direction in cardinal direction"""
		if not degrees: return ''
		degrees = int(degrees)
		cardinals_points = [
		_("north"), _("north northeast"), _("northeast"), _("east northeast"),_("east"), _("east southeast"),_("southeast"), _("south southeast"),
		_("south"), _("south southwest"), _("southwest"), _("west southwest"), _("west"), _("west northwest"), _("northwest"), _("north northwest")]
		cardinals_len = len(cardinals_points)
		cardinals_step = 360./cardinals_len
		period = degrees/360.
		normalized_period = (period - math.floor(period))*360.
		index = int(round(normalized_period/cardinals_step))
		index %= cardinals_len
		return cardinals_points[index]


	def Notice(self, index):
		"""A woeID is no longer valid, and suggests to delete it from the list"""
		winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		self.EnableMenu(False)
		self.woeIdDialog = wx.MessageDialog(gui.mainFrame, '%s "%s" %s "%s".\n%s "%s".\n%s\n%s' % (
		_("The woeID"), self.zipCode, _("assigned to"), self.city,
		_("Is not working properly, contains incomplete data or has been removed from the database of"),
		"Yahoo Weather Forecast",
		_("It could be a temporary problem and you may wait a while '..."),
		_("Do you want to delete it from your list?")),
		'%s %s' % (_addonSummary, _("Notice!")),
		wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

		def callback3(result):
			if result == wx.ID_YES:
				try:
					e = ''
					rollBack = list(self.zipCodesList)
					rollBack2 = dict(self.define_dic)
					if self.OpenedSettings:
						self.dlg.OnRemove()
					else:
						zc = self.zipCodesList.pop(index)
						decoded_zc = zc
						if _pyVersion == 2: decoded_zc = zc.decode("mbcs")
						code = Shared().GetZipCode(zc)
						if code in self.define_dic: del self.define_dic[code]
						if decoded_zc == self.defaultZipCode:
							self.zipCode = self.defaultZipCode = ''
							backup_celsius = self.celsius
							self.celsius = self.ReadConfig('c')
							self.SaveConfig()
							self.celsius = backup_celsius

				except ValueError as e: pass
				if not e:
					if not self.OpenedSettings:
						self.city = index #Temporarily for EnterDialog, deleted item position
						self.zipCode = self.tempZipCode = ''
						if self.WriteList(self.zipCodesList): Shared().Play_sound("del", 1)

					else:
						self.zipCodesList = rollBack
						self.define_dic = rollBack2
						del rollBack, rollBack2
				if not self.OpenedSettings and not self.openedTemporary: self.EnableMenu(True)

			else:
				if not self.OpenedSettings and not self.openedTemporary: self.EnableMenu(True)

		gui.runScriptModalDialog(self.woeIdDialog, callback3)


	def script_announceWeather(self, gesture):
		try:	
			if self.woeIdDialog or self.woeIdDialog.IsShown():
				return wx.Bell()
		except (AttributeError, RuntimeError): pass

		if self.zipCode != self.note[1]: self.note = [1, self.zipCode]
		ui.message(self.getWeather(self.zipCode))
		#try  to update the volume of new played sound effect, if  it's in dictionary 
		if self.OpenedSettings:
			select = self.dlg.ch_vol.GetSelection()
			if select == 1 and _curSample != "":
				if _curSample in samplesvolumes_dic:
					self.dlg.cb_vol.SetValue(samplesvolumes_dic[_curSample])
				else:
					self.dlg.cb_vol.SetValue(_volume)

	script_announceWeather.__doc__ = _("Provides the current temperature and weather conditions.")


	def script_announceForecast(self, gesture):
		try:
			if self.woeIdDialog or self.woeIdDialog.IsShown():
				return wx.Bell()
		except (AttributeError, RuntimeError): pass
		if self.zipCode != self.note[1]: self.note = [1, self.zipCode]
		ui.message(self.getWeather(self.zipCode, True))

	script_announceForecast.__doc__ = _("Provides the weather forecast and current temperature for 24 hours and the next 9 days.")


	def script_zipCodeEntry(self, gesture):
		"""Entering a temporary city"""
		try:
			if not self.zipCodesList:
				Shared().Play_sound(False, 1)
				return ui.message(_("Sorry, no list available!"))
		except AttributeError: pass
		#do not proceed if the window settings is open, but puts it in the foreground
		if not self.setZipCodeItem.IsEnabled():
			try:
				self.openedTemporary.Raise()
				self.openedTemporary.Show()
			except AttributeError: pass
			return wx.Bell()

		self.EnableMenu(False)
		self.setZipCodeDialog()

	script_zipCodeEntry.__doc__ = _("Allows you to set a temporary city.")


	def script_swapTempScale(self, gesture):
		"""set a measurement scale of degrees"""
		self.celsius = (self.celsius + 1) %3 # This construct cycles between 0, 2
		if self.OpenedSettings:
			#change the radio button in the settings window
			self.celsius = self.dlg.rb.GetSelection()
			self.celsius = (self.celsius + 1) % 3
			self.dlg.rb.SetSelection(self.celsius)
			self.dlg.rb.SetFocus()

		Shared().Play_sound("swap", 1)
		ui.message('%s %s' % (_("Scale of temperature measurement set into"), _tempScale[self.celsius]))

	script_swapTempScale.__doc__ = _("Allows you to set a temporary scale of temperature mesurement.")


	def script_announceLastBuildDate(self, gesture):
		"""announces the date and time of last weather report"""
		if not self.zipCode or self.zipCode.isspace():
			Shared().Play_sound(False, 1)
			return ui.message(_("Sorry, the woeID is not set!"))
		if not self.dom: self.dom, n = self.Open_Dom(self.zipCode)
		if not self.dom or self.dom in["not authorized", "no connect"]: self.dom = None; return
		lbd = Shared().GetLastUpdate(self.dom)
		last_build_date = _nr
		if lbd:
			year = lbd.year
			month = Shared().TranslateCalendar(str(lbd.month).rjust(2,'0'))
			day = lbd.day
			week_day = Shared().TranslateCalendar(calendar.weekday(year, lbd.month, day))
			lbdTime = lbd.time()

			if not self.to24Hours: lbdTime = Shared().To24h(lbdTime, viceversa = True)
			last_build_date = '%s %s %s %s %s %s' % (
			week_day, day, month, year, _("at"), lbdTime
			)

		ui.message('%s: %s.' % (_("Last update of the current weather report"), last_build_date))

	script_announceLastBuildDate.__doc__ = _("Announces the date of the last update of the weather report.")


	def script_weatherPlusSettings(self, gesture):
		"""Call the Weather Plus settings dialog"""
		#do not proceed if the window settings is open, but puts it in the foreground
		if not self.setZipCodeItem.IsEnabled():
			try:
				self.dlg.Raise()
				self.dlg.Show()
				self.dlg.cbx.SetFocus()
			except: pass
			return wx.Bell()

		self.onSetZipCodeDialog(None)

	script_weatherPlusSettings.__doc__ = _("Open the Weather Plus settings dialog.")


	__gestures={
		"kb:NVDA+w": "announceWeather",
		"kb:NVDA+shift+w": "announceForecast",
		"kb:nvda+shift+control+w": "zipCodeEntry",
		"kb:control+shift+w": "swapTempScale",
		"kb:nvda+alt+w": "announceLastBuildDate",
		"kb:nvda+alt+control+shift+w": "weatherPlusSettings"
	}


class EnterDataDialog(wx.Dialog):
	"""Main settings Dialog"""
	def __init__(self, parent, id=-1, title=wx.EmptyString,
			pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=wx.DEFAULT_DIALOG_STYLE,
			message = '',
			defaultZipCode = '', tempZipCode = '', zipCode = '', city = '', dom = '', celsius = None,
			toHelp = None, toClip = None, toSample = None, toWind = None, toAtmosphere = None, toAstronomy = None, to24Hours = None,
			toSpeedmeters = None, toAssign = None, scaleAs = None, volume_dic = {},
			defaultString = "", define_dic = {}, details_dic = {}, forecast_days = "", toUpgrade = None, toPerceived = None, toUmidity = None, toVisibility = None, toPressure = None, toMmhgpressure = None, toBarometric = None, toWinddir = None, toWindspeed = None, toComma = None, toWeatherEffects = None):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos,
		size=size, style=style)

		sizer = wx.BoxSizer(wx.VERTICAL)
		#loads cities list Weather.zipcodes
		z, define_dic, details_dic = Shared().LoadZipCodes()
		zipCodesList = Shared().Check_content(z, "", False) or []
		del z
		self.defaultString = defaultString
		self.testCode = self.testName = self.last_tab = ""
		if message:
			self.hotkeys_dic = {
			True: _("f1: help placing, f2: last TAB selection, f3: list and edit box, f4: control duration Weather Forecast, f5: volume controls."),
			False: _("f1: help placing, f2: last TAB selection, f3: list and edit box, f4: control duration Weather Forecast.")}
			f5 = True
			if not os.path.exists(_samples_path) or not toSample: f5 = False
			self.message1 = wx.StaticText(self, -1, self.hotkeys_dic[f5])

			sizer.Add(self.message1, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
			sizer.Add(wx.StaticText(self, -1, message), 0, wx.ALL, 5)
			sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		hbox=wx.BoxSizer(wx.HORIZONTAL)
		if _pyVersion == 2:
			cbx=wx.ComboBox(self, -1, style=wx.CB_DROPDOWN|wx.TE_RICH, choices = [i.decode("mbcs") for i in zipCodesList])
		else:
			cbx=wx.ComboBox(self, -1, style=wx.CB_DROPDOWN|wx.TE_RICH, choices = zipCodesList)

		s = tempZipCode
		if not s: s = defaultZipCode
		if _pyVersion == 2:
			try:
				s = s.encode("mbcs")
			except (UnicodeDecodeError, UnicodeEncodeError): pass

		if zipCodesList and s in zipCodesList:
			if _pyVersion == 2:
				cbx.SetStringSelection(s.decode("mbcs"))
			else:
				cbx.SetStringSelection(s)

		else:
			cbx.SetValue(s or "")
			if s: self.testCode = Shared().GetZipCode(s)

		hbox.Add(cbx, 0, wx.EXPAND|wx.ALL, 5)
		self.zipCodesList = zipCodesList
		self.tempZipCode = tempZipCode
		self.defaultZipCode = defaultZipCode
		self.define_dic = define_dic
		self.details_dic = details_dic
		self.samplesvolumes_dic = samplesvolumes_dic
		self.modifiedList = False
		if wx.version().split(".")[0] >= "4": helpButton = wx.adv.CommandLinkButton
		else: helpButton = wx.CommandLinkButton
		btn_Test = helpButton(self, -1, _("Test"), note = "", style=wx.BU_EXACTFIT)
		btn_Details = helpButton(self, -1, _("Details"), "", style=wx.BU_EXACTFIT)
		btn_Define = helpButton(self, -1, _("Define"), "", style=wx.BU_EXACTFIT)
		btn_Add = helpButton(self, -1, _("Add"), "", style=wx.BU_EXACTFIT)
		btn_Apply = helpButton(self, -1, _("Preset"), "", style=wx.BU_EXACTFIT)
		btn_Remove = helpButton(self, -1, _("Remove"), "", style=wx.BU_EXACTFIT)
		btn_Rename = helpButton(self, -1, _("Rename"), "", style=wx.BU_EXACTFIT)
		hbox.Add(btn_Test, 0, wx.EXPAND|wx.ALL, 5)
		hbox.Add(btn_Details, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
		hbox.Add(btn_Define, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
		hbox.Add(btn_Add, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
		hbox.Add(btn_Apply, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
		hbox.Add(btn_Remove, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
		hbox.Add(btn_Rename, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.BOTTOM, 5)
		self.Bind(wx.EVT_TEXT, self.OnText, cbx)
		self.Bind(wx.EVT_BUTTON, self.OnTest, btn_Test) 
		self.Bind(wx.EVT_BUTTON, self.OnDetails, btn_Details) 
		self.Bind(wx.EVT_BUTTON, self.OnDefine, btn_Define) 
		self.Bind(wx.EVT_BUTTON, self.OnAdd, btn_Add) 
		self.Bind(wx.EVT_BUTTON, self.OnApply, btn_Apply) 
		self.Bind(wx.EVT_BUTTON, self.OnRemove, btn_Remove)
		self.Bind(wx.EVT_BUTTON, self.OnRename, btn_Rename)
		self.btn_Test = btn_Test
		self.btn_Details = btn_Details
		self.btn_Define = btn_Define
		self.btn_Add = btn_Add
		self.btn_Apply = btn_Apply
		self.btn_Remove = btn_Remove
		self.btn_Rename = btn_Rename
		sizer.Add(hbox)
		#other buttons
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		btn_Import = helpButton(self, -1, _("&Import new cities..."), "", style=wx.BU_EXACTFIT)
		btn_Export = helpButton(self, -1, _("&Export your cities..."), "", style=wx.BU_EXACTFIT)
		hbox2.Add(btn_Import, 1, wx.EXPAND|wx.ALL, 5)
		hbox2.Add(btn_Export, 1, wx.EXPAND|wx.ALL, 5)
		sizer.Add(hbox2, 1, wx.ALIGN_CENTER_HORIZONTAL)
		self.Bind(wx.EVT_BUTTON, self.OnImport, btn_Import)
		self.Bind(wx.EVT_BUTTON, self.OnExport, btn_Export)
		self.btn_Import = btn_Import
		self.btn_Export = btn_Export
		if not os.path.exists(_zipCodes_path):
			btn_Export.Enable(False)
		#radio buttons
		self.rb=wx.RadioBox(
			self, -1, _("Scale of temperature measurement:"),
			wx.DefaultPosition, wx.DefaultSize,
			_tempScale,
			3, style=wx.RB_GROUP)
		self.rb.SetSelection(celsius)
		self.celsius = celsius
		sizer.Add(self.rb, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.rb1=wx.RadioBox(
			self, -1, _("Degrees shown as:"),
			wx.DefaultPosition, wx.DefaultSize,
			['%s - %s - %s' % (_tempScale[1], _tempScale[0], _tempScale[-1]),
			_("C - F - K"),
			_("Don't specify")],
			3, style=wx.RB_GROUP)
		self.rb1.SetSelection(scaleAs)
		sizer.Add(self.rb1, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		#combo box forecast days
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(self, -1, _("Weather Forecasts up to days:"))
		cb_days=wx.ComboBox(self, -1, style = wx.CB_READONLY,choices = ['%s' % i for i in range(1, 11, 1)]) #set from 1 to 10 days
		cb_days.SetValue(forecast_days)
		hbox3.Add(st, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 5)
		hbox3.Add(cb_days, 0, wx.ALL, 5)
		sizer.Add(hbox3)
		self.cb_days = cb_days
		#check boxes
		self.cbt_toClip = wx.CheckBox(self, -1, _("&Copy the weather report and weather forecast, including city details to clipboard"))
		self.cbt_toClip.SetValue(bool(toClip))
		sizer.Add(self.cbt_toClip, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.toClip = toClip

		self.cbt_toSample = wx.CheckBox(self, -1, _("Enable &audio effects (only for the current weather conditions)"))
		sizer.Add(self.cbt_toSample, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toWeatherEffects = wx.CheckBox(self, -1, _("Use only &weather effects"))
		sizer.Add(self.cbt_toWeatherEffects, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
#combo box volumes
		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		ch_vol = wx.Choice(self, -1, choices = [
		_("General audio volume"),
		_("Current audio volume")])
		if toAssign == None: toAssign = 0
		ch_vol.SetSelection(toAssign)
		self.toAssign = toAssign
		ch_vol.Bind(wx.EVT_CHOICE, self.OnChoice)
		self.ch_vol = ch_vol

		cb_vol=wx.ComboBox(self, -1, style = wx.CB_READONLY,choices = ['%s%%' % i for i in reversed(range(0, 110, 10))]) #set from 0% to 100% volume
		try:
			vol =int(volume[:-1])
		except (NameError, ValueError): vol = None
		if str(vol).isdigit() and int(vol) >= 0 and int(vol) <= 100:
			cb_vol.SetValue('%s' % volume)
		else: cb_vol.SetValue('60%')
		hbox5.Add(ch_vol, 0, wx.TOP|wx.BOTTOM, 5)
		hbox5.Add(cb_vol, 0, wx.ALL, 5)
		sizer.Add(hbox5)
		self.ch_vol = ch_vol
		self.cb_vol = cb_vol
		self.cb_vol.Bind(wx.EVT_COMBOBOX, self.OnVolume)
		self.cbt_toSample.SetValue(bool(toSample))
		self.cbt_toWeatherEffects.SetValue(bool(toWeatherEffects))
		self.OnChoice()
		if not os.path.exists(_samples_path) or not self.cbt_toSample.IsChecked():
			btn_Define.Enable(False)
			self.cbt_toSample.SetValue(False)
			self.cbt_toWeatherEffects.SetValue(False)
			self.ch_vol.Enable(False)
			self.cb_vol.Enable(False)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.cbt_toSample)
		#check boxes
		self.cbt_toHelp = wx.CheckBox(self, -1, _("Enable &help buttons in the settings window"))
		self.cbt_toHelp.SetValue(bool(toHelp))
		sizer.Add(self.cbt_toHelp, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.toHelp = toHelp
		self.OnHelp_notes()
		self.Bind(wx.EVT_CHECKBOX, self.OnHelp_notes, self.cbt_toHelp)

		self.cbt_toWind = wx.CheckBox(self, -1, _("Read &wind informations"))
		self.cbt_toWind.SetValue(bool(toWind))
		sizer.Add(self.cbt_toWind, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox3, self.cbt_toWind)

		self.cbt_toWinddir = wx.CheckBox(self, -1, _("Add wind directi&on"))
		self.cbt_toWinddir.SetValue(bool(toWinddir))
		sizer.Add(self.cbt_toWinddir, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toWindspeed = wx.CheckBox(self, -1, _("Add wi&nd speed"))
		self.cbt_toWindspeed.SetValue(bool(toWindspeed))
		sizer.Add(self.cbt_toWindspeed, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toSpeedmeters = wx.CheckBox(self, -1, _("Add speed in &meters per second of the wind"))
		self.cbt_toSpeedmeters.SetValue(bool(toSpeedmeters))
		sizer.Add(self.cbt_toSpeedmeters, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toPerceived = wx.CheckBox(self, -1, _("Add perceived &temperature"))
		self.cbt_toPerceived.SetValue(bool(toPerceived))
		sizer.Add(self.cbt_toPerceived, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.OnCheckBox3(self.cbt_toWind)

		self.cbt_toAtmosphere = wx.CheckBox(self, -1, _("&Read atmospherical informations"))
		self.cbt_toAtmosphere.SetValue(bool(toAtmosphere))
		sizer.Add(self.cbt_toAtmosphere, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox4, self.cbt_toAtmosphere)

		self.cbt_toUmidity = wx.CheckBox(self, -1, _("Add humidity va&lue"))
		self.cbt_toUmidity.SetValue(bool(toUmidity))
		sizer.Add(self.cbt_toUmidity, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toVisibility = wx.CheckBox(self, -1, _("Add &visibility value"))
		self.cbt_toVisibility.SetValue(bool(toVisibility))
		sizer.Add(self.cbt_toVisibility, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toPressure = wx.CheckBox(self, -1, _("Add atmospheric &pressure value"))
		self.cbt_toPressure.SetValue(bool(toPressure))
		sizer.Add(self.cbt_toPressure, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toMmhgpressure = wx.CheckBox(self, -1, _("Indicates the atmospheric pressure in millimeters of mercur&y (mmHg)"))
		self.cbt_toMmhgpressure.SetValue(bool(toMmhgpressure))
		sizer.Add(self.cbt_toMmhgpressure, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toBarometric = wx.CheckBox(self, -1, _("Add status of &barometric pressure"))
		self.cbt_toBarometric.SetValue(bool(toBarometric))
		sizer.Add(self.cbt_toBarometric, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.OnCheckBox4(self.cbt_toAtmosphere)

		self.cbt_toAstronomy = wx.CheckBox(self, -1, _("Read a&stronomical informations"))
		self.cbt_toAstronomy.SetValue(bool(toAstronomy))
		sizer.Add(self.cbt_toAstronomy, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_to24Hours = wx.CheckBox(self, -1, _("Enable reading of the hours in &24-hour format"))
		self.cbt_to24Hours.SetValue(bool(to24Hours))
		sizer.Add(self.cbt_to24Hours, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.to24Hours = to24Hours

		self.cbt_toComma = wx.CheckBox(self, -1, _("Use the comma to separate decimals, example (4,&15)"))
		self.cbt_toComma.SetValue(bool(toComma))
		sizer.Add(self.cbt_toComma, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toUpgrade = wx.CheckBox(self, -1, _("Check for &upgrade"))
		self.cbt_toUpgrade.SetValue(bool(toUpgrade))
		sizer.Add(self.cbt_toUpgrade, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		sizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.CENTRE| wx.ALL|wx.EXPAND, 5)
		self.btn_Ok = self.FindWindowById(wx.ID_OK)
		self.btn_Cancel = self.FindWindowById(wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self.OnEnter_key, self.btn_Ok)
		self.cbx = cbx
		self.f1 = 0 #after a few errors recommend you press F1
		self.WidgetFocusControl()
		self.ButtonsEnable(False)
		self.OnText()
		if cbx.GetValue() == "":
			#primary combo box empty
			self.btn_Ok.Enable(False)

		self.current_hour = ""
		self.SetSizerAndFit(sizer)
		self.Layout()
		self.Center(wx.BOTH|wx.Center)
		self.cbx.SetFocus() #primary combo box
		self.last_tab = cbx


	def OnHelp_notes(self, evt = None):
		"""enables or disables the help notices for the buttons"""
		if self.cbt_toHelp.IsChecked():
			self.btn_Test.SetNote(_("Testing the validity of city woeID entry and find the name of city assigned, or viceversa."))
			self.btn_Details.SetNote(_("Displays information on the current city."))
			self.btn_Define.SetNote(_("Allows you to define the area, in order to adapt the sound effects."))
			self.btn_Add.SetNote(_("Add the current city into your list."))
			self.btn_Apply.SetNote(_("Presets the current city as the default, will be used every time you restart the plugin."))
			self.btn_Remove.SetNote(_("Delete  the current city from your list."))
			self.btn_Rename.SetNote(_("Rename the current city."))
			self.btn_Import.SetNote(_("Permits to incorporate in your list new cities importing them from another list with the extension *.zipcodes; you can select the city you want to import, by turning on the check box associated."))
			self.btn_Export.SetNote(_("Permits to save your list of cities in a specified path."))
		else:
			for i in (
			self.btn_Test,
			self.btn_Details,
			self.btn_Define,
			self.btn_Add,
			self.btn_Apply,
			self.btn_Remove,
			self.btn_Rename,
			self.btn_Import,
			self.btn_Export): i.SetNote("")


	def WidgetFocusControl(self):
		"""events to moves the focus between the list, audio controls and ceck boxes"""
		self.cbx.Bind(wx.EVT_CHAR, self.OnKey)
		self.ch_vol.Bind(wx.EVT_CHAR, self.OnKey)
		self.cb_vol.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Test.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Details.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Define.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Add.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Apply.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Remove.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Rename.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Import.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Export.Bind(wx.EVT_CHAR, self.OnKey)
		self.cb_days.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter_key, self.cb_days)
		self.cbt_toClip.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toClip)
		self.cbt_toSample.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toSample)
		self.cbt_toWeatherEffects.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toWeatherEffects)
		self.cbt_toHelp.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toHelp)
		self.cbt_toWind.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toWind)
		self.cbt_toWinddir.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toWinddir)
		self.cbt_toWindspeed.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toWindspeed)
		self.cbt_toSpeedmeters.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toSpeedmeters)
		self.cbt_toPerceived.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toPerceived)
		self.cbt_toUmidity.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toUmidity)
		self.cbt_toVisibility.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toVisibility)
		self.cbt_toPressure.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toPressure)
		self.cbt_toMmhgpressure.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toMmhgpressure)
		self.cbt_toBarometric.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toBarometric)
		self.cbt_toComma.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toComma)
		self.cbt_toAtmosphere.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toAtmosphere)
		self.cbt_toAstronomy.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toAstronomy)
		self.cbt_to24Hours.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_to24Hours)
		self.cbt_toUpgrade.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toUpgrade)
		self.btn_Ok.Bind(wx.EVT_CHAR, self.OnKey)
		self.btn_Cancel.Bind(wx.EVT_CHAR, self.OnKey)


	def OnKey(self, evt):
		"""Control hot keys pressed into EnterDataDialog"""
		cur_tab = evt.GetEventObject()
		key = evt.GetKeyCode()
		controlDown = evt.CmdDown()
		if key == wx.WXK_ESCAPE:
			#exit from setting dialog
			self.EndModal(wx.ID_CANCEL)
		elif key == wx.WXK_RETURN and self.btn_Ok.IsEnabled():
			#exit from setting dialog
			self.EndModal(wx.ID_OK)

		elif controlDown and key is 1:
			#select value into combo box
			if cur_tab is self.cbx: cur_tab.SelectAll(); return

		elif key == wx.WXK_F1:
			#help input
			helpDialog = HelpEntryDialog(gui.mainFrame, message = '%s:\n%s:\n%s.\n%s.\n%s.\n%s.\n%s.\n%s:\n%s.\n%s.\n%s.\n%s.\n%s.' % (
			_("You can enter or search for a city"),
			_("By city woeID: 715399"),
			_("By only city name: Ferrara"),
			_("By state or region and city name: Emilia Romagna Ferrara"),
			_("By city name and country: Ferrara,it"),
			_("By postal code: 44100,it"),
			_("By geographic coordinates: latitude, longitude"),
			_("If the city is not found"),
			_("Try with or without the country of origin"),
			_("Try to merge the name with hyphens, or separate it with spaces"),
			_("Try deleting apostrophes"),
			_("Try changing the vowels accented with normal vowels"),
			_("Try with a closest location")
			),
			title = _("Help placing")
			)
			if helpDialog.ShowModal()is not None:
				helpDialog.Destroy()
				Shared().Play_sound("subwindow", 1)
			cur_tab.SetFocus()

		elif key == wx.WXK_F2:
			#back to the last item
			if self.last_tab:
				if cur_tab != self.last_tab:
					self.last_tab.SetFocus(); self.last_tab = cur_tab
				else: wx.Bell()

		elif key == wx.WXK_F3:
			#moves the focus on the cities list
			if cur_tab != self.cbx: self.cbx.SetFocus(); self.last_tab = cur_tab
			else: wx.Bell()

		elif key == wx.WXK_F4:
			#move the focus on the forecast days control
			if cur_tab != self.cb_days: self.cb_days.SetFocus(); self.last_tab = cur_tab
			else: wx.Bell()

		elif key == wx.WXK_F5 and self.ch_vol.IsEnabled():
			#moves the focus on the volume controls
			if cur_tab != self.ch_vol: self.ch_vol.SetFocus(); self.last_tab = cur_tab
			else: wx.Bell()

		evt.Skip()


	def ButtonsEnable(self, flag):
		"""Enable buttons for EnterDataDialog"""
		[i.Enable(flag)for i in [self.btn_Test, self.btn_Details, self.btn_Add, self.btn_Apply, self.btn_Remove, self.btn_Rename]]
		if os.path.exists(_samples_path): self.btn_Define.Enable(flag)


	def OnVolume(self, evt):
		"""volume changes event"""
		if not _handle:
			self.Warn_curSample()
			#restores last volume value
			global _volume
			self.cb_vol.SetValue(_volume)
			return self.cb_vol.SetFocus()

		if self.ch_vol.GetSelection() == 1:
			#assign volume to current sound effect
			volTest = self.cb_vol.GetValue()
			if volTest == '0%':
				#fixed minimum volume for Safety
				volTest = '10%'
				self.cb_vol.SetValue(volTest)

			samplesvolumes_dic.update({_curSample: volTest})
			#adjust sound effect volume proportioning to total volume
			volTest = Shared().AdjustVol(volTest)

		elif self.ch_vol.GetSelection() == 0:
			#general volume
			_volume = self.cb_vol.GetValue()
			volTest = _volume
			volTest = Shared().AdjustVol(volTest)

		try:
			BASS_ChannelPlay(_handle, True)
			BASS_ChannelSetAttribute(_handle, BASS_ATTRIB_VOL, _volume_dic[volTest]) #set vol (0 = mute, 1 = full)
		except Exception as e:
			Shared().SendToLog(e)

		evt.Skip()


	def OnChoice(self, evt = None):
		"""selection event for current or general samples"""
		if not _curSample:
			if evt:
				self.Warn_curSample()
				#restores last choice selection
				self.ch_vol.SetSelection(self.toAssign)
				return self.ch_vol.SetFocus()

		if _curSample in samplesvolumes_dic.keys() and self.ch_vol.GetSelection() == 1:
			self.cb_vol.SetValue(samplesvolumes_dic[_curSample])
		else: self.cb_vol.SetValue(_volume)
		if evt: evt.Skip()


	def Warn_curSample(self):
		"""no sound effect into memory"""
		wx.MessageBox('%s\n%s' % (
		_("No sound effect in memory!"),
		_("I can't reproduce the sound.")),
		'%s - %s' % (_addonSummary, _("Notice!")), wx.ICON_EXCLAMATION)


	def OnText(self, evt = None):
		"""ComboBox Text Entry Event"""
		v = self.cbx.GetValue()
		check, v1, i = Shared().ZipCodeInList(v, self.zipCodesList)
		if not check:
			if v == self.tempZipCode:
				self.btn_Test.Enable(False)
				self.btn_Details.Enable(True)
				self.btn_Add.Enable(True)
				if not self.defaultZipCode: self.btn_Apply.Enable(True)
			else:
				self.ButtonsEnable(False)
				if not v.isspace(): self.btn_Test.Enable(True)

		else:
			#value is in list
			if _pyVersion == 2:zcs = self.zipCodesList[i].decode("mbcs")
			else: zcs = self.zipCodesList[i]
			spl = self.zipCodesList[i].split()
			if len(spl[-1]) == 1:
				self.cbx.SetStringSelection(zcs[:-2])
				self.ButtonsEnable(False)
				self.btn_Test.Enable(True)
				self.btn_Remove.Enable(True)
			else:
				self.cbx.SetStringSelection(zcs)
				self.btn_Test.Enable(False)
				self.btn_Details.Enable(True)
				if os.path.exists(_samples_path): self.btn_Define.Enable(True)
				self.btn_Add.Enable(False)
				self.btn_Remove.Enable(True)
				self.btn_Rename.Enable(True)

		if v1 == Shared().GetZipCode(self.defaultZipCode):
			self.btn_Apply.Enable(False)
		elif v1 != Shared().GetZipCode(self.defaultZipCode) and self.defaultZipCode and not self.btn_Test.IsEnabled():
			self.btn_Apply.Enable(True)
		elif not self.defaultZipCode and not self.btn_Test.IsEnabled():
			self.btn_Apply.Enable(True)

		if v1 == '':
			self.ButtonsEnable(False)
			self.btn_Ok.Enable(False)
		elif self.testCode == v1 and self.testCode.isdigit():
			self.btn_Test.Enable(False)
			self.btn_Add.Enable(True)
			self.btn_Apply.Enable(True)
			self.btn_Details.Enable(True)

		if self.btn_Test.IsEnabled():
			self.btn_Ok.Enable(False)
		elif not self.btn_Test.IsEnabled() and not v.isspace() and v:
			self.btn_Ok.Enable(True)


	def OnEnter_key(self, evt):
		"""enter key event"""
		evt.Skip()
		self.EndModal(wx.ID_OK)


	def OnTest(self, evt = None):
		"""button Test event"""
		value = self.cbx.GetValue()
		self.apixuValue = woeID = coords = None
		coords = Shared().GetCoords(value)
		if coords:
			define = str(value[-2:][-1])
			if define.isdigit() and len(define) == 1: self.apixuValue = value
			value = coords

		if not value.isdigit() and not coords:
			#search for city recurrences
			woeID, self.defaultString = Shared().Search_cities(value, self.defaultString)
			if not woeID: return
			elif woeID not in ["Error", "noresult"]: value = woeID

		#Test as Cityname or woeid
		cityName, v = Shared().ParseEntry(value)
		if cityName == "no connect":
			self.Disable_all(False)
			Shared().Play_sound("warn", 1)
			return ui.message(_("Sorry, i can not receive data, verify that your internet connection is active, or try again later!"))
		elif not cityName:
			self.Disable_all()
			if woeID == value:
				return self.Yahoo_API_error(woeID, True)
			else:
				self.f1 = (self.f1 + 1) % 3
				if self.f1 == 1: return ui.message('%s %s' % (value, _("not found! Press F1 for help on entering data.")))
				return ui.message('%s %s' % (value, _("not found!")))

		value = '%s %s' % (cityName.capitalize(), v)
		self.cbx.SetValue(value)
		check, n, n =Shared().ZipCodeInList(value, self.zipCodesList)
		if not check:
			Shared().Play_sound(True)
			self.testCode = str(v)
			self.testName = cityName

		else:Shared().Play_sound("alreadyinlist")

		self.OnText()
		self.btn_Test.Enable(False)
		self.btn_Ok.Enable(True)
		self.cbx.SetFocus()


	def Yahoo_API_error(self, v, id_error = None):
		"""Notice if the code is not valid, or poorly functioning"""
		text = '%s\n%s\n%s' % (
		_("Is not working properly or has been removed from the database of"),
		"Yahoo Weather Forecast.",
		_("It could be a temporary problem and you may wait a while '..."))
		if id_error:
			text = _("Is no longer valid!")

		wx.MessageBox('%s "%s"\n%s' % (
		_("The woeID"), v,
		text,
		),
		_addonSummary, wx.ICON_EXCLAMATION)


	def Disable_all(self, s=True):
		"""disable all buttons"""
		if s: Shared().Play_sound(False, 1)
		self.cbx.SetFocus()
		self.ButtonsEnable(False)
		self.btn_Ok.Enable(False)


	def OnCheckBox(self, evt):
		"""audio manager and control events"""
		self.last_tab = evt.GetEventObject()
		if not evt.IsChecked():
			if self.cb_vol.IsEnabled(): return self.AudioControlsEnable(False)

		reload = False
		if os.path.exists(_samples_path):
			reload = True
			self.AudioControlsEnable(reload)

		if not reload:
			message = '%s.\n%s' % (
			_("This option requires the installation of some audio effects"),
			_("Do you want to install them?"))
		else:
			self.AudioControlsEnable(True)
			message = '%s\n%s\n%s' % (
			_("The audio effects are installed!"),
			_("Would you like to update?"),
			_("Or do you want to uninstall them?"))

		dl = NoticeAgainDialog(gui.mainFrame, message=message, title = '%s %s' % (_addonSummary, _("Notice!")), bUninstall= True, uninstall_button = reload)
		m = dl.ShowModal()
		if m == 5102:
			#Uninstall button
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			if wx.MessageBox(_("Are you sure you want to uninstall the sound effects?"), '%s %s' % (_addonSummary, _("Notice!")), wx.ICON_QUESTION | wx.YES_NO) == 2:
				self.cbt_toSample.SetValue(False) #disable audio check box
				self.AudioControlsEnable(False)
				self.DelTemp(_samples_path, uninstall = True)
				winsound.MessageBeep(winsound.MB_ICONASTERISK)

			self.CloseWind(dl)
			return
		elif m == 5101:
			#Close button
			if not reload:
				self.cbt_toSample.SetValue(False) #disable audio check box
				self.AudioControlsEnable(False)

			self.CloseWind(dl)
			return
		else:
			#Innstall button
			self.CloseWind(dl)
			#Download and install the Weather_samples folder
			if "_addonBaseUrl" not in globals():
				global _addonBaseUrl
				_addonBaseUrl = Shared().GetAddonBaseUrl()

			source = "/".join((_addonBaseUrl, 'weather_samples2.zip?download=1'))
			import tempfile
			target = "/".join((tempfile.gettempdir().decode("mbcs"), 'Weather_samples.zip'))
			title = _("Update in progress")
			if not reload: title = _("Installation in progress")
			message = _("Please wait...")
			wx.CallAfter(ui.message, message)
			result = Shared().Download_file(source, target, title, message)
			if result == "Error":
				self.ErrorMessage()
				if not reload: self.cbt_toSample.SetValue(False) #disable audio check box
				self.DelTemp(target)

			elif result:
				#Unpack archive
				self.DelTemp(_samples_path) #Delete old files and the Weather_samples folder
				import zipfile
				unZip = config.getUserDefaultConfigPath()
				try:
					with zipfile.ZipFile(target, "r") as z:
						z.extractall(unZip)
				except Exception as e:
					Shared().SendToLog(e)
					self.ErrorMessage(True)
					self.cbt_toSample.SetValue(False) #disable audio check box
					self.AudioControlsEnable(False)
					self.DelTemp(_samples_path, uninstall = True)
					self.DelTemp(target) #delete the temporary file Weather_samples.zip
					return self.cbt_toSample.SetFocus()

				#Installation Complete
				info_string = _("The installation of audio effects has been completed successfully!")
				path_string = '%s "%s".\n' % (_("Adding folder:"), _samples_path)
				if reload:
					info_string = _("The upgrade of audio effects has been completed successfully!")
					path_string = ""
				message = '%s\n%s%s\n%s' % (
				info_string,
				path_string,
				_("These sound effects are subject to change by the author."),
				_("Disable and re-enable this option in order to update or uninstall them."))
				wx.MessageBox(message, '%s %s' % (_addonSummary, _("Notice!")), wx.ICON_INFORMATION)
				self.cbt_toSample.SetValue(True) #enable audio check box
				self.AudioControlsEnable(True)

			self.DelTemp(target) #delete the temporary file samples.zip
			if not os.path.exists(_samples_path):
				self.cbt_toSample.SetValue(False) #disable audio check box
				self.AudioControlsEnable(False)

			self.cbt_toSample.SetFocus()


	def OnCheckBox2(self, evt):
		"""Refresh location last object in focus"""
		self.last_tab = evt.GetEventObject()
		windCheckboxis = [self.cbt_toWinddir, self.cbt_toWindspeed, self.cbt_toSpeedmeters, self.cbt_toPerceived]
		atmosphereCheckboxis = [self.cbt_toUmidity, self.cbt_toVisibility, self.cbt_toPressure, self.cbt_toBarometric]
		if self.last_tab in windCheckboxis:
			if [x.GetValue() for x in windCheckboxis].count(False) == 4:
			 	#prevents you from to disable all the check boxes in wind informations
				wx.Bell()
				self.last_tab.SetValue(True)

		elif self.last_tab in atmosphereCheckboxis:
			if [x.GetValue() for x in atmosphereCheckboxis].count(False) == 4:
				#prevents you from to disable all the check boxes in atmosphere informations
				wx.Bell()
				self.last_tab.SetValue(True)

		if not self.cbt_toPressure.IsChecked(): self.cbt_toMmhgpressure.Enable(False)
		elif self.cbt_toPressure.IsEnabled(): self.cbt_toMmhgpressure.Enable(True)
		evt.Skip()


	def OnCheckBox3(self, evt = None):
		"""disable all items if wind informations is not activate"""
		flag = True
		if not evt.IsChecked(): flag = False
		[i.Enable(flag) for i in [self.cbt_toWinddir, self.cbt_toWindspeed, self.cbt_toSpeedmeters, self.cbt_toPerceived]]


	def OnCheckBox4(self, evt = None):
		"""disable all items if atmosphere informations is not activate"""
		flag = evt.IsChecked()
		[i.Enable(flag) for i in [self.cbt_toUmidity, self.cbt_toVisibility, self.cbt_toPressure, self.cbt_toMmhgpressure, self.cbt_toBarometric]]


	def AudioControlsEnable(self, f5):
		"""remove f5 key shortcut and disable audio controls"""
		self.message1.SetLabel(self.hotkeys_dic[f5])
		return [i.Enable(f5) for i in [self.cbt_toWeatherEffects, self.ch_vol, self.cb_vol]]


	def CloseWind(self, dialog):
		dialog.Destroy()
		self.cbt_toSample.SetFocus()


	def ErrorMessage(self, e = None):
		message = _("Verify that your internet connection is active, or try again later.")
		if e: message = _("File corrupted or not available!")
		wx.MessageBox('%s\n%s' %
			(_("Sorry, i could not complete the installation of the sound effects!"), message),
			'%s %s' % (_addonSummary, _("Installation Error!")),
			wx.ICON_ERROR)


	def DelTemp(self, file, uninstall=None):
		"""Delete file"""
		Shared().FreeHandle() #frees the memory allocated by the audio sample
		if os.path.isfile(file):
			os.remove(file)
		elif os.path.isdir(file):
			for filename in os.listdir(file):
				file_path = os.path.join(file, filename)
				try:
					if os.path.isfile(file_path):
						os.remove(file_path)
				except: pass
		try:
			if uninstall:os.rmdir(file)
		except:pass


	def GetValue(self):
		"""Return values from EnterDataDialog """
		if _pyVersion >= 3:
			gv = self.cbx.GetValue()
		else:
			try:
				gv = self.cbx.GetValue().encode("mbcs")
			except (UnicodeDecodeError, UnicodeEncodeError): gv = self.cbx.GetValue()

		return (
		self.cb_days.GetValue(),
		self.cbt_toUpgrade.GetValue(),
		self.zipCodesList,
		self.define_dic,
		self.details_dic,
		self.defaultZipCode,
		gv,
		self.modifiedList,
		self.rb.GetSelection(),
		self.rb1.GetSelection(),
		self.cbt_toClip.GetValue(),
		self.cbt_toSample.GetValue(),
		self.cbt_toHelp.GetValue(),
		self.cbt_toWind.GetValue(),
		self.cbt_toSpeedmeters.GetValue(),
		self.cbt_toAtmosphere.GetValue(),
		self.cbt_toAstronomy.GetValue(),
		self.cbt_to24Hours.GetValue(),
		self.cbt_toPerceived.GetValue(),
		self.cbt_toUmidity.GetValue(),
		self.cbt_toVisibility.GetValue(),
		self.cbt_toPressure.GetValue(),
		self.cbt_toBarometric.GetValue(),
		self.cbt_toWinddir.GetValue(),
		self.cbt_toWindspeed.GetValue(),
		self.cbt_toMmhgpressure.GetValue(),
		self.cbt_toComma.GetValue(),
		self.cbt_toWeatherEffects.GetValue(),
		self.ch_vol.GetSelection(),
		self.defaultString
		)


	def OnDetails(self, evt):
		"""Displays information on the selected city"""
		value = self.cbx.GetValue()
		encoded_value = value
		if _pyVersion == 2: encoded_value = value.encode("mbcs")
		code = Shared().GetZipCode(value)
		if encoded_value in self.zipCodesList and not code.isdigit():
			self.Yahoo_API_error(code, True)
			return self.cbx.SetFocus()
		elif "ramdetails_dic" in globals() and code in ramdetails_dic:
			city, region, country, country_acronym, timezone_id, latitude, longitude = self.GetFieldsValues(ramdetails_dic, code)
		elif code in self.details_dic:
			city, region, country, country_acronym, timezone_id, latitude, longitude = self.GetFieldsValues(self.details_dic, code)
			if city == 'fail':
				#read data
				connect, n = Shared().ParseEntry(code)
				if connect == "no connect":
					Shared().Play_sound("warn", 1)
					ui.message(_("Sorry, i can not receive data, verify that your internet connection is active, or try again later!"))
					return self.cbx.SetFocus()

				if "ramdetails_dic" in globals() and code in ramdetails_dic:
					self.details_dic.update(ramdetails_dic)
					city, region, country, country_acronym, timezone_id, latitude, longitude = self.GetFieldsValues(self.details_dic, code)

		else:
			if not code in self.details_dic:
				connect, n = Shared().ParseEntry(code)
				if connect == "no connect":
					Shared().Play_sound("warn", 1)
					ui.message(_("Sorry, i can not receive data, verify that your internet connection is active, or try again later!"))
					return self.cbx.SetFocus()

				if "ramdetails_dic" in globals() and code in ramdetails_dic:
					self.details_dic.update(ramdetails_dic)
					Shared().Play_sound(True, 1)
					self.modifiedList = True
					ui.message(_("The details of this city are not in the database and so I added them to the list. Try again!"))
				else:
					self.Yahoo_API_error(code)
					return self.cbx.SetFocus()

			else:
				Shared().Play_sound("warn", 1)
				ui.message(_("Cannot identify your location, due to insufficient data."))
			return self.cbx.SetFocus()

		ui.message(_("Please wait..."))
		current_hour, dst_starts, dst_ends = Shared().GetTimezone(country_acronym, region, city, self.to24Hours, full = True)
		if not current_hour:
			#probable non-codable city
			current_hour, dst_starts, dst_ends = Shared().GetTimezone(country_acronym, region, region, self.to24Hours, full = True)

		lat = lon = ''
		if latitude: lat = (math.ceil(float(latitude)*100)/100)
		if longitude: lon = (math.ceil(float(longitude)*100)/100)
		elevation = Shared().GetElevation(latitude, longitude)
		if elevation is None:
			#try with rounded coordinates
			elevation = Shared().GetElevation(lat, lon)

		if elevation is None:elevation = _nr
		elif elevation == "no connect":
			Shared().Play_sound("warn", 1)
			ui.message(_("Sorry, i can not receive data, verify that your internet connection is active, or try again later!"))
			return self.cbx.SetFocus()

		dst = city_details = ""
		if not value[-4:].startswith(','):
			city_name = value[:-2] #usny = us
			real_city_name = '%s, %s' % (city, country_acronym)

		city_details = self.FindForGeoName(real_city_name, city_name, latitude, longitude)
		if not city_details: city_details = '%s, %s, %s, %s' % (city, region, country, country_acronym)
		city_details += ', %s' % timezone_id
		if dst_starts:
			#if there is daylight saving time
			dst = "%s:" % _("Daylight saving time")
			action_dic = {"ahead": _("ahead"), "back": _("back")}
			date, time, action, hours = Shared().Get_dst(self.to24Hours, dst_starts)
			dst +="\r\n%s %s %s %s, %s %s %s %s." % (
			_("Starts on"), date, _("at"), time, _("set your clock"), hours, _("hour"), action_dic[action])
			date, time, action, hours = Shared().Get_dst(self.to24Hours, dst_ends)
			dst += "\r\n%s %s %s %s, %s %s %s %s." % (
			_("Ends on"), date, _("at"), time, _("set your clock"), hours, _("hour"), action_dic[action])

		Shared().Play_sound("details", 1)
		title = "%s %s" % (_("Details of"), value)
		ui.message(title)
		message = "%s: %s.\r\n%s: %s.\r\n%s: %s\r\n%s: %s.\r\n%s: %s %s." % (
		_("Place"), city_details or _nr,
		_("Current local time"), current_hour or _nr,
		_("Degrees latitude"), lat or _nr,
		_("Degrees longitude"), lon or _nr,
		_("Elevation above sea level"), elevation, _("meters"))
		message += "\r\n%s" % dst or ""
		ui.message(message) 
		self.cbx.SetFocus()
		if self.toClip:
			# Copy the city details to the clipboard.
			import api
			api.copyToClip('%s\r\n%s' % (title, message))


	def OnDefine(self, evt):
		"""Define the area of the current city"""
		code = Shared().GetZipCode(self.cbx.GetValue())
		city = self.cbx.GetValue()
		def_define = 0
		if code in self.define_dic: def_define = int(self.define_dic[code])
		Shared().Play_sound("subwindow", 1)
		dl = wx.SingleChoiceDialog(
		self, '%s: "%s"' % (
		_("Define the area for"), city),
		_addonSummary,
		choices=[
		_("Hinterland"),
		_("Maritime area"),
		_("Desert zone"),
		_("Arctic zone"),
		_("Mountain zone")])
		dl.SetSelection(def_define)
		if dl.ShowModal() == wx.ID_CANCEL:
			dl.Destroy()
			return Shared().Play_sound("subwindow", 1)

		define = str(dl.GetSelection())
		if define != str(def_define):
			self.modifiedList = True
			if code in self.define_dic: self.define_dic[code] = define
			else: self.define_dic.update({code: define})
			Shared().Play_sound(True)
		dl.Destroy()
		Shared().Play_sound("winclose", 1)


	def GetFieldsValues(self, dic_type, code):
		"""returns the fields values of the current city from the record"""
		return(
		dic_type[code]['city'],
		dic_type[code]['region'],
		dic_type[code]['country'],
		dic_type[code]['country_acronym'],
		dic_type[code]['timezone_id'],
		dic_type[code]['lat'],
		dic_type[code]['lon'])


	def FindForGeoName(self, real_city_name, city_name, latitude, longitude):
		"""Retrieve details from geo name with geographic coordinates"""
		def SplitName(c):
			#separates the city from the state
			return c.split(',')[0], c.split(',')[-1].lstrip(' ')

		def GetGeo(city, acronym):
			return Shared().GetGeoName(city, lat = latitude, lon = longitude, acronym=acronym)

		def ParseName(name):
			city, acronym = SplitName(name)
			city_details = GetGeo(city, acronym)
			if not city_details:
				#try separating the name
				city = city.replace("-", " ")
				city = city.replace("_", " ")
				city_details = GetGeo(city, acronym)
				if not city_details:
					city, acronym = SplitName(name)
					#try by splitting the name
					city1 = city.split(' ')
					for city in city1:
						city_details = GetGeo(city, acronym) 
						if city_details: break

					if not city_details:
						#try to join the name
						city, acronym = SplitName(name)
						city = city.replace(" ", "-")
						city_details = GetGeo(city, acronym) 

			return city_details

		#try with the real city name 
		city_details = ParseName(real_city_name)
		if not city_details and city_name != real_city_name:
			#try with the name given by the user
			city_details = ParseName(city_name)

		if city_details: return '%s, %s' % (SplitName(real_city_name)[0], city_details)


	def OnAdd(self, evt):
		"""Add city button event"""
		value = self.cbx.GetValue()
		encoded_value = value
		if _pyVersion == 2: encoded_value = value.emcode("mbcs")
		if encoded_value not in self.zipCodesList:
			v = Shared().GetZipCode(value)

			if self.testName: value2 = '%s %s' % (self.testName.capitalize(), v.upper())
			else: value2 = self.tempZipCode
			double, name, v1 = self.CheckName(value2, value)
			if double:
				result = self.Warning(self.testName,v1,  v)
				if result == wx.ID_CANCEL: return self.cbx.SetFocus()
				elif result == wx.ID_NO:
					value = name
				else: value = value2

			elif name == value2: value = value2
			else: value = name
			if _pyVersion == 2:
				try:
					value = value.encode("mbcs")
				except (UnicodeEncodeError, UnicodeDecodeError): pass

			self.zipCodesList.append(value)
			self.zipCodesList.sort()
			#add define if is a apixu value
			if self.apixuValue:
				self	.define_dic.update({v: self.apixuValue[-2:][-1]})

			#adds cities details
			if "ramdetails_dic" in globals() and str(v) in ramdetails_dic:
				self.details_dic.update({v: ramdetails_dic[v]})
			self.ComboSet(value, True)
			self.testCode = self.testName = ''
			Shared().Play_sound("add", 1)
			self.cbx.SetFocus()
			self.OnText()


	def OnApply(self, evt):
		"""Apply predefined city button event"""
		value = self.cbx.GetValue()
		encoded_value = value
		if _pyVersion == 2: encoded_value = value.encode("mbcs")
		if encoded_value not in self.zipCodesList:
			v = Shared().GetZipCode(value)

			if self.testName: value2 = '%s %s' % (self.testName.capitalize(), v.upper())
			else: value2 = self.tempZipCode
			double, name, v1 = self.CheckName(value2, value)
			if double:
				result = self.Warning(self.testName,v1,  v)
				if result == wx.ID_CANCEL: return self.cbx.SetFocus()
				elif result == wx.ID_NO:
					value = name
				else: value = value2

			elif name == value2: value = value2
			else: value = name
			if _pyVersion == 2:
				try:
					value = value.encode("mbcs")
				except (UnicodeEncodeError, UnicodeDecodeError): pass

			self.zipCodesList.append(value)
			self.zipCodesList.sort()
			#add define if is a apixu value
			if self.apixuValue:
				self	.define_dic.update({v: self.apixuValue[-2:][-1]})

			#adds cities details
			if "ramdetails_dic" in globals() and str(v) in ramdetails_dic:
				self.details_dic.update({v: ramdetails_dic[v]})

			self.testName = self.testCode = ''
			self.ComboSet(value, True)

		self.defaultZipCode = value
		self.cbx.SetFocus()
		Shared().Play_sound("apply", 1)
		self.OnText()
		self.btn_Ok.Enable(True)
		self.ReTitle(self.defaultZipCode)


	def OnRemove(self, evt = None):
		"""Remove the city from cities list button event"""
		value = self.cbx.GetValue()
		encoded_value = value
		if _pyVersion == 2: encoded_value = value.encode("mbcs")
		if encoded_value in self.zipCodesList:
			index = self.GetIndex(value, self.zipCodesList)
			self.zipCodesList.remove(encoded_value)
			if value == self.defaultZipCode:
				self.defaultZipCode = ""
				self.ReTitle(_("None"))
				self.btn_Apply.Enable(True)

			self.cbx.Delete(index)
			self.cbx.SetValue('')
			try:
				if len(self.zipCodesList) == 0: self.ComboSet('')
				elif index == len(self.zipCodesList): self.ComboSet(self.zipCodesList[-1])
				else: self.ComboSet(self.zipCodesList[index])
			except IndexError: pass

			#Remove city definition and city details
			code = Shared().GetZipCode(value)
			if code in self.define_dic: del self.define_dic[code]
			if code in self.details_dic: del self.details_dic[code]
			Shared().Play_sound("del", 1)
			self.OnText()


	def OnRename(self, evt):
		"""rename the city selected"""
		value = self.cbx.GetValue()
		name = value.split(', ')[0]
		part_right = value.split(', ')[-1]
		Shared().Play_sound("subwindow", 1)
		dl = wx.TextEntryDialog(self,
		_("Enter new name."),
		_addonSummary,
		name)
		if dl.ShowModal() == wx.ID_OK:
			new_name = '%s, %s' % (dl.GetValue().lstrip(' ').rstrip(' ').capitalize(), part_right)
			encoded_new_name = new_name
			if _pyVersion == 2: encoded_new_name = new_name.encode("mbcs")
			if encoded_new_name in self.zipCodesList:
				if value != new_name: wx.MessageBox('%s %s' % (new_name, _("it can't be used because it already exists!")), '%s %s' % (_addonSummary, _("Notice!")), wx.ICON_EXCLAMATION)
			else:
				index = self.GetIndex(value, self.zipCodesList)
				self.zipCodesList[index] = encoded_new_name
				self.cbx.Delete(index)
				self.zipCodesList.sort()
				#update combobox
				self.ComboSet(new_name, True)
				if value == self.defaultZipCode:
					self.defaultZipCode = new_name
					self.ReTitle(_(new_name))

				Shared().Play_sound(True)

		dl.Destroy()
		Shared().Play_sound("subwindow", 1)


	def GetIndex(self, v, l):
		"""Get position of item in list"""
		try:
			i = l.index(v.encode("mbcs"))
		except ValueError:
			try:
				i = l.index(v)
			except ValueError: return None

		return i


	def ReTitle(self, s):
		"""Change title window"""

		t = self.GetLabel()
		if _pyVersion == 2:
			try:
				s = s.decode("mbcs")
			except (UnicodeEncodeError, UnicodeDecodeError): pass

		title = '%s: %s)' %(t[:t.find(':')], s)
		self.SetLabel(title)


	def CheckName(self, city, value):
		"""Check if there is the same name in the list"""
		double = False
		part_left = ''
		if ',' in value:
			part_left = value[:value.find(',')] #City name
			state = value.split()
			try:
				state = state[-2]
			except IndexError:
				try:
					state = state[-1]
				except IndexError: state = ''

			if len(state) == 2 or len(state) == 4:
				value = '%s, %s' % (part_left, state) #City name, state
		else:
			part_left = value[:-len(value.split()[-1])-1] #City name
			part_right = value.split()[-1]
			m = ''
			if part_right.isdigit():
				#Search for ID
				part_left = value[:-len(part_right)-1]
			else:
				#Search for yahoo old zip codes
				try:
					m = re.search('[A-Za-z]{4}[0-9]{4}', part_right).group()
				except AttributeError: pass
				if m: part_left = value[:-len(part_right)]
				else: part_left = value

		current = city[city.find(','):] #, it XXXXXXXX
		#Searc for state (2 or 4 caracters)
		m = ''
		try:
			m=re.search(', [a-zA-Z]{2, 4}', part_left).group()
		except AttributeError: pass
		if m: part_left = part_left[:part_left.find(m)]
		if not part_left: name = '%s%s' % (city[0].upper(), city[1:])
		else: name = '%s%s' % (part_left.capitalize(), current)

		value = name[:-len(name.split()[-1])-1]
		for zc in self.zipCodesList:
			part = zc[:-len(zc.split()[-1])-1]
			if _pyVersion == 2: part = part.decode("mbcs")
			if part == value:
				double = True
				break
		return double, name, value


	def Warning(self, cityName, name, v):
		"""Proposes an alternative name, but by offering the correct name"""

		winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		dl =wx.MessageDialog(self, '%s "%s" %s.\n%s "%s" %s.\n%s\n%s "%s".\n%s' % (
		_("The woeID"), v, _("is correct"),
		_("But the name"),
		name,
		_("already exists"),
		_("You have to change it!"),
		_("The city proper is"),
		cityName.rstrip(','),
		_("Want to use the suggested name?")),
		'%s %s' % (_addonSummary, _("Notice!")),
		wx.YES_NO |wx.CANCEL| wx.ICON_QUESTION)
		result = dl.ShowModal()
		dl.Destroy()
		return result


	def OnImport(self, evt):
		"""Import data from a file Weather.zipcodes"""

		dlg = wx.FileDialog(self,
		_("Import cities"),
		defaultDir = os.path.expanduser('~/~'),
		defaultFile = 'Weather.zipcodes',
		wildcard = '%s, %s' % (_addonSummary, '*.zipcodes|*.ZIPCODES'),
		style = wx.FD_DEFAULT_STYLE
		|wx.FD_FILE_MUST_EXIST
		)
		dlg.SetFilterIndex(0)
		if dlg.ShowModal() == wx.ID_CANCEL:
			dlg.Destroy()
			return evt.GetEventObject().SetFocus()

		#Open the file
		file = dlg.GetPath()
		dlg.Destroy()
		zipCodesList = list(self.zipCodesList)
		z, define_dic, details_dic = Shared().LoadZipCodes(file)
		#Erasing invalid lines from data file
		title = '%s %s' % (_addonSummary, os.path.basename(file))
		zImport = Shared().Check_content(z, title)
		del z
		if not zImport or len(zImport) == 0:
			return evt.GetEventObject().SetFocus()

		if self.zipCodesList:
			#Allows you to choose the import mode
			message = '%s\n%s\n%s' % (
			_("Do you want to replace your list with this?"),
			_("If you select yes, your list will be completely replaced."),
			_("If you select no, the new cities will be added to your list.")
			)
			title = '%s - %s' % (_addonSummary, _("Select import mode"))
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			if wx.MessageBox(message, title, wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION) == 2:
				#the list is totally replaced
				zipCodesList = []
				self.zipCodesList = []

		#It allows you to select the contents of the file
		Shared().Play_sound("subwindow", 1)
		dlg = SelectImportDialog(gui.mainFrame,
		title = '%s - %d %s' % (
		_("File contents"), len(zImport),
		_("cities")),
				zip_list = zImport,
checkbox_values = [],
		message = _("Activate the check boxes of the cities you want to import.")
		)

		if dlg.ShowModal() == wx.ID_CANCEL:
			dlg.Destroy()
			Shared().Play_sound("subwindow", 1)
			return evt.GetEventObject().SetFocus()

		item_selected = dlg.GetValue()
		dlg.Destroy()
		Shared().Play_sound("winclose", 1)
		ti = td = tr = 0 #total imported, total duplicates, total errors
		tl = len(zImport)
		lis = len(item_selected)
		mis = item_selected[-1] # max value
		item_selected.reverse()
		#get WoeId displayed in the combo box
		zc1 = ""; v = self.cbx.GetValue(); found = False
		if v: zc1 = Shared().GetZipCode(v)
		max = 100
		dl = wx.ProgressDialog(
		_("Importing cities in progress"),
		_("Please wait..."),
		maximum = max,
		parent=self,
		style = 0
		| wx.PD_APP_MODAL
		| wx.PD_AUTO_HIDE
		)

		keepGoing = True
		count = 0
		while keepGoing and count < max:
			if len(item_selected) != 0:
				c = item_selected.pop()
				i = zImport[c]
				t, zc, n = Shared().ZipCodeInList(i, self.zipCodesList)
				encoded_v = v; encoded_defaultZipCode = self.defaultZipCode
				if _pyVersion == 2: encoded_v = v.encode("mbcs"); encoded_defaultZipCode = self.defaultZipCode.encode("mbcs")
				if zc1 == zc and i == encoded_v and i == encoded_defaultZipCode:
					#The WoeId found in the list it's set to default
					found = True

				if not t:
					if len(zc) == 8 or zc.isdigit():
						#update the cities list
						zipCodesList.append(i)
						if zc in define_dic:
							#updates the cities definitions
							self.define_dic.update({zc: define_dic[zc]})
						if zc in details_dic:
							#update the cities details
							self.details_dic.update({zc: details_dic[zc]})

						ti += 1
					else: tr += 1

				else: td += 1

			try:
				count = c*100/mis
			except ZeroDivisionError: count = max
			wx.MilliSleep(200)
			wx.Yield()
			keepGoing = dl.Update(count)
		dl.Destroy()
		#Refresh cities list in the combobox
		if ti:
			self.zipCodesList = list(sorted(zipCodesList))
			self.cbx.Clear()
			if _pyVersion >= 3:
				self.cbx.Append(self.zipCodesList)
			else:
				[self.cbx.Append(i.decode("mbcs")) for i in self.zipCodesList]
			self.ComboSet(v)
			if found:
				if _pyVersion >= 3:
					self.defaultZipCode = self.tempZipCode = v
				else:
					try:
						self.defaultZipCode = self.tempZipCode = v.decode("mbcs")
					except (UnicodeEncodeError, UnicodeDecodeError):
						self.defaultZipCode = self.tempZipCode = v

				self.OnText()
				self.ReTitle(self.defaultZipCode)

			else:
				self.cbx.SetValue(v); self.OnText()
				if encoded_v not in zipCodesList:
					self.cbx.SetValue("")
					if v == self.defaultZipCode: self.ReTitle(_("None"))

		wx.MessageBox(
		'%s: %d %s.\n%s: %d.\n%s: %d.\n%s: %d.' % (
		_("Were added"), ti, _("new cities to the list"),
		_("Have been ignored because existing"), td,
		_("Content of imported list"), tl-tr,
		_("selected by the user"), lis),
		'%s - %s' % (_addonSummary, _("Import finished")), wx.ICON_INFORMATION)
		evt.GetEventObject().SetFocus()


	def OnExport(self, evt):
		"""Export file Weather.zipcodes"""

		file = "Weather.zipcodes"
		if self.modifiedList:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			if wx.MessageBox('%s "%s" %s\n%s\n%s' % (
			_("A copy of"),
			file,
			_("It will be exported"),
			_("But it does not yet contain the changes you just made the list!"),
			_("I proceed?")),
			'%s - %s' % (_addonSummary, _("Notice!")), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == 8:
				return evt.GetEventObject()

		dlg = wx.FileDialog(self,
		_("Export cities"),
		defaultFile=file,
		wildcard = '%s, %s' % (_addonSummary, '*.zipcodes|*.ZIPCODES'),
		style = wx.FD_SAVE
		| wx.FD_OVERWRITE_PROMPT
		)
		dlg.SetFilterIndex(0)
		if dlg.ShowModal() == wx.ID_CANCEL:
			dlg.Destroy()
			return evt.GetEventObject().SetFocus()

		#Export a copy of Weather.zipcodes
		destPath = dlg.GetPath()
		dlg.Destroy()
		if  destPath == _zipCodes_path:
			wx.MessageBox(_("You can not export the same file at the same path!"), '%s - %s' % (_addonSummary, _("Notice!")), wx.ICON_EXCLAMATION)
			return evt.GetEventObject()
		wx.CallAfter(ui.message, _("Please wait..."))
		if os.path.isfile(_zipCodes_path):
			import shutil 
			try:
				shutil .copy(_zipCodes_path, destPath)
				winsound.MessageBeep(winsound.MB_ICONASTERISK)
			except Exception as e:
				Shared().SendToLog(e)
				return Shared().WriteError(_addonSummary)
			evt.GetEventObject().SetFocus()


	def ComboSet(self, v, add = None):
		"""Update choices List ComboBox"""
		if _pyVersion == 2:
			try:
				v = v.decode("mbcs")
			except (UnicodeEncodeError, UnicodeDecodeError): pass

		if add:
			i = self.GetIndex(v, self.zipCodesList)
			if i == None: i = 0
			self.cbx.Insert(v, i)

		self.cbx.SetStringSelection(v)
		if not v: self.cbx.SetValue('')
		self.modifiedList = True
		self.cbx.SetFocus()


class Shared:
	"""Global functions"""
	def SendToLog(self, e):
		if _pyVersion == 2: log.info('%s %s: %s' % (_addonSummary, _addonVersion, str(e).decode("mbcs")))
		else: log.info('%s %s: %s' % (_addonSummary, _addonVersion, str(e)))


	def GetCoords(self, v):
		"""Checks if the value contains the geographic coordinates"""
		try:
			m = re.search('-*\d+\.\d+(,|, )-*\d+\.\d+', v).group()
		except AttributeError: return None
		return m


	def GetAcronym(self, value):
		"""converts country in acronym with two caracters"""
		#difficult countries
		p =[
		(re.compile('''C.+te d.+Ivoire'''), 'CI')
		]

		def FindOsticCountry(pattern, v):
			try:
				if re.search(pattern, v): return True
			except AttributeError: return None

		for r in p:
			if FindOsticCountry(r[0], value): return r[1]

		value = value.upper()
		acronym_dic = {
		'AFGHANISTAN': 'AF',
		'ALBANIA': 'AL',
		'ALGERIA': 'DZ',
		'AMERICAN SAMOA': 'AS',
		 'ANDORRA': 'AD',
		 'ANGOLA': 'AO',
		'ANGUILLA': 'AI',
		'ANTARCTICA': 'AQ',
		'ANTIGUA AND BARBUDA': 'AG',
		'ARGENTINA': 'AR',
		'ARMENIA': 'AM',
		'ARUBA': 'AW',
		'AUSTRALIA': 'AU',
		'AUSTRIA': 'AT',
		'AZERBAIJAN': 'AZ',
		'THE BAHAMAS': 'BS',
		'BAHAMAS': 'BS',
		'BAHRAIN': 'BH',
		'BANGLADESH': 'BD',
		'BARBADOS': 'BB',
		'BELARUS': 'BY',
		'BELGIUM': 'BE',
		'BELIZE': 'BZ',
		'BENIN': 'BJ',
		'BERMUDA': 'BM',
		'BHUTAN': 'BT',
		'BOLIVIA': 'BO',
		'BOSNIA AND HERZEGOVINA': 'BA',
		'BOTSWANA': 'BW',
		'BOUVET ISLAND': 'BV',
		'BRAZIL': 'BR',
		'BRITISH INDIAN OCEAN TERRITORY': 'IO',
		'BRUNEI': 'BN',
		'BRUNEI DARUSSALAM': 'BN',
		'BULGARIA': 'BG',
		'BURKINA FASO': 'BF',
		'BURUNDI': 'BI',
		'CAMBODIA': 'KH',
		'CAMEROON': 'CM',
		'CANADA': 'CA',
		'CAPE VERDE': 'CV',
		'CAYMAN ISLANDS': 'KY',
		'CENTRAL AFRICAN REPUBLIC': 'CF',
		'CHAD': 'TD',
		'CHILE': 'CL',
		'CHINA': 'CN',
		'CHRISTMAS ISLAND': 'CX',
		'COCOS (KEELING) ISLANDS': 'CC',
		'COLOMBIA': 'CO',
		'COMOROS': 'KM',
		'CONGO': 'CG',
		'DEMOCRATIC REPUBLIC OF CONGO': 'CD',
		'COOK ISLANDS': 'CK',
		'COSTA RICA': 'CR',
		'IVORY COAST': 'CI',
		'''CÔTE D'IVOIRE''': 'CI',
		'''COTE D'IVOIRE''': 'CI',
		'CROATIA': 'HR',
		'CUBA': 'CU',
		'CYPRUS': 'CY',
		'CZECH REPUBLIC': 'CZ',
		'CZECHIA': 'CZ',
		'DENMARK': 'DK',
		'DJIBOUTI': 'DJ',
		'DOMINICA': 'DM',
		'DOMINICAN REPUBLIC': 'DO',
		'ECUADOR': 'EC',
		'EGYPT': 'EG',
		'EL SALVADOR': 'SV',
		'EQUATORIAL GUINEA': 'GQ',
		'ERITREA': 'ER',
		'ESTONIA': 'EE',
		'ETHIOPIA': 'ET',
		'FALKLAND ISLANDS (MALVINAS)': 'FK',
		'FAROE ISLANDS': 'FO',
		'FIJI ISLANDS': 'FJ',
		'FIJI': 'FJ',
		'FINLAND': 'FI',
		'FRANCE': 'FR',
		'FRENCH GUIANA': 'GF',
		'FRENCH POLYNESIA': 'PF',
		'FRENCH SOUTHERN TERRITORIES': 'TF',
		'GABON': 'GA',
		'THE GAMBIA': 'GM',
		'GAMBIA': 'GM',
		'GEORGIA': 'GE',
		'GERMANY': 'DE',
		'GHANA': 'GH',
		'GIBRALTAR': 'GI',
		'GREECE': 'GR',
		'GREENLAND': 'GL',
		'GRENADA': 'GD',
		'GUADELOUPE': 'GP',
		'GUAM': 'GU',
		'GUATEMALA': 'GT',
		'GUERNSEY': 'GG',
		'GUINEA': 'GN',
		'GUINEA-BISSAU': 'GW',
		'GUYANA': 'GY',
		'HAITI': 'HT',
		'HEARD ISLAND AND MCDONALD ISLANDS': 'HM',
		'HONDURAS': 'HN',
		'HONG KONG': 'HK',
		'HUNGARY': 'HU',
		'ICELAND': 'IS',
		'INDIA': 'IN',
		'INDONESIA': 'ID',
		'IRAN': 'IR',
		'IRAQ': 'IQ',
		'ISLE OF MAN': 'IM',
		'IRELAND': 'IE',
		'ISRAEL': 'IL',
		'ITALY': 'IT',
		'JAMAICA': 'JM',
		'JAPAN': 'JP',
		'JERSEY': 'JE',
		'JORDAN': 'JO',
		'KAZAKHSTAN': 'KZ',
		'KENYA': 'KE',
		'KIRIBATI': 'KI',
		'''KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF''': 'KP',
		'NORTH KOREA': 'KP',
		'KOREA, REPUBLIC OF': 'KR',
		'SOUTH KOREA': 'KR',
		'KOSOVO': 'XZ',
		'KUWAIT': 'KW',
		'KYRGYZSTAN': 'KG',
		'KYRGHYZSTAN': 'KG',
		'LAOS': 'LA',
		'''LAO PEOPLE'S DEMOCRATIC REPUBLIC''': 'LA',
		'LATVIA': 'LV',
		'LEBANON': 'LB',
		'LESOTHO': 'LS',
		'LIBERIA': 'LR',
		'LIBYA': 'LY',
		'LIBYAN ARAB JAMAHIRIYA': 'LY',
		'LIECHTENSTEIN': 'LI',
		'LITHUANIA': 'LT',
		'LUXEMBOURG': 'LU',
		'MACAO': 'MO',
		'MACEDONIA': 'MK',
		'MADAGASCAR': 'MG',
		'MALAWI': 'MW',
		'MALAYSIA': 'MY',
		'MALDIVES': 'MV',
		'MALI': 'ML',
		'MALTA': 'MT',
		'MARSHALL ISLANDS': 'MH',
		'MARTINIQUE': 'MQ',
		'MAURITANIA': 'MR',
		'MAURITIUS': 'MU',
		'MAYOTTE': 'YT',
		'MEXICO': 'MX',
		'MICRONESIA': 'FM',
		'MOLDOVA': 'MD',
		'MONACO': 'MC',
		'MONGOLIA': 'MN',
		'MONTENEGRO': 'ME',
		'MONTSERRAT': 'MS',
		'MOROCCO': 'MA',
		'MOZAMBIQUE': 'MZ',
		'MYANMAR': 'MM',
		'NAMIBIA': 'NA',
		'NAURU ISLAND': 'NR',
		'NAURU': 'NR',
		'NEPAL': 'NP',
		'NETHERLANDS': 'NL',
		'NETHERLANDS ANTILLES': 'AN',
		'NEW CALEDONIA': 'NC',
		'NEW ZEALAND': 'NZ',
		'NICARAGUA': 'NI',
		'NIGER': 'NE',
		'NIGERIA': 'NG',
		'NIUE': 'NU',
		'NORFOLK ISLAND': 'NF',
		'NORTHERN MARIANA ISLANDS': 'MP',
		'NORWAY': 'NO',
		'OMAN': 'OM',
		'PAKISTAN': 'PK',
		'PALAU': 'PW',
		'PALESTINIAN TERRITORY, OCCUPIED': 'PS',
		'PANAMA': 'PA',
		'PAPUA NEW GUINEA': 'PG',
		'PARAGUAY': 'PY',
		'PERU': 'PE',
		'PHILIPPINES': 'PH',
		'PITCAIRN': 'PN',
		'POLAND': 'PL',
		'PORTUGAL': 'PT',
		'PUERTO 	RICO': 'PR',
		'QATAR': 'QA',
		'RʕNION': 'RE',
		'ROMANIA': 'RO',
		'RUSSIAN FED		ERATION': 'RU',
		'RUSSIA': 'RU',
		'RWANDA': 'RW',
		'RÉUNION': 'RE',
		'SAINT HELENA': 'SH',
		'SAINT KITTS AND NEVIS': 'KN',
		'ST. LUCIA': 'LC',
		'SAINT LUCIA': 'LC',
		'SAINT PIERRE AND MIQUELON': 'PM',
		'SAINT VINCENT AND THE GRENADINES': 'VC',
		'SAMOA': 'WS',
		'SAN MARINO': 'SM',
		'SAO TOME AND PRINCIPE': 'ST',
		'SAUDI ARABIA': 'SA',
		'SENEGAL': 'SN',
		'SERBIA AND MONTENEGRO': 'YU',
		'SERBIA': 'RS',
		'SEYCHELLES': 'SC',
		'SEYCHELLES ISLANDS': 'SC',
		'SIERRA LEONE': 'SL',
		'SINGAPORE': 'SG',
		'SLOVAKIA': 'SK',
		'SLOVENIA': 'SI',
		'SOLOMON ISLANDS': 'SB',
		'SOMALIA': 'SO',
		'SOUTH AFRICA': 'ZA',
		'SOUTH GEORGIA AND SOUTH SANDWICH ISLANDS': 'GS',
		'SPAIN': 'ES',
		'SRI LANKA': 'LK',
		'SUDAN': 'SD',
		'SOUTH SUDAN': 'SS',
		'SURINAME': 'SR',
		'SVALBARD': 'SJ',
		'SVALBARD AND JAN MAYEN': 'SJ',
		'SWAZILAND': 'SZ',
		'SWEDEN': 'SE',
		'SWITZERLAND': 'CH',
		'SYRIAN ARAB REPUBLIC': 'SY',
		'SYRIA': 'SY',
		'TAIWAN, PROVINCE OF CHINA': 'TW',
		'TAIWAN': 'TW',
		'TAJIKISTAN': 'TJ',
		'TANZANIA': 'TZ',
		'THAILAND': 'TH',
		'EAST TIMOR': 'TL',
		'TIMOR-LESTE': 'TL',
		'TOGO': 'TG',
		'TOKELAU': 'TK',
		'TONGA': 'TO',
		'TRINIDAD AND TOBAGO': 'TT',
		'TUNISIA': 'TN',
		'TURKEY': 'TR',
		'TURKMENISTAN': 'TM',
		'TURKS AND CAICOS ISLANDS': 'TC',
		'TUVALU': 'TV',
		'UGANDA': 'UG',
		'UKRAINE': 'UA',
		'UNITED ARAB EMIRATES': 'AE',
		'UNITED KINGDOM': 'GB',
		'UK': 'GB',
		'UNITED STATES': 'US',
		'UNITED STATES MINOR OUTLYING ISLANDS': 'UM',
		'URUGUAY': 'UY',
		'UZBEKISTAN': 'UZ',
		'VANUATU': 'VU',
		'VATICAN CITY': 'VA',
		'VIET NAM': 'VN',
		'VIETNAM': 'VN',
		'VIRGIN ISLANDS, BRITISH': 'VG',
		'VIRGIN ISLANDS, U.S.': 'VI',
		'U.S. VIRGIN ISLANDS': 'VI',
		'WALLIS AND FUTUNA': 'WF',
		'VENEZUELA': 'VE',
		'ÅLAND': 'AX',
		'ƌAND': 'AX',
		'WESTERN SAHARA': 'EH',
		'YEMEN': 'YE',
		'ZIMBABWE': 'ZW',
		'ZAMBIA': 'ZM',
		#US regions
		'AGUASCALIENTES': 'AG',
		'ALABAMA': 'AL',
		'ALASKA': 'AK',
		'AMERICAN SAMOA': 'AS',
		'ARIZONA': 'AZ',
		'ARKANSAS': 'AR',
		'BAJA CALIFORNIA': 'BN',
		'BAJA CALIFORNIA SUR': 'BS',
		'CALIFORNIA': 'CA',
		'CAMPECHE': 'CM',
		'CHIAPAS': 'CP',
		'CHIHUAHUA': 'CH',
		'COLIMA': 'CL',
		'COLORADO': 'CO',
		'CONNECTICUT': 'CT',
		'DELAWARE': 'DE',
		'DISTRITO FEDERAL': 'DF',
		'DISTRICT OF COLUMBIA': 'DC',
		'DURANGO': 'DU',
		'FAR SOUTH REGION': 'FS',
		'FEDERATED STATES OF MICRONESIA': 'FM',
		'FLORIDA': 'FL',
		'GEORGIA': 'GA',
		'GUANAJUATO': 'GJ',
		'GUAM': 'GU',
		'GUERRERO': 'GR',
		'HAWAII': 'HI',
		'HIDALGO': 'HI',
		'IDAHO': 'ID',
		'ILLINOIS': 'IL',
		'INDIANA': 'IN',
		'IOWA': 'IA',
		'KANSAS': 'KS',
		'KENTUCKY': 'KY',
		'JALISCO': 'JA',
		'LOUISIANA': 'LA',
		'MAINE': 'ME',
		'MARSHALL ISLANDS': 'MH',
		'MARYLAND': 'MD',
		'MASSACHUSETTS': 'MA',
		'MICHIGAN': 'MI',
		'MICHOAC': 'MC',
		'MINNESOTA': 'MN',
		'MISSISSIPPI': 'MS',
		'MISSOURI': 'MO',
		'MONTANA': 'MT',
		'MORELOS': 'MR',
		'NAYARIT': 'NA',
		'NORTHWEST REGION': 'NW',
		'NUEVO LEԎ': 'NL',
		'COAHUILA': 'CA',
		'NEBRASKA': 'NE',
		'NEVADA': 'NV',
		'NEW HAMPSHIRE': 'NH',
		'NEW JERSEY': 'NJ',
		'NEW MEXICO': 'NM',
		'NEW YORK': 'NY',
		'NORTH CAROLINA': 'NC',
		'NORTH DAKOTA': 'ND',
		'N. DAKOTA': 'ND',
		'NORTHERN MARIANA ISLANDS': 'MP',
		'OHIO': 'OH',
		'OAXACA': 'OA',
		'OKLAHOMA': 'OK',
		'OREGON': 'OR',
		'PALAU': 'PW',
		'PENNSYLVANIA': 'PA',
		'PUEBLA': 'PU',
		'PUERTO RICO': 'PR',
		'QUERʔARO': 'QE',
		'QUINTANA ROO': 'QR',
		'RHODE ISLAND': 'RI',
		'SAN LUIS POTOSÌ': 'SL',
		'SINALOA': 'SI',
		'SOUTHEAST REGION': 'SE',
		'SOUTH CAROLINA': 'SC',
		'SOUTH DAKOTA': 'SD',
		'S. DAKOTA': 'SD',
		'SONORA': 'SO',
		'SOUTHWEST REGION': 'SW',
		'TABASCO': 'TB',
		'TAMAULIPAS': 'TM',
		'TENNESSEE': 'TN',
		'TEXAS': 'TX',
		'TLAXCALA': 'TL',
		'UTAH': 'UT',
		'VERACRUZ': 'VE',
		'VERMONT': 'VT',
		'VIRGIN ISLANDS': 'VI',
		'VIRGINIA': 'VA',
		'WASHINGTON': 'WA',
		'WEST VIRGINIA': 'WV',
		'WISCONSIN': 'WI',
		'WYOMING': 'WY',
		'YUCAT': 'YU',
		'ZACATECAS': 'ZA',
		#canada regions
		'ALBERTA': 'AB',
		'BRITISH COLUMBIA': 'BC',
		'MANITOBA': 'MB',
		'NEW BRUNSWICK': 'NB',
		'NEWFOUNDLAND and Labrador': 'NL',
		'NORTHWEST TERRITORIES': 'NT',
		'NORTHEAST REGION': 'NE',
		'NUNAVUT': 'NU',
		'NOVA SCOTIA': 'NS',
		'NUNAVAT TERRITORY': 'NU',
		'ONTARIO': 'ON',
		'PRINCE EDWARD ISLAND': 'PE',
		'QUEBEC': 'QC',
		'SASKATCHEWAN': 'SK',
		'YUKON TERRITORY': 'YT',
		'YUKON': 'YT'
		}
		if value in acronym_dic: return acronym_dic[value]
		elif len(value) > 2: return ""
		return value


	def Get_dst(self, to24Hours, s):
		"""extracts date, time, add/sub total hours from the rough string"""

		dt = s.split()
		if len(dt) != 16: return None, None, None, None
			#translate month
		dt[2] = Shared().Month2Num (dt[2][:3])
		dt[2] = Shared().TranslateCalendar(str(dt[2]).rjust(2, '0'))
		#create date string
		date = '%s %s %s' % (dt[3].rstrip(","), dt[2], dt[4])
		#create time string
		time = '%s %s' % (dt[6], dt[7])
		if to24Hours: time = Shared().To24h(time)
		#get add, or sub action
		action = dt[13]
		#get number hhours to add, or subtract
		hour = dt[14]
		return date, time, action, hour


	def GetAddonBaseUrl(self, data = None):
		"""search addon base url from addon page"""

		if not data:
			data = self.GetUrlData(_addonPage)
			if not data or data == "no connect": return ""

		try:
			abl = re.search('<a href="(http([s]*)://www\..+/[Ww]eather.+\d+(\.\d*)\.nvda-addon)"', data).group(1)
			abm = abl.upper()
			abl = abl[:abm.find('/WEATHER')]
		except: return ""
		return abl


	def Add_zero(self, hour, p = True):
		""" add zero  to left of number with len 1"""

		if p:
			p = hour[-2:] #pm or am
			hour = hour[:-3] # hour and minute

		m = hour[hour.find(':')+1:] #minute
		t = '%s:%s' % (hour[:hour.find(':')].rjust(2, '0'), m.rjust(2, '0'))
		if p: return '%s %s' % (t, p)
		return t


	def To24h(self, hour, viceversa = None):
		"""Convert from 12 to 24 hours and viceversa"""
		if 'datetime.datetime' in str(type(hour)):
			#datetime format get from lastbuilddate returned in 24 hour format
			hour = '%s:%s:%s' % (hour.hour, hour.minute, hour.second)
		else:
			m = hour[-2:] #pm or am
			hour = str(hour[:-3]) #hour and minute

		if viceversa:
			#only for lastbuilddate
			t = datetime.strptime(hour, '%H:%M:%S')
			t1 =t.strftime('%H:%M:%S') #get time in 24 hour format
			t2 =t.strftime('%I:%M:%S') #get time in 12 hour format
			h = int(t1[:t1.find(":")]) #get hour in 24 hour format
			if h == 0: t1 = "AM"
			elif h >= 12: t1 = "PM"
			elif h >= 1 and h <= 11: t1 = "AM"
			t = '%s %s' % (t2, t1)

		else:
			#time get from current weather and forecast date in 12 hour format
			try:
				t= datetime.strptime(hour, "%I:%M").strftime("%H:%M") #convert to 24 hour format
			except ValueError:
				t = self.Add_zero(hour, False)

			if m.lower() == "pm":
				h = hour[:hour.find(':')] #hour
				m = hour[hour.find(':')+1:] #minute
				t = self.Add_zero('%s:%s' % (int(h)+12, m), None)

		return t


	def GetTimezone(self, country_acronym, region, city,to24Hours, full = None):
		"""reads city local time, daylight saving time start and end"""
		if country_acronym == "US":  country_acronym = '%s-%s' % (country_acronym, region) #combines with a hyphen cauntry and region
		data = self.GetUrlData("https://www.worldtimeserver.com/current_time_in_%s.aspx?city=%s" % (country_acronym, city.replace(" ", "-").title()))
		if not data or data is "no connect": return [""] * 3
		if _pyVersion >= 3: data = data.decode()
		p = re.compile('<!-- Server Time:   \d{1,2}:\d{1,2}:\d{1,2} [AP]M -->') #12 hours format
		p1 = re.compile('<!-- Server Time with seconds:   \d{2}:\d{2}:\d{2} -->') #24 hours format
		#Daylight saving time
		s = re.compile('Starts On [A-Z][a-z]+ \d{1,2}, \d{4} at \d{1,2}:\d{1,2} [AP]M <br /> Set your clock ahead \d{1} hour.')
		e = re.compile('Ends On [A-Z][a-z]+ \d{1,2}, \d{4} at \d{1,2}:\d{1,2} [AP]M <br /> Set your clock back \d{1} hour.')

		def GetHour(pattern):
			try:
				m = re.search(pattern, data).group()
			except AttributeError: m = ""
			return m

		#Daylight saving time
		dst_starts = dst_ends = ""
		if "Starts" in data:
			dst_starts = GetHour(s)
			dst_ends = GetHour(e)
		if not to24Hours:
			m =GetHour(p)
			if m != "":
				if full:
					m = m[20:-4]
					return (Shared().Add_zero(m[:5].rstrip(":")+m[-3:], False), #hour and minutes as string
					dst_starts, dst_ends #Daylight saving times
					)

				return int(m[20:][:2].rstrip(":")), "", "" #hour value as int

			return "", "", [""] * 3
		else:
			m =GetHour(p1)
			if m != "":
				if full:
					return (m[33:-7][:5].rstrip(":"), #hour and minutes as string
					dst_starts, dst_ends #Daylight saving times
					)

				return int(m[33:][:2].rstrip(":")), "", "" #hour value as int

			return "", "", [""] * 3


	def Month2Num(self, text):
		"""convert months to number"""
		calendar_dic = {
		"Jan": 1,
		"Feb": 2,
		"Mar": 3,
		"Apr": 4,
		"May": 5,
		"Jun": 6,
		"Jul": 7,
		"Aug": 8,
		"Sep": 9,
		"Oct": 10,
		"Nov": 11,
		"Dec": 12,
		}

		if text in calendar_dic: return calendar_dic[text]
		return text


	def TranslateCalendar(self, text):
		"""Translates months or days"""

		calendar_dic = {
		"01": _("january"),
		"02": _("february"),
		"03": _("march"),
		"04": _("april"),
		"05": _("may"),
		"06": _("june"),
		"07": _("july"),
		"08": _("august"),
		"09": _("september"),
		"10": _("october"),
		"11": _("november"),
		"12": _("december"),
		"0": _("Monday"),
		"1": _("Tuesday"),
		"2": _("Wednesday"),
		"3": _("Thursday"),
		"4": _("Friday"),
		"5": _("Saturday"),
		"6": _("Sunday")
		}

		text = str(text)
		if text in calendar_dic: return calendar_dic[text]
		return text


	def GetLastUpdate(self, dom):
		"""Convert date string value into datetime value"""
		try:
			return datetime.fromtimestamp(dom['current_observation']['pubDate'])
		except Exception: return None


	def ParseEntry(self, value, dom = None):
		"""parse type city nameor woeid"""

		yql_query = ""
		if value.isdigit(): yql_query = 'woeid=%s' % value
		elif Shared().GetCoords(value):
			 value = value.split(',')
			 yql_query = 'lat=%s&lon=%s' % (value[0], value[-1].lstrip(' '))
		else: yql_query = 'location=%s' % value.encode("mbcs")
		dom = self.WeatherConnect(yql_query)
		if dom == "no connect": return dom, None
		elif not dom: return "", None
		try:
			woeid = dom['location']['woeid']
			city = dom['location']['city']
			region = region2 = dom['location']['region'].lstrip(' ')
			country = dom['location']['country']
			timezone_id = dom['location']['timezone_id']
			lat = dom['location']['lat']
			lon = dom['location']['long']
		except KeyError: return "", None
		country_acronym = Shared().GetAcronym(country)
		if country and not country_acronym:
			dl = HelpEntryDialog(gui.mainFrame,message ='%s' % (
			_("It was not possible find the acronym of %s!") % country+'\n'+
			_("This does not allow to get the city local time, the sound effects will not be consistent.")+'\n'+
			_("Please report this to the author so he can add this country in database.")+'\n'+
			_("Send an email to %s") % _addonAuthor+'\n'+
			_("With  object the line below, thanks.")),
			title = '%s %s' % (_addonSummary, _("Notice!")), clip = '%s %s' % (_addonSummary, 'acronym missing=%s' % woeid), verbose=False)
			if dl.ShowModal(): dl.Destroy()

		if country_acronym not in ["US", "CA"]: region = ""
		cityName = '%s%s' % (
		city, ', %s%s' % (country_acronym, region)
		)
		ramfields_dic = {}
		[ramfields_dic .update({f: ''}) for f in _fields]
		for n, f in enumerate(_fields):
			ramfields_dic[f] = [city, region2, country, country_acronym[:2], timezone_id, lat, lon][n]

		global ramdetails_dic
		ramdetails_dic = {str(woeid): ramfields_dic}
		return cityName, woeid


	def WeatherConnect(self, yql_query):
		"""return Yahoo Weather API values"""
		request = Parse(_addonDir, yql_query)
		if request == "not authorized": return request
		data = self.GetUrlData(request)
		if not data or data == "no connect": return data
		return json.loads(data)


	def Download_file(self, url, target, title, message):
		"""Download files using the progress bar"""

		if "_addonBaseUrl" not in globals(): return "Error"
		max = 100
		dlg = wx.ProgressDialog(title,
		message,
		maximum = max,
		style = 0
		| wx.PD_CAN_ABORT
		| wx.PD_APP_MODAL
		| wx.PD_ELAPSED_TIME
		| wx.PD_ESTIMATED_TIME
		)
		dlg.Update(0, message)
		try:
			fURL = urlopen(url, timeout=6)
			header = fURL.info()
			size = None
			outFile = open(target, 'wb')
			keepGoing = True
			if "Content-Length" in header:
				size = int(header["Content-Length"])
				kBytes = size/1024
				downloadBytes = size/max
				count = 0
				while keepGoing:
					count += 1
					if count >= max: count = 99
					wx.MilliSleep(250)
					wx.Yield()
					(keepGoing, skip) = dlg.Update(count,
					'%s %s %s %s %s' %(
					_("Downloaded"), str(count*downloadBytes/1024),
					_("of"), str(kBytes), "KB"))
					b = fURL.read(downloadBytes)
					if b:
						outFile.write(b)
					else:
						break
			else:
				while keepGoing:
					(keepGoing, skip) = dlg.UpdatePulse()
					b = fURL.read(1024*8)
					if b:
						outFile.write(b)
					else:
						break
			outFile.close()
			fURL.close()
			dlg.Update(99, '%s %s %s' % (
			_("Downloaded"), str(os.path.getsize(target)/1024), "KB"))
			dlg.Hide(); dlg.Destroy()
			return keepGoing
		except Exception as e:
			try:
				outFile.close()
				fURL.close()
			except: pass
			if not "failed" in str(e) and not "Not Found" in str(e) and not "unknown url type" in str(e):
				Shared().WriteError(title)

			dlg.Hide(); dlg.Destroy()
			Shared().SendToLog(e)
			return "Error"


	def Find_keys(self):
		 return '%s = %s, %s = %s, %s = %s.' % (
		"Control+f3", _("Find..."),
		"f3", _("Find next"),
		"Shift+f3", _("Find previous"))


	def AdjustVol(self, sampleVol):
		"""adjusts volume proportional to the volume of the current audio"""
		v = int(_volume[:-1])
		s = int(sampleVol[:-1])
		dif = abs(v - s)
		if v > s: playVol = v - dif
		elif v < s: playVol = v + dif
		elif v == s: playVol = v
		if playVol < 0: playVol = 0
		elif playVol > 100: playVol = 100
		return '%s%%' % playVol


	def FreeHandle(self):
		"""Frees memory for audio stream loaded"""
		try:
			BASS_StreamFree(_handle)
			BASS_Free()
		except Exception: pass


	def Check_content(self, z, title = "", verbose = True):
		"""Check file contents weather.zipcodes"""

		zImport = []
		for i in z:
			zc = i.split()[-1]
			if (len(zc) == 8 and [True for x in list(str(range(10))) if x in zc]) or zc.isdigit():
				zImport.append(i)

		if not zImport or len(zImport) == 0:
			if verbose:
				wx.MessageBox(_("Empty file or not in cities woeID format compatible!"), title, wx.ICON_ERROR)
			return None
		return zImport


	def LoadZipCodes(self, i = None):
		"""Load woeID, city definitions and city details"""
		citiesPath = _zipCodes_path
		if i:
			#There is an import file
			citiesPath = i

		zipCodesList = []
		define_dic = {}
		details_dic = {}
		if os.path.isfile(citiesPath):
			with open(citiesPath, 'r') as file:
				for r in file:
					if r != '':
						r = r.rstrip('\r\n')
						zc = r.split('\t')
						if len(zc) == 2:
							if zc[0].startswith('#') and len(zc[-1])== 1:
								#define data
								define_dic.update({zc[0][1:]: zc[-1].rstrip('\r\n')})
							else: zipCodesList.append('%s %s' % (zc[0].capitalize(), zc[-1].rstrip('\r\n').upper()))

						elif len(zc) == 8:
							#city details
							fields_dic = {}
							n = 1
							[fields_dic.update({i: ''}) for i in _fields]
							for f in _fields:
								#load fields data
								fields_dic.update({f: zc[n]}); n += 1

							details_dic.update({zc[0]: fields_dic}) #load record (woeid + fields)

		return sorted(zipCodesList), define_dic, details_dic


	def Personal_volumes(self, dictionary = None, sav = False):
		"""Upload or save the audio volumes assigned to each sound effect"""
		if not os.path.exists(_volumes_path) and sav == False: return {}
		#It collects the samples list
		samples_list = []
		if os.path.isdir(_samples_path):
			samples_list = os.listdir(_samples_path)
			#remove extension
			samples_list = [i[:-4] for i in samples_list]

		if sav:
			if dictionary:
				#saves the volume of each sound effect
				with open(_volumes_path, "w") as file:
					for i in sorted(dictionary.keys()):
						file.write('%s\t%s\n' % (i, dictionary[i]))

				return True #dictionary saved

		else:
			#load...
			dictionary = {}
			with open(_volumes_path, "r") as file:
				for line in file:
					line = line.rstrip('\n')
					if line and line[0].isupper() and line.count('\t') == 1 and line.endswith('%'):
						i = line.split('\t')
						if len(i) == 2:
							if i[0] in samples_list: #collects only those in the file list
								dictionary.update({i[0]: i[-1].rstrip('\n')})

				return dictionary


	def TranslatePlaces(self, place):
		"""It translates the Italian regions"""

		place = place.replace("Abruzzi", "Abruzzo")
		place = place.replace("Basilicate", "Basilicata")
		place = place.replace("Latium", "Lazio")
		place = place.replace("Lombardy", "Lombardia")
		place = place.replace("The Marches", "Marche")
		place = place.replace("Piedmont", "Piemonte")
		place = place.replace("Apulia", "Puglia")
		place = place.replace("Sardinia", "Sardegna")
		place = place.replace("Sicily", "Sicilia")
		place = place.replace("Tuscany", "Toscana")
		return place


	def GetGeoName(self, city, lat, lon, acronym=""):
		"""return region and country"""
		if not lat and lon: return None
		lat = int(float(lat))
		lon = int(float(lon))
		line = ""
		address = 'http://www.geonames.org/search.html?q=%s&country=%s' % (city, acronym)
		data = Shared().GetUrlData(address)
		if not data: return None
		if _pyVersion >= 3: data = data.decode()
		for m in data.split('\n'):
			if "geonames" and "latitude" in m:
				pos = latitude = longitude = acronym = country = region = ""
				pos = m.find("latitude"); m =m[pos + 10:]
				pos = m.find("<"); latitude = m[:pos]
				latitude = int(float(latitude))
				pos = m.find("longitude") + 11; m = m[pos:]
				pos = m.find("<"); longitude = m[:pos]
				longitude = int(float(longitude))
				pos = m.find("countries")
				if pos != -1:
					m = m[pos + 10:]
					acronym = m[:2]
					pos = m.find("/"); m =m[pos + 1:]
					pos = m.find(".html")
					country = m[:pos].title()
					pos = m.find("/a>,")
					if pos != -1:
						m = m[pos + 4:]
					else:
						m = m[m.find('">') + 2:]

					pos = m.find("<")
					region = Shared().TranslatePlaces(m[:pos].lstrip(" "))

				if (lat == latitude) and (lon == longitude):
					line = '%s, %s, %s' % (region, country, acronym)
					break

		line = line.replace(", ,", "").rstrip(", ")
		if _pyVersion == 2: return line.decode("mbcs")
		else: return line


	def GetElevation(self, lat, lon):
		"""Returns elevation above sea level"""
		p=re.compile(r'>(-*\d+)</span> meters<')
		data = Shared().GetUrlData("http://veloroutes.org/elevation/?location=%s,%s&units=m" % (lat, lon))
		if data == "no connect": return data
		if data and _pyVersion >= 3: data = data.decode()
		try:
			elevation = p.search(data).group(1)
		except (TypeError, AttributeError): elevation = None
		return elevation


	def Play_sound(self, t, s = 0):
		"""Play general sound Effects"""
		sound_dic = {
		True: "Confirm",
		False: "Notfound",
		"add": "Add",
		"alreadyinlist": "Alreadyinlist",
		"apply": "apply",
		"beep": "Beep",
		"define": "Define",
		"del": "Delete",
		"details": "Details",
		"messagefailure": "Messagefailure",
		"save": "Save",
		"swap": "Swap",
		"wait": "Wait",
		"warn": "Noconnected",
		"subwindow": "Subwindow",
		"winopen": "Winopen",
		"winclose": "Winclose"
		}
		if t in sound_dic:
			filename = '%s\\%s.wav' % (_sounds_path, sound_dic[t])
			if _pyVersion == 2:
				winsound.PlaySound(filename.encode("mbcs"), s)
			else:
				winsound.PlaySound(filename, s)


	def WriteError(self, title):
		"""Notify IO error"""
		wx.MessageBox('%s\n%s' % (
		_("Be an error has occurred."),
		_("See the log for more information.")),
		'%s - %s' % (title, _("Error: failure writing file!")),
		wx.ICON_ERROR)


	def ZipCodeInList(self, v, zipCodesList):
		"""Check if it already exists ID"""
		i, t = 0, False
		zc = self.GetZipCode(v).upper()
		for i, n in enumerate(zipCodesList):
			zc1 = self.GetZipCode(n).upper()
			if zc1 == zc:
				t = True; break
		return t, zc, i


	def GetZipCode(self, value):
		"""Testing city woeID"""
		if _pyVersion >= 3: value = str(value)
		if [True for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] if i in value]:
			return value.split()[-1].strip("'")

		return value


	def GetUrlData(self, address):
		"""Gets the contents of a web page"""
		e, data = "", None
		try:
			with closing(urlopen(address)) as response:
				data = response.read()
		except Exception as e:
			if "CERTIFICATE_VERIFY_FAILED" in repr(e):
				#retry using ssl
				data = "no connect"
				gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
				try:
					e, data = "", None
					with closing(urlopen(address, context=gcontext)) as response:
						data = response.read()
				except Exception as e: pass
			elif "failed" in repr(e): data = "no connect"

		if "e" in locals() and e:
			Shared().SendToLog(e)

		return data


	def FindWoeID(self, city):
		"""Gets data-center_long, data-center_lat, data-city, data-district_county, data-province_state, data-country, data-woeid"""
		city2 = city
		if "," in city: city2 = city[:city.rfind(",")] #remove the region and country
		if not city2.isdigit(): city = city2 #else it's a postal code
		if _pyVersion == 2: city = city.encode("mbcs")
		address ="http://woeid.rosselliot.co.nz/lookup/%s" % city
		data = self.GetUrlData(address)
		if data and _pyVersion >= 3: data = data.decode()
		if not data: return ""
		elif "noresult" in data: return "noresult"
		elif data:
			if _pyVersion == 2: data = data.decode("mbcs")
			import re
			find_list = []
			cities = []
			pattern = re.compile('data-center_long="\-*[0-9]+\.*[0-9]+" data-center_lat="\-*[0-9]+\.*[0-9]+" data-city=".*" data-district_county=".*" data-province_state=".*" data-country=".*" data-woeid="[0-9]*"')
			for i in data.split('\r\n'):
				try:
					m = pattern.search(i).group()
				except AttributeError: m = None
				if m:
					m = m.split("'woeid_row' ")
					for i in m:
						find_list.append(i.split('><td>')[0])

					for i in find_list:
						for r in ['data-center_long=', 'data-center_lat=', 'data-city=', 'data-district_county=', 'data-province_state=', 'data-country=', 'data-woeid=']:
							i = i.replace(r, "")
						i = i.split('" "')
						i = [x.replace('"', '') for x in i]
						i[3] = i[3].replace('  ', ' ')
						if i[2] == i[3].split(',')[0]:
							text = ', '.join([i[3], i[4], i[5], i[6]])
						else:
							text = ', '.join([i[2], i[3], i[4], i[5], i[6]])
						text = Shared().TranslatePlaces(text)
						cities.append(text.replace("  ", " ").replace(", ,", ","))

			return cities
		return ""


	def Search_cities(self, cityName, defaultString = ""):
		"""Search for city occurrences"""
		if len(cityName) == 8 and not "," in cityName:
			#try to filter the old zipcode
			if not cityName[-2].isalpha():
				return "Error", defaultString

		woeIDList = self.FindWoeID(cityName)
		if woeIDList == "noresult": return woeIDList, defaultString
		wl = len(woeIDList)
		if wl == 0: return "Error", defaultString
		elif wl == 1: return woeIDList[0].split(', ')[-1], defaultString
		else:
			title = '%s - %d %s %s %s.' % \
			(_addonSummary, len(woeIDList), _("occurrences found"), _("for"), cityName)
			message = '%s.\n%s\n%s:' % (
			_("Choose a city."),
			Shared().Find_keys(),
			_("List of availables Cities")
			)
			dl = SelectDialog(gui.mainFrame, title = title, message = message, choices = woeIDList, last = [0], sel = 0, defaultString = defaultString)
			Shared().Play_sound("subwindow", 1)
			if dl.ShowModal() == wx.ID_CANCEL:
				n, defaultString = dl.GetValue()
				dl.Destroy()
				Shared().Play_sound("subwindow", 1)
				return "", defaultString
			else:
				select, defaultString = dl.GetValue()
				dl.Destroy()
				Shared().Play_sound("subwindow", 1)
				return woeIDList[select].split(', ')[-1], defaultString


class NoticeAgainDialog(wx.Dialog):
	"""Dialogue with variables buttons and check box to not show it again"""
	def __init__(self, parent, id=-1, title='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
	message = '',
		again = False,
		bUninstall = None,
		uninstall_button = None
		):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style)

		self.bUninstall = bUninstall
		sizer = wx.BoxSizer(wx.VERTICAL)
		if message:
			sizer.Add(wx.StaticText(self, -1, message), 0, wx.ALL, 10)
			sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		if not bUninstall:
			cbx = wx.CheckBox(self, -1, _("Do not show this message again!"))
			cbx.SetValue(again)
			sizer.Add(cbx)
			self.cbx = cbx

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		if not bUninstall:
			hbox.Add(self.CreateButtonSizer(wx.OK), 0, wx.CENTRE| wx.ALL, 5)
			cbx.SetFocus()
		else:
			buttons = [_("&Install..."), _("Upd&ate...")]
			btn_install = wx.Button(self, id=wx.ID_ANY, label=buttons[uninstall_button])
			btn_close = wx.Button(self, id=wx.ID_ANY, label = _("&Close"))
			btn_uninstall = wx.Button(self, id=wx.ID_ANY, label=_("&Uninstall..."))
			hbox.Add(btn_install, 0, wx.ALL, 5)
			hbox.Add(btn_close, 0, wx.ALL, 5)
			hbox.Add(btn_uninstall, 0, wx.ALL, 5)
			self.Bind(wx.EVT_BUTTON, self.OnUninstall, btn_uninstall)
			if not uninstall_button: btn_uninstall.Enable(False)
			self.SetEscapeId(btn_close.GetId())
			self.SetAffirmativeId(btn_install.GetId())

		sizer.Add(hbox, 1, wx.ALIGN_CENTER_HORIZONTAL)
		self.SetSizerAndFit(sizer)
		self.Center(wx.BOTH|wx.Center)
		winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)


	def OnUninstall(self, evt):
		"""Button uninstall event"""
		evt.Skip()
		self.EndModal(wx.ID_APPLY)


	def GetValue(self):
		"""Return ceckBox value"""
		if not self.bUninstall: return self.cbx.GetValue()


class SelectDialog(wx.Dialog):
	"""Dialogue that allows to choose a city"""
	def __init__(self, parent, id=-1, title='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
		message = '', choices = [], last = [], sel = 0, defaultString = ''):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style)
		sizer = wx.BoxSizer(wx.VERTICAL)
		if message:
			sizer.Add(wx.StaticText(self, -1, message), 0, wx.ALL, 10)
			sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		if _pyVersion >= 3:
			self.chb = wx.Choice(self, -1, choices = choices)
		else:
			try:
				self.chb = wx.Choice(self, -1, choices = [i.decode("mbcs") for i in choices])
			except (UnicodeEncodeError, UnicodeDecodeError):
				self.chb = wx.Choice(self, -1, choices = choices)

		self.chb.SetSelection(last[sel])
		if not self.chb.GetCurrentSelection(): self.chb.SetSelection(0)
		hbox.Add(self.chb)
		sizer.Add(hbox, 1, wx.CENTRE| wx.ALL, 5)

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.CENTRE| wx.ALL, 5)
		sizer.Add(hbox2, 1, wx.ALIGN_CENTER_HORIZONTAL)
		self.SetSizerAndFit(sizer)
		self.Center(wx.BOTH|wx.Center)

		self.chb.SetFocus()
		self.choices = choices
		self.defaultString = defaultString

		#Shortcut key event for FindText()
		self.chb.Bind(wx.EVT_CHAR, self.OnKey)


	def GetValue(self):
		"""Return the location choice from SelectDialog"""
		return self.chb.GetSelection(), self.defaultString


	def OnKey(self, evt):
		"""Control hot keys pressed into SelectDialog"""
		ctrl = evt.ControlDown()
		shift = evt.ShiftDown()
		key = evt.GetKeyCode()
		defaultString = self.defaultString
		if key == wx.WXK_F3 and ctrl:
			#Enter text to search
			dl = wx.TextEntryDialog(self,
			_("Type the search string"),
			_("Find"),
			defaultString
			)

			if dl.ShowModal() == wx.ID_OK:
				defaultString = self.defaultString = dl.GetValue()
				self.FindText(self.choices, defaultString, direction = 0)

			dl.Destroy()

		elif key == wx.WXK_F3 and shift and defaultString:
			#Find previous
			self.FindText(self.choices, defaultString, direction = -1)
		elif key == wx.WXK_F3 and defaultString:
			#Find next
			self.FindText(self.choices, defaultString, direction = 1)
        
		evt.Skip()


	def FindText(self, strings, text, direction = 0):
		"""Search and if found, displays the selected item by the user""" 
		d = direction
		if direction == -1:
			#Find previous
			s = self.GetStart_index(strings, direction)
			e = direction
		elif direction == 1:
			#Find next
			s = self.GetStart_index(strings, direction)
			e = len(strings)
		else:
			#Find to bbegin
			s = 0; e = len(strings)
		if direction == 0: direction = 1
		find = False
		for line in range(s, e, direction):
			if _pyVersion >= 3: t = strings[line].lower()
			else:
				try:
					t = strings[line].lower().decode("mbcs")
				except (UnicodeEncodeError, UnicodeDecodeError): t = strings[line].lower()

			if t.find(text.lower()) != -1:
				self.chb.SetSelection(line)
				wx.CallLater(100, ui.message, self.chb.GetStringSelection())
				find = True; break
		if not find:
			ds= ["", _("next"), _("previous")]
			if d == 0:
				wx.MessageBox('"%s" %s' % (text, _("not found!")), _("Find"), wx.ICON_EXCLAMATION)
			else:
				ds = ["", _("No results next for"), _("No previous results for")]
				winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
				wx.CallLater(100, ui.message,
				'%s %s.' % (ds[direction], text))


	def GetStart_index(self, strings, direction):
		"""Get start index for next or prev research"""
		try:
			t = self.chb.GetStringSelection()
			s = strings.index(t) + direction
		except ValueError:
			if _pyVersion == 2: s = strings.index(t.encode("mbcs")) +direction

		return s


class SelectImportDialog(wx.Dialog):
	"""Dialog box for selection of import content"""
	def __init__(self, parent, id=-1, title=wx.EmptyString, 
		pos=			wx.DefaultPosition, size=wx.DefaultSize, 
		style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,
		zip_list = [], checkbox_values = [], message = ''):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos, 
		size=size, style=style)

		sizer = wx.BoxSizer(wx.VERTICAL)
		if _pyVersion == 2: zip_list = [i.decode("mbcs") for i in zip_list]
		clb = wx.CheckListBox(self, -1, pos = wx.DefaultPosition, size = wx.DefaultSize, choices = zip_list, style = 0)
		clb.Bind(wx.EVT_CHECKLISTBOX, self.Hit_Item)
		clb.Bind(wx.EVT_LISTBOX, self.ListBoxEvent)
		sizer.Add(clb)

		border = wx.BoxSizer(wx.VERTICAL)
		if message:
			border.Add(wx.StaticText(self, -1, message), 0, wx.ALL, 10)
			border.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		border.Add(sizer, 0, wx.LEFT, 50)
		border.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL|wx.APPLY|wx.HELP), 0, wx.CENTRE| wx.ALL|wx.EXPAND, 5)
		self.btn_ok=self.FindWindowById(wx.ID_OK, self)
		btns = self.FindWindowById(wx.ID_APPLY, self)
		btns.SetLabel(_("&Select all"))
		btnd = self.FindWindowById(wx.ID_HELP, self)
		btnd.SetLabel(_("&Deselect all"))
		self.Bind(wx.EVT_BUTTON, self.OnSelectAll, btns)
		self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, btnd) 
		self.SetSizerAndFit(border)
		self.Center(wx.BOTH|wx.Center)
		self.clb = clb
		self.btnd = btnd
		self.btns = btns
		self.SetButtons(False)
		self.btn_ok.Enable(False)
		clb.SetFocus()
		clb.SetSelection(0)
		self.Hit_Item(True)

		#Set scroll dialog
		self.DoLayoutAdaptation()
		self.SetLayoutAdaptationLevel(self.GetLayoutAdaptationLevel())
		self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnCaptureMouse)
		self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnFreeMouse)


	def OnCaptureMouse(self, evt):
		evt.CaptureMouse()

	def OnFreeMouse(self, evt):
		wx.Window.ReleaseMouse()


	def ListBoxEvent(self, evt):
		"""Event scroll and highlight items in the list"""
		self.Hit_Item(True)


	def Hit_Item(self, verbose = False, evt = None):
		"""Reads the checkbox status of the selection"""
		index = self.clb.GetSelection()
		self.checkedItems = [i for i in range(self.clb.GetCount()) if self.clb.IsChecked(i)]
		if len(self.checkedItems) and not self.btn_ok.IsEnabled(): self.btn_ok.Enable(True)
		elif not len(self.checkedItems) and self.btn_ok.IsEnabled(): self.btn_ok.Enable(False)

		status = _("not checked")
		if self.clb.IsChecked(index):
			status = _("checked")

		message = '%s' % status
		if verbose is True:
			message = '%s %s' % (_("check box"), status)

		if verbose is not True: Shared().Play_sound("beep")
		wx.CallLater(100, ui.message, message)


	def OnSelectAll(self, evt):
		"""select all the check boxes in the list"""
		items = self.clb.GetCount()
		[self.clb.Check(item, check = True) for item in range(items)]
		wx.CallLater(100, ui.message, '%d %s' % (items, _("check boxes checked")))
		self.SetButtons(True)
		self.btn_ok.Enable(True)


	def OnDeselectAll(self, evt):
		"""deselect all the check boxes in the list"""
		items = self.clb.GetCount()
		[self.clb.Check(item, check = False) for item in range(items)]
		wx.CallLater(100, ui.message, '%d %s' % (items, _("check boxes not checked")))
		self.SetButtons(False)


	def SetButtons(self, flag):
		"""update buttons for Select SelectImportDialog"""
		self.btnd.Enable(flag)
		self.btns.Enable(not flag)
		self.btn_ok.Enable(flag)
		self.clb.SetFocus()


	def GetValue(self):
		"""Gets the checkboxes values from SelectImportDialog"""
		self.Hit_Item()
		return self.checkedItems


class MyDialog(wx.Dialog):
	"""Dialog for upgrade addon"""
	def __init__(self, parent, message = "", title = "", zipCodesList = None, newVersion = "", setZipCodeItem = None, setTempZipCodeItem = None, UpgradeAddonItem = None, buttons = None, simple = True):
		super(MyDialog, self).__init__(parent, title = title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		self.zipCodesList = zipCodesList
		self.newVersion = newVersion
		self.setZipCodeItem = setZipCodeItem
		self.setTempZipCodeItem = setTempZipCodeItem
		self.UpgradeAddonItem = UpgradeAddonItem
		self.verbosity = True
		sHelper.addItem(wx.StaticText(self, label=message))
		bHelper = sHelper.addDialogDismissButtons(gui.guiHelper.ButtonHelper(wx.HORIZONTAL))

		if buttons:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			confirmButton = bHelper.addButton(self, id=wx.ID_YES)
			cancelButton = bHelper.addButton(self, id=wx.ID_NO)
			cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
		else:
			winsound.MessageBeep(winsound.MB_ICONASTERISK)
			confirmButton = bHelper.addButton(self, id=wx.ID_OK)

		self.buttons = buttons
		confirmButton.SetDefault()
		confirmButton.Bind(wx.EVT_BUTTON, self.OnConfirm)
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Center(wx.BOTH|wx.Center)


	def OnConfirm(self, evt):
		""" yes and ok button event """
		if self.buttons:
			self.Hide()
			file = "%s%s.nvda-addon" % (_addonSummary, self.newVersion.split()[0])
			url = '%s/weather_plus%s.nvda-addon?download=1' % (_addonBaseUrl, self.newVersion.split()[0])
			import tempfile
			target = "/".join((tempfile.gettempdir(), file))
			message = _("Please wait...")
			title = _("Saving in progress")
			result = Shared().Download_file(url, target, title, message)
			message = _("Download canceled.")
			title = _addonSummary
			if result is True:
				self.verbosity = False
				winsound.MessageBeep(winsound.MB_ICONASTERISK)
			elif os.path.isfile(target):
				os.remove(target); view = False

			if self.verbosity:
				wx.MessageBox(message, title)

			#Start update addon
			try:
				os.startfile(target)
			except WindowsError: pass

		if self.UpgradeAddonItem: self.EnableMenu(True)
		self.Destroy()


	def EnableMenu(self, flag):
		"""Change status menu"""
		self.setZipCodeItem.Enable(flag)
		if not self.zipCodesList and flag is True:
			self.setTempZipCodeItem.Enable(False)
		else:
			self.setTempZipCodeItem.Enable(flag)
		self.UpgradeAddonItem.Enable(flag)


	def OnCancel(self, evt = None):
		"""cancell button event"""
		if self.UpgradeAddonItem: self.EnableMenu(True)
		self.Destroy()


class HelpEntryDialog(wx.Dialog):
	"""help window for data entry"""
	def __init__(self, parent, id=-1, pos = wx.DefaultPosition,
		size=wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,
		message='', title='', clip = '', verbose = True):
		wx.Dialog.__init__(self, parent = parent, id = id, title = title, pos = pos,
		size = size, style = style)
		vbox = wx.BoxSizer(wx.VERTICAL)
		text = wx.TextCtrl(self, -1, value = message, pos = wx.DefaultPosition, size=(460,480), style = wx.TE_MULTILINE|wx.TE_READONLY)
		vbox.Add(text, 1, wx.EXPAND|wx.ALL, 5)
		if not verbose:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			self.clip = clip
			cb = wx.ComboBox(self, -1, choices=[clip], pos = wx.DefaultPosition, size=wx.DefaultSize,
			style = wx.TE_READONLY)
			cb.SetValue(clip)
			btn_copytoclip = wx.Button(self, id=wx.ID_ANY, label=_("&Copy to clipboard"))
			btn_copytoclip.Bind(wx.EVT_BUTTON, self.OnCopytoclip)
			hbox.AddMany([cb, btn_copytoclip])
			vbox.Add(hbox)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(self.CreateButtonSizer(wx.OK), 0, wx.CENTRE| wx.ALL)
		vbox.Add(hbox1)
		self.SetSizerAndFit(vbox)
		self.Centre()
		text.SetFocus()
		if verbose: Shared().Play_sound("subwindow", 1)


	def OnCopytoclip(self, evt):
		"""copy textctrl value to clipboard"""
		import api
		api.copyToClip(self.clip)
		evt.Skip()