import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[B][COLOR dodgerblue]Kootech[/COLOR] [COLOR white]Updates[/COLOR][/B]'
EXCLUDES       = [ADDON_ID, 'repository.kootech', 'plugin.video.aftermathplaylists']
# Text File with build info in it.
BUILDFILE      = 'http://kodikootech.com/Repo/builds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'http://cb.srfx.in/apks.txt'

# Dont need to edit just here for icons stored locally
HOME           = xbmc.translatePath('special://home/')
PLUGIN         = os.path.join(HOME,     'addons',    ADDON_ID)
ART            = os.path.join(PLUGIN,   'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONMAINT      = os.path.join(ART, 'kootech.png')
ICONBUILDS     = os.path.join(ART, 'kootech.png')
ICONCONTACT    = os.path.join(ART, 'kootech.png')
ICONPLAYLISTS  = os.path.join(ART, 'kootech.png')
ICONSAVE       = os.path.join(ART, 'kootech.png')
ICONTRAKT      = os.path.join(ART, 'kootech.png')
ICONREAL       = os.path.join(ART, 'kootech.png')
ICONAPK        = os.path.join(ART, 'kootech.png')
ICONSETTINGS   = os.path.join(ART, 'kootech.png')
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'Yes'                                                                    

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'dodgerblue'
COLOR2         = 'grey'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR2+']%s[/COLOR]'    
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'                                          
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'                                          
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Huidige Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]' 
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Huidige Thema:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]' 

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'                                                                    
# You can add \n to do line breaks
CONTACT        = 'Voor vragen neem contact op via:\r\n\r\nlouvankooten@live.nl'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'                                                                    
# Url to wizard version
WIZARDFILE     = 'http://kodikootech.com/Repo/builds.txt'                          
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'                                                                    
# Addon ID for the repository
REPOID         = 'repository.aftermath'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/surfacingx/Aftermath/master/repository.aftermath/addon.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.githubusercontent.com/surfacingx/Aftermath/master/repository.aftermath/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'No'
# Url to notification file
NOTIFICATION   = 'http://www.kodikootech.com/Notifications/news.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
# Font size of header
FONTHEADER     = 'Font14'
HEADERMESSAGE  = '[B][COLOR dodgerblue]Kootech[/COLOR] [COLOR white]Notifications[/COLOR][/B]'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Font for Notification Window
FONTSETTINGS   = 'Font13'
# Background for Notification Window
BACKGROUND     = 'http://cb.srfx.in/img/AMaftermath.jpg'
#########################################################