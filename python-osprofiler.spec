%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# Created by pyp2rpm-1.1.0b
%global pypi_name osprofiler
%global with_doc 1

%global common_desc OSProfiler is an OpenStack cross-project profiling library.


Name:           python-%{pypi_name}
Version:        3.4.0
Release:        1%{?dist}
Summary:        OpenStack Profiler Library

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:    OpenStack Profiler Library
%{?python_provide:%python_provide python3-%{pypi_name}}
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

Requires: python3-importlib-metadata >= 1.7.0
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-prettytable >= 0.7.2
Requires: python3-oslo-messaging >= 5.2.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-requests
Requires: python3-six
Requires: python3-netaddr
Requires: python3-webob

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the OpenStack Profiler Library
Group:      Documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description doc
Documentation for the OpenStack Profiler Library
%endif

%prep
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
* Fri Sep 18 2020 RDO <dev@lists.rdoproject.org> 3.4.0-1
- Update to 3.4.0

