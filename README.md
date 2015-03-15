# scltests
Simple tests designed to keep up with regressions in scl-utils

How to run **scltests**?  
First, you have to meet the requirements, you have to have `python-click`, `PyYAML`, `mock`, and `colour_runner` (which is not yet packaged for fedora) installed.
Also user under which you will run these tests must be in user group `mock`

```
> $ ./run-tests.py --help
Usage: run-tests.py [OPTIONS] SCLS CFGS

  Run tests for given software collections SCLS and mock configs CFGS. SCLS
  and CFGS accepts multiple values in format scl1:scl2:scl3 or
  cfg1:cfg2:cfg3 where sclX is name of software collection from order.yaml
  file and cfgX is name of mock config without .cfg suffix.

Options:
  --local-scl PATH  Provide path to folder which contains scl-utils
                    repository.
  --help            Show this message and exit.
```

