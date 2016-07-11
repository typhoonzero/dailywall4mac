#!/usr/bin/env bash

PICTURE_DIR="$HOME/Pictures/bing-wallpapers/"

mkdir -p $PICTURE_DIR

urls=$(curl -s http://cn.bing.com | grep -Eo "url: \".*?\"")
    #sed -e "s/url:'\([^']*\)'.*/http:\/\/bing.com\1/" | \
    #sed -e "s/\\\//g") )
#echo "full: "${urls:6:4}
if [ "${urls:6:4}" == "http" ]; then
p2=$(echo $urls | sed -e "s/url: \"\([^']*\)\".*/\1/" | sed -e "s/\\\//g")
#echo "p2:" $p2
# download
filename=$(echo $p2|sed -e "s/.*\/\(.*\)/\1/")
#echo "file name: " $filename
if [ ! -f $PICTURE_DIR/$filename ]; then
#    echo "Downloading: $filename ..."
    curl -s -Lo "$PICTURE_DIR/$filename" $p2 > /dev/null
else
    echo "Skipping: $filename ..." > /dev/null
fi
fi 
