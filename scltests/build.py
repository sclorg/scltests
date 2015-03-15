import collections
import os
import re
import subprocess
import sys

from scltests import collection, settings
from scltests.misc import createrepo, prepare, rename_logs


class BuildCollection(object):

    dep_config = None

    def __init__(self, scl_name, config_name, local_scl):
        if BuildCollection.dep_config:
            self._mock_config = BuildCollection.dep_config
            BuildCollection.dep_config = None
        self.config_name = config_name
        self.scl_name = scl_name
        self.built = False
        self.local_scl = local_scl
        self._srpms = []

    @property
    def mock_config(self):
        if not hasattr(self, '_mock_config'):
            self._mock_config = prepare(self.config_name, self.local_scl)
            createrepo(self._mock_config.result_dir)
        return self._mock_config

    @property
    def scl(self):
        if not hasattr(self, '_scl'):
            self._scl = collection.Collection(self.scl_name)
        return self._scl

    @property
    def rpms(self):
        """
        Returns list of built rpms.
        """
        if self.built:
            dir_content = os.listdir(self.mock_config.result_dir)
            return [f for f in dir_content if re.search("^{0}.*(?<!src)\.rpm$".format(self.scl_name), f)]
        return []

    @property
    def rpms_dict(self):
        """
        Returns dictionary consisting of built rpms in format:
        {rpm_stripped_of_arch_and_dist: (rpm, full_path_to_rpm)}
        {foo-2.7-1: (foo-2.7-1.f19.noarch.rpm, /path/to/foo-2.7-1.f19.noarch.rpm)}
        """
        if not hasattr(self, '_rpms_dict'):
            rpm_info = collections.namedtuple('rpm_info', 'rpm rpm_path')
            self._rpms_dict = {self.rpm_strip(rpm): rpm_info(rpm, self.rpm_path(rpm)) for rpm in self.rpms}
        return self._rpms_dict

    def rpm_strip(self, package):
        """
        Strip information about arch and dist from rpm name.
        foo-2.7-1.f19.noarch.rpm -> foo-2.7-1
        """
        arch = self.mock_config['target_arch']
        if '.noarch.' in package:
            arch = 'noarch'
        return package.replace('.{0}.{1}.rpm'.format(self.mock_config.dist, arch), '')

    def rpm_path(self, package):
        """
        Returns full path to given package.
        """
        return os.path.join(self.mock_config.result_dir, package)

    def _build_rpm(self, path_to_specfile):
        """
        Build single srpm with mock.
        """
        path_to_srpm = self.make_srpm(path_to_specfile)
        with open('/dev/null', 'w') as devnull:
            code = subprocess.call(['mock', '-r', self.mock_config.name, '--configdir',
                                    self.mock_config.config_dir, '--resultdir', self.mock_config.result_dir,
                                    path_to_srpm], stdout=devnull)
        if not code:
            createrepo(self.mock_config.result_dir)
        rename_logs(path_to_srpm, self.mock_config.result_dir)
        return code

    def make_srpm(self, specfile):
        """
        Create srpm from specfile in SRPMS folder.
        """
        scl_dir = '{0}/{1}'.format(settings.SRPMS_DIR, self.scl_name)

        msg = subprocess.check_output(['rpmbuild',
                                       '--define', '_sourcedir {0}'.format(scl_dir),
                                       '--define', '_builddir {0}'.format(scl_dir),
                                       '--define', '_srcrpmdir {0}'.format(scl_dir),
                                       '--define', '_rpmdir {0}'.format(scl_dir),
                                       '-bs', specfile])
        srpm = re.search(r'\/.*\.rpm', msg.strip().decode('utf-8')).group()
        self._srpms.append(srpm)
        return srpm

    def delete_srpms(self):
        for srpm in self._srpms:
            os.remove(srpm)

    def build(self):
        """
        Build whole collection.
        Metapackage is built as first. Metapackage and build order is defined
        in the yaml file of collection.
        """
        try:
            meta_return_code = self._build_rpm(self.scl.meta)
            if meta_return_code:
                sys.exit('ERROR: Metapackage wasn\'t built, exiting.')
            self.mock_config.edit_opt('chroot_setup_cmd', ' {0}-build'.format(self.scl.name))
            for package in self.scl.packages:
                self._build_rpm(package)
            if self.scl.dependant:
                BuildCollection.dep_config = self.mock_config
            self.built = True
        except KeyboardInterrupt:
            self.built = False
            raise
        finally:
            self.mock_config.reset()
            self.delete_srpms()
