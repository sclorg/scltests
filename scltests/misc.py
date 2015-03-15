import functools
try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest
import itertools
import os
import subprocess
import sys
import yaml

from decorator import decorator
import pytest

from scltests import cfg, settings
from scltests.collection import Collection

#TODO change file locations of those functions according the usage

PY3 = sys.version_info.major == 3

def createrepo(path):
    """Creates or updates repository at given full path."""
    code = subprocess.call(['createrepo', path])
    return code

def rename_logs(path, result_dir):
    """Append name before every log in result dir."""
    name = os.path.basename(path)
    name.replace('src.rpm', '')
    for log in settings.LOGS:
        os.rename('{0}/{1}'.format(result_dir, log), '{0}/{1}-{2}'.format(result_dir, name, log))

def get_build_order():
    """
    Returns order of building as defined in order.yaml
    """
    with open(settings.ORDER, 'r') as f:
        order = yaml.load(f)
    return order['order']

def get_mock_configs():
    """
    Returns all mock configs.
    """
    cfgs = os.listdir(settings.CONFIG_DIR)
    return [cfg.rstrip('.cfg') for cfg in cfgs if cfg not in settings.MOCK_CFG_FILES]

def build_all():
    """
    Combine mock configs with collections to create iterable build order in format
    [[mock_config, collection_name]].
    """
    return list(itertools.product(get_mock_configs(), get_build_order()))

def prepare(config_name, local_scl):
    mock_config = cfg.MockConfig(config_name, local_scl)
    mock_config.save()
    return mock_config

def rpm_proc(rpm_path, **kw):
    proc = subprocess.Popen(['rpm', '-qp{0}'.format(kw.get('option', '')), rpm_path, '--{0}'.format(kw.get('long_option', ''))], stdout=subprocess.PIPE)
    msg = proc.stdout.read().decode('utf-8')
    return msg.strip().split('\n')

def rpms_to_parametrized(): # TODO get rid of this and think of something smarter
    """
    Parametrization of pytest test functions accepts only global variables.
    So I use this awkward looking function to get built (iterable) rpms as global variable.
    [{collection1:rpm1, collection2:rpm1}, {collection1:rpm2, collection2:rpm2}]
    Test functions iterates over this list and access tested rpms by its collection name.
    """
    scls = get_build_order()
    test_rpms = [Collection(scl)['rpms']['arch'] + Collection(scl)['rpms']['noarch'] for scl in scls]
    ziped_rpms = izip_longest(*test_rpms)
    return [dict(zip(scls, rpms)) for rpms in ziped_rpms]
