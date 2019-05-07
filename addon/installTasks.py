#-*- coding:utf-8 -*-
#Weather Plus Addon for NVDA
#Weather API = Yahoo
#Weather and 24 hour forecast
#More forecast up to 9 days
#Author: Adriano Barbieri
#Email: adrianobarb@yahoo.it
#License GNU GPL2
#Version 6.0

import addonHandler
import gui
import wx
addonHandler.initTranslation()

def onInstall():
	addon = [x for x in addonHandler.getAvailableAddons() if x.manifest["name"].upper() == "WEATHER PLUS"]
	if len(addon) > 0:
		addon = addon[0]
		gui.messageBox (
		# Translators: A message informing the user that he has installed an old version that contains a space rather than an underscore.
		_("You have installed the Weather Plus add-on which is incompatible with this one. The new name of this add-on is Weather_Plus with an underscore. Click OK to update it."),
		# Translators: The title of the dialogbox.
		_("Update confirmation"),
		wx.OK)
		addon.requestRemove()
