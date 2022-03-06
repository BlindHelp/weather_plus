#-*- coding:utf-8 -*-
#Weather Plus Addon for NVDA
#WeatherAPI (powered by WeatherAPI.com)
#Weather and 24 hour forecast
#More forecast up to 2 days
#Hourlyforecast
#Copyright (C) Adriano Barbieri 
#Email: adrianobarb@yahoo.it
#Released under GPL 2
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Version 8.8.
#NVDA compatibility: 2017.3 to beyond.
#Last Edit date March, 05th, 2022.

import os, sys, winsound, config, globalVars, ssl, json
import globalPluginHandler, scriptHandler, languageHandler, addonHandler
import random, ui, gui, wx, re, calendar, math
from logHandler import log
from gui import guiHelper
from datetime import *
import api, time
if wx.version().split(".")[0] >= "4": import wx.adv
from configobj import ConfigObj
from contextlib import closing
"""other temporary imported libraries in the code
tempfile, zipfile, shutil, stat"""
#include the modules directory to the path
sys.path.append(os.path.dirname(__file__))
import dateutil.tz, dateutil.zoneinfo
from pybass  import *
_pyVersion = int(sys.version[:1])
if _pyVersion >= 3:
	from urllib.parse import urlencode
	from urllib.request import urlopen
else:
	#nvda with python version earlier than 3
	from urllib2 import urlopen
	from urllib import urlencode

del sys.path[-1]
addonHandler.initTranslation()

#global constants
if _pyVersion <= 2:
	_addonDir = os.path.join(os.path.dirname(__file__), "..", "..").decode("mbcs")
else:
	_addonDir = os.path.join(os.path.dirname(__file__), "..", "..")
_curAddon = addonHandler.Addon(_addonDir)
_addonAuthor = _curAddon.manifest['author']
_addonSummary = _curAddon.manifest['summary']
_addonVersion = _curAddon.manifest['version']
_addonPage = _curAddon.manifest['url']
_addonBaseUrl = '%s/%s' % (_addonPage[:_addonPage.rfind('/weather')], "files/plugin")
_zipCodes_path = os.path.join(globalVars.appArgs.configPath, "Weather.zipcodes")
_volumes_path = os.path.join(globalVars.appArgs.configPath, "Weather.volumes")
_samples_path = os.path.join(globalVars.appArgs.configPath, "Weather_samples")
_searchKey_path = os.path.join(globalVars.appArgs.configPath, "Weather_searchkey")
_mydefcity_path = os.path.join(globalVars.appArgs.configPath, "Weather.default")
_sounds_path = _addonDir.replace('..\..', "") + "\sounds"
_volume_dic = {'0%': 0, '10%': 0.1, '20%': 0.2, '30%': 0.3, '40%': 0.4, '50%': 0.5, '60%': 0.6, '70%': 0.7, '80%': 0.8, '90%': 0.9, '100%': 1}
_tempScale = [_("Fahrenheit"), _("Celsius"), _("Kelvin")]
_fields = ['city', 'region', 'country', 'country_acronym', 'timezone_id', 'lat', 'lon']
_npc = "NPC" #non postal code
_nr = _("unknown")
_na = _("not available")
_plzw = _("Please wait...")
_maxDaysApi = 3 #maximum allowed for free api plan
_wait_delay = 10 #it's necessary to update after at least 10 minutes to limit frequent API calls, please don't change it!
_mainSettingsDialog = None
_tempSettingsDialog = None
_helpDialog = None
_downloadDialog = None
_searchDialog = None
_findDialog = None
_notifyDialog = None
_testCode = ''

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _addonSummary
	def __init__(self):
		#variables definition
		if "_wbdat" not in globals():
			global _wbdat; _wbdat = Shared().Weather_PlusDat()

		self.note = [1, ''] #errors counter and city in use
		self.cityDialog = None #city error dialog opened
		self.dom = "" #Weather API data corresponding to the city in use
		self.defaultZipCode = "" #city preset
		self.tempZipCode = "" #temporary city
		self.test = [""] * 2 #temporary city and current time
		self.defaultString = "" #the last search string
		self.randomizedSamples = [] #used by Play_samples()
		self.current_zipCode = "" #used by Play_samples()
		self.current_condition = "" #used by Play_samples()
		#load cities list and definitions from Weather.zipcodes
		self.zipCodesList, self.define_dic, self.details_dic = Shared().LoadZipCodes()
		#load sounds effects volumes
		global samplesvolumes_dic
		samplesvolumes_dic = Shared().Personal_volumes()
		#Reads the settings from weather.ini
		self.ReadConfig()
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.menu = gui.mainFrame.sysTrayIcon.menu.GetMenuItems()[0].GetSubMenu()
		self.WeatherMenu = wx.Menu()
		#Translators: the configuration submenu in NVDA Preferences menu
		self.mainItem = self.menu.AppendSubMenu(self.WeatherMenu, _("Weather Plus &Settings"), _("Show configuration items."))
		#Translators: item to open primary configuration window
		self.setZipCodeItem = self.WeatherMenu.Append(wx.ID_ANY, _("Set and &manage your cities..."), _("Displays or allows to set the current cities from a list"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSetZipCodeDialog, self.setZipCodeItem)
		#Translators: item to open window to set up a temporary city
		self.setTempZipCodeItem = self.WeatherMenu.Append(wx.ID_ANY, _("Set a &temporary city..."), _("Allows to set one temporary city from a list"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.setZipCodeDialog, self.setTempZipCodeItem)
		if not self.zipCodesList: self.setTempZipCodeItem.Enable(False)
		#Translators: item to open the help file for the current language
		self.AboutItem = self.WeatherMenu.Append(wx.ID_ANY, _("&Documentation"), _("Opens the help file for the current language"))
		self.AboutItem.Enable(self.isDocFolder())
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, self.AboutItem)
		#Translators: item to notify if there is an upgraded version available
		self.UpgradeAddonItem = self.WeatherMenu.Append(wx.ID_ANY, _("&Check for Upgrade..."), _("Notify if there is an upgraded version available"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onUpgrade, self.UpgradeAddonItem)
		#check if a new version is available
		if self.toUpgrade: self.onUpgrade()
		#delete the update file from the temporary folder
		self.Removeupdate()


	def terminate(self):
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
		import tempfile, stat
		if _pyVersion <= 2:
			temp = tempfile.gettempdir().decode("mbcs")
			(_, _, filenames) = os.walk(temp).next()
		else:
			temp = tempfile.gettempdir()
			(_, _, filenames) = os.walk(temp).__next__()

		for i in filenames:
			file = re.search('([wW]eather[_ ][pP]lus\d\.\d\.nvda-addon|)', i).group()
			if file: file = "\\".join((temp, file))
			if os.path.isfile(file):
				try:
					os.chmod(file, stat.S_IWRITE )
					os.remove(file)
				except: pass


	def GetScaleAs(self):
		"""return degrees indication selected"""
		scale_as = _tempScale[self.celsius]
		if self.scaleAs == 1: scale_as = scale_as[0]
		elif self.scaleAs == 2: scale_as = ""
		return scale_as


	def GetUnitValues(self, degrees):
		"""unit strings values"""
		unit_uv = _("nanometers")
		if degrees == 0:
			#Fahrenheit degrees
			unit_speed = _("miles per hour")
			unit_distance = _("miles")
			unit_precip = _("inches")
			unit_pressure = _("inches of mercury")
		else:
			#Celsius and Kelvin
			unit_speed = _("kilometers per hour")
			unit_distance = _("kilometers")
			unit_precip = _("millimeters")
			unit_pressure = _("millibars")

		if self.toMmhgpressure: unit_pressure = _("millimeters of mercury")
		return unit_speed, unit_distance, unit_precip, unit_pressure, unit_uv


	def IsOpenDialog(self, dialog):
		try:	
			if dialog or dialog.IsShown():
				#returns if the dialog specified is open
				wx.Bell()
				Dialog.Raise()
				dialog.Show()
				return True
		except: return False


	def onSetZipCodeDialog(self, evt):
		"""Opens the Weather Plus settings window"""
		#prevents multiple windows open at the same time
		self.EnableMenu(False)
		try:
			#set the correct encoding in the title
			if _pyVersion <= 2:
				preset = self.defaultZipCode.decode("mbcs")
			else:
				preset = self.defaultZipCode
		except(UnicodeDecodeError, UnicodeEncodeError): preset = self.defaultZipCode
		#opens the Weather Plus settings window
		#Translators: the title of main settings window
		title = '%s - %s - (%s: %s)' % (_addonSummary, _("Settings"), _("Preset"), preset or _("None"))
		#Translators: the message in the main settings window
		message = _("Enter a City or choose one from the list, if available.")
		saved_celsius = self.ReadConfig("c") or self.celsius
		if "_mainSettingsDialog" not in globals(): global _mainSettingsDialog
		Shared().Play_sound("winopen", 1)
		_mainSettingsDialog = EnterDataDialog(gui.mainFrame, message =message, title = title,
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
		toWindgust = self.toWindgust,
		toPerceived = self.toPerceived,
		toHumidity = self.toHumidity,
		toVisibility = self.toVisibility,
		toPressure = self.toPressure,
		toMmhgpressure = self.toMmhgpressure,
		toCloud = self.toCloud,
		toPrecip = self.toPrecip,
		toUltraviolet = self.toUltraviolet,
		toWindspeed_hf = self.toWindspeed_hf,
		toWinddir_hf = self.toWinddir_hf,
		toWindgust_hf = self.toWindgust_hf,
		toCloud_hf = self.toCloud_hf,
		toHumidity_hf = self.toHumidity_hf,
		toVisibility_hf = self.toVisibility_hf,
		toPrecip_hf = self.toPrecip_hf,
		toUltraviolet_hf = self.toUltraviolet_hf,
		toAtmosphere = self.toAtmosphere,
		toAstronomy = self.toAstronomy,
		scaleAs = self.scaleAs,
		to24Hours = self.to24Hours,
		define_dic = self.define_dic,
		details_dic = self.details_dic,
		forecast_days = self.forecast_days,
		apilang = self.apilang,
		toUpgrade = self.toUpgrade,
		toComma = self.toComma,
		toOutputwindow = self.toOutputwindow,
		toWeatherEffects = self.toWeatherEffects,
		dontShowAgainAddDetails = self.dontShowAgainAddDetails
		)


		def callback2(result):
			if result == wx.ID_OK:
				#update the settings modified by the user
				(forecast_days,
				apilang,
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
				toWindgust,
				toAtmosphere,
				toAstronomy,
				to24Hours,
				toPerceived,
				toHumidity,
				toVisibility,
				toPressure,
				toCloud,
				toPrecip,
				toWinddir,
				toWindspeed,
				toMmhgpressure,
				toUltraviolet,
				toWindspeed_hf,
				toWinddir_hf,
				toWindgust_hf,
				toCloud_hf,
				toHumidity_hf,
				toVisibility_hf,
				toPrecip_hf,
				toUltraviolet_hf,
				toComma,
				toOutputwindow,
				toWeatherEffects,
				dontShowAgainAddDetails,
				toAssign) = _mainSettingsDialog.GetValue()
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
				if apilang != self.apilang: self.apilang = apilang; self.dom = ''; save = True
				if toClip != self.toClip: self.toClip = toClip; save = True
				if toSample != self.toSample: self.toSample = toSample; save = True
				if toHelp != self.toHelp: self.toHelp = toHelp; save = True
				if toWind != self.toWind: self.toWind = toWind; save = True
				if toWinddir != self.toWinddir: self.toWinddir = toWinddir; save = True
				if toWindspeed != self.toWindspeed: self.toWindspeed = toWindspeed; save = True
				if toSpeedmeters != self.toSpeedmeters: self.toSpeedmeters = toSpeedmeters; save = True
				if toWindgust != self.toWindgust: self.toWindgust = toWindgust; save = True
				if toPerceived != self.toPerceived: self.toPerceived = toPerceived; save = True
				if toHumidity != self.toHumidity: self.toHumidity = toHumidity; save = True
				if toVisibility != self.toVisibility: self.toVisibility = toVisibility; save = True
				if toPressure != self.toPressure: self.toPressure = toPressure; save = True
				if toMmhgpressure != self.toMmhgpressure: self.toMmhgpressure = toMmhgpressure; save = True
				if toCloud != self.toCloud: self.toCloud = toCloud; save = True
				if toPrecip != self.toPrecip: self.toPrecip = toPrecip; save = True
				if toUltraviolet != self.toUltraviolet: self.toUltraviolet = toUltraviolet; save = True
				if toWindspeed_hf != self.toWindspeed_hf: self.toWindspeed_hf = toWindspeed_hf; save = True
				if toWinddir_hf != self.toWinddir_hf: self.toWinddir_hf = toWinddir_hf; save = True
				if toWindgust_hf != self.toWindgust_hf: self.toWindgust_hf = toWindgust_hf; save = True
				if toCloud_hf != self.toCloud_hf: self.toCloud_hf = toCloud_hf; save = True
				if toHumidity_hf != self.toHumidity_hf: self.toHumidity_hf = toHumidity_hf; save = True
				if toVisibility_hf != self.toVisibility_hf: self.toVisibility_hf = toVisibility_hf; save = True
				if toPrecip_hf != self.toPrecip_hf: self.toPrecip_hf = toPrecip_hf; save = True
				if toUltraviolet_hf != self.toUltraviolet_hf: self.toUltraviolet_hf = toUltraviolet_hf; save = True
				if toAtmosphere != self.toAtmosphere: self.toAtmosphere = toAtmosphere; save = True
				if toAstronomy != self.toAstronomy: self.toAstronomy = toAstronomy; save = True
				if toComma != self.toComma: self.toComma = toComma; save = True
				if toOutputwindow != self.toOutputwindow: self.toOutputwindow = toOutputwindow; save = True
				if toWeatherEffects != self.toWeatherEffects: self.toWeatherEffects = toWeatherEffects; save = True
				if scaleAs != self.scaleAs: self.scaleAs = scaleAs; save = True
				if to24Hours != self.to24Hours: self.to24Hours = to24Hours; save = True
				if _volume != self.volume: self.volume = _volume; save = True
				if toAssign != self.toAssign: self.toAssign = toAssign; save = True
				if toUpgrade != self.toUpgrade: self.toUpgrade = toUpgrade; save = True
				if dontShowAgainAddDetails != self.dontShowAgainAddDetails: self.dontShowAgainAddDetails = dontShowAgainAddDetails; save = True
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
					if self.zipCode != self.defaultZipCode:
						#preserve the  city in use
						backup = self.zipCode
						self.zipCode = self.defaultZipCode
						self.SaveConfig()
						self.zipCode = backup

					else: self.SaveConfig()

				if beep: Shared().Play_sound("save")
				#Set temporary Zip Code
				self.ExtractData(self.tempZipCode)
				test = self.tempZipCode
				if _pyVersion <= 2: test = unicode(test.decode("mbcs"))
				if not self.dontShowAgain:
					if (not self.defaultZipCode and not save) or (test != self.defaultZipCode):
						#Translators: dialog message that advise that the city will be used in temporarily mode
						message = '%s "%s" %s\n%s' % (
						_("The city"), test,
						_("has not been preset."),
						_("Will be used in temporary mode!"))
						dlg = NoticeAgainDialog(gui.mainFrame, message = message,
						#Translators: the dialog title
						title = '%s %s' % (_addonSummary, _("Notice!")))
						if dlg.ShowModal():
							dontShowAgain = dlg.GetValue()
							if dontShowAgain != self.dontShowAgain:
								self.dontShowAgain = dontShowAgain
								#preserve the default zip code and celsius values
								backup_celsius = self.celsius
								celsius = self.ReadConfig('c')
								if celsius is not None: self.celsius = celsius
								backup_zipCode = self.zipCode
								self.zipCode = self.defaultZipCode
								self.SaveConfig()
								#reassign the temporary zip code and celsius
								self.zipCode = backup_zipCode
								self.celsius = backup_celsius
								del backup_celsius, backup_zipCode

							dlg.Destroy()

			else:
				#button cancell or eskape key
				n, n, n, zipCodesList, define_dic, details_dic, defaultZipCode, n, modifiedList, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n = _mainSettingsDialog.GetValue()
				del n
				volume = self.volume
				samplesvolumes_dic = dict(self.samplesvolumes_dic)
				if modifiedList:
					#offers to save the list changed
					#Translators: the dialog title
					title = '%s %s' % (_addonSummary, _("Notice!"))
					#Translators: dialog message to warn that the list has not been saved
					message = '%s.\n%s' % (_("You have modified the list of your cities"), _("Do you want to save it?"))
					winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
					dlg= wx.MessageBox(message, title, wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
					if dlg == 2:
						#Save current cities list
						self.defaultZipCode = defaultZipCode
						self.define_dic = define_dic
						self.details_dic = details_dic
						if self.WriteList(zipCodesList):
							self.zipCodesList = zipCodesList
							Shared().Play_sound(True)

			_mainSettingsDialog.Destroy()
			Shared().Play_sound("winclose", 1)
			#enable the window for fast access of cities and Weather setting menu
			self.EnableMenu(True)

		gui.runScriptModalDialog(_mainSettingsDialog, callback2)


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
			if _pyVersion <= 2:
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
		#discard old zipcodes fromthe list
		zipCodesList = [x for x in self.zipCodesList if not x.startswith('#') and not x[x.rfind(' ')+1:].isdigit() and not Shared().IsOldZipCode(x) == True]
		if not zipCodesList:
			#Translators: dialog message of invalid city location
			message = '%s\n%s' % (
			_("The cities on your list are not compatible with the Weather API!"),
			_("They have to be tested and validated, you can do it from the addon settings window."))
			#Translators: the dialog title
			title = '%s %s' % (_addonSummary, _("Notice!"))
			gui.mainFrame.prePopup()
			dialog = MyDialog(gui.mainFrame, message, title, zipCodesList = None, newVersion = '', setZipCodeItem = self.setZipCodeItem, setTempZipCodeItem = self.setTempZipCodeItem, UpgradeAddonItem = self.UpgradeAddonItem, buttons = None, simple = True)
			dialog.Show()
			gui.mainFrame.postPopup()
			return

		s = Find_index(zipCodesList, self.tempZipCode)
		if s == None:
			s = Find_index(zipCodesList, self.defaultZipCode)

		#Translators: the dialog title to  setting a temporary city
		title = '%s - %s' % (_addonSummary, _("Setting up a temporary city"))
		#Translators: dialog message to  setting a temporary city
		message = '%s\n%s %d' % (
		Shared().Find_wbdats(), #addss short cut keys
		_("Cities List available:"),
		len(zipCodesList))
		choices=zipCodesList
		if s!= None: sel, t = s,0
		else: s, sel, t = 0, 0, -1
		Shared().Play_sound("winopen", 1)
		if "_tempSettingsDialog" not in globals(): global _tempSettingsDialog
		_tempSettingsDialog= SelectDialog(gui.mainFrame, title = title, message = message, choices = choices, last = [s], sel = 0)
		self.EnableMenu(False)

		def callback(result):
			if result == wx.ID_OK:
				selection = _tempSettingsDialog.GetValue()
				self.tempZipCode = zipCodesList[selection]
				self.ExtractData(self.tempZipCode)
				if t == -1 or s != selection: Shared().Play_sound(True)

			else:
				n = _tempSettingsDialog.GetValue()

			_tempSettingsDialog.Destroy()
			Shared().Play_sound("winclose", 1)
			self.EnableMenu(True)

		gui	.runScriptModalDialog(_tempSettingsDialog, callback)


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
		if _pyVersion <= 2:
			docFolder = os.path.dirname(__file__).decode("mbcs")
		else:
			docFolder = os.path.dirname(__file__)
		listDocs = os.listdir(docFolder.split("globalPlugins")[0]+"\\doc\\")
		if lang not in listDocs: lang = 'en'
		docFolder = docFolder.split("globalPlugins")[0]+"\\doc\\"+lang
		try:
			#prevents error if the en folder is missing
			if os.listdir(docFolder) == []:
				docFolder = docFolder.split("doc")[0]+"\\doc\\"+'en'
		except WindowsError: return False
		if os.path.exists(docFolder):
			self._docFolder = docFolder
			return True
		else:
			return False


	def onUpgrade(self, evt = None):
		"""Check for upgrade"""
		if globalVars.appArgs.secure: return #if run from systemConfig, does not check anyting

		def NoteDialog(message = "", title = "", newVersion = "", buttons = None):
			"""call the upgrade dialog"""
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
		if isinstance(data, bytes) and _pyVersion >= 3: data = data.decode()
		if not data or [True for i in ["no connect", "not found"] if i in data]:
			if evt:
				Shared().Play_sound("warn", 1)
				if "not found" in data:
					#Translators: dialog message and title used when it was not possible to find data
					NoteDialog(_("Sorry, I can not receive data, problems with the download page, try again later please!"), title)
				else:
					#Translators: dialog message and title used when it not possible to connect and receive data 
					NoteDialog(_("Sorry, I can not receive data, verify that your internet connection is active, or try again later!"), title)

			return

		#search for new version string
		try:
			newVersion = re.search(r'Version\: (\d\.\d( - \d{1,2}\.\d{1,2}\.\d{4})*)', data).group(1)
		except AttributeError: newVersion = ""
		#finally checks to see if a new version is available
		if newVersion and (float(newVersion.split()[0]) > float(_addonVersion.split()[0])):
			#Translators: dialog message that notifying the availability of a new version
			message = '%s %s %s %s\r\n%s: %s.\n%s' % (
			_addonSummary, _("version"), newVersion, _("is available."),
			_("Installed version"), _addonVersion,
			_("Do you want to download and install it?"))
			ask= view = True
		else:
			if evt: return NoteDialog(
			#Translators: dialog message used when a new version is not available
			_("Sorry, at the time an update is not available."),
			#Translators: the dialog title
			title)

		if ask:
			return NoteDialog(message, title, newVersion, True)


	def ExtractData(self, v):
		"""get city name from zip code and assign new value to current zip code"""
		self.zipCode = v
		self.city = v[:v.find(',')]
		if _pyVersion <= 2:
			try:
				self.city = self.city.decode("mbcs")
			except(UnicodeDecodeError, UnicodeEncodeError): pass


	def Play_Sample(self, condition_code = None, degrees = None, wind_f= None):
		"""Plays the sound effect if found"""
		samples_dic = {
		1000: '*', #Sunny
		1003: '*', #Partly cloudy
		1006: '*', #Cloudy
		1009: '*', #Overcast
		1030: 'Fog ambience', #Mist
		1063: 'Light rain', #Patchy rain possible
		1066: 'Snow', #Patchy snow possible
		1069: 'Sleet', #Patchy sleet possible
		1072:'Rain and snow', #Patchy freezing drizzle possible
		1087: 'Light rain', #Thundery outbreaks possible
		1114: 'Snow storm', #Blowing snow
		1117: 'Snow storm', #Blizzard
		1135: 'Fog ambience', #Fog
		1147: 'Fog ambience', #Freezing fog
		1150: 'Light rain', #Patchy light drizzle
		1153: 'Light rain', #Light drizzle
		1168: 'Sleet', #Freezing drizzle
		1171: 'Hailstorm00', #Heavy freezing drizzle
		1180: 'Light rain', #Patchy light rain",
		1183: 'Light rain', #Light rain
		1186: 'Rain', #Moderate rain at times
		1189: 'Rain', #Moderate rain
		1192: 'Heavy rain', #Heavy rain at times
		1195: 'Heavy rain', #Heavy rain
		1198: 'Light rain', #Light freezing rain
		1201: 'Rain and snow', #Moderate or heavy freezing rain
		1204: 'Sleet', #Light sleet
		1207: 'Rain and snow', #Moderate or heavy sleet
		1210: 'Snow', #Patchy light snow
		1213: 'Snow', #Light snow
		1216: 'Snow', #Patchy moderate snow
		1219: 'Snow', #Moderate snow
		1222: 'Snow storm', #Patchy heavy snow
		1225: 'Snow storm', #Heavy snow
		1237: 'Hailstorm00', #Ice pellets
		1240: 'Light rain', #Light rain shower
		1243: 'Rain', #Moderate or heavy rain shower
		1246: 'Heavy rain', #Torrential rain shower
		1249: 'Sleet', #Light sleet showers
		1252: 'Snow', #Moderate or heavy sleet showers
		1255: 'Snow', #Light snow showers
		1258: 'Snow', #Moderate or heavy snow showers
		1261: 'Light rain', #Light showers of ice pellets
		1264: 'Hailstorm00', #Moderate or heavy showers of ice pellets
		1273: 'Continuous thunder', #Patchy light rain with thunder
		1276: 'Heavy rain', #Moderate or heavy rain with thunder
		1279: 'Snow', #Patchy light snow with thunder
		1282: 'Snow storm', #Moderate or heavy snow with thunder
		'Unknown': 'Fog ambience',
		}

		v = p = sp_condition = define = ''
		current_season, p = self.Get_Season()
		if self.zipCode in self.define_dic: define = self.define_dic[self.zipCode]['define']

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
			while len(sample_list) != 0:
				i = random.choice(sample_list)
				shuffled_list.append(i);
				sample_list.remove(i)
			return shuffled_list

		def RandomizeSamples(samples_list):
			#Delete alwais from the list the last sample played
			if (self.zipCode == self.current_zipCode) and (self.current_condition == condition_code)and len(self.randomizedSamples) > 1 and _curSample in self.randomizedSamples: self.randomizedSamples.remove(_curSample); return No_double(self.randomizedSamples)
			self.current_zipCode = self.zipCode
			self.current_condition = condition_code
			#when the list is empty or zipCode is changed, is rebuilt
			self.randomizedSamples = SampleShuffle(samples_list)
			return No_double(self.randomizedSamples)

		def WindParse():
			#Delete alwais from the list the last sample played
			if (self.zipCode == self.current_zipCode) and (self.current_condition == condition_code) and len(self.randomizedSamples) > 1 and _curSample in self.randomizedSamples: self.randomizedSamples.remove(_curSample); return No_double(self.randomizedSamples)
			self.current_zipCode = self.zipCode
			self.current_condition = condition_code
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

		if condition_code in samples_dic: v = samples_dic[condition_code]
		if wind_f >= 13.0 and wind_f <= 62.0: sp_condition = 'Wind'
		elif wind_f > 63.0:
			if define == '1': sp_condition = 'Hurricane00'
			else: sp_condition = 'Tornado00'

		#special conditions
		if sp_condition:
			if sp_condition == 'Wind':
				if v in ['Snow', 'Sleet']:
					v = RandomizeSamples(['Snow and wind storm', 'Snow and wind00', 'Snow and wind01', v])
				elif v in ['*', 'Fog ambience']:
					v = WindParse()
				elif v in ['Light rain', 'Rain', 'Heavy rain', 'Continuous thunder']:
					v = RandomizeSamples(['Rain and wind', 'Rain thunder heavy rain on skylight thunder rumble and wind', 'Rain thunder heavy rain with thunder rumble and wind', 'Rain, wind and thunder', v])
			elif sp_condition == 'Tornado00':
				v = random.choice(['Tornado00', 'Tornado01'])
			elif sp_condition == 'Hurricane00':
				v = random.choice(['Hurricane00', 'Hurricane01'])

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
				#addss winter sports from November 5 to march
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
			birds = ['Birds' + str(i).rjust(2, '0') for i in range(6)]\
			+['Birds' + str(i).rjust(2, '0') for i in range(7, 13)]\
			+['Birds' + str(i).rjust(2, '0') for i in range(14, 29)]\
			+['Robin', 'Solitary sparrow', 'Swallows']
			trains = ['Level crossing', 'Train passing00', 'Train passing01', 'Train passing02']
			bikers_dic = {
			"spring": bikers,
			"summer": bikers,
			"autumn": ['Motorcycle00', 'Motorcycle03', 'Motorcycle04']}
			sea_light = ['Sea light00', 'Sea light01', 'Sea light02', 'Sea light03', 'Sea light04', 'Sea medium03']
			seaShips = ['Motorboat' + str(i).rjust(2, '0') for i in range(6)]\
			+['Jet ski' + str(i).rjust(2, '0') for i in range(3)]\
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
				#addss bathers, cicadas if temperature exceed respectively 24 and 22 degrees celsius
				bathers_dic = {0: 76, 1: 24, 2: 297} #temperatures for f, c, k scale
				cicadas_dic = {0: 72, 1: 22, 2: 295}
				samples_list = []
				cicada_beach = []
				dt = int(float(degrees.replace(',', '.')))
				if dt > bathers_dic[self.celsius] and define == "1":
					#addss bathers on the beach
					samples_list = ['Bathers on the beach00', 'Bathers on the beach01', 'Bathers on the beach02', 'Bathers on the beach03']
				if dt > cicadas_dic[self.celsius]:
					#addss the cicadas
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
					Shared().LogError(e)

			else:
				#sample not found, notify and disable audio check box
				self.toSample = 0
				#Translators: dialog message used when audio file is not found
				message = '"%s%s" %s\n%s %s.\n%s %s.' % (
				v, ext, _("not found!"),
				_("You need to upgrade the sound effects by reactivating the appropriate option from the settings of"),
				_addonSummary,
				_("But if these are already updated, then you need to update"),
				#Translators: the dialog title
				_addonSummary)
				wx.CallAfter(gui.messageBox, message, _addonSummary, wx.ICON_EXCLAMATION)
				#Try to disable the audio controls in the Settings window
				if "_mainSettingsDialog" in globals() and _mainSettingsDialog:
					_mainSettingsDialog.message1.SetLabel(_mainSettingsDialog.hotkeys[-1])
					_mainSettingsDialog.cbt_toSample.SetValue(False)
					_mainSettingsDialog.ch_vol.Enable(False)
					_mainSettingsDialog.cb_vol.Enable(False)


	def Get_Season(self, return_date=None):
		"""Return season and part of the day"""
		current_month = datetime.today().date().month
		current_day = datetime.today().date().day
		if return_date: return current_month, current_day
		try:
			current_hour = int(self.current_hour[:2])
		except TipeError: current_hour = datetime.today().time().hour

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


	def MyDefault(self, default_city=None):
		"""manage default city, read and write"""
		if default_city:
			with open(_mydefcity_path, 'wb') as w:
				try:
					w.write(default_city.encode("mbcs"))
				except(UnicodeDecodeError, UnicodeEncodeError): w.write(default_city)
				except IOError: pass

		else:
			#load default_city
			try:
				with open(_mydefcity_path, 'rb') as r:
					default_city = r.read()
			except: default_city = ''

			return default_city


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
			self.toWind = False #adds wind values
			self.toWinddir = True #adds wind direction
			self.toWindspeed = True #adds wind speed
			self.toSpeedmeters = True #adds speed in meters per second
			self.toWindgust = True #adds wind gust
			self.toPerceived = True #adds perceived temperature
			self.toHumidity = True #adds umidity value
			self.toVisibility = True #adds visibility value
			self.toPressure = True #adds pressure value
			self.toMmhgpressure = False #indicates pressure in mmHg
			self.toUltraviolet = True #adds UV radiations
			self.toCloud = True #adds cloudines values
			self.toPrecip = True #adds precipitation values
			self.toAtmosphere = False #adds atmosphere values
			self.toAstronomy = False #adds astronomy values
			self.toWindspeed_hf = True #hourlyforecast data report
			self.toWinddir_hf = True
			self.toWindgust_hf = True
			self.toCloud_hf = True
			self.toHumidity_hf = True
			self.toVisibility_hf = True
			self.toPrecip_hf = True
			self.toUltraviolet_hf = True
			self.to24Hours = True #use 24 hours format
			self.dontShowAgain = False #check box no longer display this message
			self.dontShowAgainAddDetails = False #check box no longer display this message
			self.toComma = False #use the comma as decimal separator
			self.toOutputwindow = False #use a window as output
			self.toUpgrade = True #check for upgrades
			#total days forecast
			self.forecast_days = "1" #forecasts from 1 to _maxDaysApi value
			#api response language
			self.apilang = 'English, en'
			#volume controls
			self.toAssign = 0 #general audio volume - 1 = current audio volume
			self.samplesvolumes_dic = dict(samplesvolumes_dic)#set volume from percentage to float (0, 0.1, 0.2, etc. up to 1)
			global _handle, _curSample, _volume
			self.handle = _handle = None #sound allocated in memory
			self.curSample = _curSample = None #name of audio effect in memory
			_volume = self.volume = "60%" #default volume of the current sample

		config_weather = os.path.join(globalVars.appArgs.configPath,"Weather.ini")
		if os.path.isfile(config_weather):
			config = ConfigObj(config_weather)
			config.bools = {'True': True, 'False': False, 'true': True, 'false': False, '': False}
			cws = config['Weather Settings']
			try:
				if singleRead == "c":
					if 'Celsius' in cws: return int(cws['Celsius'])

				if 'Celsius' in cws: self.celsius = int(cws['Celsius'])
				if 'Scale as' in cws: self.scaleAs = int(str(cws['Scale as']))
				if 'To Clipboard' in cws: self.toClip = config.bools[cws['To Clipboard']]
				if 'Help Buttons' in cws: self.toHelp = config.bools[cws['Help Buttons']]
				if 'Audio Effects' in cws: self.toSample = config.bools[cws['Audio Effects']]
				if 'Use only weather effects' in cws: self.toWeatherEffects = config.bools[cws['Use only weather effects']]
				if 'Assigned volume' in cws: self.toAssign = int(cws['Assigned volume'])
				if 'Samples volume' in cws: self.volume = '%s' % cws['Samples volume']
				if 'Forecast max days' in cws: self.forecast_days = cws['Forecast max days']
				if 'api response language' in cws: self.apilang = cws['api response language']
				if 'Add wind' in cws: self.toWind = config.bools[cws['Add wind']]
				if 'Addspeedtometers' in cws: self.toSpeedmeters = config.bools[cws['Addspeedtometers']]
				if 'Addperceivedtemperature' in cws: self.toPerceived = config.bools[cws['Addperceivedtemperature']]
				if 'Add atmosphere' in cws: self.toAtmosphere = config.bools[cws['Add atmosphere']]
				if 'Addhumidity' in cws: self.toHumidity = config.bools[cws['Addhumidity']]
				if 'Addvisibility' in cws: self.toVisibility = config.bools[cws['Addvisibility']]
				if 'Addwinddirection' in cws: self.toWinddir = config.bools[cws['Addwinddirection']]
				if 'Addwindspeed' in cws: self.toWindspeed = config.bools[cws['Addwindspeed']]
				if 'Addwindgust' in cws: self.toWindgust = config.bools[cws['Addwindgust']]
				if 'Add cloudines' in cws: self.toCloud = config.bools[cws['Add cloudines']]
				if 'Add precipitation' in cws: self.toPrecip = config.bools[cws['Add precipitation']]
				if 'Addpressure' in cws: self.toPressure = config.bools[cws['Addpressure']]
				if 'Indicate pressure to mmHg' in cws: self.toMmhgpressure = config.bools[cws['Indicate pressure to mmHg']]
				if 'Add ultraviolet' in cws: self.toUltraviolet = config.bools[cws['Add ultraviolet']]
				if 'Add hourlyforecast windspeed' in cws: self.toWindspeed_hf = config.bools[cws['Add hourlyforecast windspeed']]
				if 'Add hourlyforecast winddir' in cws: self.toWinddir_hf = config.bools[cws['Add hourlyforecast winddir']]
				if 'Add hourlyforecast gust' in cws: self.toWindgust_hf = config.bools[cws['Add hourlyforecast gust']]
				if 'Add hourlyforecast cloudines' in cws: self.toCloud_hf = config.bools[cws['Add hourlyforecast cloudines']]
				if 'Add hourlyforecast humidity' in cws: self.toHumidity_hf = config.bools[cws['Add hourlyforecast humidity']]
				if 'Add hourlyforecast visibility' in cws: self.toVisibility_hf = config.bools[cws['Add hourlyforecast visibility']]
				if 'Add hourlyforecast precipitation' in cws: self.toPrecip_hf = config.bools[cws['Add hourlyforecast precipitation']]
				if 'Add hourlyforecast ultraviolet' in cws: self.toUltraviolet_hf = config.bools[cws['Add hourlyforecast ultraviolet']]
				if 'Add astronomy' in cws: self.toAstronomy = config.bools[cws['Add astronomy']]
				if '24 hours clock' in cws: self.to24Hours = config.bools[cws['24 hours clock']]
				if 'Use a comma as separator' in cws: self.toComma = config.bools[cws['Use a comma as separator']]
				if 'Use a window as output' in cws: self.toOutputwindow = config.bools[cws['Use a window as output']]
				if 'Check for upgrade' in cws: self.toUpgrade = config.bools[cws['Check for upgrade']]
				if 'Dont show again' in cws: self.dontShowAgain = config.bools[cws['Dont show again']]
				if 'Dont show again add details' in cws: self.dontShowAgainAddDetails = config.bools[cws['Dont show again add details']]
				self.zipCode = self.MyDefault()
			except IOError:
				Shared().Play_sound("warn", 1)
				return wx.CallAfter(wx.MessageBox, _("I can not load the settings!"), '%s - %s' % (_addonSummary, _("Attention!")))
			_volume = self.volume

			if not self.zipCode or self.zipCode.isspace(): return
			#search in list
			self.zipCodesList, self.define_dic, details_dic = Shared().LoadZipCodes()
			if _pyVersion >= 3: city = self.FindCity(self.zipCode.decode("mbcs"))
			else: city = self.FindCity(self.zipCode)
			if city:
				if _pyVersion <= 2:
					self.defaultZipCode = self.tempZipCode= city =city.decode("mbcs")
				else:
					self.defaultZipCode = self.tempZipCode= city

				self.city = city[:city.rfind(',')] #takes the cityname
				_testCode = Shared().GetLocation(self.defaultZipCode, self.define_dic)

			else: self.defaultZipCode = self.tempZipCode = self.zipCode = '' #if  no list available


	def SaveConfig(self):
		"""Save datas into configuration Weather.ini"""
		config = ConfigObj()
		config_weather = os.path.join(globalVars.appArgs.configPath,"Weather.ini")
		config.filename = config_weather
		config ["Weather Settings"] = {
		"Celsius": self.celsius,
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
		"api response language": self.apilang,
		"Check for upgrade": self.toUpgrade,
		"Addwinddirection": self.toWinddir,
		"Addwindspeed": self.toWindspeed,
		"Addspeedtometers": self.toSpeedmeters,
		"Addwindgust": self.toWindgust,
		"Addperceivedtemperature": self.toPerceived,
		"Addhumidity": self.toHumidity,
		"Addvisibility": self.toVisibility,
		"Addpressure": self.toPressure,
		"Add cloudines": self.toCloud,
		"Add precipitation": self.toPrecip,
		"Add ultraviolet": self.toUltraviolet,
		"Add hourlyforecast windspeed": self.toWindspeed_hf,
		"Add hourlyforecast winddir": self.toWinddir_hf,
		"Add hourlyforecast gust": self.toWindgust_hf,
		"Add hourlyforecast cloudines": self.toCloud_hf,
		"Add hourlyforecast humidity": self.toHumidity_hf,
		"Add hourlyforecast visibility": self.toVisibility_hf,
		"Add hourlyforecast precipitation": self.toPrecip_hf,
		"Add hourlyforecast ultraviolet": self.toUltraviolet_hf,
		"Indicate pressure to mmHg": self.toMmhgpressure,
		"Use a comma as separator": self.toComma,
		"Use a window as output": self.toOutputwindow,
		"Use only weather effects": self.toWeatherEffects,
		"Dont show again": self.dontShowAgain,
		"Dont show again add details": self.dontShowAgainAddDetails
		}
		try:
			config.write()
			self.MyDefault(self.zipCode)
		except IOError:
			Shared().Play_sound("warn", 1)
			return ui.message(_("I can not save the settings!"))


	def WriteList(self, zipCodesList):
		"""Save cities list """
		try:
			with open(_zipCodes_path, 'w') as file:
				file.write("[cities list]\n")
				for r in sorted(zipCodesList):
					#citi and (zipcode or acronim)
					r = '%s\t%s\n' % (r[:-len(r.split()[-1])-1], r.split()[-1])
					try:
						file.write(r)
					except(UnicodeDecodeError, UnicodeEncodeError):
						file.write('%s, %s\t%s\n' % (
						_("invalid name").title(), r.split()[1].upper(), r.split()[-1]))

			#addss cities definitions
			with open(_zipCodes_path, 'a') as file:
				file.write("\n[Cities Location Key and Definitions]\n")
				for i in self.define_dic:
					if _pyVersion <= 2:
						try:
							r = '#%s\t%s\t%s\n' % (i, (self.define_dic[i]["location"].decode("mbcs")), self.define_dic[i]["define"])
						except(UnicodeDecodeError, UnicodeEncodeError): 
							r = '#%s\t%s\t%s\n' % (i, (self.define_dic[i]["location"]), self.define_dic[i]["define"])
					else: r = '#%s\t%s\t%s\n' % (i, self.define_dic[i]["location"], self.define_dic[i]["define"])
					if _pyVersion >= 3: file.write(r)
					else:
						try:
							file.write(r.encode("mbcs"))
						except(UnicodeDecodeError, UnicodeEncodeError): file.write(r)

			#addss cities details
			with open(_zipCodes_path, 'a') as file:
				file.write("\n[Cities Details]")
				for i in self.details_dic:
					r = '\n%s' % i #adds zip code number (record name)
					for f in _fields:
						#addss all the fields to record
						r += '\t%s' % self.details_dic[i][f]

					if _pyVersion >= 3: file.write(r)
					else:
						try:
							file.write(r.encode("mbcs"))
						except(UnicodeDecodeError, UnicodeEncodeError):
							try:
								file.write(r)
							except(UnicodeDecodeError, UnicodeEncodeError): continue

		except IOError:
			Shared().WriteError(_addonSummary)
			return False
		else: return True


	def FindCity(self, zipCode):
		"""Find the name of the 	city from zipcode list"""
		lzc = [x for x in self.zipCodesList]
		try:
			i = False
			i = lzc.index(zipCode)
		except (IndexError, ValueError): return i
		return self.zipCodesList[i]


	def getWeather(self, zip_code, forecast = False):
		"""Main getWeather function gets weather from Weather API"""
		if zip_code != "" and not zip_code.isspace():
			mess = ""
			if self.dom == "no connect" or self.dom and (self.tempZipCode != self.test[0]) or not self.dom or (datetime.now() - self.test[-1]).seconds/60 >= _wait_delay:
				#but refresh dom if the city are changed or if the waiting time is finished
				self.dom, mess = self.Open_Dom(zip_code)
				self.test[0] = self.tempZipCode
				self.test[-1] = datetime.now()

			if not self.dom or self.dom in ["not authorized", "no connect"]: self.dom = None; return
			try:
				self.dom['current']['last_updated_epoch']
			except (KeyError, TypeError): self.dom = None; return self.ZipCodeError()

			scale_as = self.GetScaleAs() #degrees indication selected
			if not forecast:
				condition = self.dom['current']['condition']['text']
				condition_code = self.dom['current']['condition']['code'] #for sound effects param
				cloudiness_string = _("The cloudiness is")
				precip_string = _("The precipitation is")
				unit_speed, unit_distance, unit_precip, unit_pressure, unit_uv = self.GetUnitValues(self.celsius)
				# default parameter _f for Fahrenheit
				temperature =self.dom['current']['temp_f']
				wind_chill = self.dom['current']['feelslike_f']
				wind_f = wind_speed = self.dom['current']['wind_mph'] #wind_f for sound effects param
				wind_gust = self.dom['current']['gust_mph']
				#I withdraw the most reliable pressure in millibars because the API does not exactly convert millibars to inHg
				press = self.dom["current"]["pressure_mb"]
				#and convert it to inHg
				pressure = self.Pressure_convert(press)
				if self.toMmhgpressure:
					#takes the value in mmHg from pressure_mb
					pressure = self.Pressure_convert(press, mmHg = True)

				visibility = self.dom['current']['vis_miles']
				precipitation = self.dom['current']['precip_in']
				sptm = self.Speedtometers(wind_speed, convert = False, meters = True) #takes speed in meters per second
				sptm_gust = self.Speedtometers(wind_gust, convert = False, meters = True) #takes gust speed in meters per second
				uv = self.dom['current']['uv']
				if self.celsius != 0:
					#only for Celsius and Kelvin
					temperature =self.dom['current']['temp_c']
					wind_chill = self.dom['current']['feelslike_c']
					if self.celsius == 2:
						#convert c° to k°
						temperature = self.Temperature_convert(temperature)
						wind_chill = self.Temperature_convert(wind_chill)

					wind_speed = self.dom['current']['wind_kph']
					wind_gust = self.dom['current']['gust_kph']
					if not self.toMmhgpressure:
						pressure = self.dom["current"]["pressure_mb"]

					visibility = self.dom['current']['vis_km']
					precipitation = self.dom['current']['precip_mm']
					unit_speed, unit_distance, unit_precip, unit_pressure, unit_uv = self.GetUnitValues(self.celsius)
				if not self.toSpeedmeters: sptm = sptm_gust = ""
				temperature = self.IntClean(temperature)
				wind_chill = self.IntClean(wind_chill)
				wind_speed = self.IntClean(wind_speed)
				wind_gust = self.IntClean(wind_gust)
				visibility = self.IntClean(visibility)
				pressure = self.IntClean(pressure)
				precipitation = self.IntClean(precipitation)
				uv = self.IntClean(uv)
				weatherReport = '%s %s %s %s, %s.' % (
				_("the weather report is currently"),
				temperature, _("degrees"),
				scale_as,
				condition
				)
				weatherReport = weatherReport.replace(" , ", ", ")
				if self.toWind:
					#addss wind information to the string 
					winddirstring = _("The wind direction is from")
					winddirvalue = self.GetCardinalDirection('%s' % self.dom['current']['wind_degree']) or _nr
					if self.toWinddir and self.toWindspeed:
						#adds  wind direction and speed
						weatherReport += '\n%s %s %s %s %s %s.' % (
						winddirstring, winddirvalue,
						_("with speed of"), wind_speed or _nr, unit_speed,
						sptm)
					elif self.toWindspeed and not self.toWinddir:
						#adds only wind speed
						weatherReport += '\n%s %s %s %s.' % (
						_("The wind speed is"), wind_speed or _nr, unit_speed,
						sptm
						)
					elif self.toSpeedmeters and self.toWinddir:
						#adds wind direction and speed in meters per seconds
						weatherReport += '\n%s %s, %s %s.' % (
						winddirstring, winddirvalue,
						_("with speed of"), sptm[2:-1])
					elif self.toSpeedmeters and not self.toWindspeed and not self.toWinddir:
						#adds only wind speed
						weatherReport += '\n%s %s.' % (
						_("The wind speed is"), sptm[2:-1])
					elif self.toWinddir and not self.toWindspeed and not self.toSpeedmeters:
					#adds only wind direction
						weatherReport += '\n%s %s.' % (
						winddirstring, winddirvalue)
					if self.toWindgust:
						#adds wind gust
						weatherReport += '\n%s %s %s %s.' % (
						_("The wind gusts are of"), wind_gust or _nr, unit_speed, sptm_gust)
					if self.toPerceived:
						weatherReport += '\n%s %s %s.' % (
						_("The perceived temperature is"), wind_chill or _nr, _("degrees"))

					weatherReport = weatherReport.replace("  ", " ")
					weatherReport = weatherReport.replace(" .", ".")

				if self.toAtmosphere:
					#addss information on the atmosphere
					humiditystring = _("The humidity is")
					humidityvalue = self.dom['current']['humidity'] or _nr
					cloudiness_string = _("The cloudiness is of")
					cloudiness_value = self.dom['current']['cloud']
					precip_string = _("The precipitation is of")
					if self.toHumidity and self.toVisibility:
						#adds humidity and visibility
						weatherReport += '\n%s %s%%, %s %s %s.' % (
						humiditystring, humidityvalue,
						_("and the visibility is up to"),
						visibility or _nr, unit_distance)
					elif self.toHumidity and not self.toVisibility:
						#adds only humidity
						weatherReport += '\n%s %s%%.' % (
						humiditystring, humidityvalue)
					elif self.toVisibility and not self.toHumidity:
						#adds only visibility
						weatherReport += '\n%s %s %s.' % (
						_("The visibility is up to"), visibility or _nr, unit_distance)
					if  self.toCloud and self.toPrecip:
						#adds cloudines and precipitation
						weatherReport += '\n%s %s%%, %s %s %s.' % (
						cloudiness_string, cloudiness_value,
						_("and the precipitation is"),
						precipitation or _nr, unit_precip)

					elif self.toPrecip and not self.toCloud:
						#adds only precipitation
						weatherReport += '\n%s %s %s.' % (
						precip_string,
						precipitation or _nr, unit_precip)

					elif self.toCloud and not self.toPrecip:
						#adds only cloudines
						weatherReport += '\n%s %s%%.' % (
						cloudiness_string, cloudiness_value)

					if self.toPressure:
						#adds pressure
						weatherReport += '\n%s %s %s.' % (
						_("The pressure is"), pressure or _nr, unit_pressure)
				if self.toUltraviolet:
					#adds UV radiations
					weatherReport += '\n%s %s %s.' % (
					_("The UV radiation is of"), uv or _nr, unit_uv)

				if self.toAstronomy:
					#addss astronomical information
					try:
						sr = self.dom['forecast']['forecastday'][0]['astro']['sunrise']
					except IndexError: return Shared().JsonError()
					ss = self.dom['forecast']['forecastday'][0]['astro']['sunset']
					lr = self.dom['forecast']['forecastday'][0]['astro']['moonrise']
					ls = self.dom['forecast']['forecastday'][0]['astro']['moonset']
					if self.to24Hours:
						sr = Shared().To24h(sr) #sunrise
						ss = Shared().To24h(ss) #sunset
						lr = Shared().To24h(lr) #moonrise
						ls = Shared().To24h(ls) #moonset
					else:
						sr = Shared().Add_zero(sr)
						ss = Shared().Add_zero(ss)
						lr = Shared().Add_zero(lr)
						ls = Shared().Add_zero(ls)

					weatherReport += '\n%s %s %s %s.\n%s %s %s %s.' % (
					_("The sun rises at"), sr or _nr,
					_("and sets at"), ss or _nr,
					_("The moon rises at"), lr or _nr,
					_("and sets at"), ls or _nr)
					weatherReport = weatherReport.replace("No moonrise",_("No moonrise"))
					weatherReport = weatherReport.replace("No moonset",_("No moonset"))
					weatherReport = weatherReport.replace("No sunrise", _("No sunrise"))
					weatherReport = weatherReport.replace("No sunset", _("No sunset"))

				if self.toSample and os.path.exists(_samples_path):
					self.Play_Sample(condition_code, temperature, wind_f) #He plays the appropriate sound effect if present

			else:
				#gets forecast from Weather API
				lenForecast = len(self.dom['forecast']['forecastday'])
				if not self.forecast_days: self.forecast_days = "1"
				intForecast = int (self.forecast_days)
				if intForecast > lenForecast:
					intForecast = lenForecast
					self.forecast_days = str(lenForecast)

				month1 = ""
				try:
					high = self.dom['forecast']['forecastday'][0]['day']['maxtemp_f'] or _nr
					low = self.dom['forecast']['forecastday'][0]['day']['mintemp_f'] or _nr
				except IndexError: return Shared().JsonError()
				if self.celsius != 0: #conversion only for Celsius and Kelvin degrees scale
					high = self.dom['forecast']['forecastday'][0]['day']['maxtemp_c'] or _nr
					low = self.dom['forecast']['forecastday'][0]['day']['mintemp_c'] or _nr

				weatherReport = '%s %s %s %s %s %s %s %s.' % (
				_("the forecast for today is"),
				self.dom['forecast']['forecastday'][0]['day']['condition']['text'],
				_("with a maximum temperature of"), self.IntClean(high),
				_("and a minimum of"), self.IntClean(low),
				_("degrees"), scale_as)
				weatherReport = weatherReport.replace(" .", ".")
				#addss the remaining days set from user
				for i in range(1, intForecast):
					try:
						week_day = date.fromtimestamp(self.dom['forecast']['forecastday'][i]['date_epoch'])
					except IndexError:
						#limit days weather forecast reached
						break

					month = week_day.month
					if month1 == month:
						week_day = Shared().ConvertDate(week_day, False) #Omit the month
					else:
						week_day = Shared().ConvertDate(week_day)
						month1 = month
					high = self.dom['forecast']['forecastday'][i]['day']['maxtemp_f'] or _nr
					low = self.dom['forecast']['forecastday'][i]['day']['mintemp_f'] or _nr
					if self.celsius != 0: #Celsius and Kelvin degrees scale
						high = self.dom['forecast']['forecastday'][i]['day']['maxtemp_c'] or _nr
						low = self.dom['forecast']['forecastday'][i]['day']['mintemp_c'] or _nr

					weatherReport += ' %s %s %s %s %s %s %s.' % \
					(week_day,
					self.dom['forecast']['forecastday'][i]['day']['condition']['text'],
					_("with a maximum temperature of"), self.IntClean(high),
					_("and a minimum of"), self.IntClean(low),
					_("degrees"))

			weatherReport = weatherReport.replace(". ", ".\r\n")
			#puts the city name at the left top 
			weatherReport = '%s %s, %s' % \
			(_("In"), self.city or _("Unnamed"), weatherReport)
			if mess:
				#notify last build date failed
				Shared().Play_sound("messagefailure", 1)
				weatherReport = '%s\n%s' % (mess, weatherReport)

			if self.toClip:
				# Copy the bulletin or weather forecasts to the clipboard.
				api.copyToClip(weatherReport)
			if self.toOutputwindow:
				#output to a window
				Shared().ViewDatas(weatherReport)

		else:
			Shared().Play_sound(False, 1)
			weatherReport = _("Sorry, the city is not set!")
		return weatherReport


	def Open_Dom(self, zip_code):
		"""Upload DOM data from the Weather API"""
		ui.message(_plzw)
		attempts = 2 #connection attempts
		curDate = datetime.now()
		api_query = Shared().GetLocation(zip_code, self.define_dic) or _testCode
		if not api_query: return '', self.ZipCodeError()
		def Read_API(): return Shared().WeatherConnect(api_query, self.apilang)
		dom = Read_API()
		if not dom:
			#If it doesn't receive data, try again a few times
			repeat = attempts
			while not dom:
				time.sleep(0.5)
				Shared().Play_sound("wait", 1)
				dom = Read_API()
				repeat -= 1
				if repeat == 0: break
			if not dom: return self.ZipCodeError(), ""
		elif "no connect" in dom:
			Shared().Play_sound("warn", 1)
			wx.CallAfter(ui.message, _("Sorry, I can not receive data, verify that your internet connection is active, or try again later!"))
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
				time.sleep(0.1)
				t = (t + 1) % 7 #this construct cicle from 0 to 6
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
			timezone_id = dom['location']['tz_id']
			self.current_hour, n = Shared().GetTimezone(timezone_id, to24Hours = True)
		except KeyError: return dom, ""
		return dom, message


	def IntClean(self, v):
		"""remove .0 at the end of the value and add the comma if request"""
		v = str(v)
		if v.endswith('.0'): v = v[:-2]
		if self.toComma: v = v.replace('.', ',')
		return v


	def CConvertDate(self, dd, m = True):
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
			#Convert miles to kilometers
			v = v * 1.61

		if meters:
			#convert miles into meters per second
			ms = 0.44704*vm
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
		"""convert millibars to inces of mercury or millibars to mmHg"""
		if not pressure: return ""
		#pressure value must be in millibars
		pressure = float(pressure)
		#convert millibars to incis of mercury
		pressure = pressure/33.8639
		pre = round(pressure,2)
		if mmHg:
			#convert inHg to mmHg
			pre = round((25.4*pressure),2)

		pre = self.IntClean(pre)
		if self.toComma: pre = pre.replace('.', ',')
		return pre


	def Temperature_convert(self, temperature):
		"""convert Celsius to Kelvin"""
		if not temperature: return ""
		temperature = float(temperature)
		return int(round(temperature + 273.15))


	def ZipCodeError(self):
		"""This construct cycles between 0, 1, every two errors of the same zip code he warns"""
		self.note[0] = (self.note[0] + 1) % 2
		self.note[1] = self.zipCode
		if not self.setZipCodeItem.IsEnabled(): self.note[0] = 1
		check, n, i = Shared().ZipCodeInList(self.zipCode, self.zipCodesList)
		if self.note[0] and check:
			#Problems with the city from the list
			self.Notice(i)
			return ""

		Shared().Play_sound(False,1)
		ui.message(_("Sorry, the city set is not valid or contains incomplete data!"))


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
		"""A city is no longer valid, and suggests to delete it from the list"""
		winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		self.EnableMenu(False)
		self.cityDialog = wx.MessageDialog(gui.mainFrame, '%s "%s".\n%s\n%s %s\n%s.' % (
		#Translators: dialog message in case of invalid city or with incomplete data
		_("The city"), self.zipCode,
		_("Is not working properly, contains incomplete data or has been removed from the"),
		"Weather API Database.",
		_("It could be a temporary problem and you may wait a while '..."),
		_("Do you want to delete it from your list?")),
		#Translators: the dialog title
		'%s %s' % (_addonSummary, _("Notice!")),
		wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

		def callback3(result):
			if result == wx.ID_YES:
				try:
					e = ''
					rollBack = list(self.zipCodesList)
					rollBack2 = dict(self.define_dic)
					rollBack3 = dict(self.details_dic)
					if "_mainSettingsDialog" in globals() and _mainSettingsDialog:
						_mainSettingsDialog.OnRemove()
					else:
						zc = self.zipCodesList.pop(index)
						decoded_zc = zc
						if _pyVersion <= 2: decoded_zc = zc.decode("mbcs")
						code = zc
						if code in self.define_dic: del self.define_dic[code]
						if code in self.details_dic: del self.details_dic[code]
						if decoded_zc == self.defaultZipCode:
							self.zipCode = self.defaultZipCode = ''
							backup_celsius = self.celsius
							self.celsius = self.ReadConfig('c')
							self.SaveConfig()
							self.celsius = backup_celsius

				except ValueError as e: pass
				if not e:
					if not _mainSettingsDialog:
						self.city = index #Temporarily for _mainSettingsDialog, deleted item position
						self.zipCode = self.tempZipCode = ''
						if self.WriteList(self.zipCodesList): Shared().Play_sound("del", 1)

					else:
						self.zipCodesList = rollBack
						self.define_dic = rollBack2
						self.details_dic = rollBack3
						del rollBack, rollBack2, rollBack3
				if not _mainSettingsDialog and not _tempSettingsDialog: self.EnableMenu(True)

			else:
				if not _mainSettingsDialog and not _tempSettingsDialog: self.EnableMenu(True)

		gui.runScriptModalDialog(self.cityDialog, callback3)


	def getHourlyForecast(self):
		"""announces the hourly forecast"""
		if not self.zipCode or self.zipCode.isspace():
			#warn if there is no city set
			Shared().Play_sound(False, 1)
			return ui.message(_("Sorry, the city is not set!"))

		if self.dom == "no connect" or self.dom and (self.tempZipCode != self.test[0]) or not self.dom or (datetime.now() - self.test[-1]).seconds/60 >= _wait_delay:
			#but refresh dom if the city are changed or if the waiting time is finished
			self.dom, n = self.Open_Dom(self.zipCode)
			self.test[0] = self.tempZipCode
			self.test[-1] = datetime.now()

		if not self.dom: self.dom, n = self.Open_Dom(self.zipCode)
		if not self.dom or self.dom in["not authorized", "no connect"]: self.dom = None; return self.ZipCodeError()
		#reads city local time
		timezone_id = self.dom['location']['tz_id']
		h, n = Shared().GetTimezone(timezone_id, to24Hours = True)
		hour = int(h[:h.find(':')])
		hour = (hour + 1) % 24 #this construct cicle from 0 to 23
		unit_speed, unit_distance, unit_precip, n, unit_uv = self.GetUnitValues(self.celsius)
		scale_as = self.GetScaleAs()
		wir =_("Chance of rain")
		wis = _("Chance of snow")
		weatherReport = ''
		for h in range(hour, 24):
			#hourly forecast start from the current hour
			try:
				condition = self.dom['forecast']['forecastday'][0]['hour'][h]['condition']['text']
			except IndexError: return Shared().JsonError()
			wind_degree = self.dom['forecast']['forecastday'][0]['hour'][h]['wind_degree']
			wind_degree = self.GetCardinalDirection('%s' % wind_degree) or _nr
			cloud = self.dom['forecast']['forecastday'][0]['hour'][h]['cloud']
			humidity = self.dom['forecast']['forecastday'][0]['hour'][h]['humidity']
			rain = str(self.dom['forecast']['forecastday'][0]['hour'][h]['chance_of_rain']) or _nr
			snow = str(self.dom['forecast']['forecastday'][0]['hour'][h]['chance_of_snow']) or _nr
			uv = self.dom['forecast']['forecastday'][0]['hour'][h]['uv']
			if self.celsius != 0:
				#is not Fahrenheit:
				temperature = self.dom['forecast']['forecastday'][0]['hour'][h]['temp_c']
				wind_speed = self.dom['forecast']['forecastday'][0]['hour'][h]['wind_kph']
				wind_gust = self.dom['forecast']['forecastday'][0]['hour'][h]['gust_kph']
				visibility = self.dom['forecast']['forecastday'][0]['hour'][h]['vis_km']
				precipitation = self.dom['forecast']['forecastday'][0]['hour'][h]['precip_mm']
				if self.celsius == 2:
					#Celsius and Kelvin degrees
					#convert c° to k°
					temperature = self.Temperature_convert(temperature)

			else:
				#Fahrenheit degrees
				temperature = self.dom['forecast']['forecastday'][0]['hour'][h]['temp_f']
				wind_speed = self.dom['forecast']['forecastday'][0]['hour'][h]['wind_mph']
				wind_gust = self.dom['forecast']['forecastday'][0]['hour'][h]['gust_mph']
				visibility = self.dom['forecast']['forecastday'][0]['hour'][h]['vis_miles']
				precipitation = self.dom['forecast']['forecastday'][0]['hour'][h]['precip_in']

			#clean zero values decimals and apply the comma if request
			temperature = self.IntClean(temperature)
			wind_speed = self.IntClean(wind_speed)
			wind_gust = self.IntClean(wind_gust)
			visibility = self.IntClean(visibility)
			precipitation = self.IntClean(precipitation)
			uv = self.IntClean(precipitation)
			hour = Shared().Add_zero(str(h)+":00", False) #24 hour format
			if not self.to24Hours:
				if h in range(0, 13): hour = '%s AM' % str(h).rjust(2,'0')
				else: hour = '%s PM' % (str(h-12).rjust(2, "0"))
				
			text = []
			if self.toWindspeed_hf: text.append('%s %s %s' % (_("Wind speed"), wind_speed, unit_speed))
			if self.toWinddir_hf and self.toWindspeed_hf: text.append('%s %s' % (_("Direction"), wind_degree))
			elif self.toWinddir_hf and not self.toWindspeed_hf: text.append('%s %s' % (_("Wind direction"), wind_degree))
			if self.toWindgust_hf: text.append('%s %s %s' % (_("Wind gusts"), wind_gust, unit_speed))
			if self.toCloud_hf: text.append('%s %s%%' % (_("Cloudiness"), cloud))
			if self.toPrecip_hf: text.append('%s %s %s' % (_("Precipitation"), precipitation, unit_precip))
			if self.toHumidity_hf: text.append('%s %s%%' % (_("Humidity"), humidity))
			if self.toVisibility_hf: text.append('%s %s %s' % (_("Visibility"), visibility, unit_distance))
			if self.toUltraviolet_hf: text.append('%s %s %s' % ("UV", uv, unit_uv))
			if len(text) > 2:  text[2] = text[2]+'.\n'
			line = ', '.join(text).replace('\n, ', '\n')+'.'
			weatherReport += '%s: %s, %s %s %s.\n%s.\n' % (
			hour, condition, temperature, _("degrees"), scale_as,
			line)
			weatherReport = weatherReport.replace('..', '.')
			#adds chance of rain and snow
			if rain != "0" and str(snow) != "0":
				weatherReport += '%s %s%%, %s %s%%.\n' % (
			wir,rain, wis, snow)
			elif rain!= "0" and snow == "0":
				weatherReport += '%s %s%%.\n' % (wir,rain)
			elif snow!= "0" and rain == "0":
				weatherReport += '%s %s%%.\n' % (wis, snow)

			weatherReport = weatherReport.replace(' .', '.')

		weatherReport = '%s %s:\n'% (_("Hourly forecast for"), self.city) + weatherReport
		if self.toClip:
			# Copy the hourly forecast to the clipboard.
			api.copyToClip(weatherReport)

		if self.toOutputwindow:
			Shared().ViewDatas(weatherReport)

		return ui.message(weatherReport)


	def script_announceWeather(self, gesture):
		"""announce current weather bulletin"""
		if self.IsOpenDialog(self.cityDialog): return
		if self.zipCode != self.note[1]: self.note = [1, self.zipCode]
		ui.message(self.getWeather(self.zipCode))
		#try  to update the volume of new played sound effect, if  it's in dictionary 
		if "_mainSettingsDialog"in globals() and _mainSettingsDialog:
			select = _mainSettingsDialog.ch_vol.GetSelection()
			if select == 1 and _curSample != "":
				if _curSample in samplesvolumes_dic:
					_mainSettingsDialog.cb_vol.SetValue(samplesvolumes_dic[_curSample])
				else:
					_mainSettingsDialog.cb_vol.SetValue(_volume)

	script_announceWeather.__doc__ = _("Provides the current temperature and weather conditions.")


	def script_announceForecast(self, gesture):
		"""announce the weather forecast for the set days or the hourly forecast"""
		if self.IsOpenDialog(self.cityDialog): return
		if self.zipCode != self.note[1]: self.note = [1, self.zipCode]
		repeatCount =scriptHandler.getLastScriptRepeatCount()
		if repeatCount == 1:
			ui.message(self.getHourlyForecast())
		else: ui.message(self.getWeather(self.zipCode, True))

	script_announceForecast.__doc__ = _("If pressed once, announce the weather forecast and current temperature for 24 hours and the next %d days. If pressed twice announce the hourlyforecast temperature and weather conditions.") % (_maxDaysApi -1)


	def script_zipCodeEntry(self, gesture):
		"""Entering a temporary city"""
		try:
			if not self.zipCodesList:
				Shared().Play_sound(False, 1)
				return ui.message(_("Sorry, no list available!"))
		except AttributeError: pass
		#do not proceed if the window settings is open, but puts it in the foreground
		if not self.setZipCodeItem.IsEnabled():
			if "_notifyDialog" in globals() and _notifyDialog:
				try:
					_notifyDialog.Raise()
					_notifyDialog.Show()
				except: pass
				return wx.Bell()

			elif self.cityDialog:
				try:
					self.cityDialog.Raise()
					self.cityDialog.Show()
				except: pass
				return wx.Bell()
			elif "_findDialog" in globals() and _findDialog:
				try:
					_findDialog.Raise()
					_findDialog.Show()
				except: return
				return wx.Bell()
			else:
				try:
					Shared().CloseDialog(_weatherReportDialog)
				except NameError: pass
				try:
					_tempSettingsDialog.Raise()
					_temSettingsDialog.Show()
				except: pass
				return wx.Bell()

		self.EnableMenu(False)
		self.setZipCodeDialog()

	script_zipCodeEntry.__doc__ = _("Allows you to set a temporary city.")


	def script_swapTempScale(self, gesture):
		"""swap and set a measurement degrees scale"""
		self.celsius = (self.celsius + 1) %3 # This construct cycles between 0, 2
		if _mainSettingsDialog:
			#change the radio button in the settings window
			self.celsius = _mainSettingsDialog.rb.GetSelection()
			self.celsius = (self.celsius + 1) % 3
			_mainSettingsDialog.rb.SetSelection(self.celsius)
			_mainSettingsDialog.rb.SetFocus()

		Shared().Play_sound("swap", 1)
		ui.message('%s %s' % (_("Scale of temperature measurement set into"), _tempScale[self.celsius]))

	script_swapTempScale.__doc__ = _("Allows you to set a temporary scale of temperature mesurement.")


	def script_announceLastBuildDate(self, gesture):
		"""announces the date and time of last weather report"""
		if self.IsOpenDialog(self.cityDialog): return
		if not self.zipCode or self.zipCode.isspace():
			#warn if there is no city set
			Shared().Play_sound(False, 1)
			return ui.message(_("Sorry, the city is not set!"))

		if self.dom == "no connect" or self.dom and (self.tempZipCode != self.test[0]) or not self.dom or (datetime.now() - self.test[-1]).seconds/60 >= _wait_delay:
			#but refresh dom if the city are changed or if the waiting time is finished
			self.dom, n = self.Open_Dom(self.zipCode)
			self.test[0] = self.tempZipCode
			self.test[-1] = datetime.now()

		if not self.dom: self.dom, n = self.Open_Dom(self.zipCode)
		if not self.dom or self.dom in["not authorized", "no connect"]: self.dom = None; return self.ZipCodeError()
		#not documented, displays API response json data  debugging
		repeatCount =scriptHandler.getLastScriptRepeatCount()
		if repeatCount == 2:
			title = '%s - %s' % (_addonSummary, "Note: Feature not documented, only for debiugging.")
			message ='Location: %s.\r\n' % (self.dom["location"]["name"] or '""')
			message += 'Region: %s.\r\n' % (self.dom["location"]["region"] or '""')
			message += 'Country: %s.\r\n' % (self.dom["location"]["country"] or '""')
			m = self.zipCode
			if _pyVersion < 3:
				try:
					m = self.zipCode.decode("mbcs")
				except(UnicodeDecodeError, UnicodeEncodeError): pass

			message += 'self.zipCode: %s.\r\n' % (m or '""')
			m = Shared().GetLocation(self.zipCode, self.define_dic) or _testCode
			if _pyVersion < 3:
				try:
					m = m.decode("mbcs")
				except(UnicodeDecodeError, UnicodeEncodeError): pass

			message += '_api_query: %s.\r\n' % m
			m = _testCode
			if _pyVersion < 3:
				try:
					m = m.decode("mbcs")
				except(UnicodeDecodeError, UnicodeEncodeError): pass

			message += '_testCode (temporary api query): %s.' % (m or '""')
			message += '\r\n\r\n[API response json]\n%s' % self.dom
			Shared().ViewDatas(message, title); return

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

		weatherReport = ('%s: %s.' % (_("Last update of the current weather report"), last_build_date))
		ui.message(weatherReport)
		if self.toClip:
			# Copy the bulletin last edit date to the clipboard.
			api.copyToClip(weatherReport)

	script_announceLastBuildDate.__doc__ = _("Announces the date of the last update of the weather report.")


	def script_weatherPlusSettings(self, gesture):
		"""Call the Weather Plus settings dialog"""
		#do not proceed if the window settings is open, but puts it in the foreground
		if not self.setZipCodeItem.IsEnabled():
			if "_notifyDialog" in globals() and _notifyDialog:
				try:
					_notifyDialog.Raise()
					_notifyDialog.Show()
				except: pass
				return wx.Bell()

			elif self.cityDialog:
				try:	
					self.cityDialog.Raise()
					self.cityDialog.Show()
				except: pass
				return wx.Bell()
			elif "_downloadDialog" in globals() and _downloadDialog:
				try:
					_downloadDialog.Raise()
					_downloadDialog.Show()
				except: pass
				return wx.Bell()

			elif "_helpDialog" in globals() and _helpDialog:
				try:
					_helpDialog.Raise()
					_helpDialog.Show()
				except:pass
				return wx.Bell()

			elif "_findDialog" in globals() and _findDialog:
				try:
					_findDialog.Raise()
					_findDialog.Show()
				except: pass
				return wx.Bell()

			elif "_searchDialog" in globals() and _searchDialog:
				try:
					_searchDialog.Raise()
					_searchDialog.Show()
				except: pass
				return wx.Bell()

			elif "_tempSettingsDialog" in globals() and _tempSettingsDialog:
				Shared().CloseDialog(_weatherReportDialog)
				try:
					_tempSettingsDialog.Raise()
					_tempSettingsDialog.Show()
				except: return
				return wx.Bell()

			else:
				try:
					Shared().CloseDialog(_weatherReportDialog)
				except NameError: pass
				try:
					_mainSettingsDialog.Raise()
					_mainSettingsDialog.Show()
				except: return
				return wx.Bell()

		self.onSetZipCodeDialog(None)

	script_weatherPlusSettings.__doc__ = _("Open the Weather Plus settings dialog.")


	__gestures = {
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
			define_dic = {}, details_dic = {}, forecast_days = "", apilang = "", toUpgrade = None, toPerceived = None, toHumidity = None, toVisibility = None, toPressure = None, toMmhgpressure = None, toUltraviolet = None, toCloud = None, toPrecip = None, toWinddir = None, toWindspeed = None, toWindgust = None, toComma = None, toOutputwindow = None, toWeatherEffects = None,
			toWinddir_hf = None, toWindspeed_hf = None, toWindgust_hf = None, toHumidity_hf = None, toVisibility_hf = None, toCloud_hf = None, toPrecip_hf = None, toUltraviolet_hf = None, dontShowAgainAddDetails = False):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos,
		size=size, style=style)

		self.apilang = apilang
		self.toOutputwindow = toOutputwindow
		self.toWinddir_hf = toWinddir_hf
		self.toWindspeed_hf = toWindspeed_hf
		self.toWindgust_hf = toWindgust_hf
		self.toHumidity_hf = toHumidity_hf
		self.toVisibility_hf = toVisibility_hf
		self.toCloud_hf = toCloud_hf
		self.toPrecip_hf = toPrecip_hf
		self.toUltraviolet_hf = toUltraviolet_hf
		self.dontShowAgainAddDetails = dontShowAgainAddDetails
		sizer = wx.BoxSizer(wx.VERTICAL)
		#loads cities list from Weather.zipcodes
		zipCodesList, define_dic, details_dic = Shared().LoadZipCodes()
		_testCode = self.testCode = self.testName = self.testDefine = self.last_tab = ""
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
		if _pyVersion <= 2:
			cbx=wx.ComboBox(self, -1, style=wx.CB_DROPDOWN|wx.TE_RICH, choices = [i.decode("mbcs") for i in zipCodesList])
		else:
			cbx=wx.ComboBox(self, -1, style=wx.CB_DROPDOWN|wx.TE_RICH, choices = zipCodesList)

		s = tempZipCode
		if not s: s = defaultZipCode
		if _pyVersion <= 2:
			try:
				s = s.encode("mbcs")
			except(UnicodeDecodeError, UnicodeEncodeError): pass

		if zipCodesList and s in zipCodesList:
			if _pyVersion <= 2:
				cbx.SetStringSelection(s.decode("mbcs"))
			else:
				cbx.SetStringSelection(s)

		else:
			if _pyVersion < 3:
				try:
					cbx.SetValue(s or "")
				except(UnicodeDecodeError, UnicodeEncodeError):
					try:
						cbx.SetValue(s.encode("mbcs") or "")
					except(UnicodeDecodeError, UnicodeEncodeError):
						try:
							cbx.SetValue(s.decode("mbcs") or "")
						except(UnicodeDecodeError, UnicodeEncodeError): pass

			else:
				cbx.SetValue(s or "")

			if s: self.testName = s

		hbox.Add(cbx, 0, wx.EXPAND|wx.ALL, 5)
		self.zipCodesList = zipCodesList
		self.tempZipCode = tempZipCode
		self.defaultZipCode = defaultZipCode
		self.define_dic = define_dic
		self.details_dic = details_dic
		self.samplesvolumes_dic = samplesvolumes_dic
		self.modifiedList = False
		if wx.version().split(".")[0] >= "4":
			helpButton = wx.adv.CommandLinkButton
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
		btn_Hourlyforecast = helpButton(self, -1, _("&hourlyforecast setting..."), "", style=wx.BU_EXACTFIT)
		hbox2.Add(btn_Import, 1, wx.EXPAND|wx.ALL, 5)
		hbox2.Add(btn_Export, 1, wx.EXPAND|wx.ALL, 5)
		hbox2.Add(btn_Hourlyforecast, 1, wx.EXPAND|wx.ALL, 5)
		sizer.Add(hbox2, 1, wx.ALIGN_CENTER_HORIZONTAL)
		self.Bind(wx.EVT_BUTTON, self.OnImport, btn_Import)
		self.Bind(wx.EVT_BUTTON, self.OnExport, btn_Export)
		self.Bind(wx.EVT_BUTTON, self.OnHourlyforecastSet, btn_Hourlyforecast)
		self.btn_Import = btn_Import
		self.btn_Export = btn_Export
		self.btn_Hourlyforecast = btn_Hourlyforecast
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
			_("Unspecified")],
			3, style=wx.RB_GROUP)
		self.rb1.SetSelection(scaleAs)
		sizer.Add(self.rb1, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		#combo box forecast days
		if forecast_days and isinstance(forecast_days, str):	
			forecast_days = str(forecast_days)
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(self, -1, _("Weather Forecasts up to days:"))
		cb_days=wx.ComboBox(self, -1, style = wx.CB_READONLY,choices = ['%s' % i for i in range(1, _maxDaysApi+1, 1)]) #set from 1 to max days api days
		cb_days.SetValue(forecast_days)
		if not cb_days.GetValue():
			cb_days.SetValue('1')
		hbox3.Add(st, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 5)
		hbox3.Add(cb_days, 0, wx.ALL, 5)
		sizer.Add(hbox3)
		self.cb_days = cb_days
		#combo box API languages
		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(self, -1, _("API response language:"))
		choices = Shared().APILanguage() #get languages list
		cb_apilang=wx.ComboBox(self, -1, style = wx.CB_READONLY, choices = choices)
		cb_apilang.SetValue(apilang)
		hbox4.Add(st, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 5)
		hbox4.Add(cb_apilang, 0, wx.ALL, 5)
		sizer.Add(hbox4)
		self.cb_apilang = cb_apilang
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
			self.cbt_toWeatherEffects.Enable(False)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.cbt_toSample)
		#check boxes
		self.cbt_toHelp = wx.CheckBox(self, -1, _("Enable &help buttons in the settings window"))
		self.cbt_toHelp.SetValue(bool(toHelp))
		sizer.Add(self.cbt_toHelp, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.toHelp = toHelp
		self.OnHelp_notes()
		self.Bind(wx.EVT_CHECKBOX, self.OnHelp_notes, self.cbt_toHelp)

		self.cbt_toWind = wx.CheckBox(self, -1, _("Read &wind information"))
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

		self.cbt_toWindgust = wx.CheckBox(self, -1, _("Add wind &gust speed"))
		self.cbt_toWindgust.SetValue(bool(toWindgust))
		sizer.Add(self.cbt_toWindgust, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toPerceived = wx.CheckBox(self, -1, _("Add perceived &temperature"))
		self.cbt_toPerceived.SetValue(bool(toPerceived))
		sizer.Add(self.cbt_toPerceived, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.OnCheckBox3(self.cbt_toWind)

		self.cbt_toAtmosphere = wx.CheckBox(self, -1, _("&Read atmospherical information"))
		self.cbt_toAtmosphere.SetValue(bool(toAtmosphere))
		sizer.Add(self.cbt_toAtmosphere, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox4, self.cbt_toAtmosphere)

		self.cbt_toHumidity = wx.CheckBox(self, -1, _("Add humidity va&lue"))
		self.cbt_toHumidity.SetValue(bool(toHumidity))
		sizer.Add(self.cbt_toHumidity, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toVisibility = wx.CheckBox(self, -1, _("Add &visibility value"))
		self.cbt_toVisibility.SetValue(bool(toVisibility))
		sizer.Add(self.cbt_toVisibility, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toCloud = wx.CheckBox(self, -1, _("Add cloudiness &value"))
		self.cbt_toCloud.SetValue(bool(toCloud))
		sizer.Add(self.cbt_toCloud, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toPrecip = wx.CheckBox(self, -1, _("Add precipitation &value"))
		self.cbt_toPrecip.SetValue(bool(toPrecip))
		sizer.Add(self.cbt_toPrecip, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toUltraviolet = wx.CheckBox(self, -1, _("Add &ultraviolet radiation value"))
		self.cbt_toUltraviolet.SetValue(bool(toUltraviolet))
		sizer.Add(self.cbt_toUltraviolet, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toPressure = wx.CheckBox(self, -1, _("Add atmospheric &pressure value"))
		self.cbt_toPressure.SetValue(bool(toPressure))
		sizer.Add(self.cbt_toPressure, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toMmhgpressure = wx.CheckBox(self, -1, _("Indicates the atmospheric pressure in millimeters of mercur&y (mmHg)"))
		self.cbt_toMmhgpressure.SetValue(bool(toMmhgpressure))
		sizer.Add(self.cbt_toMmhgpressure, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.OnCheckBox4(self.cbt_toAtmosphere)

		self.cbt_toAstronomy = wx.CheckBox(self, -1, _("Read a&stronomical information"))
		self.cbt_toAstronomy.SetValue(bool(toAstronomy))
		sizer.Add(self.cbt_toAstronomy, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_to24Hours = wx.CheckBox(self, -1, _("Enable reading of the hours in &24-hour format"))
		self.cbt_to24Hours.SetValue(bool(to24Hours))
		sizer.Add(self.cbt_to24Hours, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		self.to24Hours = to24Hours

		self.cbt_toComma = wx.CheckBox(self, -1, _("Use the comma to separate decimals, example (4,&15)"))
		self.cbt_toComma.SetValue(bool(toComma))
		sizer.Add(self.cbt_toComma, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toOutputwindow = wx.CheckBox(self, -1, _("&Displays output in a window"))
		self.cbt_toOutputwindow.SetValue(bool(toOutputwindow))
		sizer.Add(self.cbt_toOutputwindow, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toUpgrade = wx.CheckBox(self, -1, _("Check for &upgrade"))
		self.cbt_toUpgrade.SetValue(bool(toUpgrade))
		sizer.Add(self.cbt_toUpgrade, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		sizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.CENTRE| wx.ALL|wx.EXPAND, 5)
		self.btn_Ok = self.FindWindowById(wx.ID_OK)
		self.btn_Cancel = self.FindWindowById(wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self.OnEnter_wbdat, self.btn_Ok)
		self.cbx = cbx
		self.f1 = 0 #after a few errors recommend you press F1
		self.WidgetFocusControl()
		self.ButtonsEnable(False)
		if globalVars.appArgs.secure:
			#disable possible FileDialog openings in safe mode
			btn_Import.Enable(False)
			btn_Export.Enable(False)
			self.cbt_toSample.Enable(False)

		self.OnText()
		if cbx.GetValue() == "":
			#primary combo box empty
			self.btn_Ok.Enable(False)

		self.SetSizerAndFit(sizer)
		self.Layout()
		self.Center(wx.BOTH|wx.Center)
		self.cbx.SetFocus() #primary combo box
		self.last_tab = cbx


	def OnHelp_notes(self, evt = None):
		"""enables or disables the help notices for the buttons"""
		if self.cbt_toHelp.IsChecked():
			self.btn_Test.SetNote(_("Test the city validity  and find the data of it."))
			self.btn_Add.SetNote(_("Add the current city into your list."))
			self.btn_Details.SetNote(_("Displays information about the current city."))
			self.btn_Define.SetNote(_("Allows you to define the area, in order to adapt the sound effects."))
			self.btn_Apply.SetNote(_("Presets the current city as the default, will be used every time you restart the plugin."))
			self.btn_Remove.SetNote(_("Delete  the current city from your list."))
			self.btn_Rename.SetNote(_("Rename the current city."))
			self.btn_Import.SetNote(_("Permits to incorporate in your list new cities importing them from another list with the extension *.zipcodes; you can select the city you want to import, by turning on the check box associated."))
			self.btn_Export.SetNote(_("Permits to save your list of cities in a specified path."))
			self.btn_Hourlyforecast.SetNote(_("Allows you to choose the contents of the hourly forecast report."))
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
			self.btn_Export,
			self.btn_Hourlyforecast
			): i.SetNote("")


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
		self.btn_Hourlyforecast.Bind(wx.EVT_CHAR, self.OnKey)
		self.cb_days.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter_wbdat, self.cb_days)
		self.cb_apilang.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter_wbdat, self.cb_apilang)
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

		self.cbt_toWindgust.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toWindgust)
		self.cbt_toPerceived.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toPerceived)
		self.cbt_toHumidity.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toHumidity)
		self.cbt_toVisibility.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toVisibility)
		self.cbt_toPressure.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toPressure)
		self.cbt_toMmhgpressure.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toUltraviolet)
		self.cbt_toUltraviolet.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toMmhgpressure)
		self.cbt_toCloud.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toCloud)
		self.cbt_toPrecip.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toPrecip)
		self.cbt_toComma.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toComma)
		self.cbt_toOutputwindow.Bind(wx.EVT_CHAR, self.OnKey)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox2, self.cbt_toOutputwindow)
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
			helpDialog = HelpEntryDialog(gui.mainFrame,
			#Translators: message in the help window
			message = '%s:\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s:\n%s.\n%s.\n%s.\n%s:\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.\n%s.' % (
			_("You can enter or search for a city"),
			_("By Latitude and Longitude: 48.8567,2.3508"),
			_("By City name: Paris"),
			_("By City name and country: Toronto,Canada"),
			_("Or Toronto,CA"),
			_("By City name and region: Toronto,Ontario"),
			_("By US zip: 10001"),
			_("By UK postcode: SW1"),
			_("By Canada postal code: G2J"),
			_("By metar:<metar code>: metar:EGLL"),
			_("By iata:<3 digit airport code>: iata:DXB"),
			_("By auto:ip IP lookup: auto:ip"),
			_("By IP address (IPv4 and IPv6 supported): 100.0.0.1"),
			_("if there will be cities with the same name, will be listed"),
			_("By default, confirming a selection, is used the postal code"),
			_("If the postal code is not valid, will be used a text string: city, state, region"),
			_("You can indicate how to proceed by prefixing the following commands"),
			_("Direct (cities with the same name, will not listed), by typing D:City: D:Paris"),
			_("Geographic coordinates, by typing G:City: G:Venezia"),
			_("Text string, by typing T:City: T:Bologna"),
			_("If the city is not found"),
			_("Try to reverse the order in the search key"),
			_("Try with or without the country of origin"),
			_("Try to merge the name with hyphens, or separate it with separator"),
			_("Try deleting apostrophes"),
			_("Try changing the vowels accented with normal vowels"),
			_("Try to change in English some parts"),
			_("Try with a closest location")
			),
			#Translators: the title of the help window
			title = _("Help placing"))
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

		else:
			self.last_tab = cur_tab
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
			Shared().LogError(e)

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
		#Translators: dialog used when there is no sound in memory
		wx.MessageBox('%s\n%s' % (
		_("No sound effect in memory!"),
		_("I can't reproduce the sound.")),
		#Translators: the dialog title
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
			if _pyVersion <= 2:zcs = self.zipCodesList[i].decode("mbcs")
			else: zcs = self.zipCodesList[i]
			if Shared().IsOldZipCode(zcs):
				Shared().Play_sound("totest", 1)
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

		if v1 == self.defaultZipCode:
			self.btn_Apply.Enable(False)
		elif (v1 != self.defaultZipCode and self.defaultZipCode and not self.btn_Test.IsEnabled())\
		or (not self.defaultZipCode and not self.btn_Test.IsEnabled()):
			self.btn_Apply.Enable(True)

		if v1 == '':
			self.ButtonsEnable(False)
			self.btn_Ok.Enable(False)
		elif self.testName == v1:
			self.btn_Test.Enable(False)
			self.btn_Add.Enable(True)
			self.btn_Apply.Enable(True)
			self.btn_Details.Enable(True)

		if self.btn_Test.IsEnabled():
			self.btn_Ok.Enable(False)
		elif not self.btn_Test.IsEnabled() and not v.isspace() and v:
			self.btn_Ok.Enable(True)


	def OnEnter_wbdat(self, evt):
		"""enter key event"""
		evt.Skip()
		self.EndModal(wx.ID_OK)


	def OnTest(self, evt = None):
		"""button Test event"""
		selected_city = value = value2 = self.cbx.GetValue()
		coords = Shared().GetCoords(value)
		if coords: value = coords
		elif Shared().IsOldZipCode(value):
			value2 = value[:value.rfind(' ')] #search key with city name and country acronym
			#create a search key list from the city details if available
			c = value.split(',')[0] #get city name
			z = value.split()[-1] #get zipcode number
			search_keys = []
			self.testDefine = '0'
			if z in self.define_dic: self.testDefine = self.define_dic[z]['define'] #get a define value from old zipcode if available
			if z in self.details_dic and not 'fail' in self.details_dic[z]['city']:
				search_keys.append('%s, %s, %s' % (
				self.details_dic[z]['city'],
				self.details_dic[z]['region'],
				self.details_dic[z]['country']))
				search_keys.append('%s, %s' % (
				self.details_dic[z]['city'],
				self.details_dic[z]['country']))
				search_keys.append('%s, %s' % (
				self.details_dic[z]['lat'],
				self.details_dic[z]['lon']))
				#allows you to choose how to search for the city
				Shared().Play_sound("subwindow", 1)
				#Translators: dialog message used in the setting window to specify a certain one area
				try:
					dlc = wx.SingleChoiceDialog(
					self, '%s: "%s"' % (
					#Translators: message dialog
					_("Choose search key for"), c),
					#Translators: title dialog
					_addonSummary,
					choices=search_keys)
					dlc.SetSelection(0)
					if dlc.ShowModal() == wx.ID_CANCEL:
						dlc.Destroy()
						return Shared().Play_sound("subwindow", 1)
				finally:
					dlc.Destroy
					Shared().Play_sound("subwindow", 1)

				value = search_keys[dlc.GetSelection()]
				value2 = value

			else:
				#translators: window that warns the user that it was not possible to retrieve data from the database details
				winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
				if wx.MessageBox('%s\n%s' % (
				#Translators: the dialog message
				_("Unfortunately I could not recover enough data to find the city."),
				_("Do I try anyway?")),
				#Translators: the dialog title
				_addonSummary, wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION) !=2:
					return self.cbx.SetFocus()

				#try to locate the city deleting the number of the old zipcode
				value = value[:value.rfind(' ')]

		else:
			#search for city recurrences with geonames
			selected_city = Shared().Search_cities(value)
			if not selected_city: return
			elif selected_city not in ["Error", "noresult"]:
				value2 = value = selected_city

		#Test as Cityname
		cityName, v = Shared().ParseEntry(value, self.apilang)
		if cityName == "no connect":
			self.Disable_all(False)
			Shared().Play_sound("warn", 1)
			return ui.message(_("Sorry, I can not receive data, verify that your internet connection is active, or try again later!"))
		elif not cityName:
			self.Disable_all()
			if (selected_city == value) and value.isdigit() and not ',' in value: return self.API_errorDialog(selected_city, True)
			else:
				self.f1 = (self.f1 + 1) % 3
				if self.f1 == 1: return ui.message('%s %s' % (value2, _("not found! Press F1 for help on entering data.")))
				return ui.message('%s %s' % (value2, _("not found!")))

		value = Shared().SetCityString('%s, %s' % (cityName, v))
		try:
			self.cbx.SetValue(value)
		except(UnicodeDecodeError, UnicodeEncodeError):
			self.cbx.SetValue(value.encode("mbcs"))

		check, n, n =Shared().ZipCodeInList(value, self.zipCodesList)
		if not check:
			Shared().Play_sound(True)
			if "_testCode" not in globals(): global _testCode
			if _pyVersion <= 2: _testCode = self.testCode = value2.encode("mbcs")
			else: _testCode = self.testCode = value2
			self.testName = value

		else:Shared().Play_sound("alreadyinlist")

		self.OnText()
		self.btn_Test.Enable(False)
		self.btn_Ok.Enable(True)
		self.cbx.SetFocus()


	def API_errorDialog(self, v, id_error = None):
		"""Notice if the code is not valid, or poorly functioning"""
		text = '%s\n%s\n%s' % (
		_("Is not working properly or has been removed from the database of"),
		"Weather API.",
		_("It could be a temporary problem and you may wait a while '..."))
		if id_error:
			text = _("Is no longer valid!")

		wx.MessageBox('%s "%s"\n%s' % (
		#Translators: dialog message used to describe one of the 2 types of errors in city
		_("The city"), v,
		text,
		),
		#Translators: the dialog title
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
			#Translators: dialog message and title to manage the sound effects
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
			source = "/".join((_addonBaseUrl, 'weather_samples2.zip?download=1'))

			#perform target in temporary folder
			import tempfile
			if _pyVersion >= 3:
				target = "/".join((tempfile.gettempdir(), 'Weather_samples.zip'))
			else: target = "/".join((tempfile.gettempdir().decode("mbcs"), 'Weather_samples.zip'))
			#Translators: title and message used in tthe progress qdialog
			title = _("Update in progress")
			if not reload: title = _("Installation in progress")
			message = _plzw
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
					Shared().LogError(e)
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

				#Translators: dialog message and title used when the sound effects installation or upgrade is finished
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
		windCheckboxis = [self.cbt_toWinddir, self.cbt_toWindspeed, self.cbt_toSpeedmeters, self.cbt_toWindgust, self.cbt_toPerceived]
		atmosphereCheckboxis = [self.cbt_toHumidity, self.cbt_toVisibility, self.cbt_toPressure, self.cbt_toCloud, self.cbt_toPrecip, self.cbt_toUltraviolet]
		if self.last_tab in windCheckboxis:
			if [x.GetValue() for x in windCheckboxis].count(False) == 4:
			 	#prevents you from to disable all the check boxes in wind information
				wx.Bell()
				self.last_tab.SetValue(True)

		elif self.last_tab in atmosphereCheckboxis:
			if [x.GetValue() for x in atmosphereCheckboxis].count(False) == 5:
				#prevents you from to disable all the check boxes in atmosphere information
				wx.Bell()
				self.last_tab.SetValue(True)

		if not self.cbt_toPressure.IsChecked(): self.cbt_toMmhgpressure.Enable(False)
		elif self.cbt_toPressure.IsEnabled(): self.cbt_toMmhgpressure.Enable(True)
		evt.Skip()


	def OnCheckBox3(self, evt = None):
		"""disable all items if wind information is not activate"""
		flag = True
		if not evt.IsChecked(): flag = False
		[i.Enable(flag) for i in [self.cbt_toWinddir, self.cbt_toWindspeed, self.cbt_toSpeedmeters, self.cbt_toWindgust, self.cbt_toPerceived]]


	def OnCheckBox4(self, evt = None):
		"""disable all items if atmosphere information is not activate"""
		flag = evt.IsChecked()
		[i.Enable(flag) for i in [self.cbt_toHumidity, self.cbt_toVisibility, self.cbt_toPressure, self.cbt_toMmhgpressure, self.cbt_toCloud, self.cbt_toPrecip, self.cbt_toUltraviolet]]


	def AudioControlsEnable(self, f5):
		"""remove f5 key shortcut and disable audio controls"""
		self.message1.SetLabel(self.hotkeys_dic[f5])
		return [i.Enable(f5) for i in [self.cbt_toWeatherEffects, self.ch_vol, self.cb_vol]]


	def CloseWind(self, dialog):
		dialog.Destroy()
		self.cbt_toSample.SetFocus()


	def ErrorMessage(self, e = None):
		#Translators: dialog message and title used to notify lack of connection or corrupt file, during the sound effects installation
		message = _("Verify that your internet connection is active, or try again later.")
		if e: message = _("File corrupted or not available!")
		wx.MessageBox('%s\n%s' %
			(_("Sorry, I could not complete the installation of the sound effects!"), message),
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
			except(UnicodeDecodeError, UnicodeEncodeError): gv = self.cbx.GetValue()

		return (
		self.cb_days.GetValue(),
		self.cb_apilang.GetValue(),
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
		self.cbt_toWindgust.GetValue(),
		self.cbt_toAtmosphere.GetValue(),
		self.cbt_toAstronomy.GetValue(),
		self.cbt_to24Hours.GetValue(),
		self.cbt_toPerceived.GetValue(),
		self.cbt_toHumidity.GetValue(),
		self.cbt_toVisibility.GetValue(),
		self.cbt_toPressure.GetValue(),
		self.cbt_toCloud.GetValue(),
		self.cbt_toPrecip.GetValue(),
		self.cbt_toWinddir.GetValue(),
		self.cbt_toWindspeed.GetValue(),
		self.cbt_toMmhgpressure.GetValue(),
		self.cbt_toUltraviolet.GetValue(),
		self.toWindspeed_hf,
				self.toWinddir_hf,
		self.toWindgust_hf,
		self.toCloud_hf,
		self.toHumidity_hf,
		self.toVisibility_hf,
		self.toPrecip_hf,
		self.toUltraviolet_hf,
		self.cbt_toComma.GetValue(),
		self.cbt_toOutputwindow.GetValue(),
		self.cbt_toWeatherEffects.GetValue(),
		self.dontShowAgainAddDetails	,
		self.ch_vol.GetSelection()
		)


	def OnDetails(self, evt):
		"""Displays information about selected city"""
		ui.message(_plzw)
		dic = ''
		encoded_value = value = self.cbx.GetValue()
		if _pyVersion <= 2: encoded_value = value.encode("mbcs")
		if "ramdetails_dic" in globals() and value in ramdetails_dic: dic = ramdetails_dic
		elif value in self.details_dic: dic = self.details_dic
		if dic: city, region, country, country_acronym, timezone_id, latitude, longitude = self.GetFieldsValues(dic, value)
		else:
			if "ramdetails_dic" in globals() and encoded_value in ramdetails_dic: dic = ramdetails_dic
			elif encoded_value in self.details_dic: dic = self.details_dic
			if dic: city, region, country, country_acronym, timezone_id, latitude, longitude = self.GetFieldsValues(dic, encoded_value)
			elif not dic:
				#no city details, try to retrieve the city details from the API
				api_query = Shared().GetLocation(value, self.define_dic)
				connect, n = Shared().ParseEntry(api_query, self.apilang)
				if connect == "no connect":
					Shared().Play_sound("warn", 1)
					ui.message(_("Sorry, I can not receive data, verify that your internet connection is active, or try again later!"))
					return self.cbx.SetFocus()

				if "ramdetails_dic" in globals() and value in ramdetails_dic:
					self.details_dic.update(ramdetails_dic)
					city, region, country, country_acronym, timezone_id, latitude, longitude = self.GetFieldsValues(ramdetails_dic, encoded_value)
					if encoded_value in self.zipCodesList:
						Shared().Play_sound(True, 1)
						self.modifiedList = True
						if not self.dontShowAgainAddDetails:
							message = _("The details of this city are not in the database and so I added them to the list.")
							if self.toOutputwindow:
								#Translators: dialog message that advise that the missing city details have been reloaded and added to the city
								dl = NoticeAgainDialog(gui.mainFrame, message = message,
								#Translators: the dialog title
								title = '%s %s' % (_addonSummary, _("Notice!")))
								if dl.ShowModal():
									dontShowAgainAddDetails = dl.GetValue()
									if dontShowAgainAddDetails != self.dontShowAgainAddDetails:
										self.dontShowAgainAddDetails = dontShowAgainAddDetails

									dl.Destroy()

							else: ui.message(message)

				else:
					Shared().Play_sound("warn", 1)
					ui.message(_("Cannot identify your location, due to insufficient data."))
					return self.cbx.SetFocus()

		current_hour, current_date = Shared().GetTimezone(timezone_id, self.to24Hours)
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
			ui.message(_("Sorry, I can not receive data, verify that your internet connection is active, or try again later!"))
			return self.cbx.SetFocus()

		city_details = ""
		city_name = real_city_name = city
		if not value[-4:].startswith(','):
			city_name = value[:-2] #usny = us
			real_city_name = '%s, %s' % (city, country_acronym)

		city_details = Shared().FindForGeoName(real_city_name, city_name, latitude, longitude)
		if not city_details: city_details = '%s, %s, %s, %s' % (city, region, country, country_acronym)
		city_details += ', %s' % timezone_id
		title = "%s %s" % (_("Details of"), value)
		if not self.toOutputwindow:
			Shared().Play_sound("details", 1)
			ui.message(title)

		cd = city_details
		if _pyVersion < 3:
			try:
				cd = city_details.decode("mbcs")
			except(UnicodeDecodeError, UnicodeEncodeError): pass
		message = "%s: %s.\r\n" % (_("Place"), (cd or _nr))
		message += "%s: %s (%s).\r\n" % (_("Current local time"), (current_hour or _nr),  (current_date or _nr))
		message += "%s: %s.\r\n" % (_("Degrees latitude"), (lat or _nr))
		message += "%s: %s.\r\n" % (_("Degrees longitude"), (lon or _nr))
		message += "%s: %s %s." % (_("Elevation above sea level"), elevation, _("meters"))
		self.cbx.SetFocus()
		if self.toClip:
			# Copy the city details to the clipboard.
			api.copyToClip('%s\r\n%s' % (title, message))

		if self.toOutputwindow:
			#output to a window
			Shared().ViewDatas('%s\r\n%s' % (title, message))
		else: ui.message(message) 


	def OnDefine(self, evt):
		"""Defines the current city area"""
		encoded_value = value = self.cbx.GetValue()
		if _pyVersion <= 2: encoded_value = value.encode("mbcs")

		dd = Shared().GetDefine(value, self.define_dic)
		if dd is None:
			dd = Shared().GetDefine(encoded_value, self.define_dic)
		def_define = [int(dd) if dd is not None else 0][0]
		Shared().Play_sound("subwindow", 1)
		#Translators: dialog message used in the setting window to specify a certain one area
		dl = wx.SingleChoiceDialog(
		self, '%s: "%s"' % (
		_("Define the area for"), value),
		#Translators: title dialog
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
			Shared().Play_sound("subwindow", 1)
			return self.cbx.SetFocus()

		define = str(dl.GetSelection())
		if define != str(def_define):
			self.modifiedList = True
			if value in self.define_dic: self.define_dic[value]['define'] = define
			elif encoded_value in self.define_dic: self.define_dic[encoded_value]['define'] = define
			Shared().Play_sound(True)
		dl.Destroy()
		Shared().Play_sound("winclose", 1)
		return self.cbx.SetFocus()


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


	def OnAdd(self, evt):
		"""Add city button event"""
		value = self.cbx.GetValue()
		if value not in self.zipCodesList:
			v = value

			if self.testName: value2 = self.testName
			elif self.tempZipCode: value2 = self.tempZipCode
			double, name, v1 = self.CheckName(value2, value)
			if double:
				result = self.Warning(value2,v1,  v)
				if result == wx.ID_CANCEL: return self.cbx.SetFocus()
				elif result == wx.ID_NO:
					value = name
				else: value = value2

			elif name == value2: value = value2
			else: value = name
			if _pyVersion <= 2:
				try:
					value = value.encode("mbcs")
				except(UnicodeDecodeError, UnicodeEncodeError): pass

			self.zipCodesList.append(value)
			self.zipCodesList.sort()
			#adds search key and default define to value
			self	.define_dic.update({v: {"location": self.testCode.title() or _testCode.title(), "define": self.testDefine or '0'}})

			#addss cities details
			if "ramdetails_dic" in globals() and v in ramdetails_dic:
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
		if _pyVersion <= 2: encoded_value = value.encode("mbcs")
		if encoded_value not in self.zipCodesList:
			v = value

			if self.testName: value2 = self.testName
			elif self.tempZipCode: value2 = self.tempZipCode
			double, name, v1 = self.CheckName(value2, value)
			if double:
				result = self.Warning(value2, v1,  v)
				if result == wx.ID_CANCEL: return self.cbx.SetFocus()
				elif result == wx.ID_NO:
					value = name
				else: value = value2

			elif name == value2: value = value2
			else: value = name
			if _pyVersion <= 2:
				try:
					value = value.encode("mbcs")
				except(UnicodeDecodeError, UnicodeEncodeError): pass

			self.zipCodesList.append(value)
			self.zipCodesList.sort()
			#adds search key and default define to value
			self	.define_dic.update({v: {"location": self.testCode.title() or _testCode.title(), "define": self.testDefine or '0'}})

			#addss cities details
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
		if _pyVersion <= 2: encoded_value = value.encode("mbcs")
		if encoded_value in self.zipCodesList:
			index = self.GetIndex(value, self.zipCodesList)
			self.zipCodesList.remove(encoded_value)
			if value == self.defaultZipCode:
				self.defaultZipCode = ""
				self.ReTitle(_("None")) #removes the city from the title bar
				self.btn_Apply.Enable(True) #enable preset button

			self.cbx.Delete(index)
			self.cbx.SetValue('')
			try:
				if len(self.zipCodesList) == 0: self.ComboSet('')
				elif index == len(self.zipCodesList): self.ComboSet(self.zipCodesList[-1])
				else: self.ComboSet(self.zipCodesList[index])
			except IndexError: pass

			#Remove city definition and city details
			if value in self.define_dic: del self.define_dic[value]
			elif encoded_value in self.define_dic: del self.define_dic[encoded_value]
			if value in self.details_dic: del self.details_dic[value]
			elif encoded_value in self.details_dic: del self.details_dic[encoded_value]
			Shared().Play_sound("del", 1)
			if Shared().IsOldZipCode(self.cbx.GetValue()): time.sleep(0.5)
			self.OnText()
			self.cbx.SetFocus()


	def OnRename(self, evt):
		"""rename the city selected"""
		value = self.cbx.GetValue()
		name = value.split(', ')[0]
		part_right = value.split(', ')[-1]
		Shared().Play_sound("subwindow", 1)
		#Translators: dialog to change the city name
		dl = wx.TextEntryDialog(self,
		#Translators: the dialog message
		_("Enter new name."),
		#Translators: title dialog
		_addonSummary,
		name)
		if dl.ShowModal() == wx.ID_OK:
			new_name = '%s, %s' % (dl.GetValue().lstrip(' ').rstrip(' ').title(), part_right)
			encoded_new_name = new_name
			if _pyVersion <= 2:
				encoded_new_name = new_name.encode("mbcs")
				encoded_value = value.encode("mbcs")

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

				#update definitions and details
				if value in self.details_dic:
					dic_values = self.details_dic[value]
					del self.details_dic[value]
					self.details_dic.update({new_name: dic_values})
				elif encoded_value in self.details_dic:
					dic_values = self.details_dic[encoded_value]
					del self.details_dic[encoded_value]
					self.details_dic.update({new_name: dic_values})

				if value in self.define_dic:
					dic_values = self.define_dic[value]
					del self.define_dic[value]
					self.define_dic.update({new_name: dic_values})
				elif encoded_value in self.define_dic:
					dic_values = self.define_dic[encoded_value]
					del self.define_dic[encoded_value]
					self.define_dic.update({new_name: dic_values})

				Shared().Play_sound(True)

		dl.Destroy()
		Shared().Play_sound("subwindow", 1)
		self.cbx.SetFocus()


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
		if _pyVersion <= 2:
			try:
				s = s.decode("mbcs")
			except(UnicodeDecodeError, UnicodeEncodeError): pass

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
				#Search for Yahoo old zip codes
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
		else: name = '%s%s' % (part_left.title(), current)

		value = name[:-len(name.split()[-1])-1]
		for zc in self.zipCodesList:
			part = zc[:-len(zc.split()[-1])-1]
			if _pyVersion <= 2: part = part.decode("mbcs")
			if part == value:
				double = True
				break
		return double, name, value


	def Warning(self, cityName, name, v):
		"""Proposes an alternative name, but by offering the correct name"""

		winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		#Translators: dialog message used when the city name already exists
		dl =wx.MessageDialog(self, '%s "%s" %s.\n%s "%s" %s.\n%s\n%s "%s".\n%s' % (
		_("The city"), v, _("is correct"),
		_("But the name"),
		name,
		_("already exists"),
		_("You have to change it!"),
		_("The city proper is"),
		cityName[:cityName.rfind(' ')],
		_("Want to use the suggested name?")),
		#Translators: title dialog
		'%s %s' % (_addonSummary, _("Notice!")),
		wx.YES_NO |wx.CANCEL| wx.ICON_QUESTION)
		result = dl.ShowModal()
		dl.Destroy()
		return result


	def OnImport(self, evt):
		"""Import data from file Weather.zipcodes"""
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
		zipCodesList2, define_dic, details_dic = Shared().LoadZipCodes(file)
		if not zipCodesList2:
			wx.MessageBox(_("Empty file or not in cities format compatible!"), _addonSummary, wx.ICON_ERROR)
			return evt.GetEventObject().SetFocus()

		if self.zipCodesList:
			#Translators: dialog message and title that allows you to choose the import mode
			message = '%s\n%s\n%s' % (
			_("Do you want to replace your list with this?"),
			_("If you select yes, your list will be completely replaced."),
			_("If you select no, the new cities will be added to your list.")
			)
			#Translators: the title window
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
		_("File contents"), len(zipCodesList2),
		_("cities")),
				zip_list = zipCodesList2,
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
		tl = len(zipCodesList2)
		lis = len(item_selected)
		mis = item_selected[-1] # max value
		item_selected.reverse()
		#get city displayed in the combo box
		zc1 = ""; v = self.cbx.GetValue(); found = False
		if v: zc1 = v
		max = 100
		dl = wx.ProgressDialog(
		_("Importing cities in progress"),
		_plzw,
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
				i = zipCodesList2[c] #get city name from imported list
				t, zc, n = Shared().ZipCodeInList(i, self.zipCodesList)
				encoded_v = v; encoded_defaultZipCode = self.defaultZipCode
				if _pyVersion <= 2:
					encoded_v = v.encode("mbcs"); encoded_defaultZipCode = self.defaultZipCode.encode("mbcs")

				if zc1 == zc and i == encoded_v and i == encoded_defaultZipCode:
					#The city found in the list it's set to default
					found = True

				if not t:
					#update the cities list
					zipCodesList.append(i)
					#search for old zipcodes
					old_zc = zc.split()[-1]
					new_zd= 0 #it when it becomes 2 it has all the details and definition data
					old_zd= 0 #it when it becomes 2 it has all the details and definition data
					if old_zc in define_dic:
						#updates the old cities definitions
						old_zd += 1
						self.define_dic.update({old_zc: define_dic[old_zc]})

					elif zc in define_dic:
						#updates the cities definitions
						new_zd += 1
						self.define_dic.update({zc: define_dic[zc]})

					if old_zc in details_dic:
						#update the old cities details
						old_zd += 1
						self.details_dic.update({old_zc: details_dic[old_zc]})

					elif zc in details_dic:
						#update the cities details
						new_zd += 1
						self.details_dic.update({zc: details_dic[zc]})

					ti += 1
					if (new_zd or old_zd) <2: tr += 1

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
					except(UnicodeDecodeError, UnicodeEncodeError):
						self.defaultZipCode = self.tempZipCode = v

				self.OnText()
				self.ReTitle(self.defaultZipCode)

			else:
				self.cbx.SetValue(v); self.OnText()
				if encoded_v not in zipCodesList:
					self.cbx.SetValue("")
					if v == self.defaultZipCode: self.ReTitle(_("None"))

		wx.MessageBox(
		'%s: %d %s.\n%s: %d.\n%s: %d.\n%s: %d.\n%s: %d.' % (
		_("Were added"), ti, _("new cities to the list"),
		_("Have been ignored because existing"), td,
		_("Content of imported list"), tl,
		_("Containing incomplete data"), tr,
		_("selected by the user"), lis),
		'%s - %s' % (_addonSummary, _("Import finished")), wx.ICON_INFORMATION)
		evt.GetEventObject().SetFocus()


	def OnExport(self, evt):
		"""Export file Weather.zipcodes"""

		file = "Weather.zipcodes"
		if self.modifiedList:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			#Translators: dialog message used if the user has he added cities but hasn't saved them yet
			if wx.MessageBox('%s "%s" %s\n%s\n%s' % (
			_("A copy of"),
			file,
			_("It will be exported"),
			_("But it does not yet contain the changes you just made the list!"),
			_("I proceed?")),
			#Translators: the dialog title
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
		wx.CallAfter(ui.message, _plzw)
		if os.path.isfile(_zipCodes_path):
			import shutil 
			try:
				#copy the cities list to the destination chosen by the user
				shutil .copy(_zipCodes_path, destPath)
				winsound.MessageBeep(winsound.MB_ICONASTERISK)
			except Exception as e:
				Shared().LogError(e)
				return Shared().WriteError(_addonSummary)

			evt.GetEventObject().SetFocus()


	def OnHourlyforecastSet(self, evt):
		"""hourlyforecast report data settings"""
		dl = HourlyforecastDataSelect(self, title = _("Hourlyforecast data report values."), message = _("Disable the data you don't want to be processed:"),
		toWindspeed_hf = self.toWindspeed_hf,
		toWinddir_hf = self.toWinddir_hf,
		toWindgust_hf = self.toWindgust_hf,
		toCloud_hf = self.toCloud_hf,
		toHumidity_hf = self.toHumidity_hf,
		toVisibility_hf = self.toVisibility_hf,
		toPrecip_hf = self.toPrecip_hf,
		toUltraviolet_hf = self.toUltraviolet_hf)
		back = (self.toWindspeed_hf, self.toWinddir_hf, self.toWindgust_hf, self.toCloud_hf, self.toHumidity_hf, self.toVisibility_hf, self.toPrecip_hf, self.toUltraviolet_hf)
		Shared().Play_sound("subwindow", 1)
		try:
			if dl.ShowModal() == wx.ID_OK:
				ret = (self.toWindspeed_hf,
				self.toWinddir_hf,
				self.toWindgust_hf,
				self.toCloud_hf,
				self.toHumidity_hf,
				self.toVisibility_hf,
				self.toPrecip_hf,
				self.toUltraviolet_hf) = dl.GetValue()
				if ret != back: Shared().Play_sound(True)
		finally:
			Shared().Play_sound("subwindow", 1)
			dl.Destroy()


	def ComboSet(self, v, add = None):
		"""Update choices List ComboBox"""
		if _pyVersion <= 2:
			try:
				v = v.decode("mbcs")
			except(UnicodeDecodeError, UnicodeEncodeError): pass

		if add:
			i = self.GetIndex(v, self.zipCodesList)
			if i == None: i = 0
			self.cbx.Insert(v, i)

		self.cbx.SetStringSelection(v)
		if not v: self.cbx.SetValue('')
		self.modifiedList = True
		self.cbx.SetFocus()


class Shared:
	"""shared functions"""
	def JsonError(self):
		"""notify if the json datas hare incomplete"""
		self.Play_sound(False,1)
		return ui.message('%s %s' % (_("Sorry, the city set is not valid or contains incomplete data!"), _("It could be a temporary problem and you may wait a while '...")))


	def CloseDialog(self, dialog):
		try:
			if dialog:
				if dialog.IsShown(): dialog.Close()
				self.Play_sound("subwindow", 1)
		except Exception: pass


	def LogError(self, e):
		e = str(e)
		if _pyVersion <= 2: e = e.decode("mbcs")
		log.info('%s %s: %s' % (_addonSummary, _addonVersion, e))


	def ConvertDate(self, dd, m = True):
		"""Convert day and month into translated date string"""
		dt = '%s %s' % (
		self.TranslateCalendar(calendar.weekday(dd.year, dd.month, dd.day)),
		dd.day
		)
		if m:
			#day and month
			dt = '%s %s' % (dt, self.TranslateCalendar(str(dd.month).rjust(2,'0')))

		return dt


	def ViewDatas(self, message, title = _addonSummary):
		"""view weather report or details in a window"""
		if "_weatherReportDialog" not in globals(): global _weatherReportDialog; _weatherReportDialog = None
		Shared().CloseDialog(_weatherReportDialog)
		_weatherReportDialog = HelpEntryDialog(gui.mainFrame, title = title, message = message, verbose = True)
		def callback4(result):
			if result:
				try:
					_weatherReportDialog.Close()
					Shared().Play_sound("subwindow", 1)
				except: pass

		gui.runScriptModalDialog(_weatherReportDialog, callback4)


	def SetCityString(self, zipcode):
		""" titles city and upper country acronym"""
		try:
			zipcode = str(zipcode)
		except(UnicodeDecodeError, UnicodeEncodeError):
			try:
				zipcode = zipcode.decode("mbcs")
			except(UnicodeDecodeError, UnicodeEncodeError): pass

		return '%s%s' % (zipcode[:zipcode.find(',')].title(), zipcode[zipcode.find(','):].upper())


	def IsOldZipCode(self, zipcode):
		"""identifies incompatible zipcodes"""
		p = re.compile(r'(.+, [A-Za-z]{2,4}) [A-Za-z0-9]+[0-9]')
		try:
			m = re.search(p, zipcode).group(1)
		except AttributeError: return None
		return True


	def GetLocation(self, value, define_dic):
		"""get city location assigned to zipcode in use"""
		if isinstance(value, bytes): value = value.decode("mbcs")
		if _pyVersion <= 2: value = value.encode("mbcs")
		if value in define_dic: return define_dic[value]['location']
		return ''


	def GetDefine(self, zip_code, define_dic):
		"""load defined area assigned to city"""
		if not zip_code in define_dic: return None
		return define_dic[zip_code]["define"]


	def DbaseUpdate(self):
		"""online update of acronym database"""
		if "_acronym_dic" not in globals():
			global _acronym_dic; _acronym_dic = {}

		#load acronym database updates
		try:
			dbase = self.GetUrlData('%s/%s' % (_addonBaseUrl, "weather.dbase"), verbosity = False) #does not log the error if verbosity is False
			if isinstance(dbase, bytes) and _pyVersion >= 3: dbase = dbase.decode()
			dbase = dbase.split('\n')
			for i in dbase:
				_acronym_dic.update({i.split('\t')[0]: i.split('\t')[-1]})

		except: _acronym_dic = {}


	def FindForGeoName(self, real_city_name, city_name, latitude, longitude):
		"""Retrieve details from geo name with geographic coordinates"""
		def SplitName(c):
			#separates the city from the state
			return c.split(',')[0], c.split(',')[-1].lstrip(' ')

		def GetGeo(city, acronym):
			return Shared().GetGeoName(city, lat = latitude, lon = longitude, acronym=acronym)

		def ParseName(city, acronym):
			city_details = GetGeo(city, acronym)
			if not city_details:
				#try separating the name
				city = city.replace("-", " ")
				city = city.replace("_", " ")
				city_details = GetGeo(city, acronym)
				if not city_details:
					#try by splitting the name
					city1 = city.split(' ')
					for city in city1:
						city_details = GetGeo(city, acronym) 
						if city_details: break

					if not city_details:
						#try to join the name
						city = city.replace(" ", "-")
						city_details = GetGeo(city, acronym) 

			return city_details

		#try with the real city name 
		city, acronym = SplitName(real_city_name)
		city_details = ParseName(city, acronym)
		if not city_details and city_name != real_city_name:
			#try with the name given by the user
			city, acronym = SplitName(city_name)
			city_details = ParseName(city, acronym)

		if city_details: return '%s, %s' % (SplitName(real_city_name)[0], city_details)
		return ""


	def MakeRegionAcronym(self, value):
		"""make a region acronym"""
		if not value: return ""
		capital_Letters = []
		#collects initial capital letters
		capital_letters = [i for i in value if i.isupper()]
		l = len(capital_letters)
		#if there are two or more than 2, will be used the first and the second or the first and last of capital letters
		if l >= 2: acronym = '%s%s' % (capital_letters[0], capital_letters[-1])
		#if it is a single, will be used the first 2 characters
		elif l == 1: acronym = '%s%s' % (capital_letters[0], value[1])
		return acronym.upper()


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
		'AZERBAIGIAN': 'AZ',
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
		'BOSNIA-HERZEGOVINA': 'BA',
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
		'COOK ISLAND': 'CK',
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
		'FRENCH POLYNESIA ISLANDS': 'PF',
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
		'SPRATLY ISLANDS': 'XS',
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
		'PALESTINE': 'PS',
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
		'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS': 'GS',
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
		'UNITED STATES OF AMERICA': 'US',
		'USA': 'US',
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
		#addss online acronym database updates
		self.DbaseUpdate()
		if len(_acronym_dic):
			acronym_dic.update(_acronym_dic)

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


	def Add_zero(self, hour, p = True):
		""" add zero  to left of number with len 1"""
		if hour in ["No moonrise", "No moonset", "No sunrise", "No sunset", ""]: return hour
		if p:
			p = hour[-2:] #pm or am
			hour = hour[:-3] # hour and minute

		m = hour[hour.find(':')+1:] #minute
		t = '%s:%s' % (hour[:hour.find(':')].rjust(2, '0'), m.rjust(2, '0'))
		if p: return '%s %s' % (t, p)
		return t


	def To24h(self, hour, viceversa = None):
		"""Convert from 12 to 24 hours and viceversa"""
		if hour in ["No moonrise", "No moonset", "No sunrise", "No sunset", ""]: return hour
		if 'datetime' in str(type(hour)):
			#datetime format get from lastbuilddate returned in 24 hour format
			hour = '%s:%s' % (hour.hour, hour.minute)
		else:
			if hour.split(' ')[-1] in ('AM', 'PM'):
				m = hour[-2:] #pm or am
				hour = hour[:-3] #hour and minute without am|pm

		if viceversa:
			#only for lastbuilddate
			t = datetime.strptime(hour, '%H:%M')
			t1 =t.strftime('%H:%M') #get time in 24 hour format
			t2 =t.strftime('%I:%M') #get time in 12 hour format
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
				t = self.Add_zero('%s:%s' % (int(h)+12 if int(h) < 12 else 12, m), None)

		return t


	def GetTimezone(self, timezone_id,to24Hours):
		"""reads city local time and date"""
		date = datetime.now(dateutil.tz.gettz(timezone_id)).date()
		date = Shared().ConvertDate(date)
		hour = datetime.now(dateutil.tz.gettz(timezone_id)).time()
		hour = hour.strftime('%H:%M')
		if not to24Hours: hour = Shared().To24h(hour, viceversa=True)
		return hour, date


	def APILanguage(self):
		"""weather conditions language"""
		lang = [
		'Arabic, ar',
		'Bengali, bn',
		'Bulgarian, bg',
		'Chinese Simplified, zh',
		'Chinese Traditional, zh_tw',
		'Czech, cs',
		'Danish, da',
		'Dutch, nl',
		'English, en',
		'Finnish, fi',
		'French, fr',
		'German, de',
		'Greek, el',
		'Hindi, hi',
		'Hungarian, hu',
		'Italian, it',
		'Japanese, ja',
		'Javanese, jv',
		'Korean, ko',
		'Mandarin, zh_cmn',
		'Marathi, mr',
		'Polish, pl',
		'Portuguese, pt',
		'Punjabi, pa',
		'Romanian, ro',
		'Russian, ru',
		'Serbian, sr',
		'Sinhalese, si',
		'Slovak, sk',
		'Spanish, es',
		'Swedish, sv',
		'Tamil, ta',
		'Telugu, te',
		'Turkish, tr',
		'Ukrainian, uk',
		'Urdu, ur',
		'Vietnamese, vi',
		'Wu (Shanghainese), zh_wuu',
		'Xiang, zh_hsn',
		'Yue (Cantonese), zh_yue',
		'Zulu, zu'
		]
		return lang


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
			return datetime.fromtimestamp(dom['current']['last_updated_epoch'])
		except Exception: return None


	def Weather_PlusDat(self):
		apikey_path = _addonDir.replace('..\..', "") + "wp.dat"
		import pickle
		try:
			with open(apikey_path, 'rb') as r:
				data = pickle.load(r)
				return data['wpd']
		except: return ''


	def ParseEntry(self, value, apilang, dom = None):
		"""parse type city name"""
		api_query = ""
		if value.isdigit(): api_query = '%s' % value
		elif Shared().GetCoords(value):
			 value = value.split(',')
			 api_query = '%s, %s' % (value[0], value[-1].lstrip(' '))
		else:
			if _pyVersion <= 2:
				api_query = '%s' % value.encode("mbcs")
			else:
				api_query = '%s' % value

		dom = self.WeatherConnect(api_query, apilang)
		if dom == "no connect": return dom, None
		elif not dom: return "", None
		try:
			city = dom['location']['name']
			region = region2 = dom['location']['region'].lstrip(' ')
			country = dom['location']['country']
			timezone_id = dom['location']['tz_id']
			lat = dom['location']['lat']
			lon = dom['location']['lon']
		except KeyError: return "", None
		city_test = '%s, %s' % (city, country)
		country_acronym = self.FindForGeoName(city_test, city_test, lat, lon)[-2:]
		if country and not country_acronym:
			country_acronym = Shared().GetAcronym(country)
		if country and not country_acronym:
			#Translators: diaalog message that asks the user to report to author the city code whose country could not be determined
			dl = HelpEntryDialog(gui.mainFrame,
			#Translators: the message in the window
			message ='%s' % (
			_("""It was not possible find the acronym of "%s"!""") % country+'\n'+
			_("This may not allow you to get the city details.")+'\n'+
			_("Please report this to the author so he can add this country in database.")+'\n'+
			_("Send an email to %s") % _addonAuthor+'\n'+
			_("With  object the line below, thanks.")),
			#Translators: the dialog title
			title = '%s %s' % (_addonSummary, _("Notice!")),
			clip = '%s %s' % (_addonSummary, 'Search key = %s - Country = %s' % (api_query, country)), verbose=False)
			if dl.ShowModal(): dl.Destroy()

		region_acronym = Shared().MakeRegionAcronym(region) or city[:2]
		acronym = '%s%s' % (country_acronym or "--", region_acronym)
		cityName = '%s, %s' % (city, acronym)
		cityName = Shared().SetCityString(cityName)
		ramfields_dic = {}
		[ramfields_dic .update({f: ''}) for f in _fields]
		for n, f in enumerate(_fields):
			ramfields_dic[f] = [city, region2, country, country_acronym[:2], timezone_id, lat, lon][n]

		global ramdetails_dic
		ramdetails_dic = {cityName: ramfields_dic}
		return city, acronym


	def WeatherConnect(self, api_query, apilang):
		"""return Weather API values"""
		base_url = "http://api.weatherapi.com/v1/forecast.json"
		keywords ={
		"key":_wbdat,
		"q": api_query,
		"lang": apilang[-2:],
		"days": _maxDaysApi
		}
		weather_url = base_url + "?" + urlencode(keywords, "mbcs")
		data = self.GetUrlData(weather_url)
		if not data or data in ["no connect", "no key"]: return data
		return json.loads(data)


	def Download_file(self, url, target, title, message):
		"""Download files using the progress bar"""
		if "_addonBaseUrl" not in globals(): return "Error"
		max = 100
		if "_downloadDialog" not in globals(): global _downloadDialog
		_downloadDialog = wx.GenericProgressDialog(title,
		message,
		maximum = max,
		style = 0
		| wx.PD_CAN_ABORT
		| wx.PD_APP_MODAL
		| wx.PD_ELAPSED_TIME
		| wx.PD_ESTIMATED_TIME
		)
		_downloadDialog.Update(0, message)
		try:
			fURL = urlopen(url, timeout=6)
			header = fURL.info()
			size = None
			outFile = open(target, 'wb')
			keepGoing = True
			if "Content-Length" in header:
				size = int(header["Content-Length"])
				kBytes = size/1024
				downloadBytes = int(size/max)
				count = 0
				while keepGoing:
					count += 1
					if count >= max: count = 99
					wx.MilliSleep(250)
					wx.Yield()
					(keepGoing, skip) = _downloadDialog.Update(count,
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
					(keepGoing, skip) = _downloadDialog.UpdatePulse()
					b = fURL.read(1024*8)
					if b:
						outFile.write(b)
					else:
						break
			outFile.close()
			fURL.close()
			_downloadDialog.Update(99, '%s %s %s' % (
			_("Downloaded"), str(os.path.getsize(target)/1024), "KB"))
			_downloadDialog.Hide(); _downloadDialog.Destroy()
			return keepGoing
		except Exception as e:
			try:
				outFile.close()
				fURL.close()
			except: pass
			e = str(e)
			if not "failed" in e and not "Not Found" in e and not "unknown url type" in e:
				Shared().WriteError(title)

			_downloadDialog.Hide(); _downloadDialog.Destroy()
			Shared().LogError(e)
			return "Error"


	def Find_wbdats(self):
		"""hotkeys string that is added in the lookback windows"""
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


	def LoadZipCodes(self, i = None):
		"""Load cities, city definitions and city details"""
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
					if r != '' and not r.startswith('['):
						r = r.rstrip('\r\n')
						zc = r.split('\t')
						if len(zc) in [2, 3]:
							if zc[0].startswith('#'):
								#location and define data
								define_fields = {"location": zc[1], "define": zc[-1].rstrip('\r\n')}
								define_dic.update({zc[0][1:]: define_fields})
							else: zipCodesList.append('%s %s' % (Shared().SetCityString(zc[0]), zc[-1].rstrip('\r\n')))

						elif len(zc) == 8:
							#city details
							fields_dic = {}
							n = 1
							[fields_dic.update({i: ''}) for i in _fields]
							for f in _fields:
								#load fields data
								fields_dic.update({f: zc[n]}); n += 1

							details_dic.update({zc[0]: fields_dic}) #load record (city + fields)

		return sorted(list(set(zipCodesList))), define_dic, details_dic


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
		"""translate the Italian regions"""
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
		data = Shared().GetUrlData(address, verbosity = False) #does not log the error if it verbosity is False 
		if not data: return None
		if isinstance(data, bytes) and _pyVersion >= 3: data = data.decode()
		elif _pyVersion <= 2: data = data.decode("utf-8")
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
		return line


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
		"totest": "ToTest",
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
			if _pyVersion <= 2:
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
		"""Check if the city already exists on cities list"""
		i, t = 0, False
		zc = v
		for i, n in enumerate(zipCodesList):
			if _pyVersion <= 2:
				try:
					zc1 = n.decode("mbcs")
				except(UnicodeDecodeError, UnicodeEncodeError): zc1 = n
			else: zc1 = n
			if zc.upper() == zc1.upper():
				t = True; break

		return t, zc, i


	def GetUrlData(self, address, verbosity = True):
		"""Gets the contents of a web page"""
		error = data = ""
		try:
			with closing(urlopen(address)) as response:
				data = response.read()
		except Exception as e:
			error = e
			if "CERTIFICATE_VERIFY_FAILED" in repr(e):
				#retry using ssl
				data = "no connect"
				gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
				try:
					with closing(urlopen(address, context=gcontext)) as response:
						data = response.read()
				except Exception as e:
					error = e
					data = "no connect"
					if verbosity: Shared().LogError(error)

			elif "failed" in repr(error):
				data = "no connect"
				if verbosity: Shared().LogError(error)

		if "Not Found" in repr(error): data = "not found"
		return data


	def Find_cities(self, value):
		"""get cities recurrences engine"""
		city = value
		country = ""
		if ',' in value:
			city = value[:value.find(',')]
			country = value[value.find(',')+1:].lstrip(' ')

		cities_found = []
		addresses = [
		'http://www.geonames.org/postalcode-search.html?q=%s&country=%s' % (city, country),
		'http://www.geonames.org/search.html?q=%s&country=%s' % (city, country)]
		p=[
		re.compile(r'</small></td><td>(.+)</td><td>(.+)</td><td>(.+)</td><td>(.+)</td><td>(.+)</td>.+<small>(-*\d+\.\d+)/(-*\d+\.\d+)</small>'), #geonames with posttal codes
		re.compile(r'latitude">(-*\d+\.\d+)</span><span class="longitude">(-*\d+\.\d+)</span></span></td><td><a href="/countries/([A-Z][A-Z])/(.+)\.html">(.+)</a>, (.+)<br><small>(.+); (.+)</small>')] #geonames without postal codes
		for c in [0, -1]:
			data = self.GetUrlData(addresses[c])
			if isinstance(data, bytes) or _pyVersion == 2: data = data.decode("utf-8")
			if not data or "noresult" in data:
				if c == 0: continue
				elif c == -1: return
			for i in data.split('\n'):
				try:
					m = re.search(p[c], i).group()
					if m:
						if c == 0:
							city1 = '%s, %s, %s, %s, %s, %s, %s' % (
							re.search(p[c], m).group(1), #city name
							re.search(p[c], m).group(2), #postal code
							Shared().TranslatePlaces(re.search(p[c], m).group(3)), #region
							re.search(p[c], m).group(4), #country
							re.search(p[c], m).group(5), #province
							(math.ceil(float(re.search(p[c], m).group(6))*100)/100), #latitude
							(math.ceil(float(re.search(p[c], m).group(7))*100)/100) #longitude
							)
							city1 = city1.replace('</td><td>', ', ').replace('<tr><td>', '').replace('<tr class="odd"><td>, ', ', ').replace(', , ', ', ')
							name = '%s, %s' % (city1.split(', ')[0], city1.split(', ')[3])
						else:
							city1 = '%s, %s, %s, %s, %s, %s, %s' % (
							re.search(p[c], m).group(8).title(), #city name
							_npc,
							Shared().TranslatePlaces(re.search(p[c], m).group(6)), #region
							re.search(p[c], m).group(5), #country
							re.search(p[c], m).group(7).rstrip(' & gt'), #province
							(math.ceil(float(re.search(p[c], m).group(1))*100)/100), #latitude
							(math.ceil(float(re.search(p[c], m).group(2))*100)/100) #longitude
							)
							name = '%s, %s, %s' % (city1.split(', ')[0], city1.split(', ')[1], city1.split(', ')[2])
				except (AttributeError, ValueError): city1 = None
				#collects city datas
				if city1:
					#takes coordinates of the city found
					coords = '%s, %s' % (city1.split(', ')[-2], city1.split(', ')[-1])
					#checks if they are present in the list
					coordsInList = [True for x in cities_found if coords in x]
					nameInList = [True for x in cities_found if name in x]
					if not nameInList and not coordsInList: cities_found.append(city1)

		return sorted(list(set(cities_found)))


	def Search_cities(self, cityName):
		"""Search for city occurrences with geonames"""
		command = cityName[:cityName.find(':')+1].upper()
		city = cityName[cityName.find(':')+1:]
		if not command and (city.replace('.', '').isdigit() or self.GetCoords(cityName)): return cityName
		elif command == 'D:': return city #passes search key directly to API
		elif command == 'P:': mode = 1 #search for postal code
		elif command == 'G:': mode = 2 #search for geographical coordinates
		elif command == 'T:': mode = 3 #search for path string
		else: mode = 1 #default

		def GetValue(v, mode):
			m = m1 = m2 = ""
			try:
				country = v.split(', ')[2]
			except IndexError: mode, country = 2, ''
			try:
				#get postal code from city
				if mode is 1:
					valid_countries = ['United States', 'Canada', 'United Kingdom']
					m = v.split(', ')[1] #get postal code
					country_wpc = v.split(', ')[2] #get country
					if m == _npc\
					or country_wpc not in valid_countries: mode = 3
				if mode is 1:
					m = v.split(', ')[1]
				elif mode == 2:
					#get geographical coordinates from city
					p = re.compile(r'.+, (-*\d+\.\d+), (-*\d+\.\d+)')
					try:
						m = re.search(p, v).group(1)
						m1 = re.search(p, v).group(2)
					except AttributeError: m = m1 = None

				else:
					#get path string
					m = v.split(', ')[0]
					m1 = v.split(', ')[2]
					m2 = v.split(', ')[3]
			except IndexError: m = m1 = m2 = None
			if m is not None and mode == 1:
				if country in valid_countries: return m
				return '%s,%s' % (m, self.GetAcronym(country))

			elif (m is not None and m1 is not None) and mode is 2:
				return '%s, %s' % ((math.ceil(float(m)*100)/100), (math.ceil(float(m1)*100)/100))
			elif (m is not None and m1 is not None and m2 is not None) and mode == 3:
				text = '%s, %s, %s' % (m, m1, m2)
				text = text.lstrip(',').rstrip(' ').replace(', ,', '')
				return text

			return v

		recurrences_list = self.Find_cities(city)
		if not recurrences_list: return city #passes the search key to API
		lrl = len(recurrences_list)
		if lrl is 0: return city #passes the search key to API
		elif lrl == 1: return GetValue(recurrences_list[0], mode)
		else:
		#Translators: window that allows you to choose a city among the found occurrences
			title = '%s - %d %s %s %s.' % \
			(#Translators: the window title
			_addonSummary, lrl, _("occurrences found"), _("for"), city)
			message = '%s.\n%s\n%s:' % (
			#Translators: message dialog
			_("Choose a city."),
			Shared().Find_wbdats(), #get hotkeys
			_("List of availables Cities"))
			if "_searchDialog" not in globals(): global _searchDialog
			_searchDialog = SelectDialog(gui.mainFrame, title = title, message = message, choices = recurrences_list, last = [0], sel = 0)
			Shared().Play_sound("subwindow", 1)
			if _searchDialog.ShowModal() == wx.ID_CANCEL:
				_searchDialog.Destroy()
				Shared().Play_sound("subwindow", 1)
				return ""
			else:
				select = _searchDialog.GetValue()
				_searchDialog.Destroy()
				Shared().Play_sound("subwindow", 1)
				return GetValue(recurrences_list[select], mode)


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
			except(UnicodeDecodeError, UnicodeEncodeError):
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
		return self.chb.GetSelection()


	def OnKey(self, evt):
		"""Control hot keys pressed into SelectDialog"""
		ctrl = evt.ControlDown()
		shift = evt.ShiftDown()
		key = evt.GetKeyCode()
		defaultString = self.defaultString
		if key == wx.WXK_F3 and ctrl:
			#Enter text to search
			if "_itemStatus" not in globals():
				global _itemStatus
				_itemStatus = {}

			if "_undo" not in globals():
				global _undo
				_undo = []

			if "_defaultStrings" not in globals():
				global _defaultStrings
				_defaultStrings = []
				#load search keys saved
				sel = 0
				if os.path.isfile(_searchKey_path):
					with open(_searchKey_path, 'r') as r:
						for i in r:
							if _pyVersion <= 2: i = i.decode("mbcs")
							if i.startswith('\t'): sel = int(i.lstrip('\t')); continue
							_defaultStrings.append(i.rstrip('\n'))

			if "_selected" not in globals():
				global _selected
				_selected = sel

			if "_findDialog" not in globals(): global _findDialog
			_findDialog = FindDialog(self, message = _("Type the search string"), title = _("Find"))
			if _findDialog.ShowModal() == wx.ID_OK:
				self.defaultString = defaultString = _findDialog.GetValue()
				if defaultString and defaultString not in _defaultStrings: _defaultStrings.append(defaultString); _defaultStrings.sort()
				if defaultString: _selected = _defaultStrings.index(defaultString)
				else:
					if _notifyDialog: _notifyDialog.Destroy()
					_findDialog.Destroy()
					return
				self.FindText(self.choices, defaultString, direction = 0)

			_findDialog.Destroy()

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
				except(UnicodeDecodeError, UnicodeEncodeError): t = strings[line].lower()

			if t.find(text.lower()) != -1:
				self.chb.SetSelection(line)
				wx.CallLater(100, ui.message, self.chb.GetStringSelection())
				find = True; break
		if not find:
			ds= ["", _("next"), _("previous")]
			if d == 0:
				if "_notifyDialog" not in globals(): global _notifyDialog
				_notifyDialog = wx.MessageDialog(gui.mainFrame, '"%s" %s' % (text, _("not found!")), _("Find"), wx.OK|wx.ICON_EXCLAMATION)
				if _notifyDialog.ShowModal(): _notifyDialog.Destroy()

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
			if _pyVersion <= 2: s = strings.index(t.encode("mbcs")) +direction

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
		if _pyVersion <= 2: zip_list = [i.decode("mbcs") for i in zip_list]
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
		self.btn_ok=self.FindWindowById(wx.ID_OK)
		btns = self.FindWindowById(wx.ID_APPLY)
		btns.SetLabel(_("&Select all"))
		btnd = self.FindWindowById(wx.ID_HELP)
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
			message = _plzw
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
			Shared().FreeHandle()
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
		text = wx.TextCtrl(self, -1, value = message.rstrip('\r\n'), pos = wx.DefaultPosition, size=(800,400), style = wx.TE_MULTILINE|wx.TE_READONLY)
		vbox.Add(text, 1, wx.EXPAND|wx.ALL, 5)
		text.Bind(wx.EVT_CHAR, self.OnChar)
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
		#gets the text ending
		text.SetInsertionPointEnd()
		self.bottomText =  text.GetInsertionPoint()
		#set again the cursor to top
		text.SetInsertionPoint(0)
		text.SetFocus()
		self.text = text
		if verbose: Shared().Play_sound("subwindow", 1)


	def OnCopytoclip(self, evt):
		"""copy textctrl value to clipboard"""
		api.copyToClip(self.clip)
		evt.Skip()


	def OnChar(self, evt):
		"""check if the user have pressed enter key, ctrl-a, ctrl-c"""
		key = evt.GetKeyCode()
		if key == wx.WXK_RETURN:
			self.EndModal(wx.ID_OK)
		elif key == wx.WXK_UP\
		or key == wx.WXK_DOWN\
		or key == wx.WXK_LEFT\
		or key == wx.WXK_RIGHT\
		or key == wx.WXK_HOME\
		or key == wx.WXK_END:
			evt.Skip()
		elif key == wx.WXK_PAGEUP:
			if self.text.GetInsertionPoint() != 0: self.text.SetInsertionPoint(0)
			else: wx.Bell()
		elif key == wx.WXK_PAGEDOWN:
			if self.text.GetInsertionPoint() != self.bottomText: self.text.SetInsertionPoint(self.bottomText)
			else: wx.Bell()
		elif key == wx.WXK_CONTROL_A:
			#select all content
			self.text.SetSelection(-1, -1)
		elif key == wx.WXK_CONTROL_C:
			#copy the selection
			text = self.FindFocus()
			if text is not None: text.Copy()


class FindDialog(wx.Dialog):
	def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
	title = '', message = ''):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style)
		sizer = wx.BoxSizer(wx.VERTICAL)
		if message:
			sizer.Add(wx.StaticText(self, -1, message), 0, wx.ALL, 10)

		boxSizerH1 = wx.BoxSizer(wx.HORIZONTAL)
		textEntry = wx.TextCtrl(self)
		try:
			textEntry.SetValue(_defaultStrings[_selected])
		except IndexError: pass
		sizer.Add(textEntry, 1, wx.EXPAND|wx.ALL, 5)
		boxSizerH1.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.CENTRE| wx.ALL|wx.EXPAND, 5)
		btn_ok = self.FindWindowById(wx.ID_OK)
		btn_canc = self.FindWindowById(wx.ID_CANCEL)
		if not _defaultStrings or not textEntry.GetValue():
			btn_ok.Enable(False)
		sizer.Add(boxSizerH1)
		textEntry.Bind(wx.EVT_CHAR, self.OnKey)
		textEntry.Bind(wx.EVT_RIGHT_DOWN, self.OnContext)
		btn_ok.Bind(wx.EVT_CHAR, self.OnKey)
		btn_canc.Bind(wx.EVT_CHAR, self.OnKey)
		self.defaultStrings = _defaultStrings
		self.selected = _selected
		self.textEntry = textEntry
		self.btn_ok = btn_ok
		self.SetSizerAndFit(sizer)
		self.Center(wx.BOTH|wx.Center)
		textEntry.SetFocus()


	def OnKey(self, evt):
		"""Control f2, up and down Arrows and ctrl+z, ctrl+x, ctrl+c, ctrl+v and popup menu into FindDialog.textctrl"""
		key = evt.GetKeyCode()
		obj = evt.GetEventObject()
		tegv = self.textEntry
		tes = tegv.GetValue()
		if key == wx.WXK_DOWN and obj == tegv:
			#select the next string
			if tes and len(tes) == 1:
				for i in self.defaultStrings:
					if tes.upper() in i[0].upper(): self.selected = self.defaultStrings.index(i); break
			elif self.selected < len(self.defaultStrings) -1:
				self.selected += 1

			try:
				tegv.SetValue(self.defaultStrings[self.selected])
			except (TypeError, IndexError): pass
			return tegv.SetSelection(0, -1)
		elif key == wx.WXK_UP and obj == tegv:
			#choose the previous string
			if tes and len(tes) == 1:
				for i in self.defaultStrings:
					if tes.upper() in i[0].upper(): self.selected = self.defaultStrings.index(i); break
			elif self.selected > 0:
				self.selected -= 1
				if self.selected < 0: self.selected = 0

			try:
				tegv.SetValue(self.defaultStrings[self.selected])
			except (TypeError, IndexError): pass
			return tegv.SetSelection(0, -1)
		elif key == wx.WXK_PAGEDOWN and obj == tegv:
			#page down
			page = int((len(self.defaultStrings) + 10 - 1) / 10)
			self.selected += page
			if self.selected >= len(self.defaultStrings): self.selected = len(self.defaultStrings) -1
			try:
				tegv.SetValue(self.defaultStrings[self.selected])
			except (TypeError, IndexError): pass
			tegv.SetSelection(0, -1)
		elif key == wx.WXK_PAGEUP and tegv == obj:
			#page up
			page = int((len(self.defaultStrings) + 10 - 1) / 10)
			self.selected-= page
			if self.selected < 0: self.selected = 0
			try:
				tegv.SetValue(self.defaultStrings[self.selected])
			except (TypeError, IndexError): pass
			tegv.SetSelection(0, -1)
		elif obj == tegv:
			if key == wx.WXK_DELETE and tegv.CanCut():
				#delete search key
				return self.OnDelete()
			elif key == wx.WXK_CONTROL_Z:
				#undo
				return self.OnUndo()
			elif key == wx.WXK_CONTROL_X and tegv.CanCut():
				#cut
				return self.OnCut()
			elif key == wx.WXK_CONTROL_V and tegv.CanPaste:
				#paste
				return self.OnPaste()
		elif key == wx.WXK_F2:
			#sett focus in edit field
			tegv.SetFocus()
			try:
				tegv.SetSelection(-1, -1)
			except AttributeError: pass

		if tegv.GetValue() != '' and not self.btn_ok.IsEnabled(): self.btn_ok.Enable(True)
		if tegv.GetValue() == '' and self.btn_ok.IsEnabled(): self.btn_ok.Enable(False)
		evt.Skip()


	def OnContext(self, evt):
		"""Create and display a context menu in FindDialog.textctrl"""
		self.Bind(wx.EVT_MENU, self.OnUndo, id = wx.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.OnCut, id = wx.ID_CUT)
		self.Bind(wx.EVT_MENU, self.OnCopy, id = wx.ID_COPY)
		self.Bind(wx.EVT_MENU, self.OnPaste, id = wx.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.OnSelectAll, id = wx.ID_SELECTALL)
		self.Bind(wx.EVT_MENU, self.OnDelete, id = wx.ID_DELETE)
		self.Bind(wx.EVT_MENU, self.OnSave, id = wx.ID_SAVE)
		#Create the popup menu
		menu = wx.Menu()
		selected = [
		self.textEntry.GetSelection()[0],
		self.textEntry.GetSelection()[-1]
		]
		lenValue = len(self.textEntry.GetValue())
		if selected[0] == selected[-1]:
			#unselected
			_itemStatus['cut'] = False
			_itemStatus['copy'] = False
			_itemStatus['paste'] = self.TestClipboard()
			_itemStatus['selectall'] = True
		elif selected[0] == 0 and selected[-1] == lenValue:
			#all selected
			_itemStatus['cut'] = True
			_itemStatus['copy'] = True
			_itemStatus['paste'] = self.TestClipboard()
			_itemStatus['selectall'] = False
		elif (selected[0] != selected[-1]) and (selected[0] >= 0 and selected[-1] != lenValue):
			#partial selected
			_itemStatus['cut'] = True
			_itemStatus['copy'] = True
			_itemStatus['paste'] = bool(api.getClipData())
			_itemStatus['selectall'] = True

		_itemStatus['undo'] = bool(_undo)
		_itemStatus['save'] = bool(_defaultStrings and self.textEntry.GetValue() in _defaultStrings)
		if not self.textEntry.GetValue(): _itemStatus['selectall'] = False
		_itemStatus['delete'] = bool(self.textEntry.GetValue() and self.textEntry.GetStringSelection())

		#append pop menus
		itemUndo = menu.Append(wx.ID_UNDO, ).Enable(_itemStatus['undo'])
		itemCut = menu.Append(wx.ID_CUT, ).Enable(_itemStatus['cut'])
		itemCopy = menu.Append(wx.ID_COPY, ).Enable(_itemStatus['copy'])
		itemPaste = menu.Append(wx.ID_PASTE, ).Enable(_itemStatus['paste'])
		itemSelectAll = menu.Append(wx.ID_SELECTALL, ).Enable(_itemStatus['selectall'])
		itemDelete = menu.Append(wx.ID_DELETE, ).Enable(_itemStatus['delete'])
		menu.AppendSeparator()
		itemSave = menu.Append(wx.ID_SAVE, ).Enable(_itemStatus['save'])
		#Displays the pop-up menu
		self.PopupMenu(menu)
		menu.Destroy()


	def TestClipboard(self):
		"""test if a valid clipboard value"""
		try:
			api.getClipData()
		except: return False
		return True


	def OnCopy(self, evt):
		"""copy popup menu item"""
		api.copyToClip(self.textEntry.GetValue()[self.textEntry.GetSelection()[0]:self.textEntry.GetSelection()[-1]])
		evt.Skip()


	def OnSelectAll(self, evt):
		"""select all popup menu item"""
		self.textEntry.SetSelection(-1, -1)
		evt.Skip()


	def OnDelete(self, evt = None):
		"""delete popup menu item"""
		tegv = self.textEntry
		v = tegv.GetValue()
		self.ListPreserve(v)
		index = None
		if not self.defaultStrings or v not in self.defaultStrings:
			tegv.SetValue('')
			self.btn_ok.Enable(False)
		elif self.defaultStrings:
			try:
				index = self.defaultStrings.index(v)
				del self.defaultStrings[index]
			except ValueError: pass
			try:
				if index is not None: tegv.SetValue(self.defaultStrings[index -1])
			except IndexError:
				tegv.SetValue('') 	

			if index is not None: self.selected = index

		tegv.SetFocus()
		if not self.defaultStrings or not v:
			tegv.SetValue('')
			self.btn_ok.Enable(False)
		if v: self.textEntry.SetSelection(-1, -1)


	def OnUndo(self, evt=None):
		"""undo popup menu item"""
		if not _undo: return
		tegv = self.textEntry
		#removes double keys
		undo2 = list(set(_undo))
		[_undo.pop() for i in range(len(_undo))]
		[_undo.append(i) for i in undo2]
		#recovers the last key
		lastUndo = _undo.pop()
		index = self.ListResume(lastUndo)
		if index: tegv.SetValue(self.defaultStrings[index])
		else: tegv.SetValue(lastUndo.lstrip('\t'))
		#select all and set focus
		tegv.SetSelection(0, -1)
		tegv.SetFocus()


	def OnCut(self, evt = None):
		"""cut popup menu item"""
		tegv = self.textEntry
		v = tegv.GetValue()
		selected = tegv.GetStringSelection()
		tegv.SetValue(v.replace(selected, ''))
		api.copyToClip(selected)
		if selected in self.defaultStrings:
			index = self.defaultStrings.index(selected)
			if index < len(self.defaultStrings)-1:
				tegv.SetValue(self.defaultStrings[index + 1])
			elif index > 0: tegv.SetValue(self.defaultStrings[index - 1])
			tegv.SetSelection(0, -1)
			self.ListPreserve(selected)
			self.defaultStrings.remove(selected)
		else: self.ListPreserve(v, False)


	def OnPaste(self, evt=None):
		"""paste popup menu item"""
		tegv = self.textEntry
		selected = tegv.GetStringSelection()
		v = tegv.GetValue()
		pos = tegv.GetInsertionPoint()
		try:
			clipData = api.getClipData()
		except: clipData = None
		if clipData:
			if selected:
				#replace the selected text
				tegv.SetValue(v.replace(selected, clipData))
			else:
				#insert text from insertion point
				start = v[:pos]
				end = v[pos:]
				tegv.SetValue(start+clipData+end)

			self.ListPreserve(v, False)
			self.btn_ok.Enable(True)


	def OnSave(self, evt):
		"""save popup menu item"""
		e = None
		self.defaultStrings.append('\t%s' % self.defaultStrings.index(self.textEntry.GetValue()))
		with open(_searchKey_path, 'w') as w:
			for i in self.defaultStrings:
				if _pyVersion >= 3: i += "\n"
				else: i =i.encode("mbcs") + "\n"
				try:
					w.write(i)
				except Exception as e:
					Shared().LogError(e)

		if not e: Shared().Play_sound("save")
		self.defaultStrings.pop() #remove key index from list
		[_undo.pop() for i in range(len(_undo))] #empty the canceled list


	def ListPreserve(self, v, tolist=True):
		"""adds a pointer to the deleted key"""
		if tolist and v in self.defaultStrings and (v not in _undo or '\t' + v not in _undo):
			#in list
			_undo.append('\t' + v)
		elif v not in _undo and ('\t' + v not in _undo):
			#not in list
			_undo.append(v)


	def ListResume(self, lastUndo):
		"""restore the search key of the list"""
		if lastUndo.startswith('\t'):
			#was in the list
			self.defaultStrings.append(lastUndo.lstrip('\t'))
			self.defaultStrings.sort()
			try:
				return self.defaultStrings.index(lastUndo.lstrip('\t'))
			except indexError: return None


	def GetValue(self):
		return self.textEntry.GetValue()


class HourlyforecastDataSelect(wx.Dialog):
	"""dialog to select hourlyforecast report data"""
	def __init__(self, parent, id=-1, title='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
		message = '',
		toWinddir_hf = None, toWindspeed_hf = None, toWindgust_hf = None, toHumidity_hf = None, toVisibility_hf = None, toCloud_hf = None, toPrecip_hf = None, toUltraviolet_hf = None):
		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style)
		sizer = wx.BoxSizer(wx.VERTICAL)
		if message:
			sizer.Add(wx.StaticText(self, -1, message), 0, wx.ALL, 10)
			sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toWindspeed_hf = wx.CheckBox(self, -1, _("Add wi&nd speed"))
		self.cbt_toWindspeed_hf.SetValue(bool(toWindspeed_hf))
		sizer.Add(self.cbt_toWindspeed_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toWinddir_hf = wx.CheckBox(self, -1, _("Add wind directi&on"))
		self.cbt_toWinddir_hf.SetValue(bool(toWinddir_hf))
		sizer.Add(self.cbt_toWinddir_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toWindgust_hf = wx.CheckBox(self, -1, _("Add wind &gust speed"))
		self.cbt_toWindgust_hf.SetValue(bool(toWindgust_hf))
		sizer.Add(self.cbt_toWindgust_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toCloud_hf = wx.CheckBox(self, -1, _("Add cloudiness &value"))
		self.cbt_toCloud_hf.SetValue(bool(toCloud_hf))
		sizer.Add(self.cbt_toCloud_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toHumidity_hf = wx.CheckBox(self, -1, _("Add humidity va&lue"))
		self.cbt_toHumidity_hf.SetValue(bool(toHumidity_hf))
		sizer.Add(self.cbt_toHumidity_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toVisibility_hf = wx.CheckBox(self, -1, _("Add &visibility value"))
		self.cbt_toVisibility_hf.SetValue(bool(toVisibility_hf))
		sizer.Add(self.cbt_toVisibility_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toPrecip_hf = wx.CheckBox(self, -1, _("Add precipitation &value"))
		self.cbt_toPrecip_hf.SetValue(bool(toPrecip_hf))
		sizer.Add(self.cbt_toPrecip_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.cbt_toUltraviolet_hf = wx.CheckBox(self, -1, _("Add &ultraviolet radiation value"))
		self.cbt_toUltraviolet_hf.SetValue(bool(toUltraviolet_hf))
		sizer.Add(self.cbt_toUltraviolet_hf, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.CENTRE| wx.ALL, 5)
		sizer.Add(hbox, 1, wx.ALIGN_CENTER_HORIZONTAL)
		self.SetSizerAndFit(sizer)
		self.cbt_toWindspeed_hf.SetFocus()
		self.Center(wx.BOTH|wx.Center)


	def GetValue(self):
		"""HourlyforecastDataSelect return values"""
		return (
		self.cbt_toWindspeed_hf.GetValue(),
				self.cbt_toWinddir_hf.GetValue(),
		self.cbt_toWindgust_hf.GetValue(),
		self.cbt_toCloud_hf.GetValue(),
		self.cbt_toHumidity_hf.GetValue(),
		self.cbt_toVisibility_hf.GetValue(),
		self.cbt_toPrecip_hf.GetValue(),
		self.cbt_toUltraviolet_hf.GetValue())