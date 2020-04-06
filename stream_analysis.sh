#!/bin/sh
#echo $1 $2 >> /home/raiy/Desktop/face_test/args.txt  # Check if this script is called

VideoName=${2}$(date +'-%d-%b-%y-%T')'.flv'
InputPath='rtmp://localhost:1935/go/'             #InputPath='/var/www/'${1}'/'
dirPath='/home/raiy/Desktop/face_test'   # Path of current directory
OutputPath='/results'

sleep 4s   # Leave some time from streaming to have at least small fragment

#!/usr/bin/python3
#python3 $dirPath/face_extract.py $InputPath${1}'/' ${2}$(date +'-%d-%b-%y-%T')'.flv' $dirPath$OutputPath'/'
python3 $dirPath/face_extract.py $InputPath $VideoName $dirPath$OutputPath'/'
