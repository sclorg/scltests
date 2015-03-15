try:
    import ConfigParser
    from StringIO import StringIO
except ImportError:
    import configparser as ConfigParser
    from io import StringIO

import io
import os

from scltests import settings


class MockConfig(object):
    config_dir = settings.CONFIG_DIR

    def __init__(self, name, local_scl=None):
        self.name = name
        self.local_scl = local_scl

    def __getitem__(self, key):
        return self.config_opts[key]

    @property
    def config_opts(self):
        if not hasattr(self, '_config_opts'):
            self._load_opts()
        return self._config_opts

    @property
    def default_opts(self):
        if not hasattr(self, '_default_opts'):
            self._load_opts()
        return self._default_opts

    @property
    def abs_path(self):
        return "{0}/{1}.cfg".format(settings.CONFIG_DIR, self.name)

    @property
    def result_dir(self):
        return "{0}/{1}".format(settings.RESULT_DIR, self.root)

    @property
    def dist(self):
        if self.config_opts['dist'] == 'rawhide':
            return 'fc{0}'.format(int(self.config_opts['releasever']) + 1)
        if self.config_opts['dist'].startswith('el'):
            return '{0}.centos'.format(self.config_opts['dist'])
        return self.config_opts['dist']

    def _add_exclude(self, package):
        # TODO maybe add option to define from which section we want to exclude package
        """
        Exclude package from repositories except for 'main', 'scltests'
        and 'localscl' repositories.
        Main would exclude package from all other repos.
        Scltests is our repo where we store built rpms.
        Localscl is optional repo defined by user.
        """

        yum_conf = self['yum.conf']
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(yum_conf))
        sections = config.sections()

        for section in ['main', 'scltests', 'localscl']:
            try:
                sections.remove(section)
            except ValueError:
                continue

        for section in sections:
            config.set(section, 'exclude', '{0}*'.format(package))

        new_yum_conf = None
        try:
            output = StringIO()
            config.write(output)
            new_yum_conf = output.getvalue()  # TODO try without exception definitely not safe
        finally:
            output.close()

        return new_yum_conf

    def _load_opts(self):
        config_opts = {}
        exec(compile(open(self.abs_path, "rb").read(), self.abs_path, 'exec'))
        self._config_opts = config_opts
        self._default_opts = self.config_opts.copy()
        self._change_chroot_name()
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)  # repo folder created
        if self.local_scl:
            self.edit_opt('yum.conf', self._add_exclude('scl-utils'), replace=True)
            self.edit_opt('yum.conf', settings.REPO.format(name='localscl', dir=self.local_scl))
        self.edit_opt('yum.conf', settings.REPO.format(name='scltests', dir=self.result_dir))

    def _save(self, default):
        # TODO how to handle saving opts?
        copy = self.default_opts if default else self.config_opts.copy()  # for the security bcs of pop
        with open(self.abs_path, 'w') as f:
            yum = copy['yum.conf']
            copy.pop('yum.conf')  # dict is random ordered but we want yum.conf to be last
            for key, value in copy.items():
                f.write('config_opts[{0}] = {1}\n'.format(repr(key), repr(value)))
            f.write("\nconfig_opts['yum.conf'] = '''{0}'''".format(yum))  # yum.conf is last yay

    def reset(self):
        self._save(default=True)

    def save(self):
        self._save(default=False)

    def edit_opt(self, key, value, replace=False):
        if replace:
            self.config_opts[key] = value
        else:
            self.config_opts[key] = self.config_opts[key]+value
        self.save()
        return self.config_opts[key]

    def _change_chroot_name(self):
        if not hasattr(self, 'epoch_time'):
            import time
            self.epoch_time = str(int(time.time()))
            self.root = self.edit_opt('root', '_'+self.epoch_time)
        return self.epoch_time


def prepare(config_name, local_scl):
    mock_config = MockConfig(config_name, local_scl)
    mock_config.save()
    return mock_config
