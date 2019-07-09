#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH"

if [ ! -d "./data/zips" ] ; then
  mkdir -p ./data/zips
fi
cd ./data/zips

ZIPNAME="Dataset 1a Development_train.zip"
UNZIPPATH="../"
if [ ! -f "./$ZIPNAME" ] ; then
        echo -e "Downloading $ZIPNAME [35.3 GB]"
        wget -c -O "$ZIPNAME" https://zenodo.org/record/1470797/files/Dataset%201a%20Development_train.zip?download=1
        
        echo -e "\nUnzipping dataset"
        unzip "$ZIPNAME" -d "$UNZIPPATH"
fi

ZIPNAME="Dataset 1b Development_validation.zip"
UNZIPPATH="../"
if [ ! -f "./$ZIPNAME" ] ; then
        echo -e "Downloading $ZIPNAME [3.9 GB]"
        wget -c -O "$ZIPNAME" https://zenodo.org/record/1470797/files/Dataset%201b%20Development_validation.zip?download=1
        
        echo -e "\nUnzipping dataset"
        unzip "$ZIPNAME" -d "$UNZIPPATH"
fi

ZIPNAME="Dataset 2 Hold-out.zip"
UNZIPPATH="../"
if [ ! -f "./$ZIPNAME" ] ; then
        echo -e "Downloading $ZIPNAME [41.2 GB]"
        wget -c -O "$ZIPNAME" https://zenodo.org/record/1470797/files/Dataset%202%20Hold-out.zip?download=1
        
        echo -e "\nUnzipping dataset"
        unzip "$ZIPNAME" -d "$UNZIPPATH"
fi

ZIPNAME="Dataset 3 CERAD-like hold-out.zip"
UNZIPPATH="../"
if [ ! -f "./$ZIPNAME" ] ; then
        echo -e "Downloading $ZIPNAME [26.3 GB]"
        wget -c -O "$ZIPNAME" https://zenodo.org/record/1470797/files/Dataset%203%20CERAD-like%20hold-out.zip?download=1
        
        echo -e "\nUnzipping dataset"
        unzip "$ZIPNAME" -d "$UNZIPPATH"
fi

ZIPNAME="Tiles.zip"
UNZIPPATH="../"
if [ ! -f "./$ZIPNAME" ] ; then
        echo -e "Downloading $ZIPNAME [3.3 GB]"
        wget -c -O "$ZIPNAME" https://zenodo.org/record/1470797/files/Tiles.zip?download=1
        
        echo -e "\nUnzipping dataset"
        unzip "$ZIPNAME" -d "$UNZIPPATH"
fi

echo -e "Finish downloading neuropathology dataset"
