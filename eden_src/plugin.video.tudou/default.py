﻿# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# Plugin constants 
__addonname__ = "土豆视频(Tudou)"
__addonid__ = "plugin.video.tudou"
__addon__ = xbmcaddon.Addon(id=__addonid__)

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ORDER_LIST = [['0','最新发布'], ['1','人气最旺'], ['3','“挖”得最多']]

def GetHttpData(url):
    print "getHttpData: " + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    if response.headers.get('content-encoding', None) == 'gzip':
        httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
    response.close()
    match = re.compile('<meta http-equiv="[Cc]ontent-[Tt]ype" content="text/html; charset=(.+?)"').findall(httpdata)
    if len(match)<=0:
        match = re.compile('meta charset="(.+?)"').findall(httpdata)
    if len(match)>0:
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset, 'ignore').encode('utf8', 'ignore')
    return httpdata

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def getList(listpage):
    match0 = re.compile('<h3>类型:</h3><ul>(.+?)</ul>').search(listpage)
    catlist = re.compile('<li[^>]*><a href=".+?/c[0-9]+t([\-0-9]+)[^"]+">(.+?)</a></li>').findall(match0.group(1))
    match0 = re.compile('<h3>国家地区:</h3><ul>(.+?)</ul>').search(listpage)
    arealist = re.compile('<li[^>]*><a href=".+?/c[0-9]+t[\-0-9]+v[\-0-9]+z[\-0-9]+a([\-0-9]+)y[^"]+">(.+?)</a></li>').findall(match0.group(1))
    match0 = re.compile('<h3>年份:</h3><ul>(.+?)</ul>').search(listpage)
    yearlist = re.compile('<li[^>]*><a href=".+?/c[0-9]+t[\-0-9]+v[\-0-9]+z[\-0-9]+a[\-0-9]+y([\-0-9]+)[^"]+">(.+?)</a></li>').findall(match0.group(1))
    return catlist,arealist,yearlist

def rootList():
    li=xbmcgui.ListItem('电影')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电影')+"&url="+urllib.quote_plus('http://movie.tudou.com/albumtop/c22')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('电视剧')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电视剧')+"&url="+urllib.quote_plus('http://tv.tudou.com/albumtop/c30')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('综艺')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('综艺')+"&url="+urllib.quote_plus('http://zy.tudou.com/albumtop/c31')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('动漫')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('动漫')+"&url="+urllib.quote_plus('http://zy.tudou.com/albumtop/c9')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList(name,baseurl,page,cat,area,year,order):
    url = baseurl+'t'+cat+'a'+area+'y'+year+'h-1s'+order+'p'+page+'.html'
    link = GetHttpData(url)
    matchp = re.compile('<div class="page_nav"(.+?)</div>', re.DOTALL).findall(link)
    if len(matchp):
        match1 = re.compile('<li.+?>([0-9]+)(</a>)?</li>', re.DOTALL).findall(matchp[0])
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="side_col" id="sideCol">(.+?)<!-- side_col -->', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    match = re.compile('<div class="pack pack_(.+?)<span class="ext_arrow"></span>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    currpage = int(page)
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    catlist,arealist,yearlist = getList(listpage)
    if cat == '-1':
        catstr = '全部类型'
    else:
        catstr = searchDict(catlist,cat)
    if area == '-1':
        areastr = '全部地区'
    else:
        areastr = searchDict(arealist,area)
    if year == '-1':
        yearstr = '全部年份'
    else:
        yearstr = searchDict(yearlist,year)
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + catstr + '[/COLOR]/[COLOR FF00FF00]' + areastr + '[/COLOR]/[COLOR FFFFFF00]' + yearstr + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&url="+baseurl+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<div class="pic"><a href="(.+?)" target="_blank"><img src="(.+?)".+?>').search(match[i])
        if not match1:
            match1 = re.compile('<div class="pic"><a class="inner" target="new" href="(.+?)"><img .+?src="(.+?)">').search(match[i])
            p_url = match1.group(1)
            p_thumb = match1.group(2)
            mode = 3
            isdir = False
        else:
            p_url = match1.group(1)
            p_thumb = match1.group(2)
            mode = 2
            isdir = True

        match1 = re.compile('<div class="txt"><h6 class="caption"><a [^>]+>(.+?)</a></h6>').search(match[i])
        p_name = match1.group(1)
        match1 = re.compile('<a .*?class="vinf".*?>(.*?)</a>').search(match[i])
        if match1 and match1.group(1):
            p_name1 = p_name + '（' + match1.group(1) + '）'
        else:
            p_name1 = p_name
        match1 = re.compile('<li class="desc">(.+?)</li>').search(match[i])
        if match1:
            p_tagline = match1.group(1)
        else:
            p_tagline = ''
        match1 = re.compile('<li class="cast">(.+?)</li>').search(match[i])
        if match1:
            p_cast = re.compile('<a [^>]+>(.+?)</a>').findall(match1.group(1))
        else:
            p_cast = []
        match1 = re.compile('<span class="ext_cast">导演: <a [^>]+>(.+?)</a>').search(match[i])
        if match1:
            p_director = match1.group(1)
        else:
            p_director = ''
        match1 = re.compile('<span class="ext_type">类型: (.+?)</span>').search(match[i])
        if match1:
            p_genre = match1.group(1)
        else:
            p_genre = ''
        match1 = re.compile('<p class="ext_intro">(.+?)</p>', re.DOTALL).search(match[i])
        if match1:
            p_plot = match1.group(1)
        else:
            p_plot = ''
        match1 = re.compile('<span class="ext_date">年代: ([0-9]+)</span>').search(match[i])
        if match1:
            p_year = int(match1.group(1))
        else:
            p_year = 0
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)

    # Fetch and build user selectable page number 
    if len(matchp): matchp1 = re.compile('<li.+?>([0-9]+)</a></li>', re.DOTALL).findall(matchp[0])
    if len(matchp1):
        plist=[]
        for num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+baseurl+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+year+"&order="+order+"&page="+str(num)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems) 
        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,url,thumb):
    link = GetHttpData(url)
    match = re.compile('<div class="pack pack_video_card">\s*<div class="pic">\s*<a target="new" title="(.+?)"\s*href="\s*(http://www.tudou.com/.*?.html)\s*"></a>\s*<div class="inner">\s*<img\s*src="(.+?)"', re.DOTALL).findall(link)
    if match:
        totalItems = len(match)
        for p_name, p_url, src in match:
            p_thumb = src
            li = xbmcgui.ListItem(name+'：'+p_name, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
            #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    else:
        match = re.compile('<div class="album-btn">\s*<a href="(http://www.tudou.com/.*?.html)"', re.DOTALL).findall(link)
        if match:
            PlayVideo(name,match[0],thumb)
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '没有可播放的视频')

def PlayVideo(name,url,thumb):
    link = GetHttpData("http://www.flvcd.com/parse.php?kw="+url)
    match = re.compile('<br>下载地址：(.*?)<br>花费时间：', re.DOTALL).findall(link)
    if match:
        match = re.compile('<a href="(http://.+?)" target="_blank"').findall(match[0])
        listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
        #listitem.setInfo(type = "Video", infoLabels = {"Title":name, "Director":director, "Plot":plot, "Year":int(year)})
        xbmc.Player().play(match[0]+'|User-Agent='+UserAgent, listitem)
    else:
        match = re.compile('<br/>提示：\s*(.*?)</td>', re.DOTALL).findall(link)
        dialog = xbmcgui.Dialog()
        if match:
            ok = dialog.ok(__addonname__, match[0])
        else:
            ok = dialog.ok(__addonname__, '没有可播放的视频')

def performChanges(name,url,listpage,cat,area,year,order):
    catlist,arealist,yearlist = getList(listpage)
    change = False
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
    if len(arealist)>0:
        list = [x[1] for x in arealist]
        sel = dialog.select('地区', list)
        if sel != -1:
            area = arealist[sel][0]
            change = True
    if len(yearlist)>0:
        list = [x[1] for x in yearlist]
        sel = dialog.select('年份', list)
        if sel != -1:
            year = yearlist[sel][0]
            change = True

    list = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True

    if change:
        progList(name,url,'1',cat,area,year,order)

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
cat = '-1'
area = '-1'
year = '-1'
order = '0'
page = '1'
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
    page = urllib.unquote_plus(params["page"])
except:
    pass
try:
    order = urllib.unquote_plus(params["order"])
except:
    pass
try:
    year = urllib.unquote_plus(params["year"])
except:
    pass
try:
    area = urllib.unquote_plus(params["area"])
except:
    pass
try:
    cat = urllib.unquote_plus(params["cat"])
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
    rootList()
elif mode == 1:
    progList(name,url,page,cat,area,year,order)
elif mode == 2:
    seriesList(name,url,thumb)
elif mode == 3:
    PlayVideo(name,url,thumb)
elif mode == 4:
    performChanges(name,url,page,cat,area,year,order)
