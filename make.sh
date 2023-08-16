#!/bin/sh

pip install pyinstaller

pip install -r requirements.txt

pyinstaller --onefile --add-binary "resources/libs/*.so*:." --add-data "resources/key.pub:." --add-data "resources/subsync:resources/subsync" --add-data "resources/tools:resources/tools" --collect-all babelfish --collect-all guessit main.py