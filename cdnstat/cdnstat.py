'''
Created on Jul 21, 2017

@author: CrazyDiamond
'''
import esQuery
import os
import time
import json
def writefile(content,filename):
    try:
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        statinfo = os.stat(path)
        os.chown(filename, statinfo.st_uid, statinfo.st_gid)
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
            #all_host_cdn
            #total_clientip=0
            #total_request=0
            #
            for i in range(0,len(arrayUniqueIP)):
                hostname = str(arrayUniqueIP[i]["key"])
                unique_clientip= arrayUniqueIP[i]["1"]["value"]
                number_request= arrayUniqueIP[i]["doc_count"]
                #
                #total_clientip=total_clientip+unique_clientip
                #total_request=total_request+number_request
                #
                stringJson= '{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","unique_clientip":'+str(unique_clientip)+ ',"number_request":'+str(number_request)+'}'
                listunique.append(stringJson)
                #print stringJson
            #total_ = '{"timecheck":'+str(timenow/1000+240)+',"hostname":"all_host_cdn",'+'"unique_clientip":'+str(total_clientip)+ ',"number_request":'+str(total_request)+'}'
            #listunique.append(total_)
            filename = "/var/log/cdnstat/cdnstat-uniquevisitor.json"
            writefile(listunique,filename)
    except:
        pass

def request_traffic(timenow):
    try:
        #query_cached= 'hitmiss:"HIT" or "hit"'
        arrayRequestTraffic= esQuery.totalAndCached(timenow)
        if len(arrayRequestTraffic)>1:
            listRequestTraffic=[]
            #all_host_cdn
            #allRequest=0
            #allCachedRequest=0
            #allNonCachedRequest=0
            #
            #allTraffic=0
            #allCachedTraffic=0
            #allNonCachedTraffic=0
            #???
            
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
                requestNonCachedPerMinute= requestPerMinute - requestCachedPerMinute
                # All
                #allRequest=allRequest+requestPerMinute
                #allCachedRequest=allCachedRequest+requestCachedPerMinute
                #allNonCachedRequest=allNonCachedRequest+requestNonCachedPerMinute
                # Traffic per second
                bandwidthPerMinute = long(totalTraffic/5)
                bandwidthCachedPerMinute = long(totalCachedTraffic/5)
                bandwidthNonCachedPerMinute = bandwidthPerMinute - bandwidthCachedPerMinute
                # All Traffic
                #allTraffic=allTraffic+bandwidthPerMinute
                #allCachedTraffic=allCachedTraffic+bandwidthCachedPerMinute
                #allNonCachedTraffic=allNonCachedTraffic+bandwidthNonCachedPerMinute
                # append json request
                stringJson='{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","totalrequest":'+str(requestPerMinute)+',"cachedrequest":'+str(requestCachedPerMinute)+',"noncachedrequest":'+str(requestNonCachedPerMinute)+',"totaltraffic":'+str(bandwidthPerMinute)+',"cachedtraffic":'+str(bandwidthCachedPerMinute)+',"noncachedtraffic":'+str(bandwidthNonCachedPerMinute)+'}'
                listRequestTraffic.append(stringJson)
            #total_ = '{"timecheck":'+str(timenow/1000+240)+',"hostname":"all_host_cdn",' +'"totalrequest":'+str(allRequest)+',"cachedrequest":'+str(allCachedRequest)+',"noncachedrequest":'+str(allNonCachedRequest)+',"totaltraffic":'+str(allTraffic)+',"cachedtraffic":'+str(allCachedTraffic)+',"noncachedtraffic":'+str(allNonCachedTraffic)+'}'
            #listRequestTraffic.append(total_)
            filename = "/var/log/cdnstat/cdnstat-requestbandwidth.json"
            writefile(listRequestTraffic,filename)
    except:
        pass


def responseCode(timenow):  
    try:
        arrayResponseCode= esQuery.codeResponse(timenow)
        if len(arrayResponseCode)>0:
            listResponseCode=[]
            #All
            #allcode2xx=0
            #allcode3xx=0
            #allcode4xx=0
            #allcode5xx=0
            #
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
		#allcode2xx = allcode2xx+code2xx
		#allcode3xx = allcode3xx+code3xx
		#allcode4xx = allcode4xx+code4xx
		#allcode5xx = allcode5xx+code5xx
		#
                stringJson='{"timecheck":'+str(timenow/1000+240)+',"hostname":"' +hostname+'","code2xx":'+str(int(code2xx/5))+',"code3xx":'+str(int(code3xx/5))+',"code4xx":'+str(int(code4xx/5))+',"code5xx":'+str(int(code5xx/5))+'}'
                listResponseCode.append(stringJson)
            #total_ = '{"timecheck":'+str(timenow/1000+240)+',"hostname":"all_host_cdn",'+ '"code2xx":'+str(int(allcode2xx/5))+',"code3xx":'+str(int(allcode3xx/5))+',"code4xx":'+str(int(allcode4xx/5))+',"code5xx":'+str(int(allcode5xx/5))+'}'
            #listResponseCode.append(total_)
            #
            filename = "/var/log/cdnstat/cdnstat-httpheader.json"
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
            filename = "/var/log/cdnstat/cdnstat-geoip.json"
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
            filename = "/var/log/cdnstat/cdnstat-isp.json"
            writefile(listRequestTimeIsp,filename)
    except:
        pass

def statBwCustomer(timenow):
    try:
        arrayBwCustomer= esQuery.bwCustomer(timenow)
        print len(arrayBwCustomer)
        if len(arrayBwCustomer)>0:
            liststatBwCustomer=[]
            for i in range(0, len(arrayBwCustomer)):
                if arrayBwCustomer[i]["10"]["buckets"][0]["doc_count"] >5:
                    dictBwCustomer={}
                    dictBwCustomer["timecheck"] = timenow/1000
                    dictBwCustomer["customer_isp"] = arrayBwCustomer[i]["key"]
                    ave_bytes= arrayBwCustomer[i]["1"]["value"]
                    ave_request_time = arrayBwCustomer[i]["10"]["buckets"][0]["5"]["value"]
                    dictBwCustomer["group_name"] = arrayBwCustomer[i]["10"]["buckets"][0]["key"]
                    dictBwCustomer["doc_count"] = arrayBwCustomer[i]["10"]["buckets"][0]["doc_count"]
                    # bandwith bit/second
                    dictBwCustomer["bandwith"] = int(ave_bytes *8000 / (ave_request_time*1000000))
                    jsonBwCustomer =str(json.dumps(dictBwCustomer))
                    if dictBwCustomer["bandwith"] <2000:
                        liststatBwCustomer.append(jsonBwCustomer)
            filename = "/var/log/cdnstat/cdnstat-statBwCustomer.json"
            writefile(liststatBwCustomer,filename)
    except:
        pass 

if __name__ == '__main__':
    #TEST
    #for j in range(0,8000000):
    #    timenow = 1497052800000+j*60000
    #    request_traffic(timenow)
    #    hostnameCountIP(timenow)
    #    responseCode(timenow)
    #    locationGeo(timenow)
    #    requestTimeIsp(timenow)
    # REAL
    epoch_time = int(time.time()/60)*60000 - 240000
    hostnameCountIP(epoch_time)
    request_traffic(epoch_time)
    responseCode(epoch_time)
    locationGeo(epoch_time)
    requestTimeIsp(epoch_time)
    timenow =int(time.time())*1000
    #statBwCustomer(timenow)
