#!/bin/bash

file=$1

if [ ! -e "$file" ]; then
    echo "File $file does not exist"
    exit 1
else 
    echo "File exists"
fi
