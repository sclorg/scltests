# scltests
Simple tests designed to keep up with regressions in scl-utils

How to run **scltests**?  
First, you have to meet the requirements, you have to have `python-click`, `PyYAML`, `mock`, `createrepo, `scl-utils-build` and `colour_runner` (which is not yet packaged for fedora therefore `pip install colour_runner` is needed, currently it is only optional dep for coloured output of tests) installed. Also user under which you will run these tests must be in user group `mock`

```
> $ ./run-tests.py --help
Usage: run-tests.py [OPTIONS] COMMAND [ARGS]...

  Scltests builds and tests your software collections according to your
  defined yaml config.

Options:
  -h, --help  Show this message and exit.

Commands:
  list  list available collections and mock configs
  test  build and test collection(s)



> $ ./run-tests.py test -h                                                                                
Usage: run-tests.py test [OPTIONS] SCLS CFGS

  Run tests for given software collections SCLS and mock configs CFGS.

Arguments:

  SCLS and CFGS accept multiple values in format foo1:foo2 where fooX is
  name of software collection or mock config (see list for available
  options). Is it possible also to use all as argument. Note: all:foo1
  specifies all available collections or configs except foo1.

Options:
  --local-scl PATH  Provide path to folder which contains scl-utils
                    repository.
  -h, --help        Show this message and exit.

```

