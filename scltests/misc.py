import logging
import os
import subprocess
import sys
import yaml

from scltests import settings

# TODO change file locations of those functions according the usage
logger = logging.getLogger(__name__)

PY3 = sys.version_info.major == 3


def createrepo(path):
    """Creates or updates repository at given full path."""
    with open('/dev/null', 'w') as devnull:
        code = subprocess.call(['createrepo', path], stdout=devnull)
    return code


def rename_logs(path, result_dir):
    """Append name before every log in result dir."""
    name = os.path.basename(path)
    name.replace('src.rpm', '')
    for log in settings.LOGS:
        new_name = '{0}/{1}-{2}'.format(result_dir, name, log)
        os.rename('{0}/{1}'.format(result_dir, log), new_name)
        logger.info('{0} log file renamed to {1}.'.format(log, new_name))


def get_build_order():
    """
    Returns order of building 
    """
    return os.listdir(settings.SRPMS_DIR)


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
