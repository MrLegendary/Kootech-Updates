import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
from datetime import date, datetime, timedelta
from resources.libs import extract, downloader, notify, debridit, traktit, skinSwitch, uploadLog, wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
VERSION        = wiz.addonInfo(ADDON_ID,'version')
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
PROFILE        = xbmc.translatePath('special://profile/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
PLAYLISTS      = os.path.join(ADDONS,   'plugin.video.aftermathplaylists')
PACKAGES       = os.path.join(ADDONS,   'packages')
ADDOND         = os.path.join(USERDATA, 'addon_data')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
ADVANCED       = os.path.join(USERDATA, 'advancedsettings.xml')
FANART         = os.path.join(PLUGIN,   'fanart.jpg')
ICON           = os.path.join(PLUGIN,   'icon.png')
ART            = os.path.join(PLUGIN,   'resources', 'art')
SKIN           = xbmc.getSkinDir()
BUILDNAME      = wiz.getS('buildname')
BUILDVERSION   = wiz.getS('buildversion')
BUILDLATEST    = wiz.getS('latestversion')
BUILDCHECK     = wiz.getS('lastbuildcheck')
AUTOCLEANUP    = wiz.getS('autoclean')
AUTOCACHE      = wiz.getS('clearcache')
AUTOPACKAGES   = wiz.getS('clearpackages')
TRAKTSAVE      = wiz.getS('traktlastsave')
REALSAVE       = wiz.getS('debridlastsave')
KEEPTRAKT      = wiz.getS('keeptrakt')
KEEPREAL       = wiz.getS('keepdebrid')
SPLASH         = wiz.getS('splash')
WIZARD         = wiz.getS('wizard')
INSTALLED      = wiz.getS('installed')
EXTRACT        = wiz.getS('extract')
EXTERROR       = wiz.getS('errors')
NOTIFY         = wiz.getS('notify')
NOTEID         = wiz.getS('noteid') 
NOTEID         = 0 if NOTEID == "" else int(float(NOTEID))
NOTEDISMISS    = wiz.getS('notedismiss')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
SKINCHECK      = ['skin.aftermath.zephyr', 'skin.aftermath.silvo', 'skin.aftermath.simple', 'skin.ccm.aftermath']
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
RAM            = int(xbmc.getInfoLabel("System.Memory(total)")[:-2])
EXCLUDES       = uservar.EXCLUDES
BUILDFILE      = uservar.BUILDFILE
UPDATECHECK    = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
HEADERMESSAGE  = uservar.HEADERMESSAGE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
AUTOINSTALL    = uservar.AUTOINSTALL
REPOID         = uservar.REPOID
REPOADDONXML   = uservar.REPOADDONXML
REPOZIPURL     = uservar.REPOZIPURL
WORKING        = True if wiz.workingURL(BUILDFILE) == True else False

###########################
#### Check Updates   ######
###########################
def checkUpdate():
	BUILDNAME      = wiz.getS('buildname')
	BUILDVERSION   = wiz.getS('buildversion')
	link           = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match          = re.compile('name="%s".+?ersion="(.+?)"' % BUILDNAME).findall(link)
	if len(match) > 0:
		version = match[0]
		wiz.setS('latestversion', version)
		if version > BUILDVERSION:
			yes_pressed = DIALOG.yesno(ADDONTITLE,"Er is een update beschikbaar: %s v%s" % (BUILDNAME, version), "Klik op updaten om de nieuwste versie te installeren.", yeslabel="Updaten", nolabel="Negeren")
			if yes_pressed:
				wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Install build]" % (BUILDVERSION, version))
				url = 'plugin://%s/?mode=viewbuild&name=%s' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
				xbmc.executebuiltin('ActivateWindow(10025 ,%s, return)' % url)
				wiz.setS('lastbuildcheck', str(NEXTCHECK))
			else: 
				wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Wait 3 days]" % (BUILDVERSION, version))
				DIALOG.ok(ADDONTITLE, 'You can still update %s to %s from the %s.' % (BUILDNAME, version, ADDONTITLE))
				wiz.setS('lastbuildcheck', str(THREEDAYS))
		else: wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s]" % (BUILDVERSION, version))
	else: wiz.log("[Check Updates] ERROR: Unable to find build version in build text file")
	
def playlistInstall():
	url = 'https://raw.githubusercontent.com/surfacingx/Aftermath/master/plugin.video.aftermathplaylists/'
	link    = wiz.openURL(url+'addon.xml').replace('\n','').replace('\r','').replace('\t','')
	match   = re.compile('<addon.+?id="plugin.video.aftermathplaylists".+?ersion="(.+?)".+?>').findall(link)
	installzip = 'plugin.video.aftermathplaylists-%s.zip' % match[0]
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	lib=os.path.join(PACKAGES, installzip)
	try: os.remove(lib)
	except: pass
	downloader.download(url+installzip,lib)
	extract.all(lib, ADDONS)
	xbmc.sleep(1000)
	xbmc.executebuiltin('UpdateAddonRepos()')
	xbmc.executebuiltin('UpdateLocalAddons()')
	xbmc.sleep(1000)
	
def checkInstalled():
	current = ''
	for skin in SKINCHECK:
		skinpath = os.path.join(ADDONS,skin)
		if os.path.exists(skinpath): 
			current = skin
	if current == SKINCHECK[0]:
		yes_pressed = DIALOG.yesno(ADDONTITLE,"[COLOR dodgerblue]Kootech[/COLOR] Zephyr is currently outdated and is no longer being updated.", "Please download one of the newer community builds.", yeslabel="Build Menu", nolabel="Ignore")
		if yes_pressed:	xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % ADDON_ID)
		else: DIALOG.ok(ADDONTITLE, 'You can still install a community build from the [COLOR dodgerblue]Aftermath[/COLOR] Wizard.')
	elif current == SKINCHECK[1]:
		yes_pressed = DIALOG.yesno(ADDONTITLE,"[COLOR dodgerblue]Kootech[/COLOR] Silvo is currently outdated and is no longer being updated.", "Please download one of the newer community builds.", yeslabel="Build Menu", nolabel="Ignore")
		if yes_pressed:	xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % ADDON_ID)
		else: DIALOG.ok(ADDONTITLE, 'You can still install a community build from the [COLOR dodgerblue]Aftermath[/COLOR] Wizard.')
	elif current == SKINCHECK[2]:
		if KODIV >= 16: 
			gui   = os.path.join(ADDOND, SKINCHECK[2], 'settings.xml')
			f     = open(gui,mode='r'); g = f.read(); f.close()
			match = re.compile('<setting id=\"SubSettings.3.Label\" type=\"string\">(.+?)<\/setting>').findall(g)
			if len(match): 
				name, build, ver = match[0].replace('[COLOR dodgerblue]','').replace('[/COLOR]','').split(' ')
			else: 
				build = "Simple"
				ver = "v0.1"				
		else: 
			gui   = os.path.join(USERDATA,'guisettings.xml')
			f     = open(gui,mode='r'); g = f.read(); f.close()
			match = re.compile('<setting type=\"string\" name=\"skin.aftermath.simple.SubSettings.3.Label\">(.+?)<\/setting>').findall(g)
			name, build, ver = match[0].replace('[COLOR dodgerblue]','').replace('[/COLOR]','').split(' ')
		wiz.setS('buildname', 'Aftermath %s' % build)
		wiz.setS('buildversion', ver[1:])
		wiz.setS('lastbuildcheck', str(NEXTCHECK))
		checkUpdate()
	elif current == SKINCHECK[3]:
		yes_pressed = DIALOG.yesno(ADDONTITLE,"[COLOR dodgerblue]Aftermath[/COLOR] CCM is currently outdated and is no longer being updated.", "Please download one of the newer community builds.", yeslabel="Build Menu", nolabel="Ignore")
		if yes_pressed:	xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % ADDON_ID)
		else: DIALOG.ok(ADDONTITLE, 'You can still install a community build from the [COLOR dodgerblue]Aftermath[/COLOR] Wizard.')
	else:
		yes_pressed = DIALOG.yesno(ADDONTITLE,"Currently no build installed from %s." % ADDONTITLE, "Select 'Build Menu' to install a Community Build", yeslabel="Build Menu", nolabel="Ignore")
		if yes_pressed:	xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % ADDON_ID)
		else: DIALOG.ok(ADDONTITLE, 'You can still install a community build from the %s.' % ADDONTITLE)
		
def writeAdvanced():
	if RAM > 1536: buffer = '209715200'
	else: buffer = '104857600'
	with open(ADVANCED, 'w+') as f:
		f.write('<advancedsettings>\n')
		f.write('	<network>\n')
		f.write('		<buffermode>2</buffermode>\n')
		f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % buffer)
		f.write('		<readbufferfactor>5</readbufferfactor>\n')
		f.write('		<curlclienttimeout>10</curlclienttimeout>\n')
		f.write('		<curllowspeedtime>10</curllowspeedtime>\n')
		f.write('	</network>\n')
		f.write('</advancedsettings>\n')
	f.close()

while xbmc.Player().isPlayingVideo():
	xbmc.sleep(1000)

id   = xbmcaddon.Addon().getAddonInfo('id')
path = xbmcaddon.Addon().getAddonInfo('path').replace(ADDONS,'')[1:]
if not id == path: DIALOG.ok(ADDONTITLE, 'Please make sure that the plugin folder is the', 'Same as the ADDON_ID.')

wiz.log("[Aftermath Playlist] Installed Check")
if not os.path.exists(PLAYLISTS): playlistInstall(); wiz.log("[Aftermath Playlist: Not Installed] Installing Now")
else: wiz.log("[Aftermath Playlist: Installed]")

wiz.log("[Advanced Settings] Exists Check")
if not os.path.exists(ADVANCED): writeAdvanced(); wiz.log("[Advanced Settings] Not Found, Writing")
else: wiz.log("[Advanced Settings] File Found")

if VERSION >= WIZARD: ADDON.setSetting('splash', 'true'); ADDON.setSetting('wizard', VERSION);

wiz.log("[Auto Install Repo] Exists Check")
if AUTOINSTALL == 'Yes' and not os.path.exists(os.path.join(ADDONS, REPOID)):
	workingxml = wiz.workingURL(REPOADDONXML)
	if workingxml == True:
		link    = wiz.openURL(REPOADDONXML).replace('\n','').replace('\r','').replace('\t','')
		match   = re.compile('<addon.+?id="%s".+?ersion="(.+?)".+?>' % REPOID).findall(link)
		installzip = '%s-%s.zip' % (REPOID, match[0])
		workingrepo = wiz.workingURL(REPOZIPURL+installzip)
		if workingrepo == True:
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			lib=os.path.join(PACKAGES, installzip)
			try: os.remove(lib)
			except: pass
			downloader.download(REPOZIPURL+installzip,lib)
			extract.all(lib, ADDONS)
			f = open(os.path.join(ADDONS, REPOID, 'addon.xml'), mode='r').read()
			match = re.compile('<addon.+?id="%s".+?ame="(.+?)".+?>' % REPOID).findall(f)
			wiz.LogNotify(match[0], "Add-on updated", icon=os.path.join(ADDONS, REPOID, 'icon.png'))
			xbmc.sleep(1000)
			xbmc.executebuiltin('UpdateAddonRepos()')
			xbmc.executebuiltin('UpdateLocalAddons()')
			xbmc.sleep(1000)
		else: 
			wiz.LogNotify("Repo Install Error", "Invalid url for zip!")
			wiz.log("Error: Was unable to create a working url for repository.")
	else: 
		wiz.LogNotify("Repo Install Error", "Invalid addon.xml file!")
		wiz.log("Error: Unable to read the addon.xml file.")
else: wiz.log("[Advanced Settings] Installed")

wiz.log("[Auto Update Wizard] Checking Update")
if AUTOUPDATE == 'Yes':
	if wiz.workingURL(WIZARDFILE):
		ver = wiz.checkWizard('version')
		zip = wiz.checkWizard('zip')
		if ver > VERSION:
			yes = DIALOG.yesno(ADDONTITLE, 'Er is een nieuwe versie van %s!' % ADDONTITLE, 'Wilt u versie %s downloaden?' % ver, nolabel='Nu niet', yeslabel="Download")
			if yes:
				DP.create(ADDONTITLE,'Aan het downloaden','', 'Even geduld...')
				lib=os.path.join(PACKAGES, '%s-%s.zip' % (ADDON_ID, ver))
				try: os.remove(lib)
				except: pass
				downloader.download(zip, lib, DP)
				xbmc.sleep(2000)
				DP.update(0,"", "Installing %s update" % ADDONTITLE)
				ext = extract.all(lib, ADDONS, DP)
				DP.close()
				wiz.forceUpdate()
				wiz.LogNotify(ADDONTITLE,'Add-on updated')
	else: wiz.log("URL FOR WIZARDFILE INVALID: %s" % WIZARDFILE)
else: wiz.log("[Auto Update Wizard] Not Enabled")


wiz.log("[Notifications] Enabled Check")
if ENABLE == 'Yes':
	if not NOTIFY == 'true':
		url = wiz.workingURL(NOTIFICATION)
		if url == True:
			link  = wiz.openURL(NOTIFICATION).replace('\r','').replace('\t','')
			id, msg = link.split('|||')
			ID = int(float(id))
			if ID == NOTEID:
				if NOTEDISMISS == 'false':
					notify.Notification(msg=msg, title=ADDONTITLE, BorderWidth=10)
				else: wiz.log("[Notifications] id[%s] Dismissed" % str(ID))
			elif ID > NOTEID:
				wiz.log("[Notifications] id: %s" % str(id))
				wiz.setS('noteid', str(int(id)))
				wiz.setS('notedismiss', 'false')
				openit=notify.Notification(msg=msg, title=HEADERMESSAGE, BorderWidth=10)			
				wiz.log("[Notifications] Complete")
		else: wiz.log("[Notifications] URL(%s): %s" % (NOTIFICATION, url))
	else: wiz.log("[Notifications] Turned Off")
else: wiz.log("[Notifications] Not Enabled")

wiz.log("[Install Check]")
if INSTALLED == 'true':
	if not EXTRACT == '100':
		yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'Installed: %s / Error Count:%s' % (EXTRACT, EXTERROR), 'Would you like to try again?', nolabel='No Thanks!', yeslabel='Yes Please!')
		if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=fresh)" % (ADDON_ID, urllib.quote_plus(BUILDNAME)))
	elif SKIN in ['skin.confluence']:
		gui = wiz.checkBuild(BUILDNAME, 'gui')
		if gui == 'http://':
			DIALOG.ok(ADDONTITLE, "It looks like the skin settings was not applied to the build.", "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close")
			wiz.log('Gui set to: http://')
		elif wiz.workingURL(gui):
			yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'It looks like the skin settings was not applied to the build.', 'Would you like to apply the guiFix?', nolabel='No Thanks!', yeslabel='Yes Please!')
			if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=gui)" % (ADDON_ID, urllib.quote_plus(BUILDNAME)))
			else: wiz.log('Gui url working but cancelled: %s' % gui)
		else:
			DIALOG.ok(ADDONTITLE, "It looks like the skin settings was not applied to the build.", "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close")
			wiz.log('Gui url not working: %s' % gui)
	if KEEPTRAKT == 'true': traktit.traktIt('restore', 'all')
	if KEEPREAL  == 'true': debridit.debridIt('restore', 'all')
	wiz.clearS('install')

if not WORKING:
	wiz.log("Not a valid URL for Build File: %s" % BUILDFILE)
elif BUILDCHECK == '' and BUILDNAME == '':
	checkInstalled()
	wiz.setS('lastbuildcheck', str(NEXTCHECK))
elif not BUILDNAME == '':
	if BUILDCHECK <= str(TODAY):
		wiz.setS('lastbuildcheck', str(NEXTCHECK)); checkUpdate()
	else: 
		wiz.log("[Build Updates] Next check isnt until: %s / TODAY is: %s" % (BUILDCHECK, str(TODAY)))

if KEEPTRAKT == 'true':
	if str(TODAY) >= TRAKTSAVE:
		traktit.autoUpdate('all')
		wiz.setS('traktlastsave', str(THREEDAYS))

if KEEPREAL == 'true':
	if str(TODAY) >= REALSAVE:
		debridit.autoUpdate('all')
		wiz.setS('debridlastsave', str(THREEDAYS))

xbmc.sleep(2000)
if AUTOCLEANUP == 'true':
	if AUTOCACHE == 'true': wiz.log('[AUTO CLEAN UP][Cache: on]'); wiz.clearCache()
	else: wiz.log('[AUTO CLEAN UP][Cache: off]')
	if AUTOPACKAGES == 'true': wiz.log('[AUTO CLEAN UP][Packages: on]'); wiz.clearPackages('startup')
	else: wiz.log('[AUTO CLEAN UP][Packages: off]')
else: wiz.log('[AUTO CLEAN UP: off]')