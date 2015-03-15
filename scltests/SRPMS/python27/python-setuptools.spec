%{?scl:%scl_package python-setuptools}
%{!?scl:%global pkg_name %{name}}

%global srcname setuptools

Name:           %{?scl_prefix}python-setuptools
Version:        0.9.8
Release:        2%{?dist}
Summary:        Easily build and distribute Python packages

Group:          Applications/System
License:        Python or ZPLv2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/d/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        psfl.txt
Source2:        zpl.txt
# Submitted upstream
# https://bitbucket.org/tarek/distribute/issue/363/skip-test_sdist_with_utf8_encoded_filename
Patch0: distribute-skip-sdist_with_utf8_encoded_filename.patch
# https://github.com/jaraco/setuptools/pull/2
# Fixes security issue: http://bugs.python.org/issue17997#msg194950
Patch1: setuptools-ssl-match_hostname-wildcard.patch
# Fixes easy_install throwing SSL error when behind HTTPS proxy
# https://bugzilla.redhat.com/show_bug.cgi?id=1085459
Patch2: restore-proxy-support-SSL-connection.patch

BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python2-devel
BuildRequires:  python2-devel

# Legacy: We removed this subpackage once easy_install no longer depended on
# python-devel
Provides: %{?scl_prefix}python-setuptools-devel = %{version}-%{release}
Obsoletes: %{?scl_prefix}python-setuptools-devel < 0.6.7-1

# Provide this since some people will request distribute by name
Provides: %{?scl_prefix}python-distribute = %{version}-%{release}

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

This package contains the distribute fork of setuptools.

%prep
%setup -q -n %{srcname}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

find -name '*.txt' -exec chmod -x \{\} \;
find . -name '*.orig' -exec rm \{\} \;

for file in setuptools/command/easy_install.py ; do
    sed -i '1s|^#!python|#!%{__python}|' $file
done

%build
%{?scl:scl enable %{scl} - << \EOF}
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%{?scl:EOF}

%install
rm -rf %{buildroot}

# explicitly specify where to install scripts and library files, since the SCL python is
#  only a mock python
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --skip-build --root %{buildroot} --install-purelib %{python_sitelib} --install-scripts %{_bindir}
%{?scl:"}

rm -rf %{buildroot}%{python_sitelib}/setuptools/tests

install -p -m 0644 %{SOURCE1} %{SOURCE2} .
find %{buildroot}%{python_sitelib} -name '*.exe' | xargs rm -f
chmod +x %{buildroot}%{python_sitelib}/setuptools/command/easy_install.py

%check
#%{?scl:scl enable %{scl} "}
#%{__python} setup.py test
#%{?scl:"}


%files
%defattr(-,root,root,-)
%doc *.txt docs
%{python_sitelib}/*
%{_bindir}/easy_install
%{_bindir}/easy_install-2.*

%changelog
* Thu Apr 10 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.9.8-2
- Add patch restoring proxy (tunnel) support in SSL connections
Resolves: rhbz#1085459

* Wed Nov 06 2013 Robert Kuska <rkuska@redhat.com> - 0.9.8-1
- Update setuptools to 0.9.8
- Add patches from f20

* Thu Aug 15 2013 Robert Kuska <rkuska@redhat.com> - 0.6.28-7
- Add SSL to easy_install resolves CVE-2013-1633 and CVE-2013-2099
- For more info related to these CVEs visit rhbz#994182
Resolves: rhbz#996705

* Mon May 20 2013 Robert Kuska <rkuska@redhat.com> - 0.6.28-6
- Fix rhbz #963675

* Tue May 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.28-5
- Rebuild to generate bytecode properly after fixing rhbz#956289

* Mon Sep 17 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.28-4
- Rebuilt for SCL.

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 0.6.28-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.6.28-2
- remove rhel logic from with_python3 conditional

* Mon Jul 23 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.28-1
- New upstream release:
  - python-3.3 fixes
  - honor umask when setuptools is used to install other modules

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.27-2
- Fix easy_install.py having a python3 shebang in the python2 package

* Thu Jun  7 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.27-1
- Upstream bugfix

* Tue May 15 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.24-2
- Upstream bugfix

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.24-1
- Upstream bugfix
- Compile the win32 launcher binary using mingw

* Sun Aug 21 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.21-1
- Upstream bugfix release

* Thu Jul 14 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.19-1
- Upstream bugfix release

* Tue Feb 22 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-7
- Switch to patch that I got in to upstream

* Tue Feb 22 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-6
- Fix build on python-3.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Tue Aug 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-3
- Update description to mention this is distribute

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-2
- bump for building against python 2.7

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-1
- update to new version
- all patches are upsteam

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.13-7
- generalize path of easy_install-2.6 and -3.1 to -2.* and -3.*

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.13-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 3 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-5
- Upstream patch for compatibility problem with setuptools
- Minor spec cleanups
- Provide python-distribute for those who see an import distribute and need
  to get the proper package.

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-4
- Fix race condition in unittests under the python-2.6.x on F-14.

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-3
- Fix few more buildroot macros

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-2
- Include data that's needed for running tests

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-1
- Update to upstream 0.6.13
- Minor specfile formatting fixes

* Thu Feb 04 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-3
- First build with python3 support enabled.
  
* Thu Jan 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-2
- Really disable the python3 portion

* Thu Jan 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-1
- Update the python3 portions but disable for now.
- Update to 0.6.10
- Remove %%pre scriptlet as the file has a different name than the old
  package's directory

* Tue Jan 26 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.9-4
- Fix install to make /usr/bin/easy_install the py2 version
- Don't need python3-tools since the library is now in the python3 package
- Few other changes to cleanup style

* Thu Jan 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.9-2
- add python3 subpackage

* Mon Dec 14 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.9-1
- New upstream bugfix release.

* Sun Dec 13 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.8-2
- Test rebuild

* Mon Nov 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.8-1
- Update to 0.6.8.
- Fix directory => file transition when updating from setuptools-0.6c9.

* Tue Nov 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.7-2
- Fix duplicate inclusion of files.
- Only Obsolete old versions of python-setuptools-devel

* Tue Nov 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.7-1
- Move easy_install back into the main package as the needed files have been
  moved from python-devel to the main python package.
- Update to 0.6.7 bugfix.

* Fri Oct 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.6-1
- Upstream bugfix release.

* Mon Oct 12 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.4-1
- First build from the distribute codebase -- distribute-0.6.4.
- Remove svn patch as upstream has chosen to go with an easier change for now.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6c9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c9-4
- Apply SVN-1.6 versioning patch (rhbz #511021)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6c9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
