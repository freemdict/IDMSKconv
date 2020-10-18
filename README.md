IDMSKconv
=========
IDMSK dictionary converter

This script can extract resouces (text/audio/picture) from dictionary built with IDM-SK.

Tested dictionaries:
* LDOCE5
* OALD7
* Longman Phrasal Verbs 2e

### Changelog
Thanks to Superfan and https://github.com/hoverruan/IDMSKconv

#### 2020/10/18
- now requires python3+
- fix linux support (from https://github.com/hoverruan/IDMSKconv)
- add duplicate file support, will rename file if there is duplicates.

Test passed on Windows10 and Ubuntu18.04

Command line usage:

The script will iterate all sub-directories in dictionary dir.
If output dir or dictionary dir is not specified, the script will work in the current directory by default.
```
python IDMSKconv.py [Output dir] [Dictionary dir]
``` 
