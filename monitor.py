#!/usr/bin/python

import os
import sys
import xbmc
import xbmcaddon

import re,sys,json,time,xbmc
import hashlib,urllib,os,base64,codecs,xmlrpclib
import gzip, StringIO

from resources.lib.opensubtitles import loadsub#verificar...


__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
debug = __addon__.getSetting("debug")
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode("utf-8")
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources')).decode("utf-8")

__settings__ = xbmcaddon.Addon("service.subloader")

ignore_words = (__settings__.getSetting('ignore_words').split(','))
ExcludeTime = int((__settings__.getSetting('ExcludeTime')))*60

sys.path.append(__resource__)


def Debug(msg, force = False):
    if(debug == "true" or force):
        try:
            print "#####[SubLoader]##### " + msg
        except UnicodeEncodeError:
            print "#####[SubLoader]##### " + msg.encode( "utf-8", "ignore" )

Debug("Loading '%s' version '%s'" % (__scriptname__, __version__))

# helper function to get string type from settings
def getSetting(setting):
    return __addon__.getSetting(setting).strip()

# helper function to get bool type from settings
def getSettingAsBool(setting):
    return getSetting(setting).lower() == "true"

# check exclusion settings for filename passed as argument
def isExcluded(movieFullPath):

    if not movieFullPath:
        return False

    Debug("isExcluded(): Checking exclusion settings for '%s'." % movieFullPath)

    if (movieFullPath.find("pvr://") > -1) and getSettingAsBool('ExcludeLiveTV'):
        Debug("isExcluded(): Video is playing via Live TV, which is currently set as excluded location.")
        return False

    if (movieFullPath.find("http://") > -1) and getSettingAsBool('ExcludeHTTP'):
        Debug("isExcluded(): Video is playing via HTTP source, which is currently set as excluded location.")
        return False

    ExcludePath = getSetting('ExcludePath')
    if ExcludePath and getSettingAsBool('ExcludePathOption'):
        if (movieFullPath.find(ExcludePath) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 1." % ExcludePath)
            return False

    ExcludePath2 = getSetting('ExcludePath2')
    if ExcludePath2 and getSettingAsBool('ExcludePathOption2'):
        if (movieFullPath.find(ExcludePath2) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 2." % ExcludePath2)
            return False

    ExcludePath3 = getSetting('ExcludePath3')
    if ExcludePath3 and getSettingAsBool('ExcludePathOption3'):
        if (movieFullPath.find(ExcludePath3) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 3." % ExcludePath3)
            return False

    ExcludePath4 = getSetting('ExcludePath4')
    if ExcludePath4 and getSettingAsBool('ExcludePathOption4'):
        if (movieFullPath.find(ExcludePath4) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 4." % ExcludePath4)
            return False

    ExcludePath5 = getSetting('ExcludePath5')
    if ExcludePath5 and getSettingAsBool('ExcludePathOption5'):
        if (movieFullPath.find(ExcludePath5) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 5." % ExcludePath5)
            return False

    return True


class SubLoaderPlayer(xbmc.Player):
    from resources.lib.opensubtitles import loadsub
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        Debug("Initalized")
        self.run = True

    def onPlayBackStopped(self):
        Debug("Stopped")
        self.run = True

    def onPlayBackEnded(self):
        Debug("Ended")
        self.run = True

    def onAVStarted(self):
        check_for_specific = (__addon__.getSetting('check_for_specific').lower() == 'true')
        specific_language = (__addon__.getSetting('selected_language'))
        specific_language = xbmc.convertLanguage(specific_language, xbmc.ISO_639_2)
        self.run = True		
        #file = xbmc.Player().getPlayingFile()
        #file = xbmc.getInfoLabel('Player.Filenameandpath') #remover depois
        #title = xbmc.Player().getVideoInfoTag().getIMDBNumber() #remover depois
        #imdb = xbmc.Player().getVideoInfoTag().getIMDBNumber() #remover depois				
        st = int((__addon__.getSetting('wait_source')))*1000
        # add --> self.run = True
		
        if self.run:
            xbmc.sleep(st)		
            movieFullPath = xbmc.Player().getPlayingFile()
            Debug("movieFullPath '%s'" % movieFullPath)
            availableLangs = xbmc.Player().getAvailableSubtitleStreams()
            Debug("availableLangs '%s'" % availableLangs)
            totalTime = xbmc.Player().getTotalTime()
            Debug("totalTime '%s'" % totalTime)
			
            if (xbmc.Player().isPlayingVideo() and totalTime > ExcludeTime and ((not xbmc.getCondVisibility("VideoPlayer.HasSubtitles")) or (check_for_specific and not specific_language in availableLangs)) and all(movieFullPath.find (v) <= -1 for v in ignore_words) and (isExcluded(movieFullPath)) ):
                self.run = False			
                xbmc.sleep(1000)		
                Debug('Started: AutoSearching for Subs')
                #xbmc.executebuiltin('XBMC.ActivateWindow(SubtitleSearch)')
                #xbmc.executebuiltin('Notification("%s", "%s", "%s",)' % (file, movieFullPath, 40000))
                loadsub()
                #self.loadsub()	na realidade assi a chamada existe
                #xbmc.executebuiltin('XBMC.RunScript(special://home/addons/service.autosubs/resources/lib/OpenSubtitles.py)')										
            else:
                Debug('Started: Subs found or Excluded')
                self.run = False


player_monitor = SubLoaderPlayer()

while not xbmc.abortRequested:
    xbmc.sleep(1000)
	
del player_monitor
