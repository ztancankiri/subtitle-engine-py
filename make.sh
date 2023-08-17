#!/bin/sh
pip install pyinstaller
pip install -r requirements.txt

mkdir -p ./resources/subsync/assets && cd ./resources/subsync/assets
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-dut-tur.zip && unzip dict-dut-tur.zip && rm -rf dict-dut-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-eng-tur.zip && unzip dict-eng-tur.zip && rm -rf dict-eng-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-fre-tur.zip && unzip dict-fre-tur.zip && rm -rf dict-fre-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-ger-tur.zip && unzip dict-ger-tur.zip && rm -rf dict-ger-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-gre-tur.zip && unzip dict-gre-tur.zip && rm -rf dict-gre-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-kur-tur.zip && unzip dict-kur-tur.zip && rm -rf dict-kur-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/dict-pol-tur.zip && unzip dict-pol-tur.zip && rm -rf dict-pol-tur.zip
wget https://github.com/sc0ty/subsync/releases/download/assets/speech-eng.zip && unzip speech-eng.zip && rm -rf speech-eng.zip

cd ../../..
pyinstaller --onefile --add-binary "resources/libs/*.so*:." --add-data "resources/key.pub:." --add-data "resources/subsync:resources/subsync" --add-data "resources/tools:resources/tools" --collect-all babelfish --collect-all guessit src/main.py