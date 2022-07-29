Google Takeout Flattener
========================

Flattens/combines split ZIP archives downloaded from [Google Takeout](https://google.com/takeout) into a single directory.

(This script could, most likely, be used to flatten any split ZIP files, but this was created for and tested against Google Takeout ZIPs, hence the name).

# Usage
```shell
pip3 install -r requirements.txt
python3 googletakeoutflattener.py [DIRECTORY_HOLDING_ZIPS] [OUTPUT_DIRECTORY] --log=[CRITICAL|ERROR|WARNING|INFO|DEBUG]
```

# Disclaimer
Not affiliated with Google in any way. Use script at your own risk.
