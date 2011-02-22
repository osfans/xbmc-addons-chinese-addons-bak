﻿# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os

#NETITV(天翼高清) by robinttt,2010

THUMB_PATH = os.getcwd() + '/resources/thumbnails/'
MEDIA_PATH = os.getcwd() + '/resources/media/'

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    return httpdata

def GetThumb(reg,data):
    match1 = re.compile(reg).findall(data)
    if len(match1) > 0:
        if match1[0].find('CDATA') == -1:
             tmppic = match1[0].split('/')
             if os.path.isfile(THUMB_PATH + tmppic[len(tmppic) - 1]) == False:
                 urllib.urlretrieve('http://www.netitv.com' + match1[0], THUMB_PATH + tmppic[len(tmppic) - 1])
             thumb = THUMB_PATH + tmppic[len(tmppic) - 1]
        else:
             thumb = MEDIA_PATH + 'NetitvDefault.jpg'
    else:
        thumb = MEDIA_PATH + 'NetitvDefault.jpg'
    return thumb

def Roots():
    url = 'http://www.netitv.com/channel.xml'
    link = GetHttpData(url)
    match0 = link.replace('\r','').replace('\n','')
    match = re.compile('<channel>(.+?)</channel>').findall(match0)
    num = 0
    totalItems = len(match)
    for info in match:
        match1 = re.compile('<id>(.+?)</id>').findall(info)
        id = match1[0]
        match1 = re.compile('<name><!\[CDATA\[(.+?)]]></name>').findall(info)
        name = match1[0]
        match1 = re.compile('<uuid><!\[CDATA\[(.+?)]]></uuid>').findall(info)
        uuid = match1[0]
        if uuid <> '4' and uuid <> '5' and uuid <> '6':
            thumb = GetThumb('<pics><url><!\[CDATA\[(.+?)]]></url>', info)
            num = num + 1
            li = xbmcgui.ListItem(str(num) + '.' + name, iconImage = '', thumbnailImage = thumb)
            u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus('http://www.netitv.com/' + uuid + '/nodeXml/' + id + '.xml')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

def Channels(url,name):
    tmp = url.split('/')
    url1 = tmp[0] + '/' + tmp[1] + '/' + tmp[2] + '/' + tmp[3] + '/'
    li = xbmcgui.ListItem(u'当前位置：'.encode('utf8') + name)
    u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    totalItems = 1

    link = GetHttpData(url)
    match0 = link.replace('\r','').replace('\n','')
    match = re.compile('<node>(.+?)</node>').findall(match0)
    num = 0
    totalItems = totalItems + len(match)
    for info in match:
        match1 = re.compile('<id>(.+?)</id>').findall(info)
        id = match1[0]
        match1 = re.compile('<root>(.+?)</root>').findall(info)
        root = match1[0]
        if id == root:
            match1 = re.compile('<name><!\[CDATA\[(.+?)]]></name>').findall(info)
            name = match1[0]
            thumb = GetThumb('<pics><url><!\[CDATA\[(.+?)]]></url>', info)
            num = num + 1
            li = xbmcgui.ListItem(str(num) + '.' + name, iconImage = '', thumbnailImage = thumb)
            u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url1 + 'newsXml/' + id + '_1.xml')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)


def ListsA(url,name):
    link = GetHttpData(url)
    match0 = link.replace('\r','').replace('\n','')

    match1 = re.compile('<channel_name><!\[CDATA\[(.+?)]]></channel_name>').findall(match0)
    channelname = match1[0]
    match1 = re.compile('<node_name><!\[CDATA\[(.+?)]]></node_name>').findall(match0)
    nodename = match1[0]
    match1 = re.compile('<page_num>(.+?)</page_num>').findall(match0)
    pagenum = int(match1[0])
    match1 = re.compile('<curr_page>(.+?)</curr_page>').findall(match0)
    currpage = int(match1[0])

    li = xbmcgui.ListItem(u'当前位置：'.encode('utf8') + channelname + '->' + nodename + u' 【第'.encode('utf8') + str(currpage) + '/' + str(pagenum) + u'页】'.encode('utf8'))
    u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    totalItems = 1

    match1 = re.compile('<channel_uuid>(.+?)</channel_uuid>').findall(match0)
    uuid = match1[0]
    match1 = re.compile('<node_id>(.+?)</node_id>').findall(match0)
    nodeid = match1[0]

    if currpage > 1:
        li = xbmcgui.ListItem(u'上一页'.encode('utf8'), iconImage='', thumbnailImage = MEDIA_PATH + 'NetitvPageup.png')
        u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus('http://www.netitv.com/' + uuid + '/newsXml/' + nodeid + '_' + str(currpage - 1) + '.xml')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
        totalItems = totalItems + 1
    if currpage < pagenum:
        li = xbmcgui.ListItem(u'下一页'.encode('utf8'), iconImage='', thumbnailImage = MEDIA_PATH + 'NetitvPagedown.png')
        u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus('http://www.netitv.com/' + uuid + '/newsXml/' + nodeid + '_' + str(currpage + 1) + '.xml')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
        totalItems = totalItems + 1

    match = re.compile('<movie(.+?)</movie>').findall(match0)
    num = 0
    totalItems = totalItems + len(match)
    for info in match:
        match1 = re.compile('<name><!\[CDATA\[(.+?)]]></name>').findall(info)
        name = match1[0]
        match1 = re.compile('<id>(.+?)</id>').findall(info)
        movieid = match1[0]
        thumb = GetThumb('<pics><url meta="1"><!\[CDATA\[(.+?)]]></url>', info)
        num = num + 1
        match1 = re.compile('<sub_programs(.+?)/>').findall(info)
        if len(match1) > 0:
            match1 = re.compile('<playurls>(.+?)</playurls>').findall(info)
            if len(match1)>0:
                match2 = re.compile('type="3".+?<!\[CDATA\[(.+?)]]></url>').findall(match1[0]) 
                li = xbmcgui.ListItem(u'播放：'.encode('utf8') + name, iconImage = '', thumbnailImage = MEDIA_PATH + 'NetitvPLay.png')
                u = sys.argv[0] + "?mode=5&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(match2[0]) + "&thumb=" + urllib.quote_plus(thumb)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
            else:
                li = xbmcgui.ListItem(str(num) + '.' + name, iconImage = '', thumbnailImage = thumb)
                u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus('http://www.netitv.com/' + uuid + '/proXml/' + movieid + '_1.xml')
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
        else:
            li = xbmcgui.ListItem(str(num) + '.' + name, iconImage='', thumbnailImage = thumb)
            u=sys.argv[0] + "?mode=4&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&thumb=" + urllib.quote_plus(thumb)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

def ListsB(url,name):
    link = GetHttpData(url)
    match0 = link.replace('\r','').replace('\n','')

    match1 = re.compile('<channel_name><!\[CDATA\[(.+?)]]></channel_name>').findall(match0)
    channelname = match1[0]
    match1 = re.compile('<name><!\[CDATA\[(.+?)]]></name>').findall(match0)
    nodename = match1[0]
    match1 = re.compile('<page_num>(.+?)</page_num>').findall(match0)
    pagenum = int(match1[0])
    match1 = re.compile('<curr_page>(.+?)</curr_page>').findall(match0)
    currpage = int(match1[0])

    li = xbmcgui.ListItem(u'当前位置：'.encode('utf8') + channelname + '->' + nodename + u' 【第'.encode('utf8') + str(currpage) + '/' + str(pagenum) + u'页】'.encode('utf8'))
    u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(name) + "&url="+urllib.quote_plus(url)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    totalItems = 1

    match1 = re.compile('<channel_uuid>(.+?)</channel_uuid>').findall(match0)
    uuid = match1[0]
    match1 = re.compile('<movie id="(.+?)">').findall(match0)
    movieid = match1[0]

    if currpage > 1:
        li = xbmcgui.ListItem(u'上一页'.encode('utf8'), iconImage = '', thumbnailImage = MEDIA_PATH + 'NetitvPageup.png')
        u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus('http://www.netitv.com/' + uuid + '/proXml/' + movieid + '_' + str(currpage - 1) + '.xml')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
        totalItems = totalItems + 1
    if currpage < pagenum:
        li = xbmcgui.ListItem(u'下一页'.encode('utf8'), iconImage = '', thumbnailImage = MEDIA_PATH + 'NetitvPagedown.png')
        u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus('http://www.netitv.com/' + uuid + '/proXml/' + movieid + '_' + str(currpage + 1) + '.xml')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
        totalItems = totalItems + 1

    match = re.compile('<sub_movie(.+?)</sub_movie>').findall(match0)
    num = 0
    totalItems = totalItems + len(match)
    for info in match:
        match1 = re.compile('<name><!\[CDATA\[(.+?)]]></name>').findall(info)
        name = match1[0]
        thumb = GetThumb('<pics><url meta="1"><!\[CDATA\[(.+?)]]></url>', info)
        num = num + 1
        li = xbmcgui.ListItem(str(num) + '.' + name, iconImage = '', thumbnailImage = thumb)
        u = sys.argv[0] + "?mode=4&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&thumb=" + urllib.quote_plus(thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

def Movies(url,name,thumb):
    link = GetHttpData(url)
    match = link.replace('\r','').replace('\n','')
    sname = name.replace('(','\(').replace(')','\)')
    match1 = re.compile('<!\[CDATA\['+sname+']]>(.+?)</movie>').findall(match)
    match = re.compile('<director><!\[CDATA\[(.+?)]]></director>').findall(match1[0])
    if len(match) == 0:
        director = ''
    else:
        director = match[0]
    match = re.compile('<actor><!\[CDATA\[(.+?)]]></actor>').findall(match1[0])
    if len(match) == 0:
        studio = ''
    else:
        studio = match[0]
    match = re.compile('<description><!\[CDATA\[(.+?)]]></description>',re.DOTALL).findall(match1[0])
    if len(match) == 0:
        plot = ''
    else:
        plot = match[0]

    match = re.compile('<playurls>(.+?)</playurls>').findall(match1[0])
    match1 = re.compile('type="3".+?<!\[CDATA\[(.+?)]]></url>').findall(match[0]) 
    if len(match1) == 1:
        li = xbmcgui.ListItem(u'播放：'.encode('utf8') + name, iconImage = '', thumbnailImage = thumb)
        li.setInfo(type = "Video", infoLabels = {"Title":name, "Director":director, "Studio":studio, "Plot":plot})
        u = sys.argv[0] + "?mode=6&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(match1[0]) + "&thumb=" + urllib.quote_plus(thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li)
    elif len(match1) > 1:
        num = 0
        totalItems = len(match1)
        for info in match1:
            num = num + 1
            fullname = name + u' 【第'.encode('utf8') + str(num) + u'集】'.encode('utf8')
            li = xbmcgui.ListItem(u'播放：'.encode('utf8') + fullname, iconImage = '', thumbnailImage = thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":fullname, "Director":director, "Studio":studio, "Plot":plot})
            u=sys.argv[0] + "?mode=6&name=" + urllib.quote_plus(fullname) + "&url=" + urllib.quote_plus(info) + "&thumb=" + urllib.quote_plus(thumb)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

def PlayVideo(url,name,thumb):
    v_url = "http://biz.vsdn.tv380.com/playvod.php?" + url + "|smil"
    link = GetHttpData(v_url)
    match = re.compile('<video src="(.+?)" />').findall(link)
    listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
    xbmc.Player().play(match[0], listitem)

def PlayTV(url,name,thumb):
    v_url = "http://biz.vsdn.tv380.com/playlive.php?" + url + "|smil"
    link = GetHttpData(v_url)
    match = re.compile('<video src="(.+?)" />').findall(link)
    listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
    xbmc.Player().play(match[0], listitem)

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

params = get_params()
mode = None
name = None
url = None
thumb = None

try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

if mode == None:
    name = ''
    Roots()
elif mode == 1:
    Channels(url, name)
elif mode == 2:
    ListsA(url, name)
elif mode == 3:
    ListsB(url, name)
elif mode == 4:
    Movies(url, name, thumb)
elif mode == 5:
    PlayTV(url, name, thumb)
elif mode == 6:
    PlayVideo(url, name, thumb)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

