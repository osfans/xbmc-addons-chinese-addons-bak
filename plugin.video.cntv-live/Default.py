# -*- coding: cp936 -*-
import httplib,urllib,re,xbmcplugin,xbmcgui,xbmc,os

#CCTV Video - by Robinttt 2009.
#CNTV Video - Edit by Spy007 2010

def CATEGORIES():
         addDir('����ֱ��','/index.shtml',6,os.getcwd()+'\\resources\\media\\Default2.jpg')
         addDir('����ֱ��','/live_h/index.shtml',6,os.getcwd()+'\\resources\\media\\Defaultx.png')
         addDir('����ֱ��','/cctv1/l/index.shtml',6,os.getcwd()+'\\resources\\media\\Default3.jpg')
         addDir('��Ƶ�㲥','/podcast/index',1,os.getcwd()+'\\resources\\media\\Default4.jpg')

def LiveChannel(url,name):
         if name=='����ֱ��':
                 addDir(name+'>CCTV1�ۺ�Ƶ��',"pa://cctv_p2p_hdcctv1",7,os.getcwd()+'\\resources\\media\\cctv1.png')
                 addDir(name+'>CCTV2�ƾ�Ƶ��',"pa://cctv_p2p_hdcctv2",7,os.getcwd()+'\\resources\\media\\cctv2.png')
                 addDir(name+'>CCTV3����Ƶ��',"pa://cctv_p2p_hdcctv3",7,os.getcwd()+'\\resources\\media\\cctv3.png')
                 addDir(name+'>CCTV4���޹���',"pa://cctv_p2p_hdcctv4",7,os.getcwd()+'\\resources\\media\\cctv4.png')
                 addDir(name+'>CCTV4ŷ�޹���',"pa://cctv_p2p_hdcctv4euro",7,os.getcwd()+'\\resources\\media\\cctv4o.png')
                 addDir(name+'>CCTV4���޹���',"pa://cctv_p2p_hdcctv4america",7,os.getcwd()+'\\resources\\media\\cctv4a.png')
                 addDir(name+'>CCTV5����Ƶ��',"pa://cctv_p2p_ec_c5",7,os.getcwd()+'\\resources\\media\\cctv5.png')
                 addDir(name+'>CCTV6��ӰƵ��',"pa://cctv_p2p_hdcctv6",7,os.getcwd()+'\\resources\\media\\cctv6.png')
                 addDir(name+'>CCTV7����Ƶ��',"pa://cctv_p2p_hdcctv7",7,os.getcwd()+'\\resources\\media\\cctv7.png')
                 addDir(name+'>CCTV8���Ӿ�Ƶ��',"pa://cctv_p2p_hdcctv8",7,os.getcwd()+'\\resources\\media\\cctv8.png')
                 addDir(name+'>CCTV9Ӣ�����',"pa://cctv_p2p_hdcctv9",7,os.getcwd()+'\\resources\\media\\cctv9.png')
                 addDir(name+'>CCTV10�ƽ�Ƶ��',"pa://cctv_p2p_hdcctv10",7,os.getcwd()+'\\resources\\media\\cctv10.png')
                 addDir(name+'>CCTV11Ϸ��Ƶ��',"pa://cctv_p2p_hdcctv11",7,os.getcwd()+'\\resources\\media\\cctv11.png')
                 addDir(name+'>CCTV12����Ƶ��',"pa://cctv_p2p_hdcctv12",7,os.getcwd()+'\\resources\\media\\cctv12.png')
                 addDir(name+'>CCTV�ٶ�Ƶ��',"pa://cctv_p2p_hdcctvkids",7,os.getcwd()+'\\resources\\media\\cctvshaoer.png')
                 addDir(name+'>CCTV����Ƶ��',"pa://cctv_p2p_hdcctvmusic",7,os.getcwd()+'\\resources\\media\\cctvmusic.png')
                 addDir(name+'>CCTV����Ƶ��',"pa://cctv_p2p_hdcctvgaoqing",7,os.getcwd()+'\\resources\\media\\cctvhd.png')
                 addDir(name+'>CCTV����Ƶ��',"pa://cctv_p2p_cctvfayu",7,os.getcwd()+'\\resources\\media\\cctvf.png')
                 addDir(name+'>CCTV��������Ƶ��',"pa://cctv_p2p_hdxiyu",7,os.getcwd()+'\\resources\\media\\cctve.png')
                 addDir(name+'>CCTV����Ƶ��',"pa://cctv_p2p_hdcctvrussian",7,os.getcwd()+'\\resources\\media\\cctveyu.png')
                 addDir(name+'>CCTV��������Ƶ��',"pa://cctv_p2p_hdcctvarabic",7,os.getcwd()+'\\resources\\media\\cctvayu.png')
                 addDir(name+'>CCTV���ӹ���Ƶ��',"pa://cctv_p2p_hdgouwu",7,os.getcwd()+'\\resources\\media\\cctvgouwu.png')
                 addDir(name+'>CCTV��������Ƶ��',"pa://cctv_p2p_hdfyzq",7,os.getcwd()+'\\resources\\media\\noname.jpg')
                 addDir(name+'>CCTV�߶���Ƶ��',"pa://cctv_p2p_hdcctvgaowang",7,os.getcwd()+'\\resources\\media\\noname.jpg')
         elif name=="����ֱ��":
                 addDir(name+'>��������',"pl://cctv_p2p_hdanhui",7,os.getcwd()+'\\resources\\media\\anhui.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdbeijing",7,os.getcwd()+'\\resources\\media\\beijing.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdshanghaikatong",7,os.getcwd()+'\\resources\\media\\dongfang.png')
                 addDir(name+'>�������',"pl://cctv_p2p_hdtianjin",7,os.getcwd()+'\\resources\\media\\tianjin.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdchongqing",7,os.getcwd()+'\\resources\\media\\chongqing.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hddongnan",7,os.getcwd()+'\\resources\\media\\dongnan.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdgansu",7,os.getcwd()+'\\resources\\media\\gansu.png')
                 addDir(name+'>�㶫����',"pl://cctv_p2p_hdguangdong",7,os.getcwd()+'\\resources\\media\\guangdong.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdguangxi",7,os.getcwd()+'\\resources\\media\\guangxi.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdguizhou",7,os.getcwd()+'\\resources\\media\\guizhou.png')
                 addDir(name+'>�ӱ�����',"pl://cctv_p2p_hdhebei",7,os.getcwd()+'\\resources\\media\\hebei.png')
                 addDir(name+'>����������',"pl://cctv_p2p_hdheilongjiang",7,os.getcwd()+'\\resources\\media\\heilongjiang.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdhenan",7,os.getcwd()+'\\resources\\media\\henan.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdhubei",7,os.getcwd()+'\\resources\\media\\hubei.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdhunan",7,os.getcwd()+'\\resources\\media\\hunan.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdjiangsu",7,os.getcwd()+'\\resources\\media\\jiangsu.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdjiangxi",7,os.getcwd()+'\\resources\\media\\jiangxi.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdjilin",7,os.getcwd()+'\\resources\\media\\jilin.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdliaoning",7,os.getcwd()+'\\resources\\media\\liaoning.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdlvyou",7,os.getcwd()+'\\resources\\media\\lvyou.png')
                 addDir(name+'>���ɹ�����',"pl://cctv_p2p_hdneimeng",7,os.getcwd()+'\\resources\\media\\neimenggu.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdningxia",7,os.getcwd()+'\\resources\\media\\ningxia.png')
                 addDir(name+'>�ຣ����',"pl://cctv_p2p_hdqinghai",7,os.getcwd()+'\\resources\\media\\qinghai.png')
                 addDir(name+'>ɽ������',"pl://cctv_p2p_hdshandong",7,os.getcwd()+'\\resources\\media\\shandong.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdshanvxi",7,os.getcwd()+'\\resources\\media\\shan_xi.png')
                 addDir(name+'>ɽ������',"pl://cctv_p2p_hdshan-xi",7,os.getcwd()+'\\resources\\media\\shanxi.png')
                 addDir(name+'>�Ĵ�����',"pl://cctv_p2p_hdsichuan",7,os.getcwd()+'\\resources\\media\\sichuan.png')
                 addDir(name+'>�½�����',"pl://cctv_p2p_hdxinjiang",7,os.getcwd()+'\\resources\\media\\xinjiang.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdxizang",7,os.getcwd()+'\\resources\\media\\xizang.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdyunnan",7,os.getcwd()+'\\resources\\media\\yunnan.png')
                 addDir(name+'>�㽭����',"pl://cctv_p2p_hdzhejiang",7,os.getcwd()+'\\resources\\media\\zhejiang.png')
                 addDir(name+'>��������',"pl://cctv_p2p_hdxiamen",7,os.getcwd()+'\\resources\\media\\xiamen.png')
                 
def LiveLink(url,name):
         xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\cctvlive.exe\\" '+url+')')
		 #pl://cctv_p2p_hdanhui

def DibbleChannel(url,name):
         req=httplib.HTTPConnection("vod.cctv.com")
         req.request("get", url)
         response=req.getresponse()
         link=response.read()
         response.close()                  
         match=re.compile('<dd><a href="/podcast/(.+?)">(.+?)</a></dd>').findall(link)
         for url1,name1 in match:
                  addDir(name+'>'+name1,'http://vod.cctv.com/podcast/'+url1,2,os.getcwd()+'\\resources\\media\\Default4.jpg')
         match=re.compile('<dd><a href="/page/(.+?)">(.+?)</a></dd>').findall(link)
         for url1,name1 in match:
                  if name1.find('�ؿ�')==-1:
                          addDir(name+'>'+name1,'/page/'+url1,2,os.getcwd()+'\\resources\\media\\Default4.jpg')

def DibbleABC(url,name):
         req=httplib.HTTPConnection("vod.cctv.com")
         req.request("get", url)
         response=req.getresponse()
         link=response.read()
         response.close()
         match=re.compile('<h3>(.+?)</h3>').findall(link)
         for name1 in match:
                  addDir(name+'>'+name1,url,3,os.getcwd()+'\\resources\\media\\Default4.jpg')  

def DibbleColumn(url,name):
         req=httplib.HTTPConnection("vod.cctv.com")
         req.request("get", url)
         response=req.getresponse()
         link=response.read()
         response.close()
         match0=re.sub('\r','',link)
         match0=re.sub('\n','',match0)
         name1=name.split('>')
         name2=name.replace('>'+name1[len(name1)-1],'')
         match1=re.compile('<h3>'+name1[len(name1)-1]+'</h3>(.+?)</ul>').findall(match0)
         match=re.compile('<a href="(.+?)" target="_blank">(.+?)</a>').findall(match1[0])
         for url1,name1 in match:
                  addDir(name2+'>'+name1,url1,4,os.getcwd()+'\\resources\\media\\Default4.jpg')

def DibbleList(url,name):
         #�˴�������httplib����urllib2�õ�����Զ�ǵ�1ҳ�����ݣ������Ұ����ʱ���о��Ÿ㶨AJAX
         #�����ж�url���Ƿ���Ҫ��ʼ��
         if url.find('|')!=-1:
                tmp=url.split('|')
                elementId=tmp[0]
                pagec=tmp[1]
                paget=tmp[2]
         else:
                req=httplib.HTTPConnection("vod.cctv.com")
                req.request("get", url)
                response=req.getresponse()
                link=response.read()
                response.close()

                elementId=''
                paget=''
                match=re.compile('var elementId = "(.+?)"').findall(link)
                if len(match)>0: elementId=match[0]
                pagec='1'
                match=re.compile('"total_page">(.+?)</b>').findall(link)
                if len(match)>0: paget=match[0] 

         if elementId!='':  #��ȡӰƬ�б�
                headers = {'elementId':elementId,'currpage':pagec}
                req = httplib.HTTPConnection("vod.cctv.com") 
                req.request("get", "/act/platform/view/page/showElement.jsp", '', headers)
                response=req.getresponse()
                link= response.read()
                response.close()
                match=re.compile('href="/video/VIDE(.+?)" title="(.+?)" target="_blank"><img(.+?)src="(.+?)"').findall(link)	

                if len(match)>0:
                       match1=re.compile('"mh_title">(.+?)</span>').findall(link)
                       name=match1[0]
                       addDir('..��ǰλ��:'+name+' ��'+pagec+'/'+paget+'ҳ',elementId+'|1|'+paget,4,os.getcwd()+'\\resources\\media\\Default4.jpg')
                       if int(pagec)>1:
                              addDir('..��һҳ',elementId+'|'+str(int(pagec)-1)+'|'+paget,4,os.getcwd()+'\\resources\\media\\Pageup.png')
                       if int(pagec)<int(paget): 
                              addDir('..��һҳ',elementId+'|'+str(int(pagec)+1)+'|'+paget,4,os.getcwd()+'\\resources\\media\\Pagedown.png')
                              addDir('..���һҳ',elementId+'|'+paget+'|'+paget,4,os.getcwd()+'\\resources\\media\\Default4.jpg')
                       for url1,name1,temp,thumbnail in match:
                              thumbnail=re.sub(' ','%20',thumbnail)
                              addDir(name1,url1,5,thumbnail)


def DibbleLink(url,name):
         #��ȡӰƬʵ�ʲ��ŵ�ַ
         req=httplib.HTTPConnection("vod.cctv.com")
         req.request("get", "/video/VIDE"+url)
         response=req.getresponse()
         link=response.read()
         response.close()
         Duration=''
         Plot=''
         Studio=''
         match=re.compile('����ʱ����</strong><span class="color_jh">(.+?)</span>').findall(link)
         if len(match)>0:Duration=match[0]
         match=re.compile('����������</strong>(.+?)</p>').findall(link)
         if len(match)>0:Plot=match[0]
         match=re.compile('�ײ�Ƶ����</strong><span class="color_jh">(.+?)</span>').findall(link)
         if len(match)>0:Studio=match[0]
         match=re.compile('��Ŀ���ƣ�</strong>(.+?)</p>').findall(link)
         if len(match)>0:Studio=Studio+'  ��Ŀ:'+match[0]
         match=re.compile('�ײ�ʱ�䣺</strong><span class="color_jh">(.+?)</span>').findall(link)
         if len(match)>0:Studio=Studio+'  �ײ�:'+match[0]

         headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6'}
         req=httplib.HTTPConnection("vod.cctv.com")
         req.request("get", "/playcfg/flv_info_new.jsp?&videoId=VIDE"+url,'',headers)
         response=req.getresponse()
         link=response.read()
         response.close()
         match=re.compile('"title":"(.+?)"embed":').findall(link)
         if len(match)>0:
                  match1=re.compile('"url":"(.+?)"').findall(match[0])
                  if len(match1)==1:
                           li=xbmcgui.ListItem('���ţ�'+name,iconImage='', thumbnailImage=os.getcwd()+'\\resources\\media\\PLay.png')
                           li.setInfo(type="Video",infoLabels={"Title":name,"Plot":Plot,"Duration":Duration,"Studio":Studio})
                           xbmcplugin.addDirectoryItem(int(sys.argv[1]),'http://58.221.41.93/v.cctv.com/flash/'+match1[0],li)
                  else:
                           num=0
                           for url1 in match1:   
                                    num=num+1
                                    li=xbmcgui.ListItem('���ţ�'+name+' ����'+str(num)+'�ڡ�',iconImage='', thumbnailImage=os.getcwd()+'\\resources\\media\\PLay.png')
                                    li.setInfo(type="Video",infoLabels={"Title":name+" ����"+str(num)+"�ڡ�","Plot":Plot,"Duration":Duration,"Studio":Studio})
                                    xbmcplugin.addDirectoryItem(int(sys.argv[1]),'http://58.221.41.93/v.cctv.com/flash/'+url1,li)

                
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


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
        print ""
        CATEGORIES()

elif mode==1:
        print ""+url
        DibbleChannel(url,name) 
 
elif mode==2:
        print ""+url
        DibbleABC(url,name)
      
elif mode==3:
        print ""+url
        DibbleColumn(url,name)
      
elif mode==4:
        print ""+url
        DibbleList(url,name)   
     
elif mode==5:
        print ""+url
        DibbleLink(url,name)

elif mode==6:
        print ""+url
        LiveChannel(url,name)

elif mode==7:
        print ""+url
        LiveLink(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
