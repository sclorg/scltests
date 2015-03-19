#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        if 'all' in actual_scl:
            actual_scl = list(set(expected_scl) - set(actual_scl))
        if set(actual_scl) - set(expected_scl):
            self.fail(u'You must choose from following options: {0}.'.format(expected_scl))
        if not actual_scl:
            self.fail(u'¯\_(ツ)_/¯ You\'ve tried to be too smart and you end up with nothing to build.')
        return actual_scl


class CFGType(click.ParamType):

    def convert(self, value, param, ctx):
        expected_cfgs = get_mock_configs()
        expected_cfgs.append('all')
        actual_cfgs = value.split(':')
        if 'all' in actual_cfgs:
            actual_cfgs = list(set(expected_cfgs) - set(actual_cfgs))
        if set(actual_cfgs) - set(expected_cfgs):
            self.fail(u'You must choose from following options: {0}.'.format(expected_cfgs))
        if not actual_cfgs:
            self.fail(u'¯\_(ツ)_/¯ You\'ve tried to be too smart and you end up with nothing to build with.')
        return actual_cfgs

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# make test stubs
def make_test_function(rpm_option, rpm):
    def test(self):
        if self.collection.rpms_dict.get(rpm) is None:
            raise unittest.SkipTest('Package {0}  wasnt build.'.format(rpm))
        _, abs_path_rpm = self.collection.rpms_dict.get(rpm)
        expected_values = self.tests[rpm_option][rpm].get('has', [])
        expected_values = [value.format(**self.macros) for value in expected_values]
        actual_values = rpm_proc(abs_path_rpm, long_option=rpm_option)
        redudant = list(set(expected_values) - set(actual_values))
        self.assertFalse(redudant, msg='Following expected values wasnt found: {}'.format(redudant))

        not_expected = self.tests[rpm_option][rpm].get('not', [])
        redudant = list(set(not_expected) - set(actual_values))
        self.assertFalse(redudant, msg='Unexpected values was found: {}'.format(redudant))
    return test


class DynamicClassBase(unittest.TestCase):
    longMessage = True


def create_run_order(scls, cfgs):
    run_order = {}
    for cfg in cfgs:
        run_order[cfg] = scls
    return run_order


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Scltests builds and tests your software collections according to your defined
    yaml config.
    """
    pass


@cli.command('list', short_help='list available collections and mock configs')
def list_cmd():
    """
    List available collections and mock configs.
    """
    click.echo()
    click.echo('Available software collections: {}'.format(':'.join(get_build_order())))
    click.echo('Available mock configs: {}'.format(':'.join(get_mock_configs())))


@cli.command('test', short_help='build and test collection(s)')
@click.argument('scls', type=SCLType())
@click.argument('cfgs', type=CFGType())
@click.option('--local-scl', type=click.Path(exists=True, resolve_path=True), help='Provide path to folder which contains scl-utils repository.')
def test_cmd(scls, cfgs, local_scl):
    """
    Run tests for given software collections SCLS and mock configs CFGS.

    \b
    \b\bArguments:
    SCLS and CFGS accept multiple values in format foo1:foo2 where fooX is name of
    software collection or mock config (see list for available options).
    Is it possible also to use all as argument.
    Note: all:foo1 specifies all available collections or configs except foo1.

    """
    run_order = create_run_order(scls, cfgs)
    make_tests(run_order, local_scl)


def make_tests(run_order, local_scl):
    suites = []
    for cfg, collections in run_order.items():
        for collection in collections:
            klassname = 'Test_{0}_{1}'.format(collection, cfg)
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
            # create test class
            suites.append(type(klassname, (DynamicClassBase,), klass_objects))

    # custom test runner for coloured unittest output
    try:
        from colour_runner.runner import ColourTextTestRunner as Runner
    except ImportError:
        from unittest import TextTestRunner as Runner
    # make test suite
    loader = unittest.TestLoader()
    suites = [loader.loadTestsFromTestCase(suite) for suite in suites]
    suites = unittest.TestSuite(suites)
    # run tests
    TextTestRunner(verbosity=2).run(suites)

if __name__ == '__main__':
    cli()
