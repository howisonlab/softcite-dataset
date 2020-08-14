#!/bin/bash

for i in *.json; do
    if ! grep -qxFe "$i" files-json.txt; then
        echo "deleting: $i"
        rm "$i"
    fi
done
