'''
Created on Jul 21, 2017

@author: CrazyDiamond
'''
from elasticsearch import Elasticsearch

def queryEs(index_str, body_dict):
    try:
        es = Elasticsearch([{'host': '172.18.10.100', 'port': 9200}])
        response = es.search(index=index_str, body=body_dict)
        return response
    except:
        return ""
def uniqueCountClientIP(timenow):
    try:
        time5mago = timenow - 5*60*1000 + 1 
        body_ = {
            "size": 0,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": True
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [{
                                "range": {
                                    "time_write_log": {
                                        "gte": time5mago,
                                        "lte": timenow,
                                        "format": "epoch_millis"
                                    }
                                }
                            }],
                            "must_not": []
                        }
                    }
                }
            },
            "aggs": {
                "hostname": {
                    "terms": {
                        "field": "hostname.raw",
                        "size": 5000,
                        "order": {
                            "1": "desc"
                        }
                    },
                    "aggs": {
                        "1": {
                            "cardinality": {
                                "field": "client_ip.raw"
                            }
                        }
                    }
                }
            }
        }
        index_ = "cdnlog-*"
        response= queryEs(index_str=index_, body_dict=body_)
        return response["aggregations"]["hostname"]["buckets"]
    except:
        return []
        
def totalAndCached(timenow):
    try:
        time5mago = timenow - 5*60*1000 + 1 
        body_= {
            "size": 0,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": True
                            }
                    },
                    "filter": {
                        "bool": {
                            "must": [{
                                "range": {
                                    "time_write_log": {
                                        "gte": time5mago,
                                        "lte": timenow,
                                        "format": "epoch_millis"
                                    }
                                }
                            }],
                            "must_not": []
                        }
                    }
                }
            },
            "aggs": {
                "hostname": {
                    "terms": {
                        "field": "hostname.raw",
                        "size": 5000,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "1": {
                            "sum": {
                                "field": "bytes"
                            }
                        },
                        "3": {
                            "filters": {
                                "filters": {
                                    "hitmiss": {
                                        "query": {
                                            "query_string": {
                                                "query": "hitmiss:\"HIT\" or \"hit\"",
                                                "analyze_wildcard": True
                                            }
                                        }
                                    }
                                }
                            },
                            "aggs": {
                                "1": {
                                    "sum": {
                                        "field": "bytes"
                                    }
                                }
                            }
                        }
                    }                     
                }
            }
        }
        index_ = "cdnlog-*"
        response= queryEs(index_str=index_, body_dict=body_)
        return response["aggregations"]["hostname"]["buckets"]
    except:
        return []
 
def codeResponse(timenow):
    try:
        time5mago = timenow - 5*60*1000 + 1
        body_ = {
            "size": 0,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": True
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [{
                                "range": {
                                    "time_write_log": {
                                        "gte": time5mago,
                                        "lte": timenow,
                                        "format": "epoch_millis"
                                    }
                                }
                            }],
                            "must_not": []
                        }
                    }
                }
            },
            "aggs": {
                "hostname": {
                    "terms": {
                        "field": "hostname.raw",
                        "size": 5000,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "3": {
                            "terms": {
                                "field": "response",
                                "size": 500,
                                "order": {
                                    "_count": "desc"
                                }
                            }
                        }
                    }
                }
            }
        }
        index_ = "cdnlog-*"
        response= queryEs(index_str=index_, body_dict=body_)
        return response["aggregations"]["hostname"]["buckets"]
    except:
        return []       

def geoLocation(timenow):
    try:
        time5mago = timenow - 5*60*1000 + 1
        body_ ={
            "size": 0,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": True
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [{
                                "range": {
                                    "time_write_log": {
                                        "gte": time5mago,
                                        "lte": timenow,
                                        "format": "epoch_millis"
                                    }
                                }
                            }],
                            "must_not": []
                        }
                    }
                }
            },
            "aggs": {
                "hostname": {
                    "terms": {
                        "field": "hostname.raw",
                        "size": 1000,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "geoipcountrycode": {
                            "terms": {
                                "field": "geoip.country_code2.raw",
                                "size": 50,
                                "order": {
                                    "_count": "desc"
                                }
                            },
                            "aggs": {
                                "geoipcountryname": {
                                    "terms": {
                                        "field": "geoip.country_name.raw",
                                        "size": 50,
                                        "order": {
                                            "_count": "desc"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        index_ = "cdnlog-*"
        response= queryEs(index_str=index_, body_dict=body_)
        return response["aggregations"]["hostname"]["buckets"]
        
    except:
        return []
def ispRequestTime(timenow):
    try:
        time5mago = timenow - 5*60*1000+1
        body_ ={
            "size": 0,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "analyze_wildcard": True,
                            "query": "*"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [{
                                "range": {
                                    "time_write_log": {
                                        "gte": time5mago,
                                        "lte": timenow,
                                        "format": "epoch_millis"
                                    }
                                }
                            }],
                            "must_not": []
                        }
                    }
                }
            },
            "aggs": {
                "hostname": {
                    "terms": {
                        "field": "hostname.raw",
                        "size": 5000,
                        "order": {
                            "1": "desc"
                        }
                    },
                    "aggs": {
                        "1": {
                            "sum": {
                                "field": "bytes"
                            }
                        },
                        "customer_isp": {
                            "terms": {
                                "field": "customer_isp.raw",
                                "size": 500,
                                "order": {
                                    "1": "desc"
                                }
                            },
                            "aggs": {
                                "1": {
                                    "sum": {
                                        "field": "bytes" 
                                    }
                                },
                                "4": {
                                    "avg": {
                                        "field": "request_time"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        index_ = "cdnlog-*"
        response= queryEs(index_str=index_, body_dict=body_)
        return response["aggregations"]["hostname"]["buckets"]
    except:
        return []

def bwCustomer(timenow):
    try:
        time10mago = timenow - 10*60*1000
        #print time10mago
        #print timenow
        body_ = {
            "size": 0,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "url:\".ts\"",
                            "analyze_wildcard": True
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [{
                                "range": {
                                    "@timestamp": {
                                        "gte": time10mago,
                                        "lte": timenow,
                                        "format": "epoch_millis"
                                    }
                                }
                            }],
                            "must_not": []
                        }
                    }
                }
            },
            "aggs": {
                "6": {
                    "range": {
                        "field": "bytes",
                        "ranges": [{
                            "from": 1500000,
                            "to": 3000000
                            }
                        ],
                        "keyed": True
                    },
                    "aggs": {
                        "7": {
                            "range": {
                                "field": "request_time",
                                "ranges": [{
                                    "from": 6,
                                    "to": None
                                    }
                                ],
                                "keyed": True
                            },
                            "aggs": {
                                "8": {
                                    "terms": {
                                        "field": "customer_isp.raw",
                                        "size": 100,
                                        "order": {
                                            "1": "desc"
                                        }
                                    },
                                    "aggs": {
                                        "1": {
                                            "avg": {
                                                "field": "bytes"
                                            }
                                        },
                                        "10": {
                                            "terms": {
                                                "field": "group_name.raw",
                                                "size": 100,
                                                "order": {
                                                    "1": "desc"
                                                }
                                            },
                                            "aggs": {
                                                "1": {
                                                    "avg": {
                                                        "field": "bytes"
                                                    }
                                                },
                                                "5": {
                                                    "avg": {
                                                        "field": "request_time"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        index_ = "cdnlog-*"
        response= queryEs(index_str=index_, body_dict=body_)
        return response["aggregations"]["6"]["buckets"]["1500000.0-3000000.0"]["7"]["buckets"]["6.0-*"]["8"]["buckets"]
    except:
        pass 
