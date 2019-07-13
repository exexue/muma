#!/bin/bash

#echo "$1 $2 $3" >>/root/g.txt

rm -rf /root/Downloads/*.torrent
python3 /root/.aria2/g.py $2 "$3"
exit 0
