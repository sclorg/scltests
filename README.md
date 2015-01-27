# scltests
Simple tests designed to keep up with regressions in scl-utils

How to run **scltests**?  
First, you have to meet the requirements, you have to have `python-decorator`, `mock` and `pytest` installed. Also user
under which you will run these tests must be in user group `mock`

1. `git clone git@github.com:sclorg/scltests.git && cd scltests`
2. `py.test -v -r s`  
(`-v` is verbose mode `-r s` means report skipped tests)
