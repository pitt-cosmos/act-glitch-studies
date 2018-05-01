#!/bin/bash

ls /mnt/act6/actpol/data/season5/merlin/15022 | grep ar5 | cut -d'.' -f-3 | while read line
do
echo /mnt/act6/actpol/data/season5/merlin/15022/$line
done > s17_pa5_sublist.txt
