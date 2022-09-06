%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# Created by pyp2rpm-1.1.0b
%global pypi_name osprofiler
%global with_doc 1

%global common_desc OSProfiler is an OpenStack cross-project profiling library.


Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Profiler Library

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:    OpenStack Profiler Library
%{?python_provide:%python_provide python3-%{pypi_name}}
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

%if 0%{?rhel} && 0%{?rhel} < 9
Requires: python3-importlib-metadata >= 1.7.0
%endif
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-prettytable >= 0.7.2
Requires: python3-oslo-messaging >= 5.2.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-requests
Requires: python3-netaddr
Requires: python3-webob

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the OpenStack Profiler Library
Group:      Documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-openstackdocstheme

%description doc
Documentation for the OpenStack Profiler Library
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s osprofiler %{buildroot}%{_bindir}/osprofiler-3

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/osprofiler
%{_bindir}/osprofiler-3
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
