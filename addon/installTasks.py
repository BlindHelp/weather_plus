# -*- coding: UTF-8 -*-
#Author: Adriano Barbieri <Adrianobarb@yahoo.it>
#note: This file groups all Weather_Plus configuration files saved by the user into one folder.

import config, globalVars, gui, os, shutil

def MoveConfigFile(dest_folder):
	"""Move all Weather_Plus configuration files to a dedicated folder"""
	#List of original paths
	src_paths = [
		os.path.join(globalVars.appArgs.configPath,"Weather.ini"),
		os.path.join(globalVars.appArgs.configPath, "Weather.zipcodes"),
		os.path.join(globalVars.appArgs.configPath, "Weather.volumes"),
		os.path.join(globalVars.appArgs.configPath, "Weather_samples"),
		os.path.join(globalVars.appArgs.configPath, "Weather_searchkey"),
		os.path.join(globalVars.appArgs.configPath, "Weather.default")
		]

	#Create the destination folder if it does not exist
	if not os.path.exists(dest_folder):
		try:
			os.makedirs(dest_folder)
		except Exception: pass

	for src_path in src_paths:
		if not os.path.exists(src_path): continue
		#Extract only the file name from the source path
		file_name = os.path.basename(src_path)
		dest_path = os.path.join(dest_folder, file_name)

		#Check if the file already exists in the destination folder
		if not os.path.exists(dest_path):
			#Move the config files in new path
			try:
				shutil.move(src_path, dest_path)
			except Exception: pass

def onInstall():
	MoveConfigFile(os.path.join(globalVars.appArgs.configPath, "Weather_config"))