# yandere_Crawler
## A yande.re crawler. 
### Multi-Threading, Python 2.7 only, LAME...
- yandere_index.py - Fetch all pictures that are newer than the number in the first line.
- yandere_tag.py - Fetch all pictures from a specific tag(e.g. mogu).
- yandere_errlog.py - Retry fetching all pictures from errlog.txt that was created from yandere_index.py
- config.py - Configurations

### Install & Config
1. Git clone or download the zip file, unzip.
2. Edit config.py, change the paths (or just leave it there...). Set allow_exp to 'False' to avoid downloading explicit contents.
3. Edit yandere_index.py, change the first line '#xxxxxx' to any number that you want to start crawling.(make it 1 if you want to download from the very beginning...)
4. On Windows, double-click the .py file and enjoy! On Linux, './yandere_xxx.py' in terminal(dah...).

### Issues
1. (Fixed)Some of the pictures can't be downloaded due to the invalid character (<>/\|:"*?).
2. Can't download more than 200 pictures in a single session.
3. ...
