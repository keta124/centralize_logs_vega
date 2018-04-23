#!/bin/bash
file="/opt/workerEs-WarmHot/listindexDelete"
while IFS= read line
do
        # display $line or do somthing with $line
	echo "$line"
        curl -XDELETE localhost:9200/$line
done <"$file"
