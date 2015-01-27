import itertools
import yaml

from scltests import settings



class Collection(object):
    def __init__(self, name):
        self.name = name

    def __getitem__(self, key):
        return self.yaml_data[key]

    @property
    def yaml_file(self):
        return '{0}/{1}.yaml'.format(settings.YAML_DIR, self.name)


    @property
    def yaml_data(self):
        if not hasattr(self, '_yaml_data'):
            with open(self.yaml_file, 'r') as f:
                self._yaml_data = yaml.load(f)
        return self._yaml_data

    @property
    def meta(self):
        return self._abs_path(self['meta'])

    @property
    def packages(self):
        return [self._abs_path(package) for package in self['packages']]

    @property
    def dependant(self):
        return self.yaml_data.get('dependant', False)

    def _abs_path(self, package_name):
        return '{0}/{1}/{2}'.format(settings.SRPMS_DIR, self.name, package_name)

    @property
    def man_folders(self):

        """There are like 13293 folders with man files in %%scl-runtime package so 
        instead of listing them in yaml files we will autogenerate them."""

        man_num = ['man0p', 'man1', 'man1p', 'man1x', 'man2', 'man2x', 'man3', \
                   'man3p', 'man3x', 'man4', 'man4x', 'man5', 'man5x', 'man6', \
                   'man6x', 'man7', 'man7x', 'man8', 'man8x', 'man9', 'man9x', 'mann']
        lang_folder = '/opt/rh/{0}/root/usr/share/man'.format(self.name)
        self._man_folders = ['/opt/rh/{0}/root/usr/local/share/man/{1}'.format(self.name, num) \
                             for num in man_num if 'p' not in num]
        self._man_folders.extend(['{0}/{1}'.format(lang_folder, num) for num in man_num])
        self._man_folders.extend(['/opt/rh/{0}/root/usr/share/locale/man'.format(self.name), \
                            '/opt/rh/{0}/root/usr/share/locale/man/LC_MESSAGES'.format(self.name), \
                            '/opt/rh/{0}/root/usr/local/share/man'.format(self.name), \
                            lang_folder])
        self._man_folders.extend(['{0}/{1}'.format(lang_folder, lang) for lang in settings.MAN_LNG])
        self._man_folders.extend(['{0}/{1}/{2}'.format(lang_folder, prd[0], prd[1]) \
                                  for prd in itertools.product(settings.MAN_LNG, man_num)])
        return self._man_folders

    @property
    def locale_folders(self):

        """There is also too many local folders for each language.
        Autogenerate them."""

        local_folder = '/opt/rh/{0}/root/usr/share/locale'.format(self.name)
        self._local_folders = [local_folder]
        local_lng = ['{0}/{1}'.format(local_folder, lng) for lng in settings.MAN_LNG]
        local_lng_msg = ['{0}/{1}'.format(l, 'LC_MESSAGES') for l in local_lng]
        self._local_folders.extend(local_lng)
        self._local_folders.extend(local_lng_msg)
        return self._local_folders

    @property
    def imp_folders(self):

        """Return important folders as defined in settings.py"""

        self._imp_folders = [fld.format(self.name) for fld in settings.IMP_FLDS]
        return self._imp_folders

    @property
    def macros(self):
        default = {macro: getattr(settings, macro).format(scl=self.name) 
                   for macro in settings.MACROS}
        user_defined = {k: v.format(scl=self.name) for k,v in 
                        self.yaml_data.get('macros', {}).items()}
        return dict(itertools.chain(default.items(), user_defined.items()))

    
    

