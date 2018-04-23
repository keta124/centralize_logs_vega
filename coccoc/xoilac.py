from elasticsearch import Elasticsearch
import time
import datetime
import sys
import json

HOSTNAME =["124a1b8c5.vws.vegacdn.vn"]
def query_es(index_str, body_dict):
  try:
    es = Elasticsearch([{'host': '172.18.10.100', 'port': 9200}])
    response = es.search(index=index_str, body=body_dict)
    return response
  except:
    return ""
def response(host):
  try:
    query = 'hostname:"' + host + '" OR hostname:"cdn2.xoilac.tv"'
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
                "gte": "now-16m",
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
    index_ = "cdnlog-vegacdn-*"
    response= query_es(index_str=index_, body_dict=body_)
    total = response["hits"]["total"]
    code = response["aggregations"]["response"]["buckets"]
    aggregations =  dict(map(lambda x: (str(x["key"]), int(x["doc_count"])),code))
    if len(aggregations) >0:
      not_define = total - reduce(lambda x,y: x + y , aggregations.values())
      if not_define >0:
        aggregations['not_define'] = not_define
      return aggregations
    else:
      if total >0:
        aggregations['not_define'] = total
        return aggregations
  except Exception as e:
    print e
    return None

def referer(host):
  try:
    query = 'hostname:"' + host + '" OR hostname:"cdn2.xoilac.tv"'
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
                "gte": "now-16m",
                "lte": "now-1m",
                "format": "epoch_millis"
              }
            }
          }
        }
      },
      "aggs": {
        "referer": {
          "terms": {
            "field": "referer.raw",
            "size": 500,
            "order": {
              "_count": "desc"
            }
          }
        }
      }
    }
    index_ = "cdnlog-vegacdn-*"
    response= query_es(index_str=index_, body_dict=body_)
    total = response["hits"]["total"]
    code = response["aggregations"]["referer"]["buckets"]
    aggregations =  dict(map(lambda x: (str(x["key"]), int(x["doc_count"])),code))
    if len(aggregations) >0:
      not_define = total - reduce(lambda x,y: x + y , aggregations.values())
      if not_define >0:
        aggregations['not_define'] = not_define
      return aggregations
    else:
      if total >0:
        aggregations['not_define'] = total
        return aggregations
  except Exception as e:
    print e
    return None

def user_agent(host):
  try:
    query = 'hostname:"' + host + '" OR hostname:"cdn2.xoilac.tv"'
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
                "gte": "now-16m",
                "lte": "now-1m",
                "format": "epoch_millis"
              }
            }
          }
        }
      },
      "aggs": {
        "user_agent": {
          "terms": {
            "field": "user_agent.raw",
            "size": 500,
            "order": {
              "_count": "desc"
            }
          }
        }
      }
    }
    index_ = "cdnlog-vegacdn-*"
    response= query_es(index_str=index_, body_dict=body_)
    total = response["hits"]["total"]
    code = response["aggregations"]["user_agent"]["buckets"]
    aggregations =  dict(map(lambda x: (str(x["key"]), int(x["doc_count"])),code))
    if len(aggregations) >0:
      not_define = total - reduce(lambda x,y: x + y , aggregations.values())
      if not_define >0:
        aggregations['not_define'] = not_define
      return aggregations
    else:
      if total >0:
        aggregations['not_define'] = total
        return aggregations
  except Exception as e:
    print e
    return None

if __name__ == '__main__':
  result_response = {}
  result_referer = {}
  result_user_agent = {}
  write = {}
  for host in HOSTNAME:
    resource = response(host)
    referer = referer(host)
    user_agent = user_agent(host)
    if resource :
      result_response["response"] = resource
    if referer:
      result_referer["referer"] = referer
    if user_agent:
      result_user_agent["user_agent"] = user_agent
  result_response["timestamp"] = int(time.time())
  result_referer["timestamp"] = int(time.time())
  result_user_agent["timestamp"] = int(time.time())
  with open("/opt/coccoc/output/077723671d588b9958caa55c7cbf7d88-xoilac-response.json", "w") as f:
    f.write(json.dumps(result_response))
  f.close()
  with open("/opt/coccoc/output/077723671d588b9958caa55c7cbf7d88-xoilac-referer.json", "w") as f:
    f.write(json.dumps(result_referer))
  f.close()
  with open("/opt/coccoc/output/077723671d588b9958caa55c7cbf7d88-xoilac-user_agent.json", "w") as f:
    f.write(json.dumps(result_user_agent))
  f.close()
