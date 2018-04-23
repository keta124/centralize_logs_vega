'''
Created on Jul 29, 2017

@author: CrazyDiamond
'''

# Reindex yesterday index
# Delete old index

import esQuery
import os
import time
import datetime

def writefile(content,filename):
    try:
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        statinfo = os.stat(path)
        os.chown(filename, statinfo.st_uid, statinfo.st_gid)
        #
        # a+ mode append and read
        f= open(filename, "a+")
        for cont in content :
            linewrite = cont+"\n"
            f.write(linewrite)
        f.close()
    except:
        print "__Except write file__"
        

def hostnameCountIP(timenow):
    try:
        arrayUniqueIP= esQuery.uniqueCountClientIP(timenow)
        if len(arrayUniqueIP)>1:
            listunique =[]
            for i in range(0,len(arrayUniqueIP)):
                hostname = str(arrayUniqueIP[i]["key"])
                unique_clientip= arrayUniqueIP[i]["1"]["value"]
                number_request= arrayUniqueIP[i]["doc_count"]
                stringJson= '{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","unique_clientip":'+str(unique_clientip)+ ',"number_request":'+str(number_request)+'}'
                listunique.append(stringJson)
            filename = "/var/log/cdnstat/cdnstat-uniquevisitor-re.json"
            writefile(listunique,filename)
    except:
        pass

def request_traffic(timenow):
    try:
        #query_cached= 'hitmiss:"HIT" or "hit"'
        arrayRequestTraffic= esQuery.totalAndCached(timenow)
        if len(arrayRequestTraffic)>1:
            listRequestTraffic=[]
            for i in range(0, len(arrayRequestTraffic)):
                hostname = str(arrayRequestTraffic[i]["key"])
                # Request
                totalRequest = arrayRequestTraffic[i]["doc_count"]
                totalCachedRequest = arrayRequestTraffic[i]["3"]["buckets"]["hitmiss"]["doc_count"]
                #Traffic
                totalTraffic = arrayRequestTraffic[i]["1"]["value"]
                totalCachedTraffic = arrayRequestTraffic[i]["3"]["buckets"]["hitmiss"]["1"]["value"]
                # Request per second
                requestPerMinute = int(totalRequest/5)
                requestCachedPerMinute =int(totalCachedRequest/5)
                requestNonCachedPerMinute= requestPerMinute- requestCachedPerMinute
                # Traffic per second
                bandwidthPerMinute = long(totalTraffic/5)
                bandwidthCachedPerMinute = long(totalCachedTraffic/5)
                bandwidthNonCachedPerMinute = bandwidthPerMinute - bandwidthCachedPerMinute
                # append json request
                stringJson='{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","totalrequest":'+str(requestPerMinute)+',"cachedrequest":'+str(requestCachedPerMinute)+',"noncachedrequest":'+str(requestNonCachedPerMinute)+',"totaltraffic":'+str(bandwidthPerMinute)+',"cachedtraffic":'+str(bandwidthCachedPerMinute)+',"noncachedtraffic":'+str(bandwidthNonCachedPerMinute)+'}'
                listRequestTraffic.append(stringJson)
            #
            filename = "/var/log/cdnstat/cdnstat-requestbandwidth-re.json"
            writefile(listRequestTraffic,filename)
    except:
        pass

def responseCode(timenow):  
    try:
        arrayResponseCode= esQuery.codeResponse(timenow)
        if len(arrayResponseCode)>0:
            listResponseCode=[]
            #
            for i in range(0, len(arrayResponseCode)):
                #
                code2xx = 0
                code3xx = 0
                code4xx = 0
                code5xx = 0
                #
                hostname = str(arrayResponseCode[i]["key"])
                listcode = arrayResponseCode[i]["3"]["buckets"]
                if len(listcode)>0:
                    for j in range(0,len(listcode)):
                        codeReponse_ = arrayResponseCode[i]["3"]["buckets"][j]["key"]
                        if 200<= codeReponse_ <300:
                            code2xx = code2xx + arrayResponseCode[i]["3"]["buckets"][j]["doc_count"]
                        if 300<= codeReponse_ <400:
                            code3xx = code3xx + arrayResponseCode[i]["3"]["buckets"][j]["doc_count"]
                        if 400<= codeReponse_ <500:
                            code4xx = code4xx + arrayResponseCode[i]["3"]["buckets"][j]["doc_count"]
                        if 500<= codeReponse_ :
                            code5xx = code5xx + arrayResponseCode[i]["3"]["buckets"][j]["doc_count"]
                #
                stringJson='{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","code2xx":'+str(int(code2xx/5))+',"code3xx":'+str(int(code3xx/5))+',"code4xx":'+str(int(code4xx/5))+',"code5xx":'+str(int(code5xx/5))+'}'
                listResponseCode.append(stringJson)
            filename = "/var/log/cdnstat/cdnstat-httpheader-re.json"
            writefile(listResponseCode,filename)
            
    except:
        pass

def locationGeo(timenow):
    try:
        arrayLocationGeo= esQuery.geoLocation(timenow)
        if len(arrayLocationGeo)>0:
            listLocationGeo=[]
            for i in range(0, len(arrayLocationGeo)):
                hostname = str(arrayLocationGeo[i]["key"])
                listgeo = arrayLocationGeo[i]["geoipcountrycode"]["buckets"]
                if len(listgeo)>0:
                    for j in range(0,len(listgeo)):
                        geoipcountrycode = listgeo[j]["key"]
                        geoipcountryname = listgeo[j]["geoipcountryname"]["buckets"][0]["key"]
                        # +4 khi chia cho 5 khac 0
                        totalrequest = listgeo[j]["doc_count"]+4
                        stringJson='{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","country_code2":"'+geoipcountrycode+'","country_name":"'+geoipcountryname+'","totalrequest":'+str(int(totalrequest/5))+'}'
                        listLocationGeo.append(stringJson)
            filename = "/var/log/cdnstat/cdnstat-geoip-re.json"
            writefile(listLocationGeo,filename)
            
    except:
        pass

def requestTimeIsp(timenow):
    try:
        arrayRequestTimeIsp= esQuery.ispRequestTime(timenow)
        if len(arrayRequestTimeIsp)>0:
            listRequestTimeIsp=[]
            for i in range(0, len(arrayRequestTimeIsp)):
                hostname = str(arrayRequestTimeIsp[i]["key"])
                listisp = arrayRequestTimeIsp[i]["customer_isp"]["buckets"]
                if len(listisp)>0:
                    for j in range(0,len(listisp)):
                        customer_isp = listisp[j]["key"]
                        byte = long(listisp[j]["1"]["value"]/5)
                        request_time = round(listisp[j]["4"]["value"]+0.0009,3)
                        stringJson='{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","customer_isp":"'+customer_isp+'","byte":'+str(byte)+',"request_time":'+str(request_time)+'}'
                        listRequestTimeIsp.append(stringJson)
            filename = "/var/log/cdnstat/cdnstat-isp-re.json"
            writefile(listRequestTimeIsp,filename)
    except:
        pass


def reIndexEs():
    try:
        #start time => + 1440
        startTime =(int(time.time()/86400)*86400-86400)*1000 - 240000
        for j in range(0,1440):
            timeIndex = startTime+ j*60000
            request_traffic(timeIndex)
            hostnameCountIP(timeIndex)
            responseCode(timeIndex)
            locationGeo(timeIndex)
            requestTimeIsp(timeIndex)
        indexDate= str(datetime.datetime.fromtimestamp(startTime/1000).strftime('%Y.%m.%d'))
        #1
        index_requestbandwidth="cdnstat-requestbandwidth-ex-"+indexDate
        esQuery.deleteIndex(index_requestbandwidth)
        print index_requestbandwidth
        #2
        index_uniquevisitor="cdnstat-uniquevisitor-ex-"+indexDate
        esQuery.deleteIndex(index_uniquevisitor)
        print index_uniquevisitor
        #3
        index_httpheader="cdnstat-httpheader-ex-"+indexDate
        esQuery.deleteIndex(index_httpheader)
        print index_httpheader
        #4
        index_geoip="cdnstat-geoip-ex-"+indexDate
        esQuery.deleteIndex(index_geoip)
        print index_geoip
        #5
        index_isp="cdnstat-isp-ex-"+indexDate
        esQuery.deleteIndex(index_isp)
        print index_isp
    except:
        pass
if __name__ == '__main__':
    reIndexEs()
