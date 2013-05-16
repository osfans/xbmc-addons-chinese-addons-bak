﻿# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# Plugin constants 
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ORDER_LIST = [['7','今日增加播放'], ['6','本周增加播放'], ['1','历史最多播放'], ['3','上映时间'], ['9','近期上映'], ['10','近期更新'], ['5','最多评论'], ['11','用户好评']]
ORDER_LIST2 = [['1','最新发布'], ['2','最多播放'], ['3','最多评论'], ['8','最具争议'], ['4','最多收藏'], ['5','最广传播']]
YEAR_LIST2 = [['4','不限'], ['1','今日'], ['2','本周'], ['3','本月']]
RES_LIST = ['normal', 'high', 'super']
UserAgent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

def log(txt):
    message = '%s: %s' % (__addonname__, txt)
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)

def GetHttpData(url):
    log("%s::url - %s" % (sys._getframe().f_code.co_name, url))
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    try:
        response = urllib2.urlopen(req)
        httpdata = response.read()
        if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
        charset = response.headers.getparam('charset')
        response.close()
    except:
        log( "%s (%d) [%s]" % (
               sys.exc_info()[2].tb_frame.f_code.co_name,
               sys.exc_info()[2].tb_lineno,
               sys.exc_info()[1]
               ))
        return ''
    match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
    if match:
        charset = match[0]
    else:
        match = re.compile('<meta charset="(.+?)"').findall(httpdata)
        if match:
            charset = match[0]
    if charset:
        charset = charset.lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
    return httpdata

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def getCurrent(text,list,id):
    match = re.compile('<li class="current"><span>(.+?)</span>').search(text)
    if match:
        list.append([id, match.group(1)])

def getList(listpage,genre,area,year):
    match = re.compile('<label>类型:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    genrelist = re.compile('_g_([^_]*)_[^>]*>([^<]+)</a>').findall(match.group(1))
    getCurrent(match.group(1), genrelist, genre)
    match = re.compile('<label>地区:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    arealist = re.compile('_a_([^_]*)_[^>]*>([^<]+)</a>').findall(match.group(1))
    getCurrent(match.group(1), arealist, area)
    match = re.compile('<label>上映:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    yearlist = re.compile('_r_([^_]*)_[^>]*>([^<]+)</a>').findall(match.group(1))
    getCurrent(match.group(1), yearlist, year)
    return genrelist,arealist,yearlist

def getList2(listpage,genre):
    match = re.compile('<label>类型:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    if match:
        genrelist = re.compile('<li><a href="/v_showlist/[^g]*g([0-9]+)[^\.]*\.html"[^>]*>(.+?)</a></li>').findall(match.group(1))
        getCurrent(match.group(1), genrelist, genre)
    else:
        genrelist = []
    return genrelist

def rootList():
    link = GetHttpData('http://www.youku.com/v/')
    match0 = re.compile('<div class="left">(.+?)<!--left end-->', re.DOTALL).search(link)
    match = re.compile('<li><a href="/([^/]+)/([^\.]+)\.html"[^>]+>(.+?)</a></li>').findall(match0.group(1))
    totalItems = len(match)
    for path, id, name in match:
        if path == 'v_olist':
            u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&genre=&area=&year=&order=7&page=1"
        else:
            u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&genre=0&year=1&order=2&page=1"
        li = xbmcgui.ListItem(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True,totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList(name,id,page,genre,area,year,order):
    url = 'http://www.youku.com/v_olist/%s_a_%s_s__g_%s_r_%s_o_%s_p_%s.html' % (id, area, genre, year, order, page)
    link = GetHttpData(url)
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).search(link)
    plist = []
    if match:
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match.group(1))
        if match1:
            for num, temp in match1:
                if (num not in plist) and (num != page):
                    plist.append(num)
            totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="filter" id="filter">(.+?)<!--filter end-->', re.DOTALL).search(link)
    if match:
        listpage = match.group(1)
    else:
        listpage = ''
    if id == 'c_95':
        match = re.compile('<ul class="p">(.+?)</ul>', re.DOTALL).findall(link)
    else:
        match = re.compile('<ul class="p pv">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1 + len(plist)
    currpage = int(page)

    genrelist,arealist,yearlist = getList(listpage,genre,area,year)
    if genre:
        genrestr = searchDict(genrelist,genre)
    else:
        genrestr = '全部类型'
    if area:
        areastr = searchDict(arealist,area)
    else:
        areastr = '全部地区'
    if year:
        yearstr = searchDict(yearlist,year)
    else:
        yearstr = '全部年份'
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + genrestr + '[/COLOR]/[COLOR FF00FF00]' + areastr + '[/COLOR]/[COLOR FFFFFF00]' + yearstr + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&genre="+urllib.quote_plus(genre)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('/id_(.+?).html"').search(match[i])   
        p_id = match1.group(1)
        match1 = re.compile('<li class="p_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="p_title"><a .*?">(.+?)</a>').search(match[i])
        p_name = match1.group(1)
        match1 = re.compile('<li class="p_status"><span class="status">(.+?)</span>').search(match[i])
        if match1:
            if match1.group(1) == '资料':
                mode = 99
            p_name1 = p_name + '（' + match1.group(1) + '）'
        else:
            p_name1 = p_name
        if match[i].find('<span class="ico__SD"')>0:
            p_name1 += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name1 += '[高清]'
            p_res = 1
        else:
            p_res = 0
        if match[i].find('<li class="p_ischarge">')>0:
            p_name1 += '[付费节目]'
        if id in ('c_96','c_95'):
            mode = 2
            isdir = False
        else:
            mode = 3
            isdir = True
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&id="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)
        
    for num in plist:
        li = xbmcgui.ListItem("... 第" + num + "页")
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&genre="+urllib.quote_plus(genre)+"&area="+urllib.quote_plus(area)+"&year="+year+"&order="+order+"&page="+str(num)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)         
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def getMovie(name,id,thumb,res):
    if len(id)==21:
        link = GetHttpData('http://www.youku.com/show_page/id_' + id + '.html')
        match = re.compile('<a class="btnShow btnplayposi".*?href="(http://v.youku.com/v_show/id_.+?.html)"', re.DOTALL).search(link)
        if not match:
            match = re.compile('<div class="btnplay">.*?href="(http://v.youku.com/v_show/id_.+?.html)"', re.DOTALL).search(link)
        if match:
            # 播放正片
            PlayVideo(name, match.group(1), thumb, res)
        else:
            # 解析预告片
            match = re.compile('class="btnShow btnplaytrailer".*?data="\{videoId:(\d+),', re.DOTALL).search(link)
            if match:
                url = 'http://v.youku.com/v_show/id_' + match.group(1)
                PlayVideo(name, url, thumb, res)
    else:
        PlayVideo(name, 'http://v.youku.com/v_show/id_'+id+'.html', thumb, res)

def seriesList(name,id,thumb,res):
    url = "http://www.youku.com/show_point_id_%s.html?dt=json&__rt=1&__ro=reload_point" % (id)
    data = GetHttpData(url)
    pages = re.compile('<li data="(point_reload_[0-9]+)"', re.DOTALL).findall(data)
    if len(pages)>1:
        for i in range(1,len(pages)):
            url = "http://www.youku.com/show_point/id_%s.html?dt=json&divid=%s&tab=0&__rt=1&__ro=%s" % (id, pages[i], pages[i])
            link = GetHttpData(url)
            data += link
    match = re.compile('<div class="item">(.+?)</div><!--.item-->', re.DOTALL).findall(data)
    totalItems = len(match)

    for i in range(0,len(match)):
        match1 = re.compile('<div class="link"><a .*?href="(http://v.youku.com/v_show/id_.+?.html)"').search(match[i])
        if match1:
            p_url = match1.group(1)
        else:
            continue
        match1 = re.compile('<div class="thumb"><img .*?src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<div class="title">[\s]*<a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1)
        if match[i].find('<span class="ico__SD"')>0:
            p_name += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name += '[高清]'
            p_res = 1
        else:
            p_res = 0
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList2(name,id,page,genre,year,order):
    url = 'http://www.youku.com/v_showlist/t%sd%s%sg%sp%s.html' % (order, year, id, genre, page)
    link = GetHttpData(url)
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).search(link)
    plist = []
    if match:
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match.group(1))
        if match1:
            for num, temp in match1:
                if (num not in plist) and (num != page):
                    plist.append(num)
            totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="filter" id="filter">(.+?)<!--filter end-->', re.DOTALL).search(link)
    if match:
        listpage = match.group(1)
    else:
        listpage = ''
    match = re.compile('<ul class="v">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1 + len(plist)
    currpage = int(page)

    genrelist = getList2(listpage, genre)
    if genre == '0':
        genrestr = '全部类型'
    else:
        genrestr = searchDict(genrelist,genre)
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + genrestr + '[/COLOR]/[COLOR FF00FF00]' + searchDict(YEAR_LIST2,year) + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST2,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=12&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&genre="+urllib.quote_plus(genre)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<li class="v_link"><a href="(http://v.youku.com/v_show/id_.+?.html)"').search(match[i])
        p_url = match1.group(1)
        match1 = re.compile('<li class="v_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="v_title"><a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1).replace('&quot;','"')
        if match[i].find('<span class="ico__SD"')>0:
            p_name += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name += '[高清]'
            p_res = 1
        else:
            p_res = 0
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

    for num in plist:
        li = xbmcgui.ListItem("... 第" + num + "页")
        u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&genre="+urllib.quote_plus(genre)+"&year="+year+"&order="+order+"&page="+str(num)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)         
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,url,thumb,res):
    res_limit = int(__addon__.getSetting('movie_res'))
    if res > res_limit:
        res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s&format=%s" % (url, RES_LIST[res]))
    match = re.compile('"(http://f.youku.com/player/getFlvPath/.+?)" target="_blank"').findall(link)
    if len(match)>0:
        stackurl = 'stack://' + ' , '.join(match)
        listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        xbmc.Player().play(stackurl, listitem)
    else:
        if link.find('该视频为加密视频')>0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：该视频为加密视频')
        elif link.find('解析失败，请确认视频是否被删除')>0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：该视频或为收费节目')

def performChanges(name,id,listpage,genre,area,year,order):
    genrelist,arealist,yearlist = getList(listpage,genre,area,year)
    change = False
    dialog = xbmcgui.Dialog()
    if len(genrelist)>0:
        list = [x[1] for x in genrelist]
        sel = dialog.select('类型', list)
        if sel != -1:
            genre = genrelist[sel][0]
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
    sel = dialog.select('排序', list)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True

    if change:
        progList(name,id,'1',genre,area,year,order)

def performChanges2(name,id,listpage,genre,year,order):
    genrelist = getList2(listpage, genre)
    change = False
    dialog = xbmcgui.Dialog()
    if len(genrelist)>0:
        list = [x[1] for x in genrelist]
        sel = dialog.select('类型', list)
        if sel != -1:
            genre = genrelist[sel][0]
            change = True
    list = [x[1] for x in YEAR_LIST2]
    sel = dialog.select('范围', list)
    if sel != -1:
        year = YEAR_LIST2[sel][0]
        change = True
    list = [x[1] for x in ORDER_LIST2]
    sel = dialog.select('排序', list)
    if sel != -1:
        order = ORDER_LIST2[sel][0]
        change = True

    if change:
        progList2(name,id,'1',genre,year,order)

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
name = ''
id = ''
genre = ''
area = ''
year = ''
order = ''
page = '1'
url = None
thumb = None
res = 0

try:
    res = int(params["res"])
except:
    pass
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
    genre = urllib.unquote_plus(params["genre"])
except:
    pass
try:
    id = urllib.unquote_plus(params["id"])
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
    progList(name,id,page,genre,area,year,order)
elif mode == 2:
    getMovie(name,id,thumb,res)
elif mode == 3:
    seriesList(name,id,thumb,res)
elif mode == 4:
    performChanges(name,id,page,genre,area,year,order)
elif mode == 10:
    PlayVideo(name,url,thumb,res)
elif mode == 11:
    progList2(name,id,page,genre,year,order)
elif mode == 12:
    performChanges2(name,id,page,genre,year,order)

