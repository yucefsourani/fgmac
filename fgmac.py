au#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  fgmac.py
#
#  Copyright 2016 youcef sourani <youcef.m.sourani@gmail.com>
#
#  www.arfedora.blogspot.com
#
#  www.arfedora.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import subprocess
import platform
import sys
import time





############################################################################################
def init_check():

    if os.getuid()==0:
        sys.exit("Run Script Without Root Permissions.")

    if platform.linux_distribution()[0]!="Fedora" and platform.linux_distribution()[1]!="23":
        sys.exit("Fedora 23 Not Found.")


    if not sys.version.startswith("3"):
        sys.exit("Use Python 3 Try run python3 fmac.py")


    if os.getenv("XDG_CURRENT_DESKTOP")!="GNOME" :
        sys.exit("Your Desktop Is Not gnome shell")

init_check()
#############################################################################################





#############################################################################################
home=os.getenv("HOME")
def get_all_extensions():
	result=[]
	if os.path.isdir("%s/.local/share/gnome-shell/extensions"%home):
		for filee in os.listdir("%s/.local/share/gnome-shell/extensions"%home):
			if filee not in result:
				result.append(filee)

	if os.path.isdir("/usr/local/share/gnome-shell/extensions"):
		for filee in os.listdir("/usr/local/share/gnome-shell/extensions"):
			if filee not in result:
				result.append(filee)

	for filee in os.listdir("/usr/share/gnome-shell/extensions"):
		if filee not in result:
			result.append(filee)

	return result

old_extension=get_all_extensions()
############################################################################################





############################################################################################


extensions_to_enable=["user-theme@gnome-shell-extensions.gcampax.github.com",\
"places-menu@gnome-shell-extensions.gcampax.github.com",\
"activities-config@nls1729","favorites@cvine.org","hide-dash@xenatt.github.com",\
"Move_Clock@rmy.pobox.com","CoverflowAltTab@palatis.blogspot.com"]


gsettings=["gsettings set org.gnome.desktop.background show-desktop-icons false",\
           "gsettings set org.gnome.desktop.background  picture-uri \
           'file://%s/Pictures/gnome/Dark_Ivy.jpg' "%home,\
           "gsettings set org.gnome.desktop.screensaver picture-uri \
           'file://%s/Pictures/gnome/Blinds.jpg' "%home,\
           "gsettings set org.gnome.desktop.interface icon-theme 'Gmac-icons' ",\
           "gsettings set org.gnome.shell.extensions.user-theme name 'Gmac-Shell' ",\
           "gsettings set org.gnome.nautilus.preferences sort-directories-first true",\
           "gsettings set org.gnome.nautilus.preferences executable-text-activation ask",\
           "gsettings set org.gnome.desktop.peripherals.touchpad scroll-method 'two-finger-scrolling' ",\
           "gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true",\
           "gsettings set  org.gnome.desktop.interface gtk-theme  Gmac",\
           "gsettings set org.gnome.desktop.interface enable-animations true",\
           "gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' ",\
           "gsettings set org.gnome.nautilus.preferences always-use-location-entry false",\
           "gsettings set org.gnome.desktop.interface cursor-theme 'Gmac-Cursor' ",\
           "gsettings set org.gnome.Terminal.Legacy.Settings dark-theme false",\
           "gsettings set org.gnome.Terminal.Legacy.Settings default-show-menubar false"]


dconf=["dconf write /org/gnome/shell/extensions/activities-config/transparent-panel 0", \
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-no-text false",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-icon-padding 5",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-no-icon false",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-icon-path \"\'%s/.icons/logo-top.png\'\""%home,\
                   "dconf write /org/gnome/shell/extensions/activities-config/enable-conflict-detection true",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-hot-corner-threshold 0",\
                   "dconf write /org/gnome/shell/extensions/activities-config/pointer-barriers-supported true",\
                   "dconf write /org/gnome/shell/extensions/activities-config/maximized-window-effect 0",\
                   "dconf write /org/gnome/shell/extensions/activities-config/panel-hide-app-menu-button-icon false",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-text-padding 0",\
                   "dconf write /org/gnome/shell/extensions/activities-config/panel-background-color-hex-rgb \"\'#ffffff\'\"",\
                   "dconf write /org/gnome/shell/extensions/activities-config/panel-hide-rounded-corners false",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-text \"\'Dashbord\'\"",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-hot-corner false",\
                   "dconf write /org/gnome/shell/extensions/activities-config/first-enable false",\
                   "dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-removed \"false\"",\
                   "dconf write /org/gnome/shell/extensions/favorites/icon false",\
                   "dconf write /org/gnome/shell/extensions/favorites/position 2"]





#########################################################################################################




def make_folders():
    folders=["%s/.icons"%home,"%s/.themes"%home,"%s/.local/share/gnome-shell/extensions"%home,\
             "%s/.config/gconf/apps"%home,"%s/.config/autostart"%home]
    for folder in folders:
        os.makedirs(folder,exist_ok=True)

make_folders()



def install_packs():
    check=subprocess.call("sudo dnf install  -y --best --allowerasing gnome-shell-extension-user-theme \
                    gnome-shell-extension-places-menu dconf plymouth-plugin-script docky GConf2 gnome-tweak-tool",shell=True)
    if check!=0:
        sys.exit("Fail Check Your Internet || Check sudo .")

    print ("Please Wait.")
    for extension in os.listdir("extensions"):
        if extension not in old_extension:
            subprocess.call("cp -r extensions/%s %s"%(extension, \
                                                      "%s/.local/share/gnome-shell/extensions"%home),shell=True)



install_packs()




def fmac_themes():
    subprocess.call("cp -r Gmac GmacOS Gmac-Shell %s/.themes"%home,shell=True)

fmac_themes()



def fmac_icons():
    subprocess.call("cp -r Gmac-icons Gmac-Cursor  logo-top.png   %s/.icons"%home,shell=True)

fmac_icons()



def fmac_backgrounds():
    subprocess.call("cp -r gnome %s/Pictures"%home,shell=True)

fmac_backgrounds()



def fmac_plymouth():
    subprocess.call("sudo cp -r mbuntu /usr/share/plymouth/themes/",shell=True)

fmac_plymouth()


def fmac_docky():
    gc="%gconf.xml"
    subprocess.call("cp  docky.desktop %s/.config/autostart"%home,shell=True)
    subprocess.call("cp -r docky-2 %s/.config/gconf/apps"%home,shell=True)
    subprocess.call("cp  %s %s/.config/gconf/apps"%(gc,home),shell=True)
fmac_docky()

if old_extension!=None:
	for i in old_extension:
		subprocess.call("gnome-shell-extension-tool -d %s"%i,shell=True)
		time.sleep(0.5)



for i in extensions_to_enable:
	if os.path.isdir("%s/.local/share/gnome-shell/extensions/%s"%(home,i)) or \
    os.path.isdir("/usr/share/gnome-shell/extensions/%s"%i)or \
    os.path.isdir("/usr/local/share/gnome-shell/extensions/%s"%i):
		subprocess.call("gnome-shell-extension-tool -e  %s"%i,shell=True)
		time.sleep(0.5)



for conf in gsettings:
	subprocess.call("%s"%conf,shell=True)
	time.sleep(0.5)

for conf in dconf:
    subprocess.call("%s"%conf,shell=True)
    time.sleep(0.5)





print ("Please Wait.")
subprocess.call("sudo plymouth-set-default-theme mbuntu -R",shell=True)
subprocess.call("sudo dracut -f",shell=True)

print("Please Reboot System.")
