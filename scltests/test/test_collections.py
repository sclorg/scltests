import copy
import itertools
import pytest

from scltests.test.conftest import TestCollectionsCore, checkdecorator
from scltests.misc import get_build_order, rpm_proc, rpms_to_parametrized





class TestCollections(TestCollectionsCore):


    def test_collection_was_built(self):
        assert self.collection.built

    def test_rpms_count(self):
        assert len(self.expected_rpms) == len(self.actual_rpms)

    def test_rpms_redudant(self):
        redudant_from_expected = set(self.expected_rpms) - set(self.actual_rpms)
        redudant_from_actual = set(self.actual_rpms) - set(self.expected_rpms)
        assert not (redudant_from_expected or redudant_from_actual), \
            "{0} package(s) wasn't built. Packages which were built and \
            are redudant: {1}.".format(redudant_from_expected or 'None', redudant_from_actual or 'None')

    def test_scl_runtime_has_man_folders(self, runtime_path):
        expected_man_folders = self.scl.man_folders
        actual_folders = rpm_proc(runtime_path, option='l')
        redudant = set(expected_man_folders) - set(actual_folders)
        assert not redudant, "Following man folders/files are missing: {0}".format(redudant)

    def test_scl_runtime_has_local_folders(self, runtime_path):
        expected_locals = self.scl.locale_folders
        actual_folders = rpm_proc(runtime_path, option='l')
        redudant = set(expected_locals) - set(actual_folders)
        assert not redudant, "Following locale folders/files are missing: {0}".format(redudant)

    def test_scl_runtime_has_important_folders(self, runtime_path):
        expected_imp_folders = self.scl.imp_folders
        actual_folders = rpm_proc(runtime_path, option='l')
        redudant = set(expected_imp_folders) - set(actual_folders)
        assert not redudant, "Following important folders/files are missing: {0}".format(redudant)
    
    @pytest.mark.parametrize('rpms', rpms_to_parametrized())
    @checkdecorator('list')
    def test_qpl_rpms(self, rpms, macros):
        rpm = rpms.get(self.scl.name)
        _, abs_path_rpm = self.collection.rpms_dict.get(rpm)
        expected_values = self.scl['list'][rpm].get('has', [])
        expected_values = [value.format(**macros) for value in expected_values]  # TODO map function
        actual_values = rpm_proc(abs_path_rpm, option='l')
        
        redudant = set(expected_values) - set(actual_values)
        assert not redudant

        not_expected = self.scl['list'][rpm].get('not', [])
        assert not set(not_expected).intersection(set(actual_values))

    @pytest.mark.parametrize('rpms', rpms_to_parametrized())
    @checkdecorator('provides')
    def test_provides_of_rpms(self, rpms, macros):
        rpm = rpms.get(self.scl.name)
        _, abs_path_rpm = self.collection.rpms_dict.get(rpm)
        expected_values = self.scl['provides'][rpm].get('has', [])
        expected_values = [value.format(**macros) for value in expected_values]

        actual_values = rpm_proc(abs_path_rpm, long_option='--provides')
        redudant = set(expected_values) - set(actual_values)
        assert not redudant

        not_expected = self.scl['provides'][rpm].get('not', [])
        assert not set(not_expected).intersection(set(actual_values))



