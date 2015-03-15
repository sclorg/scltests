# scl stuff
%{?scl:%scl_package python}
%{!?scl:%global pkg_name %{name}}

# if in scl, kill the default bytecompilation process and bytecompile at the end of %%install
%{?scl:%global __os_install_post /usr/lib/rpm/brp-scl-compress %{_scl_root} \
    %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip} \
    /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump} \
    } \
    /usr/lib/rpm/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/brp-python-hardlink}

Summary: Fake Python interpreter package
Name: %{?scl_prefix}python
Version: 2.7.5
Release: 1%{?dist}
URL: http://www.python.org/
License: Python
Group: Development/Languages

%{?scl:Requires: %{scl}-runtime}
Requires: %{?scl_prefix}python-libs%{?_isa} = %{version}-%{release}
%{?scl:BuildRequires: %{scl}-runtime}

Source0: pythondeps-scl.sh
Source1: macros.python2
Source2: brp-python-bytecompile-with-scl-python

Provides: %{?scl_prefix}python(abi) = 2.7
Obsoletes: %{?scl_prefix}Distutils
Provides: %{?scl_prefix}Distutils
Obsoletes: %{?scl_prefix}python2 
Provides: %{?scl_prefix}python2 = %{version}
Obsoletes: %{?scl_prefix}python-elementtree <= 1.2.6
Obsoletes: %{?scl_prefix}python-sqlite < 2.3.2
Provides: %{?scl_prefix}python-sqlite = 2.3.2
Obsoletes: %{?scl_prefix}python-ctypes < 1.0.1
Provides: %{?scl_prefix}python-ctypes = 1.0.1
Obsoletes: %{?scl_prefix}python-hashlib < 20081120
Provides: %{?scl_prefix}python-hashlib = 20081120
Obsoletes: %{?scl_prefix}python-uuid < 1.31
Provides: %{?scl_prefix}python-uuid = 1.31
Provides: %{?scl_prefix}python-argparse = %{version}-%{release}

# filter pkgconfig Provides
# TODO: create some files that will trigger this
%{?scl:%filter_from_provides s|pkgconfig(|%{?scl_prefix}pkgconfig(|g}
%{?scl:%filter_from_requires s|python(abi|%{?scl_prefix}python(abi|g}
%{?scl:%filter_setup}

%description
Some description

%package libs
Summary: Runtime libraries for Python
Group: Applications/System

%{?scl:Requires: %{scl}-runtime}

%description libs
Libs description

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{?scl_prefix}python%{?_isa} = %{version}-%{release}
Obsoletes: %{?scl_prefix}python2-devel
Provides: %{?scl_prefix}python2-devel = %{version}-%{release}

%description devel
Devel description

%package tools
Summary: A collection of development tools included with Python
Group: Development/Tools
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Obsoletes: %{?scl_prefix}python2-tools
Provides: %{?scl_prefix}python2-tools = %{version}

%description tools
Tools description

%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description test
Test description


%prep
%setup -T -c


%build


%install
# install the macros file
mkdir -p %{buildroot}/%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rpm
install -m 644 %{SOURCE1} %{buildroot}/%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rpm/macros.python2%{?scl:.%{scl}}
%{?scl:sed -i 's|^\(%@scl@__python2\)|\1 %{_bindir}/python2|' %{buildroot}%{_root_sysconfdir}/rpm/macros.python2.%{scl}}
%{?scl:sed -i 's|@scl@|%{scl}|g' %{buildroot}%{_root_sysconfdir}/rpm/macros.python2.%{scl}}

# install bytecompilation script and dep generation script
%{?scl:mkdir -p %{buildroot}%{_root_prefix}/lib/rpm/redhat}
%{?scl:cp -a %{SOURCE0} %{buildroot}%{_root_prefix}/lib/rpm}
%{?scl:cp -a %{SOURCE2} %{buildroot}%{_root_prefix}/lib/rpm/redhat}

# create fake python 2.7 binaries
mkdir -p %{buildroot}%{_bindir}
cat >> %{buildroot}%{_bindir}/python2.7 << EOF
#!/bin/bash
%{_root_bindir}/python "\$@"
EOF
chmod a+x %{buildroot}%{_bindir}/python2.7
cat %{buildroot}%{_bindir}/python2.7

ln -s %{_bindir}/python2.7 %{buildroot}%{_bindir}/python2
ln -s %{_bindir}/python2.7 %{buildroot}%{_bindir}/python

# create fake python 2.7 libdirs
mkdir -p %{buildroot}%{_prefix}/lib{,64}/python2.7/site-packages


%files
%{_bindir}/*

%files libs
%{_prefix}/lib/python2.7
%{_prefix}/lib/python2.7/site-packages
%{_prefix}/lib64/python2.7
%{_prefix}/lib64/python2.7/site-packages

%files devel
%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rpm/macros.python2%{?scl:.%{scl}}
%{?scl:%{_root_prefix}/lib/rpm/pythondeps-scl.sh}
%{?scl:%{_root_prefix}/lib/rpm/redhat/brp-python-bytecompile-with-scl-python}

%files test

%changelog
* Fri Sep 12 2014 Slavek Kabrda <bkabrda@redhat.com>
- rebuilt

