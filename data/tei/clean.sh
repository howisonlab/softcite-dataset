#!/bin/bash

for i in *.tei.xml; do
    if ! grep -qxFe "$i" files-xml.txt; then
        echo "deleting: $i"
        rm "$i"
    fi
done
