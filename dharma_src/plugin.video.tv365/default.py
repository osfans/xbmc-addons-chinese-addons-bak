# -*- coding: cp936 -*-
import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys

#Live TV -http://www.tv365w.com/ - by Robinttt 2010.

def Roots():
    url='http://www.tv365w.com/1.js'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<a target=\\\\"etshowlist\\\\" href=\\\\"(.+?)\\\\" tppabs=\\\\".+?\\\\">(.+?)<\\\\/a>').findall(link)
    num=0
    for url,name in match:
        num=num+1
        url=url.replace('\/','/')
        if name.find('����㲥��̨')==-1:
            li=xbmcgui.ListItem(str(num)+'.'+name)
            u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus('http://www.tv365w.com/'+url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
            print url
        else:
            li=xbmcgui.ListItem(str(num)+'.'+name)
            u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus('http://www.tv365w.com/'+url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Channel_TV(url,name):
    li=xbmcgui.ListItem('��ǰλ�ã�'+name)
    u=sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    num=0
    match=re.compile('<TD(.+?)/TD>').findall(link)
    for td in match:
        match1=re.compile('href="(.+?)">(.+?)<').findall(td)
        if len(match1)>=1:
            channel=match1[0][1]
            for i in range(0,len(match1)):
                if match1[i][0].find('/itv/')!=-1:
                    num=num+1
                    url='http://www.tv365w.com'+match1[i][0].replace('..','')
                    if i>0:
                        li=xbmcgui.ListItem(str(num)+'.'+channel+match1[i][1])
                    else:
                        li=xbmcgui.ListItem(str(num)+'.'+channel)
                    u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(channel)+"&url="+urllib.quote_plus(url)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def Channel_Radio(url,name):
    li=xbmcgui.ListItem('��ǰλ�ã�'+name)
    u=sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

    num=1
    li=xbmcgui.ListItem(str(num)+'.�Ƽ�')
    u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>�Ƽ�')+"&url="+urllib.quote_plus('http://www.tv365w.com/list/radio.htm')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
    for url1,name1 in match:
        if url1.find('/radio/radio')!=-1:
            num=num+1
            li=xbmcgui.ListItem(str(num)+'.'+name1)
            u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>'+name1)+"&url="+urllib.quote_plus('http://www.tv365w.com'+url1)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def List_Radio(url,name):
    li=xbmcgui.ListItem('��ǰλ�ã�'+name)
    u=sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
    num=0
    for url1,name1 in match:
        if url1.find('new/')!=-1:
            if url1.find('/radio/new/')==-1:
                 url1='http://www.tv365w.com/radio/'+url1
            else:
                 url1='http://www.tv365w.com'+url1
            num=num+1
            li=xbmcgui.ListItem(str(num)+'.'+name1)
            u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name1)+"&url="+urllib.quote_plus(url1)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def Path_TV(url,name):
    #��ȡ��ý���ַ��mms��ַ���������ԣ�������ַ���ܲ�����  
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<param name="URL" value="(.+?)"').findall(link)
    if len(match)>0:
       li=xbmcgui.ListItem('���ţ�'+name+'  ��'+match[0]+'��')
       li.setInfo(type="Video",infoLabels={"Title":name})
       xbmcplugin.addDirectoryItem(int(sys.argv[1]),match[0],li)


def Path_Radio(url,name):
    #��ȡ��ý���ַ��mms��ַ���������ԣ�������ַ���ܲ�����  
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('"mms://(.+?)"').findall(link)
    if len(match)>0:
       li=xbmcgui.ListItem('���ţ�'+name+'  ��mms://'+match[0]+'��')
       li.setInfo(type="Video",infoLabels={"Title":name})
       xbmcplugin.addDirectoryItem(int(sys.argv[1]),'mms://'+match[0],li)


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                  param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
mode=None
name=None
url=None
thumb=None


try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass


if mode==None:
    name=''
    Roots()

elif mode==1:
    Channel_TV(url,name)

elif mode==2:
    Path_TV(url,name)

elif mode==3:
    Channel_Radio(url,name)

elif mode==4:
    List_Radio(url,name)

elif mode==5:
    Path_Radio(url,name)


xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
