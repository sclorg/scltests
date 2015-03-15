import unittest

import click

from scltests import build
from scltests.misc import rpm_proc, get_build_order, get_mock_configs


# define options for click commands
class SCLType(click.ParamType):

    def convert(self, value, param, ctx):
        expected_scl = get_build_order()
        expected_scl.append('all')
        actual_scl = value.split(':')
        if set(actual_scl) - set(expected_scl):
            self.fail('You must choose from following options: {}.'.format(expected_scl))
        return actual_scl


class CFGType(click.ParamType):

    def convert(self, value, param, ctx):
        expected_cfgs = get_mock_configs()
        expected_cfgs.append('all')
        actual_cfgs = value.split(':')
        if set(actual_cfgs) - set(expected_cfgs):
            self.fail('You must choose from following options: {}.'.format(expected_cfgs))
        return actual_cfgs


# make test stubs
def make_test_function(rpm_option, rpm):
    def test(self):
        if self.collection.rpms_dict.get(rpm) is None:
            raise unittest.SkipTest('{} not found.'.format(rpm))
        _, abs_path_rpm = self.collection.rpms_dict.get(rpm)
        expected_values = self.tests[rpm_option][rpm].get('has', [])
        expected_values = [value.format(**self.macros) for value in expected_values]
        actual_values = rpm_proc(abs_path_rpm, long_option=rpm_option)
        redudant = set(expected_values) - set(actual_values)
        self.assertFalse(redudant, msg='Missing: {}'.format(redudant))

        not_expected = self.tests[rpm_option][rpm].get('not', [])
        redudant = set(not_expected) - set(actual_values)
        self.assertFalse(redudant, msg='Redudant: {}'.format(redudant))
    return test


class DynamicClassBase(unittest.TestCase):
    longMessage = True


def create_run_order(scls, cfgs):
    run_order = {}
    for cfg in cfgs:
        run_order[cfg] = scls
    return run_order


@click.command()
@click.argument('scls', type=SCLType())
@click.argument('cfgs', type=CFGType())
@click.option('--local-scl', type=click.Path(exists=True, resolve_path=True), help='Provide path to folder which contains scl-utils repository.')
def main(scls, cfgs, local_scl):
    """
    Run tests for given software collections SCLS and mock configs CFGS.
    SCLS and CFGS accepts multiple values in format scl1:scl2:scl3
    or cfg1:cfg2:cfg3 where sclX is name of software collection from order.yaml
    file and cfgX is name of mock config without .cfg suffix.
    """
    run_order = create_run_order(scls, cfgs)
    make_tests(run_order, local_scl)


def make_tests(run_order, local_scl):
    suites = []
    for cfg, collections in run_order.items():
        for collection in collections:
            klassname = 'Test_{0}_{1}'.format(collection, cfg)
            suites.append(klassname)
            # build collection
            build_collection = build.BuildCollection(collection, cfg, local_scl)
            build_collection.build()
            # {object_name: object}
            klass_objects = {}
            # add test functions
            for option in build_collection.scl['tests']:
                for rpm in build_collection.scl['tests'][option]:
                    klass_objects['test_{0}_{1}'.format(option, rpm)] = make_test_function(option, rpm)
            # add other objects
            klass_objects['collection'] = build_collection
            klass_objects['tests'] = build_collection.scl.yaml_data['tests']
            macros = build_collection.scl.macros
            macros['dist'] = build_collection.mock_config.dist
            macros['arch'] = build_collection.mock_config['target_arch'].replace('_', '-')
            klass_objects['macros'] = macros
            globals()[klassname] = type(klassname, (DynamicClassBase,), klass_objects)

    from colour_runner import runner as clr_run
    loader = unittest.TestLoader()
    suites = [loader.loadTestsFromTestCase(globals()[suite]) for suite in suites]
    suites = unittest.TestSuite(suites)
    clr_run.ColourTextTestRunner(verbosity=2).run(suites)

if __name__ == '__main__':
    main()
