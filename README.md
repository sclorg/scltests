# scltests
Simple tests designed to keep up with regressions in scl-utils

How to run **scltests**?  
First, you have to meet the requirements, you have to have `python-click`, `PyYAML`, `mock`, and `colour_runner` (which is not yet packaged for fedora therefore `pip install colour_runner` is needed) installed. Also user under which you will run these tests must be in user group `mock`

```
> $ ./run-tests.py --help
Usage: run-tests.py [OPTIONS] SCLS CFGS

  Run tests for given software collections SCLS and mock configs CFGS. SCLS
  and CFGS accepts multiple values in format scl1:scl2:scl3 or
  cfg1:cfg2:cfg3 where sclX is name of software collection from order.yaml
  file and cfgX is name of mock config without .cfg suffix. You can also use
  all as parameter which means exactly what you would expect. all can be
  also chained with other values, e.g. all:python27 would mean -  build
  every collection except for python27, same applies for configs.


Options:
  --local-scl PATH  Provide path to folder which contains scl-utils
                    repository.
  --help            Show this message and exit.
```

