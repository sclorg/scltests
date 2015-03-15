import os
import subprocess
import sys
import yaml

from scltests import settings

# TODO change file locations of those functions according the usage

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


def rpm_proc(rpm_path, **kw):
    proc = subprocess.Popen(['rpm', '-qp{0}'.format(kw.get('option', '')), rpm_path, '--{0}'.format(kw.get('long_option', ''))], stdout=subprocess.PIPE)
    msg = proc.stdout.read().decode('utf-8')
    return msg.strip().split('\n')
