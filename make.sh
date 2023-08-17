#!/bin/sh
pip install pyinstaller
pip install -r requirements.txt

mkdir -p ./resources/assets && cd ./resources/assets
wget -N https://github.com/sc0ty/subsync/releases/download/assets/dict-dut-tur.zip -O dict-dut-tur.zip && unzip dict-dut-tur.zip && rm -rf dict-dut-tur.zip
wget -N https://github.com/sc0ty/subsync/releases/download/assets/dict-eng-tur.zip -O dict-eng-tur.zip && unzip dict-eng-tur.zip && rm -rf dict-eng-tur.zip
wget -N https://github.com/sc0ty/subsync/releases/download/assets/dict-fre-tur.zip -O dict-fre-tur.zip && unzip dict-fre-tur.zip && rm -rf dict-fre-tur.zip
wget -N https://github.com/sc0ty/subsync/releases/download/assets/dict-ger-tur.zip -O dict-ger-tur.zip && unzip dict-ger-tur.zip && rm -rf dict-ger-tur.zip
wget -N https://github.com/sc0ty/subsync/releases/download/assets/dict-gre-tur.zip -O dict-gre-tur.zip && unzip dict-gre-tur.zip && rm -rf dict-gre-tur.zip
wget -N https://github.com/sc0ty/subsync/releases/download/assets/dict-pol-tur.zip -O dict-pol-tur.zip && unzip dict-pol-tur.zip && rm -rf dict-pol-tur.zip
wget -N https://github.com/sc0ty/subsync/releases/download/assets/speech-eng.zip -O speech-eng.zip && unzip speech-eng.zip && rm -rf speech-eng.zip

cd ../..
pyinstaller engine.spec