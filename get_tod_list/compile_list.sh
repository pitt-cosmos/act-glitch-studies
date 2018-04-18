#!/bin/bash

while read line; do
  while read tod; do
    echo $tod | awk '{print $1}' >> output.txt
  done < $line
done < lists.txt
