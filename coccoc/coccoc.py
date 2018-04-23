from elasticsearch import Elasticsearch
import time
import datetime
import sys
import json
HOSTNAME =["qc-static.coccoc.com",
  "qc-static2.coccoc.com",
  "nt-cdn.coccoc.com",
  "coccoc-video-static",
  "cdn2.coccoc.com",
  "cdn2.cache.vn",
  "shop-cdn.coccoc.com",
  "cdn1.rungrinh.vn"]
def queryEs(index_str, body_dict):
    try:
        es = Elasticsearch([{'host': '172.18.10.100', 'port': 9200}])
        response = es.search(index=index_str, body=body_dict)
        return response
    except:
        return ""
def coccoc_response(host):
  try:
    query = 'hostname:"'+host+'"'
    body_ = {
      "size": 0,
      "query": {
        "filtered": {
          "query": {
            "query_string": {
              "query": query,
              "analyze_wildcard": True
            }
          },
          "filter": {
            "range": {
              "time_write_log": {
                "gte": "now-4m",
                "lte": "now-1m",
                "format": "epoch_millis"
              }
            }
          }
        }
      },
      "aggs": {
        "response": {
          "terms": {
            "field": "response",
            "size": 50,
            "order": {
              "_count": "desc"
            }
          }
        }
      }
    }
    index_ = "cdnlog-*"
    response= queryEs(index_str=index_, body_dict=body_)
    code = response["aggregations"]["response"]["buckets"]
    coccoc =  dict(map(lambda x: (str(x["key"]), (int(x["doc_count"]+5)/3)),code))
    if len(coccoc) >0:
      return coccoc
  except:
    return None
if __name__ == '__main__':
  cc = {}
  write = {}
  for host in HOSTNAME:
    resource = coccoc_response(host)
    if resource :
      cc[host] = resource
  write["resource"] =  cc
  write["timestamp"] = int(time.time())
  # with open("coccoc.json", "w") as f:
  with open("/opt/coccoc/output/e0a9420584bb3f4712ddc6e8215eab1b-coccoc.json", "w") as f:
    f.write(json.dumps(write))
  f.close()
