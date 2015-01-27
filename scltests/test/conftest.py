import copy
import functools
import itertools

import pytest

from scltests import build
from scltests.misc import build_all, PY3, rpm_proc, rpms_to_parametrized

from decorator import decorator

if not PY3:
    filter = itertools.ifilter



@pytest.fixture(params=build_all(), scope='session', autouse=True)
def collection(request):
    collection = build.BuildCollection(request.param[1], request.param[0])
    collection.build()
    return collection


class TestCollectionsCore(object):

    @pytest.fixture(autouse=True)
    def set_up(self, collection):
        self.yaml = collection.scl.yaml_data
        self.scl = collection.scl
        self.dist = collection.mock_config.dist
        self.arch = collection.mock_config['target_arch']
        self.actual_rpms = collection.rpms
        arch_rpms = ['{0}.{1}.{2}.rpm'.format(rpm, self.dist, self.arch).format(scl=self.scl.name) 
            for rpm in self.yaml['rpms']['arch']]
        noarch_rpms = ['{0}.{1}.{2}.rpm'.format(rpm, self.dist, 'noarch').format(scl=self.scl.name)
            for rpm in self.yaml['rpms']['noarch']]
        self.expected_rpms = copy.copy(arch_rpms + noarch_rpms)
        self.collection = collection

    @pytest.fixture()
    def runtime_path(self):
        sub = '{0}-runtime'.format(self.collection.scl_name)
        rpm = next(filter(lambda x: x.startswith(sub), self.actual_rpms))
        runtime_path = self.collection.rpm_path(rpm)
        return runtime_path

    @pytest.fixture()
    def macros(self):
        macros = self.scl.macros
        macros['dist'] = self.dist
        macros['arch'] = self.arch.replace('_', '-')
        return macros


class checkdecorator(object):

    def __init__(self, option):
        self.option = option

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(fn, fn_self, *args):
            test_option_values = fn_self.yaml.get(self.option, None)

            if not test_option_values:
                pytest.skip('Skipping because {0}.yaml does not contain test values for option: {1}'.format(fn_self.scl.name, self.option))
            
            tested_rpm = args[0].get(fn_self.scl.name)

            value = fn_self.yaml.get(self.option).get(tested_rpm)

            if value is None:
                pytest.skip('Skipping because {0} package is not listed in tested option: {1}.'.format(tested_rpm, self.option))

            if tested_rpm is None:
                pytest.skip('Skipping None rpm.')

            if tested_rpm not in fn_self.collection.rpms_dict:
                pytest.skip('Skipping {0} package as it is not in built packages.'.format(tested_rpm))

            return fn(fn_self, *args)
        return decorator(wrapper, fn)
