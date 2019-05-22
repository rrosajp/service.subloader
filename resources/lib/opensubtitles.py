#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, xbmc, xbmcaddon, xbmcgui
import base64, gzip, xmlrpclib, xbmcvfs
import StringIO, re, hashlib, json, urlparse
import codecs, urllib, xbmcplugin




def loadsub():

	try:
		addon = "service.subloader"#alterar quando estiver tudo ligado
		setting = xbmcaddon.Addon(addon).getSetting
		server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
#		token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token'] (token antigo)
		token = server.LogIn('', '', 'en', 'XBMC_Subtitles_Unofficial_v5.2.15')['token']
		media = xbmc.Player().getVideoInfoTag().getMediaType()




		langDict = {
			'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq',
			'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur',
			'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut',
			'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre',
			'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin',
			'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn',
			'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit',
			'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni',
			'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per',
			'Polish': 'pol', 'Portuguese': 'por', 'Portuguese(Brazil)': 'pob', 'Romanian': 'rum',
			'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv',
			'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam',
			'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

		codePageDict = {
			'ara': 'cp1256', 'ar': 'cp1256', 'ell': 'cp1253', 'el': 'cp1253', 'heb': 'cp1255',
			'he': 'cp1255', 'tur': 'cp1254', 'tr': 'cp1254', 'rus': 'cp1251', 'ru': 'cp1251'}

		release = ['cam', 'camrip', 'telesync', 'ts', 'hdts', 'hc', 'hcrip', 'pdvd', 'predvdrip', 
			'telecine', 'tc', 'hdtc', 'ppv', 'ppvrip', 'screener', 'scr', 'dvdscr', 'dvdcreener', 'bdscr', 
			'r5', 'r5line', 'line', 'dvd', 'dvdrip', 'dvdr', 'dvdmux', 'dvdfull', 'dvd5', 'dvd9', 
			'hdtv', 'dsr', 'dsrip', 'satrip', 'dthrip', 'dvbrip', 'pdtv', 'dtvrip', 'tvrip', 'hdtvrip', 
			'vod', 'vodrip', 'vodr', 'webdl', 'webdlrip', 'web', 'hdrip', 'webrip', 'webr', 'webcap', 
			'blu', 'ray', 'bluray', 'bdrip', 'brip', 'brrip', 'bdmv', 'rip', 'dl', 'cap', 'divx', 'xvid']

		langs = []

		filter = []
		


		if setting('subtitles'):
			langs.append(langDict[setting('subtitles.lang.1')])
			if not setting('subtitles.lang.2') == 'None':
				langs.append(langDict[setting('subtitles.lang.2')])
			if not setting('subtitles.lang.3') == 'None':
				langs.append(langDict[setting('subtitles.lang.3')])
		else:
			raise Exception()
			
		sublanguageid = ','.join(langs)




# Get IMDBNumber or Name ************************************************************************************************************

		imdb = xbmc.Player().getVideoInfoTag().getIMDBNumber()

		if imdb.ljust(2)[:2].strip() == 'tt':
			imdbid = re.sub('[^0-9]', '', imdb)
		else:
			imdbid = 'None'
			if media == 'movie' or media == 'video':
				title = (xbmc.Player().getVideoInfoTag().getOriginalTitle()).lower()
				year = xbmc.Player().getVideoInfoTag().getYear()
				query = title + " " + str(year)
			if media == 'episode':
				query = (xbmc.Player().getVideoInfoTag().getTVShowTitle()).lower()
				season = xbmc.Player().getVideoInfoTag().getSeason()
				episode = xbmc.Player().getVideoInfoTag().getEpisode()
			else:
				raise Exception()

#************************************************************************************************************************************



# Get release type ******************************************************************************************************************

		vidPath = xbmc.Player().getPlayingFile()
		fmt = re.split('[.:;()[\]{}\\\\/\s\&\€\#\=\$\?\!\%\+\-_\*]', vidPath)
		fmt = [i.lower() for i in fmt]
		fmt = [i for i in fmt if i in release]

		if fmt:
			fmtst = ''.join(fmt)
		else:
			fmt = re.split('[.:;()[\]{}\\\\/\s\&€\#\=\$\?\!%\+\-_\*[0-9]', vidPath)
			fmt = [i.lower() for i in fmt]
			fmt = [i for i in fmt if i in release]
			if fmt:
				fmtst = ''.join(fmt)
			else:
				if setting('notif') and setting('subsearch'):
					xbmc.executebuiltin('Notification("%s", "%s", "%s",)' % ("Opening sub dialog", "No release type detected", 5000))
					raise Exception()
				else:
					raise Exception()
				

#************************************************************************************************************************************




		if fmtst == 'cam' or fmtst == 'camrip':
			fmt = ['cam-rip', 'cam.rip', 'cam rip', 'cam', 'camrip']
			fmtflex = ['cam-rip', 'cam.rip', 'cam rip', 'cam', 'camrip', 'telesync', 'ts', 'hdts', 'hc', 'hcrip', 'pdvd', 'predvdrip']
		if fmtst == 'telesync' or fmtst == 'ts' or fmtst == 'hdts' or fmtst == 'hc' or fmtst == 'hcrip' or fmtst == 'pdvd' or fmtst == 'predvdrip':
			fmt = ['telesync', 'ts', 'hdts', 'hc', 'hcrip', 'pdvd', 'predvdrip']
			fmtflex = ['cam-rip', 'cam.rip', 'cam rip', 'cam', 'camrip', 'telesync', 'ts', 'hdts', 'hc', 'hcrip', 'pdvd', 'predvdrip']
		if fmtst == 'telecine' or fmtst == 'tc' or fmtst == 'hdtc':
			fmt = ['telecine', 'tc', 'hdtc']
			fmtflex = fmt
		if fmtst == 'ppv' or fmtst == 'ppvrip':
			fmt = ['ppv', 'ppvrip']
			fmtflex = fmt
		if fmtst == 'screener' or fmtst == 'scr' or fmtst == 'dvdscr' or fmtst == 'dvdcreener' or fmtst == 'bdscr':
			fmt = ['screener', 'scr', 'dvdscr', 'dvdcreener', 'bdscr']
			fmtflex = ['screener', 'scr', 'dvdscr', 'dvdcreener', 'bdscr', 'dvd', 'dvd-r', 'dvdrip', 'dvd rip', 'dvdr', 'dvdmux', 'dvdfull', 'dvd5', 'dvd9', 'dvd-rip', 'dvd.rip', 'dvd-mux', 'dvd.mux', 'dvd-5', 'dvd-9']
		if fmtst == 'r5' or fmtst == 'r5line' or fmtst == 'line':
			fmt = ['r5', 'r5line', 'line', 'r5.line', 'r5-line', 'r5 line']
			fmtflex = fmt
		if fmtst == 'dvd' or fmtst == 'dvdrip' or fmtst == 'dvdr' or fmtst == 'dvdmux' or fmtst == 'dvdfull' or fmtst == 'dvd5' or fmtst == 'dvd9':
			fmt = ['dvd', 'dvd-r', 'dvdrip', 'dvdr', 'dvdmux', 'dvdfull', 'dvd5', 'dvd9', 'dvd-rip', 'dvd rip', 'dvd.rip', 'dvd-mux', 'dvd.mux', 'dvd-5', 'dvd-9']
			fmtflex = ['screener', 'scr', 'dvdscr', 'dvdcreener', 'bdscr', 'dvd', 'dvd-r', 'dvdrip', 'dvd rip', 'dvdr', 'dvdmux', 'dvdfull', 'dvd5', 'dvd9', 'dvd-rip', 'dvd.rip', 'dvd-mux', 'dvd.mux', 'dvd-5', 'dvd-9']
		if fmtst == 'hdtv' or fmtst == 'dsr' or fmtst == 'dsrip' or fmtst == 'satrip' or fmtst == 'dthrip' or fmtst == 'dvbrip' or fmtst == 'pdtv' or fmtst == 'dtvrip' or fmtst == 'tvrip' or fmtst == 'hdtvrip':
			fmt = ['hdtv', 'dsr', 'dsrip', 'satrip', 'dthrip', 'dvbrip', 'pdtv', 'dtvrip', 'tvrip', 'hdtvrip', 'hdtv-rip', 'hdtv.rip', 'hdtv rip']
			fmtflex = fmt
		if fmtst == 'vob' or fmtst == 'vodrip' or fmtst == 'vodr':
			fmt = ['r5', 'r5line', 'line', 'r5.line', 'r5-line', 'r5 line']
			fmtflex = fmt
		if fmtst == 'webdl' or fmtst == 'webdlrip' or fmtst == 'dl':
			fmt = ['web-dl', 'webdl', 'web.dl', 'web dl', 'webdlrip']
			fmtflex = ['web-dl', 'webdl', 'web.dl', 'web dl', 'webdlrip', 'webrip', 'web-rip', 'web.rip', 'web rip', 'webr', 'web', 'webcap', 'web-cap', 'web.cap', 'web cap', 'hdrip']
		if fmtst == 'webrip' or fmtst == 'webr' or fmtst == 'webcap' or fmtst == 'web' or fmtst == 'cap':
			fmt = ['webrip', 'web-rip', 'web.rip', 'web rip', 'webr', 'web', 'webcap', 'web-cap', 'web.cap', 'web cap']
			fmtflex = ['web-dl', 'webdl', 'web.dl', 'web dl', 'webdlrip', 'webrip', 'web-rip', 'web.rip', 'web rip', 'webr', 'web', 'webcap', 'web-cap', 'web.cap', 'web cap', 'hdrip']
		if fmtst == 'bluray' or fmtst == 'blurayrip' or fmtst == 'blu' or fmtst == 'ray':
			fmt = ['blu', 'ray', 'bluray', 'blu-ray', 'blu.ray', 'blu ray']
			fmtflex = ['blu', 'ray', 'bluray', 'blu-ray', 'blu.ray', 'blu ray', 'bdrip', 'bd-rip', 'bd.rip', 'bd rip', 'brrip', 'br-rip', 'br.rip', 'br rip', 'brip', 'b-rip', 'b.rip', 'b rip', 'bdmv']
		if fmtst == 'bdrip' or fmtst == 'brip' or fmtst == 'brrip' or fmtst == 'bdmv':
			fmt = ['bdrip', 'bd-rip', 'bd.rip', 'bd rip', 'brrip', 'br-rip', 'br.rip', 'br rip', 'brip', 'b-rip', 'b.rip', 'b rip', 'bdmv']
			fmtflex = ['blu', 'ray', 'bluray', 'blu-ray', 'blu.ray', 'blu ray', 'bdrip', 'bd-rip', 'bd.rip', 'bd rip', 'brrip', 'br-rip', 'br.rip', 'br rip', 'brip', 'b-rip', 'b.rip', 'b rip', 'bdmv']
		if fmtst == 'hdrip':
			fmt = ['hdrip', 'hd-rip', 'hd rip', 'hd.rip']
			fmtflex = ['web-dl', 'webdl', 'web.dl', 'web dl', 'webdlrip', 'hdrip', 'webrip', 'web-rip', 'web.rip', 'web rip', 'webr', 'web', 'webcap', 'web-cap', 'web.cap', 'web cap']










		filelocal = xbmc.getInfoLabel('Player.Filenameandpath')#funciona local
		filestr = vidPath.split('/')[-1]#funciona em cache torrents seren





		if setting('notif'):
			xbmc.executebuiltin('Notification("%s", "%s", "%s",)' % (fmtst, filestr, 4000))




		if media == 'episode':
			if imdbid is not 'None':
				result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid, 'season': season, 'episode': episode}])['data']
			else:
				result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'query': query, 'season': season, 'episode': episode}])['data']
		else:
			if imdbid is not 'None':
				result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid}])['data']
			else:
				result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'query': query}])['data']






		result = [i for i in result if i['SubSumCD'] == '1']
	
	
		for lang in langs:
			filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in fmt)]
#			filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in quality)]
#			filter += [i for i in result if i['SubLanguageID'] == lang]


		try:
			lang = filter[0]['SubLanguageID']
		except Exception:
			if setting('strict'):
				raise Exception()
			else:
				for lang in langs:
					filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in fmtflex)]
					lang = filter[0]['SubLanguageID']
# colocar aqui um raise exception e criar log...




#		try:
#			lang = xbmc.convertLanguage(filter[0]['SubLanguageID'], xbmc.ISO_639_1)
#		except Exception:
#			lang = filter[0]['SubLanguageID']




#		lang = filter[0]['SubLanguageID']
		content = [filter[0]['IDSubtitleFile'], ]
		content = server.DownloadSubtitles(token, content)
		content = base64.b64decode(content['data'][0]['data'])
		content = gzip.GzipFile(fileobj=StringIO.StringIO(content)).read()

		subtitle = xbmc.translatePath('special://temp/')
		subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)

		file = xbmcvfs.File(subtitle, 'w')
		file.write(str(content))
		file.close()

		xbmc.sleep(1000)
		xbmc.Player().setSubtitles(subtitle)
	

		if setting('notif'):
			xbmc.sleep(4000)
			test = [filter[0]['MovieReleaseName'], ]
			xbmc.executebuiltin('Notification("%s", "%s", "%s",)' % (lang, test, 4000))

	except Exception:
		if setting('subsearch'):
			xbmc.executebuiltin('XBMC.ActivateWindow(SubtitleSearch)')
