#!/bin/bash
file="/opt/workerEs-WarmHot/listindexHotWarm"
while IFS= read line
do
        # display $line or do somthing with $line
	echo "$line"
	a="localhost:9200/$line/_settings"
	echo $a
        curl -XPUT $a -d '{"index.routing.allocation.require.box_type" : "warm"}' 
done <"$file"
