'''
Created on Aug 22, 2017

@author: crazydiamond
'''
import os
import time
import datetime

def writefile(content,filename):
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        statinfo = os.stat(path)
        os.chown(filename, statinfo.st_uid, statinfo.st_gid)
        #
        # a+ mode append and read
        f= open(filename, "w")
        for cont in content :
            linewrite = cont+"\n"
            f.write(linewrite)
        f.close()
    except:
        print "__Except write file__"

def dateIndex(days):
    try:
        startTime =(time.time()-days*86500)*1000
        indexDate= str(datetime.datetime.fromtimestamp(startTime/1000).strftime('%Y.%m.%d'))
        return indexDate
    except:
        return "1970.01.18"
def hotwarm():
    try:
        listWrite =[]
        # cdnlog
        dateCdn = dateIndex(10)
	cdnlog = "cdnlog-" + dateCdn
	cliptv_live_fpt1 = "cdnlog-cliptv-live-fpt1-" + dateCdn
	cliptv_live_tpcom1 = "cdnlog-cliptv-live-tpcom1-" + dateCdn
	cliptv_live_vdc1 = "cdnlog-cliptv-live-vdc1-" + dateCdn
	cliptv_live_vt1 = "cdnlog-cliptv-live-vt1-" + dateCdn
	cliptv_live_vt2 = "cdnlog-cliptv-live-vt2-" + dateCdn
	cliptv_vod_fpt1 = "cdnlog-cliptv-vod-fpt1-" + dateCdn
	cliptv_vod_vdc1 = "cdnlog-cliptv-vod-vdc1-" + dateCdn
	cliptv_vod_vt1 = "cdnlog-cliptv-vod-vt1-" + dateCdn
	cliptv_vod_vt2 = "cdnlog-cliptv-vod-vt2-" + dateCdn

	vegacdn_live_fpt1 = "cdnlog-vegacdn-live-fpt1-" + dateCdn
	vegacdn_live_tpcom1 = "cdnlog-vegacdn-live-tpcom1-" + dateCdn
	vegacdn_live_vdc1 = "cdnlog-vegacdn-live-vdc1-" + dateCdn
	vegacdn_live_vt1 = "cdnlog-vegacdn-live-vt1-" + dateCdn
	vegacdn_live_vt2 = "cdnlog-vegacdn-live-vt2-" + dateCdn
	vegacdn_vod_fpt1 = "cdnlog-vegacdn-vod-fpt1-" + dateCdn
	vegacdn_vod_vdc1 = "cdnlog-vegacdn-vod-vdc1-" + dateCdn
	vegacdn_vod_vt1 = "cdnlog-vegacdn-vod-vt1-" + dateCdn
	vegacdn_vod_vt2 = "cdnlog-vegacdn-vod-vt2-" + dateCdn
        #
	listWrite.append(cdnlog)
	listWrite.append(cliptv_live_fpt1)
	listWrite.append(cliptv_live_tpcom1)
	listWrite.append(cliptv_live_vdc1)
	listWrite.append(cliptv_live_vt1)
	listWrite.append(cliptv_live_vt2)
	listWrite.append(cliptv_vod_fpt1)
	listWrite.append(cliptv_vod_vdc1)
	listWrite.append(cliptv_vod_vt1)
	listWrite.append(cliptv_vod_vt2)
	listWrite.append(vegacdn_live_fpt1)
	listWrite.append(vegacdn_live_tpcom1)
	listWrite.append(vegacdn_live_vdc1)
	listWrite.append(vegacdn_live_vt1)
	listWrite.append(vegacdn_live_vt2)
	listWrite.append(vegacdn_vod_fpt1)
	listWrite.append(vegacdn_vod_vdc1)
	listWrite.append(vegacdn_vod_vt1)
	listWrite.append(vegacdn_vod_vt2)

        writefile(listWrite,"/opt/workerEs-WarmHot/listindexHotWarm")
    except:
        print "__Except hot warm__"

def delete():
    try:
        listWrite =[]
        #
        dateWeblog = dateIndex(4)
        indexWeblog = "weblog-"+dateWeblog
        indexLogstash = "logstash-"+dateWeblog
        # cdnlog
        dateCdn = dateIndex(60)
        indexCdnVDC = "cdnlog-vdc-"+dateCdn
        indexCdnFPT = "cdnlog-fpt-"+dateCdn
        indexCdnVT1 = "cdnlog-vt1-"+dateCdn
        indexCdnVT2 = "cdnlog-vt2-"+dateCdn
        indexCdn = "cdnlog-"+dateCdn
        # cloud-httpstat
        indexCloudstat = "cloud-httpstat-agents-"+dateCdn
        # ATTT
        dateATTT = dateIndex(4)
        indexSuricataAlert ="suricataids-alert-"+dateATTT
        indexSuricataHttp ="suricataids-http-"+dateATTT
        indexSuricataDns ="suricataids-dns-"+dateATTT
        indexMonitorIDS ="monitorids-"+dateATTT
        #
        listWrite.append(indexWeblog)
        listWrite.append(indexLogstash)
        listWrite.append(indexCdnFPT)
        listWrite.append(indexCdnVDC)
        listWrite.append(indexCdnVT1)
        listWrite.append(indexCdnVT2)
        listWrite.append(indexCdn)
        listWrite.append(indexCloudstat)
        listWrite.append(indexSuricataAlert)
        listWrite.append(indexSuricataHttp)
        listWrite.append(indexSuricataDns)
        listWrite.append(indexMonitorIDS)
        #
        writefile(listWrite,"/opt/workerEs-WarmHot/listindexDelete")
    except:
        print "__Except delete__"

if __name__ == '__main__':
    hotwarm()
    #delete()
