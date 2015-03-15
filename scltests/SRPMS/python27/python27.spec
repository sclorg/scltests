%global scl_name_base python
%global scl_name_version 27
%global scl %{scl_name_base}%{scl_name_version}

%scl_package %scl
%global _turn_off_bytecompile 1

%global install_scl 1

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary: Package that installs %scl
Name: %scl_name
Version: 1.1
Release: 17%{?dist}
License: GPLv2+
Source0: macros.additional.%{scl}
Source1: README
Source2: LICENSE
BuildRequires: help2man
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=857354
BuildRequires: iso-codes
BuildRequires: scl-utils-build
%if 0%{?install_scl}
Requires: %{scl_prefix}python
Requires: %{scl_prefix}python-jinja2
Requires: %{scl_prefix}python-nose
Requires: %{scl_prefix}python-pip
Requires: %{scl_prefix}python-simplejson
Requires: %{scl_prefix}python-setuptools
Requires: %{scl_prefix}python-sphinx
Requires: %{scl_prefix}python-sqlalchemy
Requires: %{scl_prefix}python-virtualenv
Requires: %{scl_prefix}python-wheel
Requires: %{scl_prefix}python-werkzeug
%endif

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -T -c

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .

%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
mkdir -p %{buildroot}%{_root_prefix}/lib/rpm/redhat
cat >> %{buildroot}%{_scl_scripts}/%{scl} << EOF
#Module1.0
prepend-path    X_SCLS              %{scl}
prepend-path    PATH                %{_bindir}
prepend-path    LD_LIBRARY_PATH     %{_libdir}
prepend-path    MANPATH             %{_mandir}
prepend-path    PKG_CONFIG_PATH     %{_libdir}/pkgconfig
prepend-path    XDG_DATA_DIRS       %{_datadir}
EOF
#automaticaly create enable script for compatibility
%scl_enable_script
%scl_install

# Add the aditional macros to macros.%%{scl}-config
cat %{SOURCE0} >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config
sed -i 's|@scl@|%{scl}|g' %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

# Create the scldevel subpackage macros
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# install generated man page
mkdir -p %{buildroot}%{_mandir}/man7/
install -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%files

%files runtime
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Tue Jan 20 2015 Robert Kuska <rkuska@redhat.com> - 1.1-17
- change
